# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Transfer In List Aeroo Report",
    "version": "8.0.1.0.0",
    "category": "Stock",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "report_aeroo",
        "ipr_stock_list_common",
        "stock_interwarehouse_operation"
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/stock_transfer_in_list.xml",
        "reports/stock_move_transfer_in_list.xml",
        "wizards/print_stock_transfer_in_list_views.xml",
    ],
}
