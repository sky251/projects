from odoo import fields, api, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super(StockRule,self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
                                                                   name,  origin, company_id, values)
        move_values['product_packaging'] = self.env['sale.order.line'].browse(
            values['sale_line_id']).product_packaging.id
        return move_values
