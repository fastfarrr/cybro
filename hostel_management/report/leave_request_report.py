# -*- coding: utf-8 -*-
from odoo import models,api
class LeaveRequestReport(models.AbstractModel):
    _name = "report.hostel_management.leave_report"

    @api.model
    def _get_report_values(self,docids,data=None):
        docs = self.env['leave.request.report.wizard'].browse(docids)
        return{
            'doc_ids' : docids,
            'doc_model' : 'leave.request.report.wizard',
            'data' : data,
            'docs' : docs,

        }


