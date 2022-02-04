from odoo import api, fields, models


class PurchaseOrderWizard(models.TransientModel):
    _name = "purchase.order.wizard"
    _description = "Purchase Order Wizard"

    product_ids = fields.Many2many(
        "product.product", "product_po_rel", "po_id", "product_id", string="Product"
    )

    def action_open_wizard(self):
        ctx = self._context
        return {
            "name": "Select Product",
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }

    def update_selected_po(self):
        for order in self._context.get("active_ids"):
            po = self.env["purchase.order"].browse(order)
            print("\n\n\n PO", po.read())
            if po.state not in ['done', 'cancel'] and not po.invoice_ids:
                for product in self.product_ids:
                    data = {
                        "product_id": product.id,
                        "name": product.name,
                        "price_unit": product.list_price,
                        "order_id": po.id,
                    }
                    self.env["purchase.order.line"].create(data)
