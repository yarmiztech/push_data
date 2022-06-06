
from odoo import fields, models, api,_
from odoo.tools.misc import get_lang

class AccountMove(models.Model):
    _inherit = 'account.move'

    def all_branch_custom(self):

            for invoices in self.env['account.move'].search([('move_type','=','out_invoice')]):
                for line in invoices.line_ids:
                    if invoices.branch_id:
                        line.branch_id = invoices.branch_id.id
                        line.move_type = invoices.move_type
                    else:
                        line.branch_id = 1
                        line.move_type = 'out_invoice'
    def all_branch_vendor(self):

            for invoices in self.env['account.move'].search([('move_type','=','in_invoice')]):
                for line in invoices.line_ids:
                    if invoices.branch_id:
                        line.branch_id = invoices.branch_id.id
                        line.move_type = invoices.move_type
                    else:
                        line.branch_id = 1
                        line.move_type = 'in_invoice'

    @api.depends('branch_id')
    @api.constrains('branch_id')
    def onchange_branch_id(self):
        if self.branch_id:
            for line in self.invoice_line_ids:
                line.branch_id = self.branch_id.id
                line.move_type = self.move_type
        for line in self.invoice_line_ids:
            line.move_type = self.move_type


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    branch_id = fields.Many2one("company.branches", string="Branch")
    move_type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt')])



# class BranchAccountPartnerLedger(models.TransientModel):
#     _inherit = "account.report.partner.ledger"
#     _name = "account.branch.partner.ledger"
#     _description = "Account Branch Partner Ledger"
#
#     branch_id = fields.Many2one('company.branches', string='Branch')
#
#     # def _print_report(self, data):
#     #     data = self.pre_print_report(data)
#     #     data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency})
#     #     return self.env.ref('accounting_pdf_reports.action_report_partnerledger').report_action(self, data=data)
#
#     # def _build_contexts(self, data):
#     #     result = {}
#     #     result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
#     #     result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
#     #     result['date_from'] = data['form']['date_from'] or False
#     #     result['date_to'] = data['form']['date_to'] or False
#     #     result['strict_range'] = True if result['date_from'] else False
#     #     result['company_id'] = data['form']['company_id'][0] or False
#     #     result['branch_id'] = data['form']['branch_id'][0] or False
#     #     return result
#     # #
#     # # def _print_report(self, data):
#     # #     raise NotImplementedError()
#     #
#     # def check_report(self):
#     #     self.ensure_one()
#     #     data = {}
#     #     data['ids'] = self.env.context.get('active_ids', [])
#     #     data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
#     #     data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id', 'branch_id'])[0]
#     #     used_context = self._build_contexts(data)
#     #     data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)
#     #     return self.with_context(discard_logo_check=True)._print_report(data)
#
#
#     def _print_report(self, data):
#         data = self.pre_print_report(data)
#         data['form'].update({'branch_id': self.branch_id})
#         return self.env.ref('accounting_pdf_reports.action_report_partnerledger').report_action(self, data=data)
#
#         # return self.env.ref('branch_wise_partner_ledger.action_reports_partnerledger_branch').report_action(self, data=data)
