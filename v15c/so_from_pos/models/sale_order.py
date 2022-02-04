from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pos_id = fields.Many2one('pos.order', string="POS Order Ref", compute="get_pos_order_reference", readonly=True)

    def get_pos_order_reference(self):
        for rec in self:
            ref = self.env['pos.order'].search([('sale_id', '=', rec.id)])
            rec.pos_id = ref.id
