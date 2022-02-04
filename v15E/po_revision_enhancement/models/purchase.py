from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    revised_po = fields.Boolean(string="Revised PO", default=False, copy=False, readonly=True, tracking=True)
    approved = fields.Boolean(string="Approved?", default=False, copy=False, readonly=True, tracking=True)
    po_id = fields.Many2one('purchase.order', default=False, copy=False, readonly=True)
    rfq_approver_id = fields.Many2one('res.users', string='RFQ Approver', copy=False)
    last_rev_id = fields.Many2one('revision.history', compute='_compute_get_last_record', copy=False, invisible=True)
    from_apporoval_datetime = fields.Datetime(default=datetime.today())
    to_apporoval_datetime = fields.Datetime(default=datetime.today() + timedelta(days=2))
    revision_ids = fields.One2many('revision.history', 'revision_purchase_id', default=False, copy=False)
    latest_revision_date = fields.Datetime(copy=False, invisible=True)
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('approve', 'Approve'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    @api.onchange('rfq_approver_id')
    def onchange_rfq_approver(self):
        for order in self:
            if order.rfq_approver_id.id == order.env.user.id:
                raise UserError(_("Select different RFQ Approver than logged in user"))

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        if 'rfq_approver_id' in vals and vals.get('rfq_approver_id'):
            template = self.env.ref('po_revision_enhancement.rfq_approver_mail_template')
            template.send_mail(self.id)
        return res

    def _compute_get_last_record(self):
        record = self.env['revision.history'].search([('revision_purchase_id', '=', self.id)], limit=1,
                                                     order='create_date desc')
        if record:
            self.last_rev_id = record.id
        else:
            self.last_rev_id = False
        print("\n\n\n Record", record.desc_of_change)

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'approve']:
                continue
            if order.revised_po:
                if not order.rfq_approver_id:
                    raise ValidationError(_('Select RFQ Approver'))
                if not order.approved and order.rfq_approver_id.id != order.env.user.id:
                    raise ValidationError(_('this order need to approve before confirm order.'))
                if order.rfq_approver_id.id == order.env.user.id:
                    raise ValidationError(_('You cannot confirm this Order'))

            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def button_approve_action(self):
        for order in self:
            if order.revised_po:
                if not order.rfq_approver_id:
                    raise ValidationError(_('Select RFQ Approver'))

                if order.env.user.id == order.rfq_approver_id.id:
                    order.state = 'approve'
                    order.approved = True

                else:
                    raise ValidationError(_('You are not RFQ Approver of this record'))

    def action_open_menu(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'To Approve PO',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'views': [
                [self.env.ref('purchase.purchase_order_kpis_tree').id, 'list'],
                [self.env.ref('purchase.purchase_order_form').id, 'form']
            ],
            'domain': [('approved', '=', False), ('revised_po', '=', True),
                       ('rfq_approver_id.id', '=', self.env.user.id)]}
