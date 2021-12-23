# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OpenSaleOrder(models.TransientModel):
    _name = "open.sale.order.wizard"
    _description = "Open Sale Orders"

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)
    is_for_all_customers = fields.Boolean("All Customers?", default=True)
    report_for = fields.Selection([('partner', 'Partner'), ('categ', 'Product Category')], default="partner",
                                  required=True)
    customer_ids = fields.Many2many('res.partner', string="Select Customers")
    category_ids = fields.Many2many('product.category', string="Select Categories")
    is_for_all_categories = fields.Boolean("All Categories?", default=True)

    def get_report(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Please provide valid dates.")
        customer_ids = []
        categ_ids = []
        if self.is_for_all_customers:
            customer_ids = self.env['res.partner'].search([]).ids
        else:
            customer_ids = self.customer_ids.ids
        if not self.is_for_all_categories:
            categ_ids = self.category_ids.ids

        data = {
            'report_for': self.report_for,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'customer_ids': customer_ids,
            'categories': categ_ids or False,
        }
        if self._context.get('report_type') == 'pdf':
            return self.env.ref('ak_open_so_report.action_report_open_saleorder').report_action([], data=data)
        if self._context.get('report_type') == 'xlsx':
            self.env.ref('ak_open_so_report.action_report_open_saleorder_xlsx').report_file = "Open Sale Orders"
            return self.env.ref('ak_open_so_report.action_report_open_saleorder_xlsx').report_action([], data=data)

    # report_file = "New_name.xlsx"
    @api.onchange('report_for')
    def onchange_report_for(self):
        """onchange partner and categ"""
        for rec in self:
            if rec.report_for == 'partner':
                rec.is_for_all_customers = True
                rec.is_for_all_categories = True
            if rec.report_for == 'categ':
                rec.is_for_all_customers = True
                rec.is_for_all_categories = True
