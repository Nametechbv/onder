{
    'name': 'Customer Support Ticket',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Müşteri destek talepleri için bilet yönetimi modülü.',
    'description': """
        Müşteri Destek Ticket Modülü
        ============================
        Bu modül, müşterilerin destek taleplerini oluşturmasını, 
        takip etmesini ve yönetmesini sağlar.
    """,
    'author': 'NametechBV',
    #'website': 'https://www.sirketiniz.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ticket_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}