from odoo import _, api, fields, models


class SalesCrmFollowup(models.Model):
    _name = "sales.crm.followup"
    _description = "Sales Follow-up"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "due_date asc, id desc"

    name = fields.Char(string="Summary", required=True, tracking=True)
    lead_id = fields.Many2one(
        comodel_name="crm.lead",
        string="Opportunity",
        required=True,
        index=True,
        ondelete="cascade",
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        related="lead_id.partner_id",
        store=True,
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned To",
        default=lambda self: self.env.user,
        tracking=True,
    )
    due_date = fields.Date(string="Due Date", required=True, tracking=True)
    done_date = fields.Date(string="Completed On", readonly=True)
    priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3", "Urgent"),
        ],
        string="Priority",
        default="1",
    )
    state = fields.Selection(
        selection=[
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="planned",
        required=True,
        tracking=True,
    )
    is_overdue = fields.Boolean(
        string="Overdue",
        compute="_compute_is_overdue",
        search="_search_is_overdue",
    )
    notes = fields.Text(string="Notes")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    @api.depends("due_date", "state")
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for followup in self:
            followup.is_overdue = bool(
                followup.state == "planned"
                and followup.due_date
                and followup.due_date < today
            )

    def _search_is_overdue(self, operator, value):
        today = fields.Date.context_today(self)
        overdue_domain = [("state", "=", "planned"), ("due_date", "<", today)]
        # Normalise "is_overdue = True" and "is_overdue != False" to the same set.
        wants_overdue = (operator in ("=", "==")) == bool(value)
        if wants_overdue:
            return overdue_domain
        return ["!", "&"] + overdue_domain

    def action_mark_done(self):
        self.write({"state": "done", "done_date": fields.Date.context_today(self)})

    def action_mark_cancelled(self):
        self.write({"state": "cancelled"})

    def action_reset_planned(self):
        self.write({"state": "planned", "done_date": False})

    @api.model
    def _cron_notify_overdue_followups(self):
        """Schedule a to-do reminder on each overdue, still-planned follow-up.

        Run daily by ir.cron. A reminder is only scheduled when the assignee
        has no existing open activity on the record, so repeated cron runs do
        not pile up duplicate reminders.
        """
        today = fields.Date.context_today(self)
        overdue = self.search(
            [("state", "=", "planned"), ("due_date", "<", today), ("user_id", "!=", False)]
        )
        for followup in overdue:
            already_reminded = followup.activity_ids.filtered(
                lambda a: a.user_id == followup.user_id
            )
            if already_reminded:
                continue
            followup.activity_schedule(
                act_type_xmlid="mail.mail_activity_data_todo",
                summary=_("Overdue follow-up: %s", followup.name),
                note=_(
                    "This follow-up for %(lead)s was due on %(date)s.",
                    lead=followup.lead_id.display_name,
                    date=followup.due_date,
                ),
                user_id=followup.user_id.id,
            )
        return True
