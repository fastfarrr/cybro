# -*- coding:utf-8 -*-
from odoo import models,api
class StudentReport(models.AbstractModel):
    """created as an abstract model it won't store anything in
    the database its connect the ir.action report model"""
    _name = 'report.hostel_management.student_report'
    _description = 'Report Created'


    @api.model
    def _get_report_values(self, docids,data=None):
        docs = self.env['student.report.wizard'].browse(docids)
        return{
            'doc_ids': docids,
            'doc_model' : 'student.report.wizard',
            'data': data,
            'docs': docs,
        }




