# -*- coding: utf-8 -*-
{
    'name': 'Search by Lot/Serial number',
    'description': 'Search by Lot/Serial number in POS',
    'category': 'Sale',
    'summary': 'Allows to search a product by lot/serial number in POS',
    'version': '15.0.1.0.0',
    'author': 'Aktiv Software',
    'website': 'www.aktivsoftware.com',
    'depends': ['stock', 'point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale.assets': [
            'search_by_lot_and_serial_no/static/src/js/ProductScreen.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,

}
