# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Inti Prima Rasa - Pos Receipt",
    "version": "8.0.2.0.0",
    "category": "Point Of Sale",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "depends": [
        "point_of_sale",
        "pos_restaurant_table_management",
        "pos_card_payment_info",
        "pos_payment_method_display",
        "pos_order_discount",
        "proxy_backend_ecspos_aeroo",
    ],
    "data": [
        "security/res_groups.xml",
        "reports/report_pos_order_reprint.xml",
        "views/point_of_sale_views.xml",
        "views/pos_order_views.xml"
    ],
    "qweb": [
        "static/src/xml/point_of_sale_template.xml",
    ],
}
