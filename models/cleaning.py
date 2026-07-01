# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError


class Cleaning(models.Model):
    """class to handle the cleaning of hostel room"""
    _name = 'hostel.cleaning'
    _description = 'cleaning'
    _rec_name = 'room'

    room = fields.Many2one('hostel.room')
    start_time = fields.Datetime(required=True)
    staff_id=fields.Many2one('res.users',readonly=True)
    company_id = fields.Many2one('res.company')
    state = fields.Selection(selection=[('new', 'New'), ('assigned', 'Assigned'
                                                         ), ('done', 'Done'
                                                             )], default='new')



    def assign_staff(self):
        """ Assign staff based on who logged in """
        for rec in self:
            if rec.state != 'new':
                raise UserError("Staff has already been assigned.")

            rec.staff_id = self.env.user
            rec.company_id = self.env.user.company_id.id
            rec.state = 'assigned'

    def completed_cleaning(self):
        self.state = 'done'
