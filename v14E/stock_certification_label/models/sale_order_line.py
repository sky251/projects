from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    certification_ids = fields.One2many(comodel_name="certification.certification", inverse_name="sale_line_id",
                                        string="Certifications")
    manufacture_date = fields.Date(string="Manufacturing / Re-control Date", default=date.today())
    extra_annotation = fields.Text(string="Extra annotation")

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'product_packaging': self.product_packaging or False,
        })
        return values


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
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
        res = super(SaleOrder, self).write(vals)
        line_without_certification = []
        for line in self.order_line:
            if not any(line.certification_ids.mapped('is_active')):
                line_without_certification.append(line.name)
        if line_without_certification:
            n1 = '\n'
            raise UserError(
                f"There is No active Certification Please activate at least one certification in \nLine Product :\n {n1.join(line_without_certification)}")
        return res
