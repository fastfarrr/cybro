# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class Room(models.Model):
    """model for room management"""
    _name = 'hostel.room'
    _rec_name = "room_number"
    _description = "details of room"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    # students_in_room=fields
    facilities_ids= fields.Many2many('hostel.facilities',
                                  string="Facilities")
    room_type = fields.Selection([('dorm','Dorm'),
                                  ('shared','shared'),
                                  ('private','private')],string="Room Type", required=True)
    number_of_beds = fields.Integer(string="Number of Beds", required=True)
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')
    rent = fields.Integer(string="Rent", required=True)
    state = fields.Selection(selection=[('empty', "Empty"),
                                        ('partial', "Partial"),
                                        ('full', "Full")], default='empty',
                             required=True, tracking=True, )

    room_number = fields.Char(string="Sequence Name", required=True,
                              readonly=True,
                              copy=False, default=lambda self: _('New'))
    # company_id = fields.Many2one("res.company", string="Company")
    student_id=fields.One2many('student.details','room_id',readonly=True)
    total_rent=fields.Monetary(string="Total Rent",readonly=True,compute='_total_rent')


    @api.model_create_multi
    def create(self, vals_list):
        """override method to create new room number"""
        for vals in vals_list:
            print(vals)
            if vals.get('room_number', _("New")) == _("New"):
                vals['room_number'] = self.env['ir.sequence'].next_by_code(
                    'hostel.room_seq') or _("New")

        return super(Room, self).create(vals_list)

    def _total_rent(self):
        """function to calculate total rent based on rent and facilities charge"""
        for record in self:
            record.total_rent=record.rent+record.facilities_ids.charge


