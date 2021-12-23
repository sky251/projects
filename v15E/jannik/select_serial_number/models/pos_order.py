from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    def _order_line_fields(self, line, session_id=None):
        if line and 'name' not in line[2]:
            session = self.env['pos.session'].browse(session_id).exists() if session_id else None
            if session and session.config_id.sequence_line_id:
                # set name based on the sequence specified on the config
                line[2]['name'] = session.config_id.sequence_line_id._next()
            else:
                # fallback on any pos.order.line sequence
                line[2]['name'] = self.env['ir.sequence'].next_by_code('pos.order.line')

        if line and 'tax_ids' not in line[2]:
            product = self.env['product.product'].browse(line[2]['product_id'])
            line[2]['tax_ids'] = [(6, 0, [x.id for x in product.taxes_id])]
        if 'lot_name' in line[2]['pack_lot_ids'][0][2]:
            lot = self.env['stock.production.lot'].search([('name', '=', line[2]['pack_lot_ids'][0][2].get('lot_name')), ('product_id', '=', line[2]['product_id'])])
            if lot:
                line[2]['tax_ids'] = [(4, tax.id) for tax in lot.tax_ids]
        # Clean up fields sent by the JS
        line = [
            line[0], line[1], {k: v for k, v in line[2].items() if k in self.env['pos.order.line']._fields}
        ]
        return line