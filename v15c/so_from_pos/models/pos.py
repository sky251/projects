from odoo import api, fields, models, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    sale_id = fields.Many2one('sale.order', string="Sale Order Ref", readonly=True)

    @api.model
    def create(self, values):
        res = super().create(values)
        if values.get('partner_id'):
            order_line = []
            for line in res.lines:
                order_line.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.full_product_name,
                    'product_uom_qty': line.qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                }))
            for value in res:
                data = {
                    'partner_id': value.partner_id.id,
                    'order_line': order_line,
                    'date_order': value.date_order,
                    'pricelist_id': value.pricelist_id.id,
                    'user_id': value.user_id.id,
                    'company_id': value.company_id.id,
                    'pos_id': value.id,
                }
            so = self.env['sale.order'].create(data)
            res.sale_id = so.id
        return res


