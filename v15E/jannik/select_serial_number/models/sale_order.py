# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import json


class SaleOrder(models.Model):
    _inherit = "sale.order"

    lot_ids = fields.Many2many('stock.production.lot', string="Lot/Serial Number", copy=False, compute="compute_order_line_lot")

    def compute_order_line_lot(self):
        for record in self:
            lot_list = []
            record.lot_ids = False
            for order_line in record.order_line:
                if order_line.stock_lot_id:
                    lot_list.append(order_line.stock_lot_id.id)
            if lot_list:
                record.lot_ids = lot_list

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.picking_ids:
            for picking in self.picking_ids:
                for move in picking.move_ids_without_package:
                    order_line_id = self.env['sale.order.line'].search(
                        [('order_id', '=', self.id), ('product_id', '=', move.product_id.id)])
                    if order_line_id and order_line_id.stock_lot_id:
                        for line in order_line_id:
                            if line.product_tracking == 'lot' or line.product_tracking == 'serial':
                                move.write(
                                    {'lot_id': line.stock_lot_id.id})
        return res

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_taxes(order_line):
            price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
            order = order_line.order_id
            if order_line.lot_id and order_line.product_id.tracking in ['lot','serial']:
                other_taxes = order_line.tax_id._origin.filtered(lambda tax: tax.amount_type !='based_on_margin').compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)
                lot_id = self.env['stock.production.lot'].search([('name', '=', order_line.lot_id), ('product_id', '=', order_line.product_id.id)])
                sh_taxes = {}
                if lot_id.tax_ids.filtered(lambda tax: tax.amount_type == 'based_on_margin'):
                    if lot_id.cost_price:
                        price -= lot_id.cost_price
                        sh_taxes =  order_line.tax_id._origin.filtered(lambda tax: tax.amount_type =='based_on_margin').compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)
                        if sh_taxes and sh_taxes['taxes']:
                            other_taxes['taxes'].append(sh_taxes['taxes'][0])
                            other_taxes['total_included'] += sh_taxes['taxes'][0]['amount']
                            if order_line.tax_id._origin.filtered(lambda tax: tax.amount_type =='based_on_margin').price_include:
                                # order.amount_total += other_taxes['total_included']
                                order.amount_total = 0
                                # for i in order_line.order_id.order_line:
                                taxts = 0
                                for y in other_taxes['taxes']:
                                    taxts += y['amount']
                                order_line.price_subtotal = order_line.product_id.list_price * order_line.product_uom_qty - taxts
                                order.amount_total += order_line.price_subtotal
                                for y in other_taxes['taxes']:
                                    order.amount_total += y['amount']
                    return other_taxes
            else:
                return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)

        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            total = order.amount_untaxed + sum(i['tax_amount'] for i in tax_lines_data if 'tax_amount' in i)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, total, order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    stock_lot_id = fields.Many2one(
        'stock.production.lot', string="Lot", copy=False)
    lot_id = fields.Char(string="Lot/Serial", copy=False)
    product_tracking = fields.Selection(related="product_id.tracking")

    @api.onchange('product_id', 'lot_id', 'product_uom_qty')
    def onchange_lot_number(self):
        if self.product_id:
            if self.product_tracking == 'lot' or self.product_tracking == 'serial':
                if self.lot_id:
                    check_lot_ids = self.env['stock.production.lot'].search(
                        [('name', '=', self.lot_id)])
                    if check_lot_ids:
                        if any(lot.product_id.id == self.product_id.id for lot in check_lot_ids):
                            for lot in check_lot_ids.filtered(lambda lot: lot.product_id.id == self.product_id.id):
                                if lot.product_id.id == self.product_id.id:
                                    if self.product_uom_qty and self.product_uom_qty > 1:
                                        raise ValidationError(_('You cannot enter quantity greater than 1.'))
                                    if self.product_uom_qty > lot.product_qty:
                                        raise ValidationError(
                                            _('This product is not in stock.'))
                                    else:
                                        if lot.id in self.order_id.lot_ids.ids:
                                            raise ValidationError(_('Given Lot Number already exist with same product.'))
                                        if lot and lot.tax_ids:
                                            self.tax_id = [
                                                (6, 0, lot.tax_ids.ids)]
                                            # self.order_id.lot_ids = [
                                            #     (6, 0, lot.id)]
                                            self.stock_lot_id = lot.id
                                else:
                                    raise ValidationError(
                                        _('This product does not exist in the given Lot Number.'))
                        else:
                            raise ValidationError(
                                _('This product does not exist in the given Lot Number.'))
                    else:
                        raise ValidationError(
                            _('Please enter a valid Serial Number.'))
        else:
            self.lot_id = False
            self.stock_lot_id = False

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        lot = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id),('name', '=', self.lot_id)])
        res.update({'lot_id': lot})
        return res
