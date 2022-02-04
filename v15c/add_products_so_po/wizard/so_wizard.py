from odoo import api, fields, models


class PosOrderWizard(models.TransientModel):
    _name = "sale.order.wizard"
    _description = "Sale Order Wizard"

    product_ids = fields.Many2many(
        "product.product", "product_so_rel", "so_id", "product_id", string="Product"
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

    def update_selected_so(self):
        for order in self._context.get("active_ids"):
            so = self.env["sale.order"].browse(order)
            print("\n\n\n PO", so.read())
            if so.state not in ['done', 'cancel'] and not so.invoice_ids:
                for product in self.product_ids:
                    data = {
                        "product_id": product.id,
                        "name": product.name,
                        "price_unit": product.list_price,
                        "order_id": so.id,
                    }
                    self.env["sale.order.line"].create(data)
            else:
                continue
