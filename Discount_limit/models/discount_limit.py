# -*- coding: utf-8 -*-
from odoo import models,fields


class DiscountLimit(models.TransientModel):
    """inherited the settings model and added a discount_limit field in it"""
    _inherit= "res.config.settings"

    limit=fields.Boolean(string="limit",
                         related='company_id.limit',readonly=False)
    discount_limit = fields.Float(string="Discount Limit",
                                  related='company_id.discount_limit',
                                  readonly=False,store=True)





