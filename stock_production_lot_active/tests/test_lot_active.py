from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestRestrictLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env.ref("product.product_product_16")
        cls.product.write({"tracking": "lot"})
        cls.warehouse = cls.env.ref("stock.warehouse0")

    def test_duplicate_inactive_lot(self):
        # it should not be possible to create a new lot with the same name and company
        # even when the first lot is inactive
        with self.assertRaises(ValidationError):
            self.env["stock.production.lot"].create(
                {
                    "name": "lot1",
                    "product_id": self.product.id,
                    "company_id": self.warehouse.company_id.id,
                    "active": False,
                }
            )
            self.env["stock.production.lot"].create(
                {
                    "name": "lot1",
                    "product_id": self.product.id,
                    "company_id": self.warehouse.company_id.id,
                    "active": True,
                }
            )
