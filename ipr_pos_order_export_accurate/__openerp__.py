# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Export PoS Order for Accurate",
    "version": "8.0.1.0.0",
    "category": "Point Of Sale",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "pos_order_summary",
        "ipr_pos_accurate_info",
        "report_aeroo",
        "supplier_invoice_export_accurate"
    ],
    "data": [
        "reports/report_pos_order_accurate.xml",
        "wizards/pos_order_export_accurate_views.xml"
    ]
}
