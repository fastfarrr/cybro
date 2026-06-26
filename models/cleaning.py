# -*- coding: utf-8 -*-
from odoo import models,fields
from odoo.exceptions import UserError

class Cleaning(models.Model):
    _name = 'hostel.cleaning'
    _description = 'cleaning'
    _rec_name = 'Room'

    Room = fields.Many2one('hostel.room')
    start_time = fields.Datetime(required=True)
    cleaning_staff_id=fields.Many2one('hr.employee')
    company_id = fields.Many2one('res.company')
    state=fields.Selection(selection=[('new','New'),('assigned','Assigned'
                                                     ),('done','Done'
                                                        )],default='new')

    def assign_staff(self):
        if self.state == 'new':
            self.state = 'assigned'
        else:
            raise UserError("staff already have been assigned")

    def completed_cleaning(self):
        self.state = 'done'

