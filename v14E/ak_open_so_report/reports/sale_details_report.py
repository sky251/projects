# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import api, fields, models
from datetime import datetime, date
import pandas
from odoo.exceptions import ValidationError


class ReportSaleDetails(models.AbstractModel):
    _name = "report.ak_open_so_report.report_open_so_wizard"
    _description = "Report Sale Details"

    @api.model
    def _get_report_values(self, docids, data=None):
        partners = self.env['res.partner'].browse(data.get('customer_ids'))
        start_date = pandas.to_datetime(data.get('start_date'))
        end_date = pandas.to_datetime(data.get('end_date'))

        picking_ids = self.env['stock.picking'].search([('sale_id', '!=', False),
                                                        ('partner_id', 'in', partners.ids),
                                                        ('state', 'not in', ['done', 'cancelled']),
                                                        ('scheduled_date', '>=', start_date),
                                                        ('scheduled_date', '<=', end_date)])
        partners = picking_ids.mapped('partner_id')
        categories_used = []

        for pick in picking_ids:
            for line in pick.move_ids_without_package:
                categories_used.append(line.product_id.categ_id.id)
        print("\n\n\n\n\n categories_used ", categories_used)
        if not picking_ids:
            raise ValidationError("No pending Sale Orders.")

        if data.get('categories'):
            product_category_ids = self.env['product.category'].search([('id', 'in', categories_used)]).browse(
                data.get('categories'))
        else:
            product_category_ids = self.env['product.category'].search([('id', 'in', categories_used)])

        return {
            'docs': partners,
            'data': data,
            'picking_ids': picking_ids,
            'categories': product_category_ids,
        }
