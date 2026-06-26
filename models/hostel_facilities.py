# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelFacilities(models.Model):
    """To assign hostel facilities to users and by default AC,TV and
    wifi will be there while activating the apk"""
    _name = 'hostel.facilities'
    _description = 'Hostel.Facilities'

    name = fields.Char(String="Facility Name",required=True)
    charge = fields.Monetary(String="Facility Charge")
    company_id = fields.Many2one('res.company',
                                 string="company_id",
                                 default=lambda self: self.env.user.
                                 company_id.id)
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  string="Currency")

    @api.constrains('charge')
    def _check_charge(self):
        """function for charge cannot be less than or equal to zero"""
        for record in self:
            if record.charge <= 0:
                raise ValidationError("The charge cannot be less than 0 or 0")
