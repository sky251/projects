from odoo import api, fields, models

class LozanoReport(models.Model):
    _name = 'lozano.report'
    _description = 'LozanoReport'

    name = fields.Char(string="Name")

