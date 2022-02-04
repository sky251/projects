{
    'name': 'Available Quantity',
    'description': 'This module shows available product quantity in warehouse',
    'category': 'Stock',
    'summary': '',
    'version': '15.0.1.0.0',
    'author': 'Aktiv Software',
    'website': 'www.aktivsoftware.com',
    'depends': ['stock', ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}