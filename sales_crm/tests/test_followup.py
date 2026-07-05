from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestFollowup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lead = cls.env["crm.lead"].create(
            {"name": "Followup Deal", "type": "opportunity"}
        )
        cls.today = fields.Date.context_today(cls.env["sales.crm.followup"])

    def test_is_overdue_flag(self):
        overdue = self.env["sales.crm.followup"].create(
            {
                "name": "Late call",
                "lead_id": self.lead.id,
                "due_date": self.today - timedelta(days=2),
            }
        )
        self.assertTrue(overdue.is_overdue)

        upcoming = self.env["sales.crm.followup"].create(
            {
                "name": "Future call",
                "lead_id": self.lead.id,
                "due_date": self.today + timedelta(days=2),
            }
        )
        self.assertFalse(upcoming.is_overdue)

    def test_is_overdue_search(self):
        overdue = self.env["sales.crm.followup"].create(
            {
                "name": "Late",
                "lead_id": self.lead.id,
                "due_date": self.today - timedelta(days=1),
            }
        )
        found = self.env["sales.crm.followup"].search([("is_overdue", "=", True)])
        self.assertIn(overdue, found)

    def test_mark_done_sets_state_and_date(self):
        followup = self.env["sales.crm.followup"].create(
            {"name": "Quote", "lead_id": self.lead.id, "due_date": self.today}
        )
        followup.action_mark_done()
        self.assertEqual(followup.state, "done")
        self.assertEqual(followup.done_date, self.today)
        self.assertFalse(followup.is_overdue)

    def test_cron_schedules_reminder_without_duplicates(self):
        user = self.env["res.users"].create(
            {
                "name": "Rep",
                "login": "rep_followup",
                "groups_id": [
                    (4, self.env.ref("sales_crm.group_sales_crm_user").id)
                ],
            }
        )
        followup = self.env["sales.crm.followup"].create(
            {
                "name": "Overdue task",
                "lead_id": self.lead.id,
                "due_date": self.today - timedelta(days=3),
                "user_id": user.id,
            }
        )
        Followup = self.env["sales.crm.followup"]
        Followup._cron_notify_overdue_followups()
        self.assertEqual(len(followup.activity_ids), 1)

        # Running again must not pile up a second reminder.
        Followup._cron_notify_overdue_followups()
        self.assertEqual(len(followup.activity_ids), 1)
