from odoo import api, models


class ReportDetails(models.AbstractModel):
    _name = "report.stock_certification_label.report_label"
    _description = "Report Details"

    @api.model
    def _get_report_values(self, docids, data=None):

        # partners = self.env['res.partner'].browse(data.get('customer_ids'))
        return {
                # 'docs': self.env.company,
                'data': data,
                'company' : self.env.company
                }