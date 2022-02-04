# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Image Preview SO',
    'description': '',
    'category': 'Sale',
    'summary': '',
    'version': '15.0.1.0.0',
    'author': 'Patel Akash',
    'website': 'www.aktivsoftware.com',
    'depends': ['sale_management', ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
