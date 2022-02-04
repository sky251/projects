{
    'name': 'Cancel SO',
    'description': 'Cancel selected sale order and send mail to Partner.',
    'category': 'Sale',
    'summary': '',
    'version': '15.0.1.0.0',
    'author': 'Aktiv Software',
    'website': 'www.aktivsoftware.com',
    'depends': ['sale_management', ],
    'data': [
        'data/cancel_so_mail_template.xml',
        'views/cancel_so_server_action_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
