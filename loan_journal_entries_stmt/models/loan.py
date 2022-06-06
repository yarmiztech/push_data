from odoo import fields,models,api,_
from odoo.tests.common import Form
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class HrLoan(models.Model):
    _inherit = 'hr.loan'


    payment_journal = fields.Many2one('account.journal',string='Payment Journal',domain=[('type', 'in', ('bank', 'cash'))])
    journal_created = fields.Boolean(string="Jcreate",default=False)
    loan_move_id = fields.One2many('account.move','loan_ref_id')


    def action_created_invoice(self):
        self.ensure_one()
        return {
            'name': ('Loan Journal'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'target': 'current',
            'res_id': self.loan_move_id.id,
            }


    def action_approve_journal(self):
            if not self.payment_journal:
                raise UserError(_("Please Select Payment Journal"))
            pay_id_list = []
            label = self.name
            temp = (0, 0, {
                'account_id': self.env['account.account'].sudo().search(
                    [('name', '=', 'Wages Payable'),
                     ('company_id', '=', self.company_id.id)]).id,
                'name': label,
                # 'move_id': move_id.id,
                'date': self.date,
                # 'partner_id': driver_id.id,
                'debit': self.loan_amount,
                'credit': 0,
            })
            pay_id_list.append(temp)
            acc =self.payment_journal.payment_credit_account_id
            temp = (0, 0, {
                'account_id': acc.id,
                'name': label,
                # 'move_id': move_id.id,
                'date': self.date,
                # 'partner_id': driver_id.id,
                'credit': self.loan_amount,
                'debit': 0,
            })
            pay_id_list.append(temp)
            vals = {
                'journal_id': self.payment_journal.id,
                'state': 'draft',
                'move_type': 'entry',
                'loan_ref_id': self.id,
                'line_ids':pay_id_list,
                'ref': self.employee_id.name + '/' + self.name,
            }
            pay_id_list = []
            move_id = self.env['account.move'].create(vals)
            for move in move_id:
                move.action_post()
            if self.env['account.bank.statement'].search([]):
                if self.env['account.bank.statement'].search(
                        [('company_id', '=', self.payment_journal.company_id.id),
                         ('journal_id', '=', self.payment_journal.id)]):
                    bal = self.env['account.bank.statement'].search(
                        [('company_id', '=', self.payment_journal.company_id.id),
                         ('journal_id', '=', self.payment_journal.id)])[
                        0].balance_end_real
                else:
                    bal = 0
            else:
                credit = sum(self.env['account.move.line'].search(
                    [('account_id', '=', self.payment_journal.payment_credit_account_id.id)]).mapped(
                    'debit'))
                debit = sum(self.env['account.move.line'].search(
                    [('account_id', '=', self.payment_journal.payment_debit_account_id.id)]).mapped(
                    'debit'))
                bal = debit - credit
            final = 0
            final = bal - self.loan_amount
            stmt = self.env['account.bank.statement'].create({'name': self.name,
                                                              'balance_start': bal,
                                                              'journal_id': self.payment_journal.id,
                                                              'balance_end_real': final
                                                              })
            payment_list = []
            supplier_amount = -self.loan_amount
            product_line = (0, 0, {
                'date': self.payment_date,
                'name': self.employee_id.name,
                'partner_id': self.payment_journal.company_id.partner_id.id,
                'payment_ref': self.name,
                'amount': supplier_amount
            })
            payment_list.append(product_line)
            if stmt:
                stmt.line_ids = payment_list
                # stmt.move_line_ids = move_id.line_ids.ids
                # stmt.line_ids = payment_list
                unwanted_move = stmt.move_line_ids.mapped('move_id')
                stmt.stmt_ref_lines = payment_list
                unwanted_move.unlink()
                stmt.write({'state': 'confirm'})
                # stmt.move_line_ids = False

            self.journal_created =True


class AccountMove(models.Model):
    _inherit = "account.move"
    loan_ref_id = fields.Many2one('hr.loan')
