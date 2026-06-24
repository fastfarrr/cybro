# -*- coding: utf-8 -*-
from odoo import fields, models, _, api
from datetime import date
from odoo.exceptions import UserError



class Student(models.Model):
    """model for student details designed to create a student"""
    _name = 'student.details'
    _rec_name = "student_name"
    _description = 'Student Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_name = fields.Char(string="Student Name")
    street = fields.Char(string="Street Address", required=True)
    state_id = fields.Many2one('res.country.state',
                               string="State", required=True)
    country_id = fields.Many2one('res.country',
                                 string="Country", required=True)
    zip_code = fields.Char(string="Zip Code", required=True)
    dob = fields.Date(string="Dob", required=True)
    room_id = fields.Many2one('hostel.room',
                              string="Room",readonly=True)
    email = fields.Char(string="Email", required=True)
    image = fields.Image(string="Image")
    is_email_from = fields.Boolean(string="Receive mail", default=False)
    student_id = fields.Char(string="Sequence Name", readonly=True,
                             copy=False, default=lambda self: _("New"), )
    company_id = fields.Many2one("res.company",
                                 string="Company", related="room_id.company_id")

    student_age = fields.Integer(string="Age",
                                 compute="_compute_student_age", store=True)
    partner_id = fields.Many2one('res.partner', string="partner", store=True,
                                 copy=False, readonly=True)
    is_button_clicked = fields.Boolean(default=False)
    invoicing=fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        """override method to create new student_id"""
        for vals in vals_list:
            if vals.get('student_id', _("New")) == _("New"):
                vals['student_id'] = self.env['ir.sequence'].next_by_code(
                    'student.details_seq') or _("New")

            partner_id = self.env['res.partner'].create({
                "name": vals.get('student_name'),
                "email": vals.get('email'),
                "street": vals.get('street'),
                "state_id": vals.get('state_id'),
                "country_id": vals.get('country_id')
            })
            vals['partner_id'] = partner_id.id

        return super(Student, self).create(vals_list)

    def change_state(self):
        """to assign room automatically based on available bedspace"""

        for rec in self:
            if not rec.room_id:
                room = self.env['hostel.room'].search(
                    [('state', '!=', 'full')], limit=1)

                if not room:
                    raise UserError(_("No room available"))

                rec.room_id = room.id
                print(rec.room_id)


            """to change the state based on available number of beds"""

            students_count = self.env['student.details'].search_count([
                ('room_id', '=', rec.room_id.id),

            ])
            if students_count < rec.room_id.number_of_beds:
                rec.room_id.state = 'partial'
            else:
                rec.room_id.state = 'full'
            self.is_button_clicked = True



    @api.depends('dob')
    def _compute_student_age(self):
        """to calculate student age based on date selection"""
        for record in self:
            if record.dob:
                today = date.today()
                birth = record.dob
                record.student_age = today.year - birth.year - (
                        (today.month, today.day) < (birth.month, birth.day)
                )
            else:
                record.student_age = 0
