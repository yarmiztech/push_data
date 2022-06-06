{
    'name': "POS Custom",
    'author':
        'Enzapps',
    'summary': """
    New module for Alshab Custom
""",

    'description': """
    New module for Alshab Custom
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base', 'point_of_sale' ],
    "images": ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/session_report.xml',
        'views/day_book.xml',
        'views/pos_session_inherit.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}