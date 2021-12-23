from odoo import fields, api, models
import json


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends('line_ids.amount_currency', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        """ Computed field used for custom widget's rendering.
            Only set on invoices.
        """
        def compute_taxes(line):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            order = line.move_id
            if line.lot_id and line.product_id.tracking in ['lot','serial']:
                sh_taxes = {}
                other_taxes = line.tax_ids._origin.filtered(lambda tax: tax.amount_type !='based_on_margin').compute_all(price, order.currency_id, line.quantity, product=line.product_id, partner=order.partner_shipping_id)
                if line.lot_id.tax_ids.filtered(lambda tax: tax.amount_type == 'based_on_margin'):
                    if line.lot_id.cost_price:
                        price -= line.lot_id.cost_price
                        sh_taxes =  line.tax_ids._origin.filtered(lambda tax: tax.amount_type =='based_on_margin').compute_all(price, order.currency_id, line.quantity, product=line.product_id, partner=order.partner_shipping_id)
                        if sh_taxes:
                            other_taxes['taxes'].append(sh_taxes['taxes'][0])
                            other_taxes['total_included'] += sh_taxes['taxes'][0]['amount']
                            order.amount_total = other_taxes['total_included']
                            if line.tax_ids._origin.filtered(lambda tax: tax.amount_type =='based_on_margin').price_include:
                                # order.amount_total = 0
                                # for i in line.move_id.invoice_line_ids:
                                #     order.amount_total += i.price_subtotal
                                # for i in other_taxes['taxes']:
                                #     order.amount_total += i['amount']
                                order.amount_total = 0
                                # for i in order_line.order_id.order_line:
                                taxts = 0
                                for y in other_taxes['taxes']:
                                    taxts += y['amount']
                                line.price_subtotal = line.product_id.list_price * line.quantity - taxts
                                order.amount_total += line.price_subtotal
                                for y in other_taxes['taxes']:
                                    order.amount_total += y['amount']
                return other_taxes
            else:
                return line.tax_ids._origin.compute_all(price, order.currency_id, line.quantity, product=line.product_id, partner=order.partner_shipping_id)
                
        for move in self:
            if not move.is_invoice(include_receipts=True):
                # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
                move.tax_totals_json = None
                continue
            tax_lines_data = move._prepare_tax_lines_data_for_totals_from_object(move.invoice_line_ids, compute_taxes)
            total = move.amount_untaxed + sum(i['tax_amount'] for i in tax_lines_data if 'tax_amount' in i)
            move.tax_totals_json = json.dumps({
                **self._get_tax_totals(move.partner_id, tax_lines_data, total, move.amount_untaxed, move.currency_id),
                'allow_tax_edition': move.is_purchase_document(include_receipts=False) and move.state == 'draft',
            })


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    lot_id = fields.Many2one('stock.production.lot')