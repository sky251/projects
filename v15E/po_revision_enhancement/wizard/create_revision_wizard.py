from odoo import api, fields, models
from datetime import datetime, date


class CreateRevisionWizard(models.TransientModel):
    _name = "create.revision.wizard"
    _description = "Create Revision Wizard"

    description_of_change = fields.Text(string='Description on Revised PO', required=True)

    def create_purchase_order(self):
        po = self.env['purchase.order'].browse(self._context.get('active_id'))
        order_line = []
        for line in po.order_line:
            order_line.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_qty': line.product_qty,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
            }))

        sequence = self.env["ir.sequence"].next_by_code("revision.history.sequence.code")
        data = {
            'name': po.name + sequence,
            'partner_id': po.partner_id.id,
            'order_line': order_line,
            'revised_po': True,
            'po_id': po.id,
        }
        revised_po = self.env['purchase.order'].create(data)

        revision_history = [
            (0, 0,
             {'revision_level': 'High', 'desc_of_change': self.description_of_change, 'revision_date': date.today(),
              'approval_stamp_id': self.env.user.id, 'revision_purchase_name': revised_po.name,
              'revision_purchase_id': revised_po.id})]
        po.revision_ids = revision_history
        po.latest_revision_date = date.today()
        po.last_rev_id = revised_po.id
