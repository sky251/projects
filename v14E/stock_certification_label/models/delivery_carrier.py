from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    light_label = fields.Boolean(string="Light Label")
