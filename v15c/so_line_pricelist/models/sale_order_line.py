from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    def select_pricelist_wizard_popup(self):
        return {
            'name': 'Select Pricelist',
            'type': 'ir.actions.act_window',
            'res_model': 'pricelist.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
