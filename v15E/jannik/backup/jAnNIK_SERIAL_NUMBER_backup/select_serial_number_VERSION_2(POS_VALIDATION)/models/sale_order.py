# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print("\n\n\n\n\n action_confirm::::::::::::::::::::::::::::::::::",
              res, self, self.picking_ids)
        if self.picking_ids:
            for picking in self.picking_ids:
                print("\n\n\n\n picking:::::::::::::::::::::::::::::::::", picking)
                for move in picking.move_ids_without_package:
                    print("\n\n\n move:::::::::::::::::::::beforrrrrrrrrrrrrrrr:::::::::",
                          move, move.product_id, move.lot_id)
                    order_line_id = self.env['sale.order.line'].search(
                        [('order_id', '=', self.id), ('product_id', '=', move.product_id.id)])
                    print(
                        "\n\n\n orderrrrrrrrrrrrrrrrrrrrrrrrrrr lineeeeeeeeeee", order_line_id)
                    # lot_list = []
                    if order_line_id and order_line_id.stock_lot_id:
                        if order_line_id.product_tracking == 'lot' or order_line_id.product_tracking == 'serial':
                        # check_lot_id =
                            print("\n\n\n order_line_id.stock_lot_id.id##########",
                                  order_line_id.stock_lot_id.id)
                            # lot_list.append(order_line_id.lot_id.id)
                            move.write({'lot_id': order_line_id.stock_lot_id.id})
                            print("\n\n\n move:::::::::::::::::afterrrrrrrrrrrrrrr:::::::::::::",
                                  move, move.product_id, move.lot_id)
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    stock_lot_id = fields.Many2one('stock.production.lot', string="Lot", copy=False)
    lot_id = fields.Char(string="Lot/Serial", copy=False)
    # tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False),
    #                                                                  ('active', '=', True)], compute="get_lot_taxes")
    product_tracking = fields.Selection(related="product_id.tracking")

    @api.onchange('product_id', 'lot_id', 'product_uom_qty')
    def onchange_lot_number(self):
        if self.product_id:
            if self.product_tracking == 'lot' or self.product_tracking == 'serial':
                if self.lot_id:
                    check_lot_ids = self.env['stock.production.lot'].search(
                        [('name', '=', self.lot_id)])
                    print(
                        "\n\n\n check_lot_ids#####################################", check_lot_ids)
                    if check_lot_ids:
                        if any(lot.product_id.id == self.product_id.id for lot in check_lot_ids):
                            for lot in check_lot_ids.filtered(lambda lot: lot.product_id.id == self.product_id.id):
                                print("\n\n\n\n LOtttt checcccccccccccccccccccccccccccc", lot)
                                print("\n\n\n\n PRODUCTTTTTTTTTTTTTTTTTTTTTTTT detailsssssssssssssssss",
                                      lot.product_id, self.product_id, self.product_uom_qty, lot.product_qty)
                                if lot.product_id.id == self.product_id.id:
                                    if self.product_uom_qty > lot.product_qty:
                                        raise ValidationError(
                                            _('This product is not in stock.'))
                                    else:
                                        print("\n\n\n\n taxesssssssssssssssss append")
                                        if lot and lot.tax_ids:
                                            self.tax_id = [(6, 0, lot.tax_ids.ids)]
                                            self.stock_lot_id = lot.id
                                else:
                                    raise ValidationError(
                                        _('This product does not exist in the given Lot Number.'))
                    else:
                        raise ValidationError(
                            _('Please enter a valid Serial Number.'))
        else:
            self.lot_id = False
            self.stock_lot_id = False

    # @api.depends('lot_id')
    # def get_lot_taxes(self):
    #     """get taxes from lot"""
    #     for rec in self:
    #         rec.tax_id = False
    #         if rec.lot_id and (rec.product_tracking == 'lot' or rec.product_tracking == 'serial'):
    #             lot_id = self.env['stock.production.lot'].search(
    #                 [('name', '=', rec.lot_id)])
    #             print("\n\n\n\n lotttttttttttttttttttttttt ", lot_id)
    #             if lot_id and lot_id.tax_ids:
    #                 rec.tax_id = [(6, 0, lot_id.tax_ids.ids)]
    #             # else:
    #             #     rec.tax_id = False

    # def _prepare_procurement_values(self, group_id=False):
    #     res = super()._prepare_procurement_values(group_id)
    #     if self.product_id.type == 'product' and self.lot_id and (self.product_tracking == 'lot' or self.product_tracking == 'serial'):
    #         lot_id = self.env['stock.production.lot'].search(
    #             [('name', '=', self.lot_id)])
    #         print("\n\n\n\n lotttttttttttttttttttttttt _prepare_procurement_values ", lot_id)
    #         if lot_id:
    #             res.update({'lot_id': lot_id.id})
    #     return res
