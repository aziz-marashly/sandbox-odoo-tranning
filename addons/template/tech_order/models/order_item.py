from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OrderItem(models.Model):
    _name = 'order.item'
    _description = 'Order Item'

    meal_id = fields.Many2one('order.meal', string="Meal", ondelete="restrict")  # restrict
    order_id = fields.Many2one('meal.order', string="Order")
    quantity = fields.Float(string="Quantity")
    price = fields.Float("Price")
    total_price = fields.Float(string='Total Price')

    @api.constrains('price')
    def check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError('Price should be more than zero')

    @api.constrains('total_price')
    def check_total_price(self):
        for record in self:
            if record.total_price <= 0:
                raise ValidationError('Total price should be more than zero')
