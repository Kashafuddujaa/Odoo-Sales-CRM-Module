from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestLeadScoring(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Acme Corp"})
        cls.stage_open = cls.env["crm.stage"].create(
            {"name": "Test Open", "is_won": False}
        )
        cls.stage_won = cls.env["crm.stage"].create(
            {"name": "Test Won", "is_won": True}
        )

    def _make_lead(self, **vals):
        base = {
            "name": "Test Deal",
            "type": "opportunity",
            "stage_id": self.stage_open.id,
        }
        base.update(vals)
        return self.env["crm.lead"].create(base)

    def test_score_is_bounded_and_graded(self):
        lead = self._make_lead(
            partner_id=self.partner.id,
            expected_revenue=40000.0,
            probability=80.0,
        )
        self.assertGreaterEqual(lead.lead_score, 0)
        self.assertLessEqual(lead.lead_score, 100)
        self.assertIn(lead.score_grade, ("cold", "warm", "hot"))

    def test_engagement_raises_score(self):
        lead = self._make_lead(expected_revenue=10000.0, probability=20.0)
        baseline = lead.lead_score
        for i in range(3):
            self.env["sales.crm.interaction"].create(
                {"name": f"Call {i}", "lead_id": lead.id, "partner_id": self.partner.id}
            )
        lead.invalidate_recordset()
        self.assertGreater(
            lead.lead_score,
            baseline,
            "Logging recent interactions should increase the lead score.",
        )

    def test_score_capped_at_100_and_hot(self):
        lead = self._make_lead(expected_revenue=10_000_000.0, probability=100.0)
        for i in range(10):
            self.env["sales.crm.interaction"].create(
                {"name": f"c{i}", "lead_id": lead.id}
            )
        # An open follow-up contributes the final 5 points needed to reach 100.
        self.env["sales.crm.followup"].create(
            {
                "name": "Close it",
                "lead_id": lead.id,
                "due_date": fields.Date.context_today(lead),
            }
        )
        lead.invalidate_recordset()
        self.assertEqual(lead.lead_score, 100)
        self.assertEqual(lead.score_grade, "hot")

    def test_won_stage_closes_open_followups(self):
        lead = self._make_lead()
        followup = self.env["sales.crm.followup"].create(
            {
                "name": "Send contract",
                "lead_id": lead.id,
                "due_date": fields.Date.context_today(lead),
            }
        )
        self.assertEqual(followup.state, "planned")
        lead.stage_id = self.stage_won
        self.assertEqual(
            followup.state,
            "done",
            "Moving a lead to a won stage should auto-complete open follow-ups.",
        )

    def test_interaction_and_followup_counts(self):
        lead = self._make_lead(partner_id=self.partner.id)
        self.env["sales.crm.interaction"].create(
            {"name": "Intro", "lead_id": lead.id, "partner_id": self.partner.id}
        )
        self.env["sales.crm.followup"].create(
            {"name": "Nudge", "lead_id": lead.id, "due_date": fields.Date.context_today(lead)}
        )
        lead.invalidate_recordset()
        self.assertEqual(lead.interaction_count, 1)
        self.assertEqual(lead.followup_count, 1)
        self.assertEqual(lead.open_followup_count, 1)
