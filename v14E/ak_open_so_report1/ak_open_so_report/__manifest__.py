# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software
# mail:   odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#           Aktiv Software:
#              - Monali Parekh
#              - Shivam Kachhia
#              - Akash Patel
#              - Saurabh Yadav
#              - Tanvi Gajera


{
    'name': "Aggregate Sale Order Report of Pending Deliveries",
    'summary': """Aggregate Sale Order Report of Pending Deliveries""",
    'website': "http://www.aktivsoftware.com",
    'author': 'Aktiv Software',
    'description': """
            The functionality of this module is to print a report of SO which are open but not delivered yet.\n
            User can get report by partners as well as category of products.\n
            User can print report for particular customers as well.\n
        """,
    'category': 'Sales/Sales',
    'version': '14.0.1.0.0',
    'license': 'OPL-1',
    'depends': ['contacts', 'stock', 'sale_management', 'report_xlsx'],
    'data': [
        'wizards/open_sale_order_wizard_views.xml',
        'static/ir.model.access.csv',
        'reports/reports.xml',
        'reports/open_so_report_template.xml',
        'views/res_partner_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    # 'price': 10,
    # 'currency': 'EUR',
}
