# Odoo Sales CRM Module

[![CI](https://github.com/KashafUdDuja/Odoo-Sales-CRM-Module/actions/workflows/ci.yml/badge.svg)](https://github.com/KashafUdDuja/Odoo-Sales-CRM-Module/actions/workflows/ci.yml)
![Odoo](https://img.shields.io/badge/Odoo-17.0-714B67)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

A custom CRM module for Odoo that streamlines customer relationship management
and sales operations. It extends Odoo's native CRM with automated lead scoring,
scheduled follow-ups, a full customer interaction log, security-scoped
pipelines, printable reports and a custom OWL KPI dashboard.

## Features

* **Lead & opportunity management** — native CRM extended with an automated
  0–100 lead score and Hot/Warm/Cold grade
* **Customer & contact management** — customer tier and lifetime value on every
  partner
* **Sales pipeline** with the native Kanban plus a scored list view
* **Activity scheduling & follow-ups** with overdue tracking and a daily
  reminder cron
* **Sales dashboard & KPIs** — a custom OWL dashboard (open pipeline, won this
  month, average score, overdue follow-ups, stage breakdown)
* **Customer interaction history** — log calls, emails, meetings and notes
* **Security groups & permissions** — Salesperson / Manager / Administrator with
  record rules
* **Search, filters & group by** across all custom models
* **Automated workflows** — moving a lead to a won stage auto-closes its open
  follow-ups
* **Reporting & analytics** — pivot/graph analysis and a QWeb PDF opportunity
  summary

## Tech Stack

Python · Odoo 17 Framework & ORM · OWL (JavaScript) · XML/QWeb · PostgreSQL · Docker

## Quick start

```bash
docker compose up -d
# open http://localhost:8069, create a database,
# then Apps → search "Sales CRM" → Install
```

Full instructions, including running without Docker and executing the test
suite, are in [docs/SETUP.md](docs/SETUP.md).

## Architecture

The module uses a **hybrid** design — it inherits `crm.lead` and `res.partner`
and adds standalone `sales.crm.interaction` and `sales.crm.followup` models,
plus an abstract dashboard data provider. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the data model, scoring
formula, security tiers and load order.

```
sales_crm/
├── models/      # lead/partner extensions, interaction, follow-up, dashboard
├── views/       # views, actions, menus
├── security/    # groups, record rules, access matrix
├── data/        # cron + seed stage
├── report/      # QWeb PDF report
├── static/src/  # OWL dashboard (js / xml / scss)
├── tests/       # TransactionCase suites
├── demo/        # demonstration data
└── i18n/        # translation template
```

## Testing

TransactionCase suites cover lead scoring, the won-stage workflow, follow-up
overdue logic and cron de-duplication, and record-rule security. They run in CI
on every push via `.github/workflows/ci.yml`, which installs the module into a
fresh Odoo 17 container against PostgreSQL.

## Project goals

This project demonstrates building modular ERP applications on Odoo while
following clean architecture and best practices: custom models, business logic,
XML/OWL views, security rules, automated workflows, reporting and tests.

## Roadmap

Delivered in phases — see [docs/ROADMAP.md](docs/ROADMAP.md). Phase 1 (the core
module) is complete; later phases add integrations and intelligence:

* Email integration
* Calendar synchronization
* REST API support
* Customer portal
* Sales forecasting dashboard
* AI-powered lead scoring
* Multi-company support

## License

MIT — see [LICENSE](LICENSE).
