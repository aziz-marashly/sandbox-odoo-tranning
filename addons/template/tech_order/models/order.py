from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta



class MealOrder(models.Model):
    _name='meal.order'
    _description='Meal Order'
    _order = 'name'

    def customer_domain(self):
        customers = self.env['res.partner'].search([('is_company', '=', True)])
        return [('id', 'in', customers.ids)]

    name = fields.Char("Name", copy=False, default="New")
    type = fields.Selection([('internal', 'Internal'), ('external', 'External')],
                            string="Type", default="internal")

    order_date = fields.Date("Order Date", readonly=False)#, default=fields.datetime.now().date()
    total_price = fields.Float(string="Total Price", readonly=True, default=0,
                               groups="tech_order.tech_order_mgr")
    note = fields.Text("Note", translate=True)
    expected_duration = fields.Float("Expected Duration")
    customer_id = fields.Many2one('res.partner', "Customer", ondelete='restrict', domain=customer_domain)#[('is_company', '=', True)])
    table_number = fields.Integer("Table Number")
    is_urgent = fields.Boolean("Is Urgent", copy=False)
    active = fields.Boolean(default=True)
    order_tag_ids = fields.Many2many('order.tag', "Tags")
    item_ids = fields.One2many('order.item', 'order_id', string="Items")
    expected_date = fields.Datetime("Expected Date", compute="_compute_expected_date",
                                    inverse="inverse_expected_date", readonly=False)
    external_item_ids = fields.Many2many('external.item', string="External Item",
                                         readonly=True)
    #readonly=True, copy=False, store=False, required=False
    # readonly=False, copy=True, store=True, required=False

    # order_tag_ids = fields.Many2many('order.tag',
    #                                  relation="Tags", column1='order', column2='tag')

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('in_process', 'In Process'),
                              ('delivered', 'Delivered'),
                              ('cancelled', 'Cancelled'),
                              ],
                             string="State", default='draft')

    _sql_constraints = [
            ('unique_name', 'unique (name)', 'Order Name already exists!'),
            ]

    @api.depends('order_date', 'expected_duration')
    def _compute_expected_date(self):
        for record in self:
            record.expected_date = timedelta(days=0)
            if record.order_date and record.expected_duration:
                record.expected_date = record.order_date + timedelta(days=record.expected_duration)

    def inverse_expected_date(self):
        for record in self:
            record.expected_duration = (record.expected_date.date() - record.order_date).days


    @api.constrains('order_date')
    def check_order_date(self):
        if self.order_date and self.order_date > datetime.now().date():
            raise ValidationError(_("Order Date Must be in present or past"))

    @api.constrains('table_number')
    def check_table_number(self):
        max_table_number = self.env['ir.config_parameter'].sudo().get_param('tech_order.max_table_number')
        if self.table_number > int(max_table_number):
            raise ValidationError("Max Table Number is " + str(max_table_number))

    def action_confirm(self):
        self.state = 'confirmed'

    def action_in_process(self):
        self.state = 'in_process'

    def action_delivered(self):
        self.state = 'delivered'

    def action_cancelled(self):
        self.state = 'cancelled'

    def check_urgent(self):
        for order in self:
            expected_date = order.expected_date.date() - timedelta(days=1)
            if expected_date == datetime.now().date():
                order.is_urgent = True

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('order_meal_name_seq')
        return super(MealOrder, self).create(vals)

    def fetch_order(self):
        # user = self.env.user
        # rec = self.env.ref('tech_order.model_meal_order')
        # en = self.env
        # raise ValidationError(str(user) + " " + str(rec) + " " + str(en))

        # state in (confirmed, in_process)
        # AND
        # (
        # external and expected_date > current date
        # OR
        # internal and table_umber == 0
        # )
        ########
        # self.env.user.has_group('')
        orders = self.search([('state', 'in', ('confirmed', 'in_process')),
                              '|', '&', ('type', '=', 'external'), ('expected_date', '<', datetime.now()),
                              '&', ('type', '=', 'internal'), ('table_number', '=', 0)]) #, limit=3, order_by='id'
        orders[0].unlink()
        #######
        # orders = orders.read(['name', 'type', 'customer_id'])
        #######

        orders = self.read_group(
                [('state', 'in', ('confirmed', 'in_process')),
                 '|', '&', ('type', '=', 'external'), ('expected_date', '<', datetime.now()),
                 '&', ('type', '=', 'internal'), ('table_number', '=', 0)],
                ['name', 'type', 'customer_id'],
                ['type', 'customer_id'],
                lazy=False
                )

        #To Do --> try search_count


        #  offset=1
        #  limit=1
        # order = 'order_date ASC'
        # orderby = 'order_date',
        # count = True
        #######
        # raise ValidationError(str(orders))


        #Draft --> Confirm, Cancel
        #Confirm --> In Process, Cancel
        #In Process --> Delivered
        #Delivered --> X

    # #1
        # @api.model_create_multi
        # def create(self, vals_list):
          # return list_of_object

    # #2
    # @api.model
    # def create(self, vals):
    #     return object
