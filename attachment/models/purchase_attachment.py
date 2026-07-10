# # -*- coding: utf-8 -*-
from odoo import models,fields
class PurchaseConfigSettings(models.TransientModel):
    """class to inherit purchase settings"""
    _inherit = 'res.config.settings'

    is_file_attached=fields.Boolean(string="Purchase Attachment")

    def set_values(self):
        """set values for purchase order settings"""
        super(PurchaseConfigSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'purchase_order_attachment.is_file_attached',self.is_file_attached
        )

    def get_values(self):
        """get values for purchase order settings"""
        res=super(PurchaseConfigSettings,self).get_values()
        value=self.env['ir.config_parameter'].sudo().get_param(
            'purchase_order_attachment.is_file_attached',default=False
        )
        res.update(is_file_attached = value == 'True')
        return res
