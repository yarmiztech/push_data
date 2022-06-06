# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, api, models,_


class POSOrder(models.Model):
    _inherit = 'pos.order'

    def default_branch_user(self):
        return self.env.user.branch_id.id
        # self.env.user.company_id

    branch_id = fields.Many2one('company.branches',default=default_branch_user)



class ResUsers(models.Model):
    _inherit = "res.users"
    branch_id = fields.Many2one('company.branches')

class AccountMove(models.Model):
    _inherit = 'account.move'
    branch_id = fields.Many2one('company.branches')
    #
    # @api.onchange('branch_id')
    # def onchange_branch_id(self):
    #     if self.branch_id:
    #         print(self.name)
    #
    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('/')) == _('/'):
    #         if 'company_id' in vals:
    #             vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
    #                 'account.move') or _('New')
    #         else:
    #             vals['name'] = self.env['ir.sequence'].next_by_code('account.move') or _('New')
    #
    #     res = super(AccountMove, self).create(vals)
        # if 'branch_id' in vals:
        #     print('dfgfdg')
        #     if self.env['account.move'].search([('branch_id','=',res.branch_id.id)]):
        #         if len(self.env['account.move'].search([('branch_id', '=', res.branch_id.id)])) >=2:
        #             last_move_id  = self.env['account.move'].search([('branch_id', '=', res.branch_id.id)])[1].name[-4:]
        #             last_move_id = int(last_move_id)
        #             prefit = self.env['account.move'].search([('branch_id','=',res.branch_id.id)])[1].name[:-4]
        #             # for i in len(last_move_id+1)
        #             res.name = prefit+'00'+str(last_move_id+1)
        # return res
class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    absolute_discount = fields.Float(string="Discount per Unit (abs)", default=0.0)


class PosConfig(models.Model):
    _inherit = 'pos.config'
    branch_id = fields.Many2one('company.branches')

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    branch_id = fields.Many2one('company.branches')

    @api.constrains('product_id','account_id','name')
    def constraint_product_id(self):
        if self.move_id:
            self.branch_id = self.move_id.branch_id


class pos_session(models.Model):
    _inherit = 'pos.session'


    @api.constrains('move_id')
    def onchange_move_id(self):
        if self.move_id:
                self.move_id.branch_id = self.config_id.branch_id
                for line in self.move_id.line_ids:
                    line.branch_id = self.config_id.branch_id

    def action_pos_session_closing_control(self):
        rec = super(pos_session, self).action_pos_session_closing_control()
        if self.move_id:
            self.move_id.branch_id = self.config_id.branch_id
        return rec
    # def action_pos_session_validate(self):
    #     rec = super(pos_session, self).action_pos_session_validate()
    #     # if self.cash_journal_id:
    #         # self.cash_journal_id.branch_id = self.config_id.branch_id
    #         # self.move_id.branch_id = self.config_id.branch_id
    #         if self.move_id:
    #             self.move_id.branch_id = self.config_id.branch_id
    #     return rec


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    branch_id = fields.Many2one('company.branches')

    def _select(self):
        return super(PosOrderReport, self)._select() + ',s.branch_id AS branch_id'

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',s.branch_id'



class PosDetails(models.TransientModel):
    _inherit = 'pos.details.wizard'
    _description = 'Point of Sale Details Report'
    branch_id = fields.Many2many('company.branches')



    def generate_report(self):
        branch_name = {}
        if self.branch_id:
        # for branch in self.branch_id:
        #     branch_name['branch'] =branch.name

            print(branch_name)
            data = {'date_start': self.start_date, 'date_stop': self.end_date, 'config_ids': self.pos_config_ids.search([('branch_id','=',self.branch_id.ids)]).ids,'branch_id':self.branch_id.mapped('name')}
            return self.env.ref('point_of_sale.sale_details_report').report_action([], data=data)
        else:
            return super(PosDetails, self).generate_report()