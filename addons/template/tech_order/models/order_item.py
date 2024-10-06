from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OrderItem(models.Model):
    _name = 'order.item'
    _description = 'Order Item'

    meal_id = fields.Many2one('order.meal', string="Meal", ondelete="restrict")  # restrict
    total_price = fields.Float(string='Total Price', compute="_compute_total_price")
    quantity = fields.Float(string="Quantity")
    price = fields.Float("Price")
    order_id = fields.Many2one('meal.order', string="Order")
    state = fields.Selection(related='order_id.state', string="State", store=True)

    # @api.onchange('price', 'quantity')
    # def set_total_price(self):
    #     self.total_price = self.price * self.quantity

    @api.onchange('meal_id')
    def set_price(self):
        self.price = self.meal_id.price

    @api.constrains('price')
    def check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError('Price cannot be zero 🤦‍♂️')

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = 0
            if record.price:
                record.total_price = record.quantity * record.price






