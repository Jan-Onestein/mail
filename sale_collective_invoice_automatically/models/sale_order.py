# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order = fields.Datetime(readonly=False)

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

    @api.onchange('partner_invoice_id')
    def onchange_partner_invoice(self):
        self.ensure_one()
        if self.partner_invoice_id:
            self.collective_invoice = self.partner_invoice_id.collective_invoice
            self.invoice_period_type = self.partner_invoice_id.invoice_period_type
            self.invoice_period_amount = self.partner_invoice_id.invoice_period_amount

    @api.model
    def cron_create_collective_invoice(self):
        orders = self.search([('invoice_status','=','to invoice'),('collective_invoice','in',['partner','order'])])
        invoice_groups = {}
        for order in orders:

            reference_date = fields.Date.to_date(order.date_order)
            today = fields.Date.from_string(fields.Date.today())

            while reference_date < today:
                period_type = order.invoice_period_type
                period_amount = order.invoice_period_amount
                if period_type == 'days':
                    reference_date = reference_date + relativedelta(days=period_amount)
                elif period_type == 'weeks':
                    reference_date = reference_date + relativedelta(weeks=period_amount)
                elif period_type == 'months':
                    reference_date = reference_date + relativedelta(months=period_amount)
                elif period_type == 'years':
                    reference_date = reference_date + relativedelta(years=period_amount)

                if reference_date == today:
                    if order.collective_invoice not in invoice_groups:
                        invoice_groups[order.collective_invoice] = self.env['sale.order']
                    invoice_groups[order.collective_invoice] |= order
                    break

        for collective_invoice in invoice_groups:
            invoice_groups[collective_invoice]._create_collective_invoice(collective_invoice)

    def _create_collective_invoice(self, collective_invoice):
        if collective_invoice == 'order':
            self._create_invoices(grouped=True)
        elif collective_invoice == 'partner':
            self._create_invoices(grouped=False)
