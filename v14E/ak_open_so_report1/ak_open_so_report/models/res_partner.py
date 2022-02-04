# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
	_inherit = "res.partner"

	has_picking = fields.Boolean(compute='compute_picking')

	#this function is to check whether partner has any picking or not
	def compute_picking(self):
		for rec in self:
			picking_ids = self.env['stock.picking'].search([('sale_id', '!=', False), ('partner_id', '=', rec.id), ('state', 'not in', ['done', 'cancelled'])])
			if picking_ids:
				rec.has_picking = True
			else:
				rec.has_picking = False
