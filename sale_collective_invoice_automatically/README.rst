=====================================
Sale Collective Invoice Automatically
=====================================

Sale Collective Invoice Automatically

This module introduces a scheduled action (which runs once per day) with the
goal to automatically invoice a group of sale orders and a set of policies in
order to the system deciding what orders should be invoiced and when.

Configuration
=============

This module introduces 3 fields on the res.partner model (accessible on the
tab 'Invoicing' of the standard res.partner form view) and the same 3 fields on
the sale.order model (accessible on the tab 'Other Info' in the 'Invoicing'
paragraph). A Sale Order automatically loads, for these fields, the same values
set on the related Customer (if any), but the user is then allowed to change
them.

The first field is "Collective Invoice" and it allows the user to select among
4 options ("Not Applicable", "Per Period", "Per Period per SO" and "At Complete
Delivery"; default is "Not Applicable"). This field defines the behaviour that
the user should use regarding collective invoice for a sale order.

Please, select:
- Not Applicable: If you want the Sale Order to be not affected by this module.
- Per Period: If you want the Sale Order to be invoiced after a time period and
you also want it to be grouped with all other eligible Sale Orders in a single
invoice.
- Per Period per SO: If you want the Sale Order to be invoiced after a time
period but you also want it to be invoiced singularly.
- At Complete Delivery: If you want the Sale Order to be automatically invoiced
when it's fully delivered.

The other two fields are "Invoice Period Type" (it allows to select among
"Days", "Weeks", "Months" and "Years"; default is "Days") and "Invoice Period
Amount" (it receives an integer number). These two fields, together, define the
collective invoice period.

Usage
=====

Once the module has been installed, the functionalities this module offers are
totally automated and don't require any further intervention from the user
beyond the configuration of partners and sale orders as explained above.

Collective Invoice Functionality
================================

Everyday a scheduled action runs and checks for all the Sale Orders in need of
invoicing (Invoice Status: To Invoice) which also are configured to
automatically invoice based on time periods. Then they are furtherly filtered
and only the Sale Orders which according to their collective invoice period
could be invoiced the current day are kept (this check always uses the SO "Date
Order" as reference date and checks if the current date comes N collective
invoice periods later).

The gathered Sale Orders are then invoiced according to their "Collective
Invoice" option: that is "Per Period per SO" orders are all invoiced one by one
and "Per Period" orders are invoice collectively according to base Odoo
workflow.

Note: This periodic invoicing, even if it doesn't directly involve or depend
from Transfers has basically the effect of invoicing all the transfers which
happen during a time period. That's because Sale Orders (which sale storable
products) get an invoice status "To Invoice" when there is at least one product
which is transfered but not invoiced yet.

Complete Delivery Functionality
===============================

Each time a picking is transfered or canceled, the system will check if it is
originated by a Sale Order with "Collective Invoice" set to "At Complete
Delivery". In that case, the system will check if the order is now
completely transfered (which means: there are no pickings related to that SO
which are not in state Done or Cancel) and if it is, then will automatically
invoice the Order.