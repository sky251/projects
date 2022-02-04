from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    available_qty_ids = fields.One2many('available.quantity', 'product_id', string='Available Qty',
                                        compute='_compute_available_qty'
                                        )

    def _compute_available_qty(self):
        stock = self.env['stock.quant'].search(
            [('product_id', '=', self.id), ('on_hand', '=', True)])
        if stock:
            qty = 0
            data = {}
            keys = []
            for quant in stock:
                for location in quant.location_id:
                    for warehouse in location.warehouse_id:
                        if warehouse.id in keys:
                            value = data[warehouse.id]
                            data[warehouse.id] = value + quant.quantity
                        else:
                            qty = qty + quant.quantity
                            data[warehouse.id] = qty
                            keys.append(warehouse.id)
                            qty = 0

            for key, value in data.items():
                new = self.env['available.quantity'].create({'warehouse_id': key, 'available_qty': value})
                self.available_qty_ids = [(4, new.id)]
        else:
            self.available_qty_ids = False
