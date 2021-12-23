from odoo import models, fields, api


class ProductCertification(models.Model):
    _name = "product.certification"
    _description = "Certification"

    image = fields.Binary()
    name = fields.Char(string="Name")
    inline_text = fields.Text(string="Inline text", translate=True)
    text_at_bottom = fields.Text(string="Text at the bottom", translate=True)


class CertificationActivation(models.Model):
    _name = "certification.certification"
    _description = "Certification Activation"

    certification_id = fields.Many2one('product.certification')
    is_active = fields.Boolean("Selection")
    sale_line_id = fields.Many2one(comodel_name="sale.order.line", string="Sale Line")
    sale_certification_ids = fields.Many2many(related="sale_line_id.product_id.certification_ids")
    purchase_certification_ids = fields.Many2many(related="purchase_line_id.product_id.certification_ids")
    purchase_line_id = fields.Many2one(comodel_name="purchase.order.line", string="Purchase Line")