# -*- coding: utf-8 -*-
from odoo import fields, models, _, api


class Student(models.Model):
    _name = 'student.details'
    _rec_name = "student_name"
    _description = 'Student Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_name = fields.Char(string="Student Name", required=True)
    # student_id = fields.Integer(string="Student ID",required=True)
    street = fields.Char(string="Street Address", required=True)
    state_id = fields.Many2one('res.country.state',
                               string="State", required=True)
    country_id = fields.Many2one('res.country',
                                 String="Country", required=True)
    zip_code = fields.Char(string="Zip Code", required=True)
    dob = fields.Date(string="Dob", required=True)
    room_id = fields.Many2one('hostel.room',
                           string="Room", required=True)
    email = fields.Char(string="Email", required=True)
    image = fields.Image(string="Image")
    is_email_from = fields.Boolean(string="Receive mail", default=False)
    student_id = fields.Char(String="Sequence Name", readonly=True,
                             copy=False, default=lambda self: _("New"),
                             required=True)
    state = fields.Selection(selection=[('draft', "draft"),
                                        ('confirmed', "confirmed"),
                                        ], default='draft',
                             required=True, tracking=True, )


    @api.model_create_multi
    def create(self, vals_list):
        """override method to create new student_id"""
        for vals in vals_list:
            if vals.get('student_id', _("New") == _("New")):
                vals['student_id'] = self.env['ir.sequence'].next_by_code(
                    'student.details_seq') or _("New")
            return super(Student, self).create(vals_list)

    def Change_state(self):
        self.state='confirmed'
        for rec in self:
            if rec.room_id:
                rec.room_id.state='Full'



