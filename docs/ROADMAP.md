# Roadmap

The project is delivered in phases. Phase 1 is the production-ready core module;
later phases extend reach and intelligence.

## Phase 1 — Core CRM Module

The installable, tested addon.

| Milestone | Scope | Status |
|-----------|-------|--------|
| M0 | Docker scaffold, installable addon, app icon | Done |
| M1 | Models: lead/partner extensions, interaction, follow-up, ACL | Done |
| M2 | Views: list/form/kanban/calendar/search, menus, actions | Done |
| M3 | Business logic: lead scoring, won-stage workflow, overdue cron | Done |
| M4 | Security: Salesperson/Manager/Administrator groups, record rules | Done |
| M5 | OWL KPI dashboard, pivot/graph analysis, QWeb PDF report | Done |
| M6 | TransactionCase tests + GitHub Actions CI | Done |
| M7 | Docs, README, i18n template, demo data | Done |
| M8 | Live boot verification on a real Odoo instance | Pending |

## Phase 2 — Integrations & Reach

- Email integration (sync incoming/outgoing mail into interactions)
- Calendar synchronization for follow-ups
- REST API endpoints (see `controllers/`)
- Customer self-service portal

## Phase 3 — Intelligence & Scale

- Sales forecasting dashboard (trend + projection)
- AI-powered lead scoring to replace the rule-based `_compute_lead_score`
- Multi-company hardening
- Automated email/SMS follow-up sequences

## Phase 4 — Release Engineering

- Odoo App Store packaging and listing assets
- Performance and index tuning, load testing
- Migration scripts and version bumps (17 → 18)
