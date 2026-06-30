# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date


class LeaveRequest(models.Model):
    """to handle checkin and checkout"""
    _name = "leave_request"
    _description = "LeaveRequest"
    _rec_name = "status"

    leave_date = fields.Date(string="Leave date", required=True)
    arrival_date = fields.Date(string="Arrival date", required=True)
    status = fields.Selection(selection=[('new', "New"),
                                         ('approved', "Approved"), ],
                              default='new')
    student_id = fields.Many2one('student.details', string="Student",
                                 required=True)

    def approve(self):
        """when click the button it need to change the status to approved and
        create a cleaning request if room is empty """
        for record in self:

            room = record.student_id.room_id

            if not room:
                raise UserError("the student does not assigned any room")

            record.status = 'approved'
            record.student_id.room_id = False

            record.student_id.is_button_clicked = False
            record.student_id.is_vacate_clicked = True

        student_count = self.env['student.details'].search_count([
            ('room_id', '=', room.id)
        ])
        if student_count == 0:
            room.state = 'empty'
            self.env['hostel.cleaning'].create({
                'room': room.id,
                'start_time': date.today(),
                'company_id': room.company_id.id,
                'cleaning_staff_id': record.student_id.employee_id.id

            })
        elif student_count < room.count_of_bed:
            room.state = 'partial'

        else:
            room.state = 'full'


    @api.constrains('arrival_date', 'leave_date')
    def _check_date(self):
        for record in self:
            if record.leave_date > record.arrival_date:
                raise ValidationError(
                    "The arrival date cannot be lower than leave date")
