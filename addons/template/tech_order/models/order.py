from odoo import models, fields, _, api
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = "meal.order"
    _description = "Meal Order "
    _order = "name"

    name = fields.Char(string="Name", required=True,
                       default=lambda self: _('New'))
    total_price = fields.Float("Price", copy=False)
    order_type = fields.Selection([('internal', 'Internal'), ('external', 'External')],
                                  string="Type", required=True,
                                  default="internal")
    note = fields.Text("NOTE")
    order_date = fields.Date("Order Date", copy=False, default=fields.datetime.now().date(),
                             readonly=False)
    customer_id = fields.Many2one("res.partner", string="Customer")
    is_urgent = fields.Boolean("Is Urgent", copy=False)
    active = fields.Boolean(default=True)
    table_number = fields.Integer("Table Number")
    expected_duration = fields.Float("Expected Duration")

    order_tag_ids = fields.Many2many('order.tag', "Tags")

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Order Name already exists!'),
    ]

    @api.constrains('order_date')
    def check_order_date(self):
        for record in self:
            if record.order_date > datetime.now().date():
                raise ValidationError("Order Date Must be in present or past")

