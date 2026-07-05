{
    "name": "Sales CRM",
    "version": "17.0.1.0.0",
    "category": "Sales/CRM",
    "summary": "Lead scoring, follow-ups, interaction history and a KPI dashboard on top of Odoo CRM.",
    "description": """
Sales CRM
=========
A custom CRM extension that adds automated lead scoring, scheduled
follow-ups, a customer interaction log, security-scoped pipelines,
QWeb PDF reporting and an OWL KPI dashboard.
""",
    "author": "Kashaf Ud Duja",
    "website": "https://github.com/KashafUdDuja/Odoo-Sales-CRM-Module",
    "license": "MIT",
    "depends": [
        "base",
        "mail",
        "crm",
        "sale_management",
    ],
    # NOTE: this list grows one milestone at a time so the module always
    # installs cleanly. Later milestones add views, custom security groups,
    # reports and dashboard assets.
    "data": [
        # security: groups & record rules first, then the access matrix
        "security/sales_crm_security.xml",
        "security/ir.model.access.csv",
        # seed data
        "data/crm_stage_data.xml",
        "data/ir_cron_data.xml",
        # views (actions defined before the menus that reference them)
        "views/crm_lead_views.xml",
        "views/interaction_views.xml",
        "views/followup_views.xml",
        "views/res_partner_views.xml",
        "views/menus.xml",
        "views/config_views.xml",
        "views/dashboard_views.xml",
        # reports
        "report/report_templates.xml",
        "report/sales_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sales_crm/static/src/scss/dashboard.scss",
            "sales_crm/static/src/js/dashboard.js",
            "sales_crm/static/src/xml/dashboard.xml",
        ],
    },
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
