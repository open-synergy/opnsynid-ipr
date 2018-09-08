# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "PoS Sales Summary Aeroo Report",
    "version": "8.0.1.0.0",
    "category": "Point Of Sale",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "report_aeroo",
        "point_of_sale"
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/pos_sale_summary_reports.xml",
        "wizards/print_pos_sale_summary_views.xml",
    ],
}
