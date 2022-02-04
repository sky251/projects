# -*- coding: utf-8 -*-
{
    "name": "Certifications and Product labels in delivery",
    "summary": """
       
        """,
    "version": "14.0.1.0.0",
    "author": "Aktiv Software",
    "website": "https://www.aktivsoftware.com",
    "depends": ["delivery", "product_packaging_type", "purchase", "contacts"],
    "data": [
        'views/certification_view.xml',
        'views/warning_view.xml',
        'static/ir.model.access.csv',
        'data/certification_data.xml',
        'data/warning_data.xml',
        'views/product_template_view.xml',
        'views/sale_order_views.xml',
        'views/product_packaging_type_view.xml',
        'views/purchase_order_views.xml',
        'views/delivery_carrier_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',
        'reports/reports.xml',
        'reports/css_report.xml',
    ],
}
