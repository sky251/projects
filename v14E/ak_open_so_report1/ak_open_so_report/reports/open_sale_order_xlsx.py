# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import models
from odoo import api, fields, models
from xlwt import easyxf
from datetime import datetime
import pandas
from odoo.exceptions import ValidationError


class OpenSaleOrderXlsx(models.TransientModel):
    _name = "report.ak_open_so_report.report_open_so_wizard_xlsx"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        partners = self.env['res.partner'].browse(data.get('customer_ids'))
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d %H:%M:%S")
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

        if not picking_ids:
            raise ValidationError("No pending Sale Orders.")

        if data.get('categories'):
            product_category_ids = self.env['product.category'].search([('id', 'in', categories_used)]).browse(
                data.get('categories'))
        else:
            product_category_ids = self.env['product.category'].search([('id', 'in', categories_used)])

        sheet = workbook.add_worksheet('open sale order')
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 22)
        sheet.set_column('C:C', 25)
        sheet.set_column('E:E', 17)
        sheet.set_column('G:G', 10)
        bold = workbook.add_format({'bold': True, 'valign': 'vcenter', 'align': 'center', 'fg_color': '#cccccc'})
        header_label = workbook.add_format({'bold': True, 'valign': 'vcenter', 'align': 'center', 'border': 6})
        align_left = workbook.add_format({'bold': True, 'fg_color': '#D7E4BC'})
        center = workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        left = workbook.add_format({'align': 'right'})
        right = workbook.add_format({'align': 'left'})
        sheet.merge_range(1, 2, 2, 4, "Open Sale Order Report", header_label)
        sheet.write(4, 0, "Start Date :")
        sheet.write(4, 1, start_date.strftime('%Y-%m-%d'), right)
        sheet.write(4, 5, "End Date :", left)
        sheet.write(4, 6, end_date.strftime('%Y-%m-%d'), center)
        row = 6
        col = 0

        # partners xlsx report
        if data.get('report_for') == "partner":
            sheet.set_column('D:D', 28)
            sheet.set_column('F:F', 27)
            for obj in partners:
                sheet.write(row, col, 'Name : ', bold)
                col = col + 1
                sheet.merge_range(row, col, row, col + 1, obj.name, align_left)
                row = row + 2
                col = 0
                sheet.write(row, col, 'Sr no', bold)
                col = col + 1
                sheet.write(row, col, 'Order Date', bold)
                col = col + 1
                sheet.write(row, col, 'Expected Delivery Date', bold)
                col = col + 1
                sheet.write(row, col, 'Product Name', bold)
                col = col + 1
                sheet.write(row, col, 'Sale Order', bold)
                col = col + 1
                sheet.write(row, col, 'Product category', bold)
                col = col + 1
                sheet.write(row, col, 'Qty', bold)
                row = row + 1
                col = 0
                counter = 1
                for picking in picking_ids.filtered(lambda x: x.partner_id == obj):
                    for line in picking.move_ids_without_package:
                        sheet.write(row, col, counter, center)
                        col = col + 1
                        sheet.write(row, col, line.picking_id.sale_id.date_order.strftime('%Y-%m-%d'), center)
                        col = col + 1
                        sheet.write(row, col, line.picking_id.sale_id.expected_date.strftime('%Y-%m-%d'), center)
                        col = col + 1
                        sheet.write(row, col, line.product_id.name, center)
                        col = col + 1
                        sheet.write(row, col, line.picking_id.sale_id.name, center)
                        col = col + 1
                        sheet.write(row, col, line.product_id.categ_id.display_name, center)
                        col = col + 1
                        sheet.write(row, col, line.product_uom_qty, center)
                        counter = counter + 1
                        row = row + 1
                        col = 0
                row = row + 3
                col = 0

        else:
            for doc in product_category_ids:
                sheet.set_column('F:F', 20)
                sheet.set_column('D:D', 25)
                sheet.write(row, col, 'Name : ', bold)
                col = col + 1
                sheet.merge_range(row, col, row, col + 1, doc.display_name, align_left)
                row = row + 2
                col = 0
                sheet.write(row, col, 'Sr no', bold)
                col = col + 1
                sheet.write(row, col, 'Order Date', bold)
                col = col + 1
                sheet.write(row, col, 'Expected Delivery Date', bold)
                col = col + 1
                sheet.write(row, col, 'Product Name', bold)
                col = col + 1
                sheet.write(row, col, 'Sale Order', bold)
                col = col + 1
                sheet.write(row, col, 'Product category', bold)
                col = col + 1
                sheet.write(row, col, 'Qty', bold)
                row = row + 1
                col = 0
                counter = 1
                for picking in picking_ids.filtered(lambda x: x.product_id.categ_id == doc):
                    for line in picking.move_ids_without_package:
                        sheet.write(row, col, counter, center)
                        col = col + 1
                        sheet.write(row, col, line.picking_id.sale_id.date_order.strftime('%Y-%m-%d'), center)
                        col = col + 1
                        sheet.write(row, col, line.picking_id.sale_id.expected_date.strftime('%Y-%m-%d'), center)
                        col = col + 1
                        sheet.write(row, col, line.product_id.name, center)
                        col = col + 1
                        sheet.write(row, col, picking.partner_id.name, center)
                        col = col + 1
                        sheet.write(row, col, picking.sale_id.name, center)
                        col = col + 1
                        sheet.write(row, col, line.product_uom_qty, center)
                        counter = counter + 1
                        row = row + 1
                        col = 0
                row = row + 3
                col = 0
