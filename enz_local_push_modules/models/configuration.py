from odoo import fields,models,api
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


class SynchConfiguration(models.Model):
    _name = 'synch.configuration'

    server = fields.Char(string='Server Url')
    db = fields.Char(string='Database Name')
    username = fields.Char(string='User Name')
    password = fields.Char(string='Password')
    activate = fields.Boolean(default=False)


