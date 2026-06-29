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
                              string="Room", readonly=True)
    email = fields.Char(string="Email", required=True)
    image = fields.Image(string="Image")
    is_email_from = fields.Boolean(string="Receive mail", default=False)
    student_id = fields.Char(string="Sequence Name", readonly=True,
                             copy=False, default=lambda self: _("New"), )
    company_id = fields.Many2one("res.company",
                                 string="Company", related="room_id.company_id")

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')

    student_age = fields.Integer(string="Age",
                                 compute="_compute_student_age", store=True)
    partner_id = fields.Many2one('res.partner', string="partner",
                                 store=True,
                                 copy=False,
                                 readonly=True)
    is_button_clicked = fields.Boolean(default=False)
    is_vacate_clicked = fields.Boolean(default=False)
    invoice_count = fields.Integer(compute="_compute_invoice_count",
                                   string="Invoice Count", store=True)
    active = fields.Boolean(default=True)
    employee_id = fields.Many2one('hr.employee', readonly=True)
    monthly_amount = fields.Monetary(string="Monthly Amount")
    invoice_status = fields.Selection(selection=[('pending', "Pending"),
                                                 ('done', "Done"'')],
                                      compute='_compute_invoice_status')

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
                rec.employee_id = room.cleaning_staff

            """to change the state based on available number of beds"""

            students_count = self.env['student.details'].search_count([
                ('room_id', '=', rec.room_id.id),

            ])
            if students_count < rec.room_id.number_of_beds:
                rec.room_id.state = 'partial'
            else:
                rec.room_id.state = 'full'
            # To make hidden and visible button called Allot,Vacate
            self.is_button_clicked = True
            self.is_vacate_clicked = False

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

    @api.depends('student_id')
    def _compute_invoice_count(self):
        """to count the invoice for a student"""
        for student in self:
            student.invoice_count = self.env['account.move'].search_count([
                ('student_id', '=', student.id),
                ('move_type', '=', 'out_invoice'),

            ])

    def action_view_invoices(self):
        """creating the smart button"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'name': 'Invoice',
            'view_mode': 'list',
            'target': 'current',
            'domain': [
                ('student_id', '=', self.id),
                ('move_type', '=', 'out_invoice')
            ]
        }

    def vacate_student(self):
        """function for vacate student room"""
        for rec in self:
            if rec.room_id:
                room = rec.room_id
                rec.room_id = False

                students_count = self.env['student.details'].search_count([
                    ('room_id', '=', room.id)

                ])
                if students_count == 0:
                    room.state = 'cleaning'

                    if room.state == 'cleaning':
                        self.env['hostel.cleaning'].create({
                            'room': room.id,
                            'start_time': date.today(),
                            'company_id': room.company_id.id,
                            'cleaning_staff_id': rec.employee_id.id
                        })



                elif students_count < room.number_of_beds:
                    room.state = 'partial'
                else:
                    room.state = 'full'
            else:
                raise UserError(_("Not assigned room"))

        # to archive the students while clicking this button
        self.active = False

        # To make hidden and visible button called Allot,Vacate
        self.is_button_clicked = False
        self.is_vacate_clicked = True

    def unlink(self):
        """to delete the student with its leave request"""
        rooms = []
        for rec in self:
            if rec.room_id:
                rooms.append(rec.room_id)
            leave_requests = self.env['leave_request'].search([
                ('student_id', '=', rec.id)
            ])
            leave_requests.unlink()
            res = super(Student, self).unlink()

            for room in rooms:
                student_count = self.env['student.details'].search_count([
                    ('room_id', '=', room.id)

                ])
                if student_count == 0:
                    room.state = 'empty'
                elif student_count < rec.room.number_of_beds:
                    room.state = 'partial'
                else:
                    room.state = 'full'
        return res

    @api.depends('invoice_count')
    def _compute_invoice_status(self):
        for rec in self:
            invoices = self.env['account.move'].search([
                ('student_id', '=', rec.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted')
            ])

            rec.invoice_status = 'done'  # default value

            if not invoices:
                rec.invoice_status = 'pending'
            else:
                for invoice in invoices:
                    if invoice.amount_residual > 0:
                        rec.invoice_status = 'pending'
                        break

    