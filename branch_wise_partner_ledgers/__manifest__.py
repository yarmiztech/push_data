
{
    'name': 'Branch Wise Report',
    'version': '14.0.1.0.0',
    'summary': """Ability To get Branch Wise Report""",
    'description': """Ability To get Branch Wise Report""",
    'category': 'Sales',
    'author': 'Enzapps',
    'company': 'Enzapps',
    'maintainer': 'Enzapps',
    'website': "https://www.enzapps.com",
    'depends': ['account','base','boraq_company_branches','accounting_pdf_reports'],
    'data': [
       # 'security/ir.model.access.csv',
       'views/partner_ledger.xml',
        'reports/report_partner_ledger.xml',
        'reports/report.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': '',
    'installable': True,
    'auto_install': False,
    'application': False,
}
