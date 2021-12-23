from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    certification_ids = fields.One2many(comodel_name="certification.certification", inverse_name="purchase_line_id",
                                        string="Certifications")

    @api.onchange("product_id")
    def onchange_on_product_id_certification(self):
        if self.product_id and self.product_id.certification_ids:
            required_certification = [certification_id.name for certification_id in self.product_id.certification_ids if
                                      certification_id not in self.order_id.partner_id.certification_ids]
            if required_certification:
                return {
                    'warning': {
                        'title': 'Warning',
                        'message':
                            'The product you are adding requires the certifications ({}) that the supplier does not have'.format(
                                ",".join(required_certification))
                    }
                }


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        line_without_certification = []
        for line in res.order_line:
            if not any(line.certification_ids.mapped('is_active')):
                line_without_certification.append(line.name)
        if line_without_certification:
            n1 = '\n'
            raise UserError(
                f"There is No active Certification Please activate at least one certification in \nLine Product :\n {n1.join(line_without_certification)}")

        return res

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        line_without_certification = []
        for line in self.order_line:
            if not any(line.certification_ids.mapped('is_active')):
                line_without_certification.append(line.name)
        if line_without_certification:
            n1 = '\n'
            raise UserError(
                f"There is No active Certification Please activate at least one certification in \nLine Product :\n {n1.join(line_without_certification)}")
        return res
