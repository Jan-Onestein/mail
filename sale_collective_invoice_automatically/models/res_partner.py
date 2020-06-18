# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    collective_invoice = fields.Selection([
            ('no','Not Applicable'),
            ('partner', 'Per Period'),
            ('order', 'Per Period per SO'),
            ('complete', 'At Complete Delivery')
        ], string='Collective Invoice', default='no')

    invoice_period_type = fields.Selection([
            ('days','Days'),
            ('weeks', 'Weeks'),
            ('months', 'Months'),
            ('years', 'Years'),
        ], string='Invoice Period Type', default='days')

    invoice_period_amount = fields.Integer(string='Invoice Period Amount')
