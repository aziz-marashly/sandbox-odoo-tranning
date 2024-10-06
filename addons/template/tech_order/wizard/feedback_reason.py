from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class FeedbackReason(models.TransientModel):
    _name="feedback.reason"
    _description = "Feedback Reason"

    _transient_max_count = 3
    _transient_max_hours = 3

    reason = fields.Char('Reason', required=True)

    def add_reason(self):
        feedback_id = self.env['customer.feedback'].browse(self.env.context.get('active_id'))
        _logger.error("feedback_id +++ " + str(feedback_id))
        # feedback_id.state = 'rejected'
        # feedback_id.reason = self.reason
        feedback_id.update({'state':'rejected', 'reason':self.reason})
        # customer.feedback(3, )
