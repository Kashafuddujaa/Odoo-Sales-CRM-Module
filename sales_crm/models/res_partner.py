from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    interaction_ids = fields.One2many(
        comodel_name="sales.crm.interaction",
        inverse_name="partner_id",
        string="Interactions",
    )
    interaction_count = fields.Integer(
        string="Interaction Count",
        compute="_compute_interaction_count",
    )
    customer_lifetime_value = fields.Monetary(
        string="Lifetime Value",
        compute="_compute_customer_lifetime_value",
        currency_field="crm_currency_id",
        help="Total expected revenue of won opportunities for this customer.",
    )
    customer_tier = fields.Selection(
        selection=[
            ("bronze", "Bronze"),
            ("silver", "Silver"),
            ("gold", "Gold"),
            ("platinum", "Platinum"),
        ],
        string="Customer Tier",
        compute="_compute_customer_lifetime_value",
    )
    crm_currency_id = fields.Many2one(
        comodel_name="res.currency",
        compute="_compute_crm_currency_id",
    )

    def _compute_crm_currency_id(self):
        currency = self.env.company.currency_id
        for partner in self:
            partner.crm_currency_id = currency

    @api.depends("interaction_ids")
    def _compute_interaction_count(self):
        counts = dict(
            self.env["sales.crm.interaction"]._read_group(
                domain=[("partner_id", "in", self.ids)],
                groupby=["partner_id"],
                aggregates=["__count"],
            )
        )
        for partner in self:
            partner.interaction_count = counts.get(partner, 0)

    def _compute_customer_lifetime_value(self):
        Lead = self.env["crm.lead"]
        won_by_partner = dict(
            Lead._read_group(
                domain=[
                    ("partner_id", "in", self.ids),
                    ("stage_id.is_won", "=", True),
                ],
                groupby=["partner_id"],
                aggregates=["expected_revenue:sum"],
            )
        )
        for partner in self:
            value = won_by_partner.get(partner, 0.0) or 0.0
            partner.customer_lifetime_value = value
            if value >= 100000:
                partner.customer_tier = "platinum"
            elif value >= 50000:
                partner.customer_tier = "gold"
            elif value >= 10000:
                partner.customer_tier = "silver"
            else:
                partner.customer_tier = "bronze"

    def action_view_partner_interactions(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Interactions",
            "res_model": "sales.crm.interaction",
            "view_mode": "tree,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }
