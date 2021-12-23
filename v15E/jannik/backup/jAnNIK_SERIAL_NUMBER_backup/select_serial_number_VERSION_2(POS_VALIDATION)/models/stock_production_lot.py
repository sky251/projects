# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    tax_ids = fields.Many2many('account.tax', string="Taxes", copy=False)

    def get_lot_taxes(self, product, lot):
        print("\n\n\n\n\n\n lottttttttttttttttttttttttttttttttttttttttt", product, lot, product[0], lot[0])
        lot_ids = self.search([('name', '=', lot[0])])
        print("\n\n\n\n lotttttttttttttttttttttttttssssssssssssssssssssssss lot_ids", lot_ids)
        response_msg = []
        # tax_name = []
        if lot_ids:
            if any(lot.product_id.id == product[0] for lot in lot_ids):
            # if any()
                for lot in lot_ids.filtered(lambda lot: lot.product_id.id == product[0]):
                    # if lot.product_id.id == product[0]:
                    product_uom_qty = 1
                    if product_uom_qty > lot.product_qty:
                        response_msg.append({'msg': 'This product is not in stock.'})
                    else:
                        print("\n\n\n\n taxesssssssssssssssss append")
                        if lot and lot.tax_ids:
                            for tax in lot.tax_ids:
                                response_msg.append({'id': tax.id, 'name': tax.name})
                            # self.tax_id = [(6, 0, lot.tax_ids.ids)]
                            # self.stock_lot_id = lot.id
            else:
                response_msg.append({'msg': 'This product does not exist in the given Lot Number.'})


            # move_line_id = self.env['stock.move.line'].search(
            #     [('product_id', '=', product), ('lot_id', '=', lot_id.id)], order='id desc', limit=1)
            # print("\n\n\n\n move_line_id:::::::::::::::::::::::", move_line_id)
            # if move_line_id and move_line_id.origin:
            #     purchase_id = self.env['purchase.order'].search(
            #         [('name', '=', move_line_id.origin)])
            #     print(
            #         "\n\n\n\n purchase_id#########################################", purchase_id)
            #     if purchase_id and purchase_id.second_hand_tax and move_line_id.tax_code:
            #         for tax in move_line_id.tax_code:
            #             response_msg.append({'id': tax.id, 'name': tax.name})

            # for tax in lot_id.tax_ids:
            #     response_msg.append({'id':tax.id,'name':tax.name})
        else:
            response_msg.append({'msg': 'Please enter a valid Serial Number.'})
        print("\n\n\n\nn\n RESPONSEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE MSGESSSSSSSSSSSSSSSSSSSSSSSSSSSSS", response_msg)
        return response_msg

    # def get_lot_taxes(self, lot):
    #     lot_id = self.search([('name', '=', lot[0])])
    #     tax_name = []
    #     if lot_id:
    #         for tax in lot_id.tax_ids:
    #             tax_name.append({'id': tax.id, 'name': tax.name})
    #     return tax_name


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
