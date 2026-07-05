# Contributing

Thanks for your interest in improving Sales CRM.

## Development setup

See [docs/SETUP.md](docs/SETUP.md) to run the module with Docker.

## Guidelines

- Target **Odoo 17.0**. Keep the module installable at every commit.
- Follow Odoo conventions: models in `models/`, one class per file where
  practical; views, security and data in their respective folders.
- Wrap user-facing strings in `_()` so they land in `i18n/sales_crm.pot`.
- Prefer extending existing behaviour over duplicating native CRM logic.

## Tests

Every behavioural change should ship with or update a `TransactionCase` test in
`sales_crm/tests/`. Run them locally before opening a PR:

```bash
odoo --stop-after-init --no-http -d test_db \
  --addons-path=/path/to/odoo/addons,/path/to/this/repo \
  -i sales_crm --test-enable --test-tags=/sales_crm
```

CI runs the same suite on every push and pull request to `main`.

## Pull requests

- Keep PRs focused and describe the "why".
- Ensure CI is green.
- Update `docs/` and the `.pot` template when behaviour or strings change.
