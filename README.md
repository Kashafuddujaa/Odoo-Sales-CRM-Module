# Sales CRM Module for Odoo 17

A custom CRM module for **Odoo 17** that extends the native CRM with lead scoring, follow-up management, customer interaction tracking, role-based security, reporting, and a custom OWL KPI dashboard.

## Features

- Automated lead scoring (0–100) with Hot/Warm/Cold grading
- Lead & opportunity management
- Customer interaction history (calls, emails, meetings, notes)
- Scheduled follow-ups with reminders
- Custom OWL KPI dashboard
- Role-based security (Salesperson, Manager, Administrator)
- QWeb PDF reports
- Search, filters, and analytics
- Docker support with demo data

## Tech Stack

- Python
- Odoo 17
- XML / QWeb
- OWL (JavaScript)
- PostgreSQL
- Docker

## Screenshots

> *(Add screenshots here)*

- Dashboard
- Leads List
- Lead Form
- Sales Pipeline
- Settings

## Quick Start

```bash
docker compose up -d
```

Open **http://localhost:8069**, create a database, then install **Sales CRM** from the Apps menu.

## Testing

- ✅ 18/18 automated tests passing
- Demo data included
- CI workflow supported

## Project Structure

```
sales_crm/
├── models/
├── views/
├── security/
├── data/
├── report/
├── static/src/
├── tests/
├── demo/
└── i18n/
```

## Documentation

- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`

## Roadmap

Future improvements include:

- Email integration
- Calendar sync
- REST API
- Customer portal
- AI lead scoring
- Multi-company support
