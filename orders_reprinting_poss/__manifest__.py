{
    'name': 'Order Reprinting In POS',
    'version': '14',
    'category': 'Point of Sale',
    'summary': 'POS Order Reprinting',
    'author': 'Enzapps Private Limited',
    'company': 'Enzapps Private Limited',
    'images': ['static/description/icon.png'],
    'website': 'https://www.enzapps.com',
    'depends': ['point_of_sale'],
    'data': [
             'security/ir.model.access.csv',
             'report/report_saledetails.xml',
             'report/receipt_report.xml',
             'report/receipt_report_label.xml',
             'report/pos_pdf_templates.xml',
             'report/pos_label.xml',
             'views/pos_template.xml',
             'views/point_of_sale_report.xml',
            ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'installable': True,
    'auto_install': False,
}


