from odoo import fields, api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move"

    product_packaging = fields.Many2one('product.packaging', string='Package')
