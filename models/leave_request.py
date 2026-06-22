# -*- coding: utf-8 -*-
from odoo import models,fields
class LeaveRequest(models.Model):
    _name= "leave_request"
    _description = "LeaveRequest"
    _rec_name = "status"

    leave_date=fields.Date(string="Leave date",required=True)
    arrival_date=fields.Date(string="Arrival date",required=True)
    status = fields.Selection(selection=[('new', "New"),
                                        ('approved', "Approved"),],
                             default='new',
                             required=True, tracking=True, )

    def approve(self):
        self.status='approved'