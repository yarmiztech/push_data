# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, api, models


class Employee(models.Model):
    _inherit = "hr.employee"

    branch_id = fields.Many2one('company.branches')

    @api.onchange('user_id')
    def onchange_user_id_n(self):
        if self.user_id:
            self.branch_id = self.user_id.branch_id

class ProductTemplate(models.Model):
    _inherit = "product.template"

    branch_id = fields.Many2one('company.branches')



class Location(models.Model):
    _inherit = "stock.location"

    branch_id = fields.Many2one('company.branches', string='Branch Name')

