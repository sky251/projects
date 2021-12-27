from odoo import models, api, fields


class Product(models.Model):
    _inherit = "product.product"

    lot_ids = fields.Many2many("stock.production.lot", compute="get_lot_names")

    def get_lot_names(self):
        for rec in self:
            lot_names = [i.name for i in self.env['stock.production.lot'].search([('product_id', '=', rec.id)])]
            rec.lot_ids = [(6, 0, lot_names)]