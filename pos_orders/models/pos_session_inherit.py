from odoo import fields, models, api

class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    total_discount = fields.Float('Total Discount', compute='get_total_discount')

    # @api.depends('order_ids')
    def get_total_discount(self):
        discount = 0
        for order in self.order_ids:
            for line in order.lines:
                discount += line.price_unit*(line.discount)/100
        self.total_discount = discount
