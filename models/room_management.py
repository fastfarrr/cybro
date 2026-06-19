# -*- coding: utf-8 -*-

from odoo import fields, models, api,_


class Room(models.Model):
    _name = 'hostel.room'
    _rec_name = "room_number"
    _description = "details of room"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    room_type = fields.Char(string="Room Type", required=True)
    number_of_beds = fields.Integer(string="Number of Beds", required=True)
    rent = fields.Integer(string="Rent", required=True)
    state = fields.Selection(selection=[('Empty', "Empty"),
                                        ('Partial', "Partial"),
                                        ('Full', "Full")], default='Empty',
                             required=True, tracking=True, )

    room_number = fields.Char(string="Sequence Name", required=True,
                              readonly=True,
                              copy=False, default = lambda self: _('New'))

    @api.model_create_multi
    def create(self, vals_list):
        """override method to create new room number"""
        for vals in vals_list:
            print(vals)
            if vals.get('room_number', _("New")) == _("New"):
                vals['room_number'] = self.env['ir.sequence'].next_by_code(
                    'hostel.room_seq') or _("New")
        return super(Room, self).create(vals_list)
