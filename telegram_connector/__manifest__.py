# -*- coding: utf-8 -*-
{
    'name' : 'Telegram connector',
    'version': '0.1.0',
    'summary' : 'Technical Module for Telegram Integration',
    'description': """
Telegram Integration for Odoo
====================
    """,
    'category': 'Extra Tools',
    'author' : 'Doan Man',
    'website': 'http://www.init.vn/',
    'depends' : ['base', 'mail'],
    'external_dependencies': {
    },
    'images' : [
        'static/description/banner.png',
        'static/description/telegram_architecture.png',
        'static/description/telegram_features.png',
        'static/description/telegram_interface.png',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/telegram_config_views.xml',
        'views/telegram_message_log_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {
    },
    'license': 'LGPL-3',
}