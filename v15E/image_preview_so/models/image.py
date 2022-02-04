from odoo import api, fields, models


class Images(models.Model):
    _name = 'image.image'
    _description = 'Images'

    image = fields.Binary(string='Image')
    sale_id = fields.Many2one('sale.order')
