from odoo import models, fields, api


class ProductWarning(models.Model):
    _name = "product.warning"
    _description = "Warning"

    image = fields.Binary()
    name = fields.Char(string="Name")
    text_to_print = fields.Text(string="Text to print", translate=True)

