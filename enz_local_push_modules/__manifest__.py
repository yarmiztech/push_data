# -*- coding: utf-8 -*-
{
    'name': 'POS Data Pushing-Main',
    'version': '14.0',
    'summary': 'POS',
    'sequence': -100,
    'description': """Local""",
    'category': '',
    'website': 'https://enzapps.com',
    'depends': ['base','sale','account','point_of_sale'],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'views/configuration.xml',
        'views/pos.xml'

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
