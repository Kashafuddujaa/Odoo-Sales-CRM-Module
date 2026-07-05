from odoo import api, fields, models


class SalesCrmInteraction(models.Model):
    _name = "sales.crm.interaction"
    _description = "Customer Interaction"
    _inherit = ["mail.thread"]
    _order = "date desc, id desc"

    name = fields.Char(
        string="Subject",
        required=True,
        tracking=True,
    )
    interaction_type = fields.Selection(
        selection=[
            ("call", "Call"),
            ("email", "Email"),
            ("meeting", "Meeting"),
            ("note", "Note"),
        ],
        string="Type",
        default="call",
        required=True,
        tracking=True,
    )
    direction = fields.Selection(
        selection=[
            ("inbound", "Inbound"),
            ("outbound", "Outbound"),
        ],
        string="Direction",
        default="outbound",
    )
    date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now,
        required=True,
        tracking=True,
    )
    duration = fields.Float(
        string="Duration (hours)",
        help="Logged duration for calls and meetings.",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        index=True,
        tracking=True,
    )
    lead_id = fields.Many2one(
        comodel_name="crm.lead",
        string="Opportunity",
        index=True,
        ondelete="cascade",
        tracking=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
        tracking=True,
    )
    summary = fields.Text(string="Summary")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    @api.onchange("lead_id")
    def _onchange_lead_id(self):
        for interaction in self:
            if interaction.lead_id and interaction.lead_id.partner_id:
                interaction.partner_id = interaction.lead_id.partner_id
