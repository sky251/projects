from odoo import api, fields, models


class AvailableQuantity(models.Model):
    _name = 'available.quantity'
    _description = 'AvailableQuantity'

    product_id = fields.Many2one('product.product', string='Product')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    available_qty = fields.Float(string='Available Quantity')
