# -*- coding: utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import ValidationError

class HostelFacilities(models.Model):
    _name = 'hostel.facilities'
    _description = 'Hostel.Facilities'

    name = fields.Char(String="Facility Name")
    charge = fields.Integer(String="Facility Charge")
    state = fields.Selection(selection=[('draft', "draft"),
                                        ('confirmed', "confirmed"),
                                        ], default='draft',
                             required=True, tracking=True, )
    company_id= fields.Many2one('res.company',string="company_id",default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(related='company_id.currency_id',string="Currency")

    @api.constrains('charge')
    def _check_charge(self):
        for record in self:
            if record.charge<=0:
                raise ValidationError("The charge cannot be less than 0 or 0")









