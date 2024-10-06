from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    feedbacks_ids = fields.One2many('customer.feedback', 'customer_id', string="FeedBacks", readonly=1)