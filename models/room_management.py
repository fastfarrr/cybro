# -*- coding: utf-8 -*-


from odoo import fields, models, api, _


class Room(models.Model):
    """model for room management"""
    _name = 'hostel.room'
    _rec_name = "room_number"
    _description = "details of room"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    facilities_ids = fields.Many2many('hostel.facilities',
                                      string="Facilities")
    room_type = fields.Selection([('dorm', 'Dorm'),
                                  ('shared', 'shared'),
                                  ('private', 'private')], string="Room Type",
                                 required=True)
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
                                        ('full', "Full"),
                                        ('cleaning', 'Cleaning')],
                             default='empty', required=True, tracking=True, )

    room_number = fields.Char(string="Sequence Name", required=True,
                              readonly=True,
                              copy=False, default=lambda self: _('New'))

    student_id = fields.One2many('student.details',
                                 'room_id', readonly=True)
    total_rent = fields.Monetary(string="Total Rent", readonly=True,
                                 compute='_total_rent')
    invoice_id = fields.Many2one('account.move', string="Invoice",
                                 readonly=True)

    cleaning_staff = fields.Many2one('hr.employee')
    pending_amount = fields.Monetary(string="Pending Amount", readonly=True,
                                     compute='_compute_pending_amount')

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
            total_charge = 0
            for facility in record.facilities_ids:
                total_charge += facility.charge
            record.total_rent = total_charge + record.rent

    def monthly_invoice(self):
        rental_product = self.env.ref('hostel_management.rental_product1',
                                      raise_if_not_found=False)
        for room in self:
            for student in room.student_id:
                invoice_vals = {
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.today(),
                    'partner_id': room.company_id.id,
                    'student_id': student.id,
                    'invoice_line_ids': [(0, 0, {
                        'product_id': rental_product.id,
                        'quantity': 1,
                        'price_unit': room.total_rent,
                    })],

                }

                invoice = self.env['account.move'].create(invoice_vals)
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'name': 'customer invoice',
                    'view_mode': 'form',
                    'res_id': invoice.id,
                    'target': 'current'

                }

    def _compute_pending_amount(self):
        '''to calculate pending amount based on the unpaid invoices'''
        for record in self:
            student_ids = record.student_id.ids
            invoices = self.env['account.move'].search([
                ('student_id', 'in', student_ids),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted')
            ])
            print(invoices)
            record.pending_amount = sum(invoices.mapped('amount_residual'))

