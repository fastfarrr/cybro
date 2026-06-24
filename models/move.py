# -*- coding: utf-8 -*-
from odoo import models,fields
class Move(models.Model):
    _inherit = "account.move"
    student_id = fields.Many2one('student.details',string="Student")