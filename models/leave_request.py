# -*- coding: utf-8 -*-
from odoo import models,fields,api
from odoo.exceptions import ValidationError
class LeaveRequest(models.Model):
    """to handle checkin and checkout"""
    _name= "leave_request"
    _description = "LeaveRequest"
    _rec_name = "status"

    leave_date=fields.Date(string="Leave date",required=True)
    arrival_date=fields.Date(string="Arrival date",required=True)
    status = fields.Selection(selection=[('new', "New"),
                                        ('approved', "Approved"),],
                             default='new')
    student_id=fields.Many2one('student.details',string="Student",
                               required=True)

    def approve(self):
        """when click the button it need to change the status to approved"""
        self.status='approved'
        # if self.status=='approved':
        #     self.env["student_details"].search_count([
        #         ('room_id','=',room.id)
        #     ])

    @api.constrains('arrival_date','leave_date')
    def _check_date(self):
        for record in self:
            if record.leave_date > record.arrival_date:
                raise ValidationError(
                    "The arrival date cannot be lower than leave date")
