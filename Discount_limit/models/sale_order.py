from odoo import models
from odoo.tools import date_utils
from datetime import date
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        limit=float(self.env['ir.config_parameter'].sudo().get_param(
        'Discount_Limit.discount_limit'))
        print(limit)
        day = date.today()
        start_date, end_date = date_utils.get_month(day)
        total_discount = 0
        sale_order = self.env['sale.order'].search([
            ('date_order','>=',start_date),
            ('date_order','<=',end_date),
            ('state', 'in',['sale'] ),
        ])
        print(sale_order)
        print(start_date)
        print(end_date)
        for order in sale_order:
            for line in order.order_line:
                total_discount+=(line.product_uom_qty *
                                 line.price_unit *
                                 line.discount/100)

        print("total",total_discount)

        current_discount= 0
        for line in self.order_line:
            current_discount+=(line.product_uom_qty *
                               line.price_unit *
                               line.discount/100)

        print("current",current_discount)


        if total_discount + current_discount > limit:
            raise UserError("You cant apply discount due to limit on this month")

        res=super().action_confirm()
        return res



