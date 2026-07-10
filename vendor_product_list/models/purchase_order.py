from odoo import models,fields,api
from odoo import Command
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_vendor_product = fields.Boolean(string="Vendor Product")

    @api.onchange('product_id','partner_id')
    def product_id_on_change(self):
        for order in self:
            if order.is_vendor_product:
                a=self.env['purchase.order.line'].Command.create({
                    ('product_id','=',order.partner_id.partner_id.name.id)
                })
                order.purchase_order_line=a



