from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel_so(self):
        for order in self.browse(self._context.get('active_ids')):
            order.state = 'cancel'
            template = self.env.ref('cancel_so.cancel_so_mail_template')
            template.send_mail(order.id, email_values={"email_to": order.partner_id.email})
