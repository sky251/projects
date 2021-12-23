from odoo import _, api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    label_height = fields.Integer(related="packaging_type_id.label_height", store=True)


class ProductPackagingType(models.Model):
    _inherit = "product.packaging.type"

    label = fields.Selection(
        [("200_50", "200x50mm"), ("200_60", "200x60mm"), ("200_70", "200x70mm"),
         ("200_100", "200x100mm"), ("200_150", "200x150mm"), ("200_180", "200x180mm")],
        string="Label")
    tare = fields.Float(string="Tare (kg)", digits=(16, 2))
    label_height = fields.Integer(store=True)

    @api.onchange('label')
    def get_label_height(self):
        for rec in self:
            if rec.label == '200_50':
                rec.label_height = 50
            if rec.label == '200_60':
                rec.label_height = 60
            if rec.label == '200_70':
                rec.label_height = 70
            if rec.label == '200_100':
                rec.label_height = 100
            if rec.label == '200_150':
                rec.label_height = 150
            if rec.label == '200_180':
                rec.label_height = 180
