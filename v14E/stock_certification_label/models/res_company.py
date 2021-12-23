from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    fda_reg_nr = fields.Char(string="FDA Registration nr")
    gen_cond_purchase = fields.Text(string="General conditions of purchase", translate=True)
    gen_cond_sale = fields.Text(string="General conditions of sale", translate=True)
    custom_agent_data = fields.Text(string="Customs agent data", translate=True)
