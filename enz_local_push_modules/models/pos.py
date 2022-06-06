from odoo import fields,models,api,_
from odoo.exceptions import UserError, ValidationError


class pos_session(models.Model):
    _inherit = 'pos.session'

    pushed = fields.Boolean(default=False)
    def push_to_main(self):
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            url = synch.server
            db = synch.db
            username = synch.username
            password = synch.password
            # password = "YEZPR#ADM@786"
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

            for order in self.order_ids.mapped('payment_ids').mapped('payment_method_id'):
                list = []
                # for move in order.lines:
                for move in order:
                    main_product = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                [[['name', '=', 'Daily Sales Product']]],
                                                {'fields': ['name', 'id']})
                    vat_id = models.execute_kw(db, uid, password, 'account.tax', 'search_read',
                                               [[['name', '=', 'Vat 15%'], ['type_tax_use', '=', 'sale']]],
                                               {'fields': ['name', 'id']})

                    if main_product:
                        product_lines = (0, 0, {
                            'product_id': main_product[0]['id'],
                            # 'product_uom_qty': move.qty,
                            'product_uom_qty': 1,
                            # 'price_unit': move.price_unit,
                            # 'price_unit':order.move_id.amount_total,
                            'price_unit':sum(self.order_ids.mapped('payment_ids').filtered(lambda a:a.payment_method_id == order).mapped('amount'))*100/115,
                            # 'tax_id': move.tax_ids.ids,
                            'tax_id': [vat_id[0]['id']],
                        })
                        list.append(product_lines)
                    else:
                        raise UserError(
                            _('Product Not Available in ur Pushing Server'))
                type = 'credit';
                main_journal='';

                # if order.payment_ids:
                    # if order.payment_ids.payment_method_id.name != 'Cash':
                # if order.payment_method_id.name != 'Cash':
                if order.name != 'Cash':
                    type = 'bank';
                    main_journal = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                     [[['name', '=', 'Bank']]],
                                                     {'fields': ['name', 'id']})
                    main_journal = main_journal[0]['id']
                    main_partner = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                     [[['name', '=', 'Walking Customer']]],
                                                     {'fields': ['name', 'id']})
                    if not main_partner:
                        raise UserError(
                            _('Walking Customer Not Available in ur Pushing Server'))
                    branch_id = '';

                    # if order.branch_id:
                    if self.order_ids.mapped('branch_id'):
                        branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                      [[['name', '=', self.order_ids.mapped('branch_id').name]]],
                                                      {'fields': ['name', 'id']})
                        branch_id = branch_id[0]['id']

                    sale_order = models.execute_kw(db, uid, password, 'sale.order', 'create',
                                                   [{
                                                       'partner_id': main_partner[0]['id'],
                                                       'purchase_type_cash': type,
                                                       'order_line': list,
                                                       'client_order_ref': order.name,
                                                       'branch_id': branch_id,
                                                       'bank_journal_id': main_journal,
                                                   }]
                                                   )
                    print(sale_order, 'sale_order')
                else:
                        type = 'cash';

                        main_partner = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                         [[['name', '=', 'Walking Customer']]],
                                                         {'fields': ['name', 'id']})
                        if not main_partner:
                            raise UserError(
                                _('Walking Customer Not Available in ur Pushing Server'))
                        branch_id = '';
                        if self.order_ids.mapped('branch_id'):
                            branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[['name', '=', self.order_ids.mapped('branch_id').name]]],
                                              {'fields': ['name', 'id']})
                            branch_id = branch_id[0]['id']


                        sale_order = models.execute_kw(db, uid, password, 'sale.order', 'create',
                                                    [{
                                                        'partner_id': main_partner[0]['id'],
                                                        'purchase_type_cash': type,
                                                        'order_line':list,
                                                        'client_order_ref':order.name,
                                                        'branch_id': branch_id,
                                                        'bank_journal_id':main_journal,
                                                    }]
                                                    )
                        print(sale_order,'sale_order')
            self.pushed =True
