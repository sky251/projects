from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    certification_ids = fields.Many2many(comodel_name="product.certification", string="Certifications")
    warning_ids = fields.Many2many(comodel_name="product.warning", string="Warnings")
    warning_word = fields.Char(string="Warning Word", translate=True)
    conservation = fields.Char(string="Conservation / Caution", translate=True)
    un_number = fields.Integer(string="UN Number")
    un_denomination = fields.Char(string="UN denomination", translate=True)
    hp_phrases = fields.Text(string="H and P phrases", translate=True)
    sc_cas = fields.Char(string="CAS")
    ec_text = fields.Char(string="EC text")
    origin_agriculture_bio = fields.Selection(
        [("eu_agriculture", "EU Agriculture"), ("no_eu_agriculture", "No EU Agriculture")],
        string="Origin of agriculture BIO")
