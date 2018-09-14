# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Inti Prima Rasa - Pos Order Rekapitulasi Billing",
    "version": "8.0.1.1.1",
    "category": "Point Of Sale",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "depends": [
        "report_aeroo",
        "proxy_backend_ecspos_aeroo",
        "pos_restaurant",
        "pos_orders",
        "ipr_pos_receipt",
        "pos_order_discount",
        "pos_order_return"
    ],
    "data": [
        "reports/report_pos_order_rekap_billing.xml",
        "wizards/print_rekap_bill.xml",
        "views/point_of_sale_views.xml",
        "views/restaurant_printer_view.xml",
        "views/pos_config_views.xml"
    ],
    "qweb": [
        "static/src/xml/ipr_pos_order_rekap_billing.xml",
    ],
}
