{
    'name': 'Sale order Pricelist',
    'description': ' This module is for apply different pricelist for different product on sale order',
    'category': 'Sale',
    'summary': '',
    'version': '15.0.1.0.0',
    'author': 'Aktiv Software',
    'website': 'www.aktivsoftware.com',
    'depends': ['sale_management', ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/select_pricelist_wizard_views.xml',
        'views/sale_order_line_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
