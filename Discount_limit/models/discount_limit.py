# -*- coding: utf-8 -*-
from odoo import models,fields
class DiscountLimit(models.TransientModel):
    _inherit= "res.config.settings"
    discount_limit = fields.Monetary(string="Discount Limit",default=500)
    company_id = fields.Many2one('res.company')
    currency_id = fields.Many2one('res.currency')

    def set_values(self):
        super(DiscountLimit,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'Discount_Limit.discount_limit',self.discount_limit)

    def get_values(self):
        res=super(DiscountLimit,self).get_values()
        self.env['ir.config_parameter'].sudo().get_param(
            'Discount_Limit.discount_limit')
        res.update(discount_limit=self.discount_limit)
        print("after update",res)
        return res
