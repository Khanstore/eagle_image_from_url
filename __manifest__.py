# -*- coding: utf-8 -*-
{
    'name': 'Eagle Image from URL',
    'summary': 'Automatically import product and partner images from image URLs',
    'description': """
Eagle Image from URL
====================
Automatically fetch and set images from URLs for products and contacts/partners.
'author': 'SM Ashraf',
'website': 'https://www.eagle-erp.com',
Features:
- Product variant image URL
- Product template image URL
- Partner/contact image URL
- Works on create and write
- Uses a browser-like User-Agent
- Logs URL download errors without breaking record saves
""",
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'depends': ['base', 'product'],
    'data': [
        'views/product_view.xml',
        'views/partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
