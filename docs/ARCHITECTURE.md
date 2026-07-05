# Architecture

`sales_crm` is a single Odoo 17 addon that follows a **hybrid** design: it
extends Odoo's native CRM (`crm.lead`, `res.partner`) and adds custom
standalone models for interactions and follow-ups.

## Data model

| Model | Kind | Responsibility |
|-------|------|----------------|
| `crm.lead` | inherit | Adds lead scoring, grade, related interactions/follow-ups, won-stage automation |
| `res.partner` | inherit | Adds interaction count, customer tier, lifetime value |
| `sales.crm.interaction` | new | Log of calls, emails, meetings and notes |
| `sales.crm.followup` | new | Scheduled follow-up task with overdue tracking |
| `sales.crm.dashboard` | abstract | Read-only provider of aggregated KPIs for the OWL dashboard |

### Lead scoring

`crm.lead._compute_lead_score` produces a stored `0–100` score from four capped
components, so the maximum is exactly 100:

- Expected revenue (up to 35)
- Probability (up to 25)
- Engagement — number of interactions (up to 20)
- Recency — days since the last interaction (−10 to +15)
- Open follow-up bonus (5)

The score maps to a `score_grade`: `cold` (<40), `warm` (40–69), `hot` (≥70).

### Won-stage workflow

`crm.lead.write` detects a move into any stage flagged `is_won` and
auto-completes that lead's still-planned follow-ups, so closed deals leave no
dangling tasks.

### Overdue follow-up reminders

`sales.crm.followup._cron_notify_overdue_followups` runs daily (`ir.cron`) and
schedules a to-do activity on each overdue, still-planned follow-up for its
assignee. It skips records that already have an open activity for that user, so
repeated runs never duplicate reminders.

## Security

Three tiered groups in an application category:

- **Salesperson** (`group_sales_crm_user`) — implies internal user; sees and
  manages only their own interactions and follow-ups.
- **Manager** (`group_sales_crm_manager`) — implies Salesperson; sees all
  records and can delete them.
- **Administrator** (`group_sales_crm_admin`) — implies Manager; also sees the
  Configuration menu.

Model-level rights live in `security/ir.model.access.csv`; row-level visibility
is enforced by record rules in `security/sales_crm_security.xml`. Menus are
gated so non-sales users never see the app.

## Frontend

The dashboard is an OWL client action (`tag="sales_crm_dashboard"`). The
component (`static/src/js/dashboard.js`) calls
`sales.crm.dashboard.get_dashboard_data` over ORM RPC and renders KPI cards, a
pipeline-by-stage bar chart and a lead-grade breakdown. Because the query runs
with the caller's rights, salespeople see only their own numbers.

## Reporting

- Pivot and graph analysis on the pipeline (`action_sales_crm_report`).
- A QWeb PDF **Opportunity Summary** (`report/`) printable from any opportunity,
  listing its interactions and follow-ups.

## Load order

The manifest loads data deliberately: security groups and rules first, then the
access CSV that references them, then seed data, views (actions before the menus
that reference them), and finally reports. This keeps the module installable at
every step.

## Directory layout

```
sales_crm/
├── models/        # Python business logic
├── views/         # backend views, actions, menus
├── security/      # groups, record rules, access matrix
├── data/          # cron + seed stage
├── report/        # QWeb PDF templates + report action
├── wizard/        # (reserved for Phase 2)
├── controllers/   # (reserved for Phase 2 REST/portal)
├── static/src/    # OWL dashboard: js / xml / scss
├── tests/         # TransactionCase suites
├── demo/          # demonstration records
└── i18n/          # translation template
```
