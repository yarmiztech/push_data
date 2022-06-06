# -*- coding: utf-8 -*-
{
    'name': "Loan Journal Entries",
    'author':
        'Enzapps',
    'summary': """
This module will help to create Journals entries for loan amount.
""",

    'description': """
        This module will help to create Journals entries for loan Amount.
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base','hr','account','ohrms_loan'],
    "images": ['static/description/icon.png'],
    'data': [
       'views/loan_form.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
