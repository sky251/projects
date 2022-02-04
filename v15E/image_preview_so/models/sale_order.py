from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    image_ids = fields.One2many('image.image','sale_id',string='Select Image')