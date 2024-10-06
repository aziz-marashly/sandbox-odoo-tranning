from odoo import models, fields
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta



class MealIngredient(models.Model):
    _name='meal.ingredient'
    _description='Meal Ingredient'
    _order = 'id'

    name = fields.Char("Name", required=True)
    quantity = fields.Float("Quantity")
    product_id = fields.Many2one('product.product', 'Product', ondelete="restrict")
    meal_id = fields.Many2one('order.meal', "Meal")