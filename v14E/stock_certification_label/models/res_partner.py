from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_schedule = fields.Text(string="Delivery Schedule")
    certification_ids = fields.Many2many('product.certification', string="Certifications")
