from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    interaction_ids = fields.One2many(
        comodel_name="sales.crm.interaction",
        inverse_name="lead_id",
        string="Interactions",
    )
    interaction_count = fields.Integer(
        string="Interaction Count",
        compute="_compute_interaction_count",
    )
    last_interaction_date = fields.Datetime(
        string="Last Interaction",
        compute="_compute_last_interaction_date",
        store=True,
    )
    followup_ids = fields.One2many(
        comodel_name="sales.crm.followup",
        inverse_name="lead_id",
        string="Follow-ups",
    )
    followup_count = fields.Integer(
        string="Follow-up Count",
        compute="_compute_followup_count",
    )
    open_followup_count = fields.Integer(
        string="Open Follow-ups",
        compute="_compute_followup_count",
    )
    lead_score = fields.Integer(
        string="Lead Score",
        compute="_compute_lead_score",
        store=True,
        help="Automated 0-100 score derived from value, engagement and probability.",
    )
    score_grade = fields.Selection(
        selection=[
            ("cold", "Cold"),
            ("warm", "Warm"),
            ("hot", "Hot"),
        ],
        string="Grade",
        compute="_compute_lead_score",
        store=True,
    )

    @api.depends("interaction_ids")
    def _compute_interaction_count(self):
        counts = dict(
            self.env["sales.crm.interaction"]._read_group(
                domain=[("lead_id", "in", self.ids)],
                groupby=["lead_id"],
                aggregates=["__count"],
            )
        )
        for lead in self:
            lead.interaction_count = counts.get(lead, 0)

    @api.depends("interaction_ids.date")
    def _compute_last_interaction_date(self):
        for lead in self:
            dates = lead.interaction_ids.mapped("date")
            lead.last_interaction_date = max(dates) if dates else False

    @api.depends("followup_ids", "followup_ids.state")
    def _compute_followup_count(self):
        for lead in self:
            lead.followup_count = len(lead.followup_ids)
            lead.open_followup_count = len(
                lead.followup_ids.filtered(lambda f: f.state == "planned")
            )

    @api.depends(
        "expected_revenue",
        "probability",
        "interaction_ids",
        "last_interaction_date",
        "followup_ids.state",
    )
    def _compute_lead_score(self):
        """Weighted 0-100 score across value, probability, engagement and recency.

        Weights are capped so the maximum reachable score is exactly 100:
        revenue 35 + probability 25 + engagement 20 + recency 15 + open follow-up 5.
        """
        today = fields.Date.context_today(self)
        for lead in self:
            revenue_points = min(35.0, (lead.expected_revenue or 0.0) / 2000.0)
            probability_points = (lead.probability or 0.0) * 0.25
            engagement_points = min(20.0, len(lead.interaction_ids) * 4.0)

            recency_points = 0.0
            if lead.last_interaction_date:
                days_since = (today - lead.last_interaction_date.date()).days
                if days_since <= 7:
                    recency_points = 15.0
                elif days_since <= 30:
                    recency_points = 8.0
                elif days_since > 60:
                    recency_points = -10.0

            has_open_followup = any(
                f.state == "planned" for f in lead.followup_ids
            )
            followup_points = 5.0 if has_open_followup else 0.0

            score = (
                revenue_points
                + probability_points
                + engagement_points
                + recency_points
                + followup_points
            )
            score = int(round(max(0.0, min(100.0, score))))
            lead.lead_score = score
            if score >= 70:
                lead.score_grade = "hot"
            elif score >= 40:
                lead.score_grade = "warm"
            else:
                lead.score_grade = "cold"

    def write(self, vals):
        res = super().write(vals)
        if vals.get("stage_id"):
            won_leads = self.filtered(lambda lead: lead.stage_id.is_won)
            open_followups = won_leads.followup_ids.filtered(
                lambda f: f.state == "planned"
            )
            if open_followups:
                open_followups.action_mark_done()
        return res

    def action_view_interactions(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Interactions",
            "res_model": "sales.crm.interaction",
            "view_mode": "tree,form",
            "domain": [("lead_id", "=", self.id)],
            "context": {
                "default_lead_id": self.id,
                "default_partner_id": self.partner_id.id,
            },
        }

    def action_view_followups(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Follow-ups",
            "res_model": "sales.crm.followup",
            "view_mode": "tree,form,calendar",
            "domain": [("lead_id", "=", self.id)],
            "context": {"default_lead_id": self.id},
        }
