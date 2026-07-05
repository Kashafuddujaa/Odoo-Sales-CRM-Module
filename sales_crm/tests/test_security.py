from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_user = cls.env.ref("sales_crm.group_sales_crm_user")
        cls.group_manager = cls.env.ref("sales_crm.group_sales_crm_manager")

        cls.salesperson = cls.env["res.users"].create(
            {
                "name": "Sales Person",
                "login": "sec_salesperson",
                "groups_id": [(6, 0, [cls.group_user.id])],
            }
        )
        cls.manager = cls.env["res.users"].create(
            {
                "name": "Sales Manager",
                "login": "sec_manager",
                "groups_id": [(6, 0, [cls.group_manager.id])],
            }
        )
        cls.lead = cls.env["crm.lead"].create(
            {"name": "Shared Deal", "type": "opportunity"}
        )

    def test_salesperson_sees_only_own_interactions(self):
        own = self.env["sales.crm.interaction"].create(
            {"name": "Mine", "lead_id": self.lead.id, "user_id": self.salesperson.id}
        )
        other = self.env["sales.crm.interaction"].create(
            {"name": "Theirs", "lead_id": self.lead.id, "user_id": self.manager.id}
        )

        visible = (
            self.env["sales.crm.interaction"]
            .with_user(self.salesperson)
            .search([])
        )
        self.assertIn(own, visible)
        self.assertNotIn(other, visible)

    def test_manager_sees_all_interactions(self):
        own = self.env["sales.crm.interaction"].create(
            {"name": "Mine", "lead_id": self.lead.id, "user_id": self.salesperson.id}
        )
        managers = self.env["sales.crm.interaction"].create(
            {"name": "Theirs", "lead_id": self.lead.id, "user_id": self.manager.id}
        )

        visible = self.env["sales.crm.interaction"].with_user(self.manager).search([])
        self.assertIn(own, visible)
        self.assertIn(managers, visible)

    def test_salesperson_cannot_unlink(self):
        record = (
            self.env["sales.crm.interaction"]
            .with_user(self.salesperson)
            .create(
                {
                    "name": "Temp",
                    "lead_id": self.lead.id,
                    "user_id": self.salesperson.id,
                }
            )
        )
        from odoo.exceptions import AccessError

        with self.assertRaises(AccessError):
            record.unlink()
