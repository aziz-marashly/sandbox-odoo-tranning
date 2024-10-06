from odoo import models, fields



class MealCategory(models.Model):
    _name = "order.meal.category"
    _description = "Order Meal Category"
    _order = "name"
    # _rec_name = "test"

    name = fields.Char("Name", required=True)
    # state
    # sequence
    # active

class Meal(models.Model):
    _name = "order.meal"
    _description = "Order Meal"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    price = fields.Float("Price", copy=False)
    category_id = fields.Many2one("order.meal.category", string="Category",ondelete="restrict")# cascade