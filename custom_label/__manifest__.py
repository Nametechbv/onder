{
    'name': "Custom Label",
    'version': '1.0',
    'summary': 'Adds custom fields to product labels',
    'author':'NametechBV',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'reports/product_label_report.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}