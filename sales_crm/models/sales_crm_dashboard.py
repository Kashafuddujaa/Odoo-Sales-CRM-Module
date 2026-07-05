from odoo import api, fields, models


class SalesCrmDashboard(models.AbstractModel):
    _name = "sales.crm.dashboard"
    _description = "Sales CRM Dashboard Data Provider"

    @api.model
    def get_dashboard_data(self):
        """Return live pipeline KPIs for the OWL dashboard.

        All queries run with the calling user's access rights, so the numbers
        respect the record rules defined for Salespeople vs. Managers.
        """
        Lead = self.env["crm.lead"]
        Followup = self.env["sales.crm.followup"]
        today = fields.Date.context_today(self)
        month_start = today.replace(day=1)

        open_domain = [
            ("type", "=", "opportunity"),
            ("active", "=", True),
            ("stage_id.is_won", "=", False),
        ]
        open_leads = Lead.search(open_domain)
        open_count = len(open_leads)
        pipeline_value = sum(open_leads.mapped("expected_revenue"))
        avg_score = (
            round(sum(open_leads.mapped("lead_score")) / open_count, 1)
            if open_count
            else 0.0
        )

        won_leads = Lead.search(
            [
                ("type", "=", "opportunity"),
                ("stage_id.is_won", "=", True),
                ("date_closed", ">=", fields.Datetime.to_string(month_start)),
            ]
        )
        won_count = len(won_leads)
        won_value = sum(won_leads.mapped("expected_revenue"))

        overdue_followups = Followup.search_count(
            [("state", "=", "planned"), ("due_date", "<", today)]
        )

        stage_groups = Lead._read_group(
            domain=[("type", "=", "opportunity"), ("active", "=", True)],
            groupby=["stage_id"],
            aggregates=["expected_revenue:sum", "__count"],
        )
        by_stage = [
            {
                "stage": stage.display_name if stage else "Undefined",
                "value": value or 0.0,
                "count": count,
            }
            for stage, value, count in stage_groups
        ]

        grade_groups = Lead._read_group(
            domain=open_domain,
            groupby=["score_grade"],
            aggregates=["__count"],
        )
        by_grade = {(grade or "unknown"): count for grade, count in grade_groups}

        return {
            "open_count": open_count,
            "pipeline_value": pipeline_value,
            "avg_score": avg_score,
            "won_count": won_count,
            "won_value": won_value,
            "overdue_followups": overdue_followups,
            "by_stage": by_stage,
            "by_grade": {
                "hot": by_grade.get("hot", 0),
                "warm": by_grade.get("warm", 0),
                "cold": by_grade.get("cold", 0),
            },
            "currency_symbol": self.env.company.currency_id.symbol or "",
        }
