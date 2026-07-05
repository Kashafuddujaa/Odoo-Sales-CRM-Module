# Setup

## Prerequisites

- Docker and Docker Compose, **or** a local Odoo 17 installation
- Port `8069` free for the Odoo web UI

## Run with Docker (recommended)

From the repository root:

```bash
docker compose up -d
```

This starts two containers:

- `sales_crm_db` — PostgreSQL 15
- `sales_crm_odoo` — Odoo 17, with this repo's `sales_crm/` mounted into
  `/mnt/extra-addons`

Then:

1. Open <http://localhost:8069>.
2. Create a database (master password is `admin`, set in `odoo.conf` — change it
   for anything beyond local use).
3. Go to **Apps**, remove the *Apps* filter, search for **Sales CRM**, and click
   **Install**. If it does not appear, click **Update Apps List** first.

To load sample records, install with demo data (create the database with the
"Load demonstration data" option enabled).

Stop and remove everything:

```bash
docker compose down          # keep data
docker compose down -v       # also delete the database volume
```

## Install into an existing Odoo

1. Copy or symlink the `sales_crm/` directory into one of your `addons_path`
   folders.
2. Restart Odoo with the addons path updated, e.g.:

   ```bash
   odoo -d your_db -u sales_crm --addons-path=/path/to/addons
   ```

3. Enable developer mode, update the apps list, and install **Sales CRM**.

## Run the tests

Against a throwaway database:

```bash
odoo \
  --stop-after-init --no-http \
  -d test_db \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/path/to/this/repo \
  -i sales_crm --test-enable --test-tags=/sales_crm
```

The same command runs automatically in CI (`.github/workflows/ci.yml`) on every
push and pull request to `main`.

## First steps after install

- The **Sales CRM** app appears in the top menu (visible to the *Salesperson*
  group; the admin user is granted *Administrator* on install).
- Open **Sales CRM → Dashboard** for live pipeline KPIs.
- Assign users to **Salesperson**, **Manager** or **Administrator** under
  **Settings → Users**.
