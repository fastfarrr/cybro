# -*- coding: utf-8 -*-
from odoo import fields, models

class Room(models.Model):
    _name = 'hostel.room'
    _rec_name = "room_number"
    _description = "details of room"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    room_number = fields.Char(string="Room Number", required=True)
    room_type = fields.Char(string="Room Type", required=True)
    number_of_beds = fields.Integer(string="Number of Beds", required=True)
    rent = fields.Integer(string="Rent", required=True)
    state = fields.Selection(selection=[('Empty', "Empty"),
                                        ('Partial', "Partial"),
                                        ('Full', "Full")], default='Empty',
                             required=True, tracking=True,)





