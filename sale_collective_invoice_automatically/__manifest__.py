# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Automatically Create Collective Invoice from Transfers",
    "version": "13.0.1.0.0",
    "category": "Warehouse Management",
    "summary": "Automatically Create Collective Invoice from Transfers",
    "author": "Onestein",
    "website": "http://github.com/OCA/stock-logistics-workflow",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "account",
        "sale_stock",
        "stock_account",
    ],
    "data": [
        "data/ir_cron.xml",
        "views/res_partner.xml",
        "views/sale_order.xml"
    ],
    "installable": True,
}
