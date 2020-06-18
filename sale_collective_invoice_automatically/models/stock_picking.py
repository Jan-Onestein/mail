# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_done(self):
        res = super(StockPicking, self).action_done()
        for pick in self:
            order = pick.sale_id
            if order and order.collective_invoice == 'complete' and all([p.state in 'cancel', 'done'] for p in order.picking_ids):
                order._create_invoices(grouped=True)
        return res

    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()
        for pick in self:
            order = pick.sale_id
            if order and order.collective_invoice == 'complete' and all(
                    [p.state in 'cancel', 'done'] for p in order.picking_ids):
                order._create_invoices(grouped=True)
        return res
