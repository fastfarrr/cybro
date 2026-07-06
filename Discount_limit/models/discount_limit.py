# -*- coding: utf-8 -*-
from odoo import models,fields
class DiscountLimit(models.TransientModel):
    """inherited the settings model and added a discount_limit field in it"""
    _inherit= "res.config.settings"
    discount_limit = fields.Float(string="Discount Limit",default=0.0,
                                     company_dependent=True)

    def set_values(self):
        super(DiscountLimit,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'Discount_Limit.discount_limit',self.discount_limit)

    def get_values(self):
        res=super(DiscountLimit,self).get_values()
        discount_limit=float(self.env['ir.config_parameter'].sudo().get_param(
            'Discount_Limit.discount_limit',default=0.0))
        res.update(discount_limit=discount_limit)
        print("after update",res)
        return res


