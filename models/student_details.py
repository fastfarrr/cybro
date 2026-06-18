# -*- coding: utf-8 -*-
from odoo import fields,models
class Student(models.Model):
    _name = 'student.details'
    _rec_name = "student_name"
    _description = 'Student Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_name = fields.Char(string="Student Name",required=True)
    student_id = fields.Integer(string="Student ID",required=True)
    street = fields.Char(string="Street Address",required=True)
    state_id = fields.Many2one('res.country.state',
                               string="State",required=True)
    country_id = fields.Many2one('res.country',
                                 String="Country",required=True)
    zip_code = fields.Char(string="Zip Code",required=True)
    dob = fields.Date(string="Dob",required=True)
    room = fields.Many2one('hostel.room',
                           string="Room",required=True)
    email = fields.Char(string="Email",required=True)
    image = fields.Image(string="Image")
    email_from = fields.Boolean(string="Receive mail",default=False)



