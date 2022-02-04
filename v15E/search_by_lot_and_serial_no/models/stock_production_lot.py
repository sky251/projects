from odoo import api, fields, models

class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def get_lot_no(self):
        print("\n\n\n\n\n get Lot calling")
