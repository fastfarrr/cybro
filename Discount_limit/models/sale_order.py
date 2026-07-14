from odoo import models
from odoo.tools import date_utils
from datetime import date
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    """class to inherit sale order"""
    _inherit = 'sale.order'


    def action_confirm(self):
        """to set limit for discount while clicking confirm in order"""
        for order in self:
            if order.company_id.limit:
                limit=order.company_id.discount_limit
                # print(limit)
                day = date.today()
                start_date, end_date = date_utils.get_month(day)
                sale_order = self.env['sale.order'].search([
                    ('date_order','>=',start_date),
                    ('date_order','<=',end_date),
                    ('state', 'in',['sale']),
                    ('company_id','in',order.company_id.id)
                ])
                total_discount=0
                for sale in sale_order:
                    total_discount += (sale.amount_undiscounted - sale.amount_total)





                current_discount = (
                            order.amount_undiscounted - order.amount_total)


                if total_discount + current_discount > limit:
                    raise UserError(
                        "You can't apply discount because the monthly discount limit has been exceeded."
                    )

        return super().action_confirm()








