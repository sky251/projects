from odoo import api, fields, models, _


class PricelistWizard(models.TransientModel):
    _name = 'pricelist.wizard'
    _description = 'Pricelist Wizard'

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')

    def update_line_price_unit(self):
        for line in self.env['sale.order.line'].browse(self._context.get('active_id')):
            line.price_unit = self.pricelist_id.get_product_price(line.product_id, line.product_uom_qty,
                                                                  line.order_partner_id)
