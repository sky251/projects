from odoo import api, fields, models, _


class PosOrderWizard(models.TransientModel):
    _name = 'pos.order.wizard'
    _description = 'Pos order Wizard'

    partner_id = fields.Many2one('res.partner', string='Partner')

    @api.model
    def action_open_wizard(self):
        ctx = self._context
        return {
            'name': 'Updated Customer',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
        }

    def update_selected_pos(self):
        for partner in self._context.get('active_ids'):
            self.env['pos.order'].browse(partner).partner_id = self.partner_id
