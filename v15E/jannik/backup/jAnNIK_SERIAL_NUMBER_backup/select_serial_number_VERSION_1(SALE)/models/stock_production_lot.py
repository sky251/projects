# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    tax_ids = fields.Many2many('account.tax', string="Taxes", copy=False)

    def get_lot_taxes(self, lot):
        lot_id = self.search([('name', '=', lot[0])])
        tax_name = []
        if lot_id:
            for tax in lot_id.tax_ids:
                tax_name.append({'id': tax.id, 'name': tax.name})
        return tax_name


# class StockRule(models.Model):
#   _inherit = "stock.rule"

#   def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
#         res = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
#         res['lot_ids'] = [(6, 0, [values.get('lot_id', False)])]
#         return res


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_id = fields.Many2one('stock.production.lot',
                             string="Lot/Serial Number")

    # def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
    #     res = super()._prepare_move_line_vals(quantity, reserved_quant)
    #     if self.lot_ids:
    #         res.update({
    #             'lot_id': self.lot_ids.id,
    #             })
    #     return res
