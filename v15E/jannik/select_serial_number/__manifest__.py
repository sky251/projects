# -*- coding: utf-8 -*-
{
    'name': 'Select serial number on sales order line',
    'description': 'Select serial number on sales order line',
    'category': 'Sale',
    'summary': 'Allows to select a serial number from the specific product in sale',
    'version': '15.0.1.0.0',
    'author': 'Aktiv Software',
    'website': 'www.aktivsoftware.com',
    'depends': ['sale_management', 'purchase', 'stock', 'account', 'point_of_sale'],
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_production_lot_views.xml',
        'views/pos_templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'select_serial_number/static/src/js/ProductScreen.js',
        ],
    },
    'license': 'LGPL-3',
    # 'qweb': ['static/src/xml/EditListPopUp.xml'],
}
