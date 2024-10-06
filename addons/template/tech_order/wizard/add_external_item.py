from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from odoo.tools.safe_eval import safe_eval, test_python_expr

import logging
_logger = logging.getLogger(__name__)

class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    @api.constrains('domain')
    def _check_domain(self):
        for field in self:
            raise ValidationError(str(field.domain) + " " + str(safe_eval(field.domain or '[]')))
            safe_eval(field.domain or '[]')

class ExternalItemWizard(models.TransientModel):
    _name="external.item.wizard"
    _description = "External Item Wizard"

    _transient_max_count = 3
    _transient_max_hours  = 3




    # def set_default_val(self):
    #     # raise ValidationError(str(self.env.context))
    #     return self.env.context
    #     # raise ValidationError(str(self.current_id))
    #

    # def m()
    # save_eval("[('id', '=', context.get('active_id', False))]")
    #     return ()
    #
    # def _get_domain(self):
    #     r = m()
    #     parse(r)
    #

        # def _purchase_order_domain(self):
        #     sale_order = self.env['sale.order'].browse(int(self._context.get('active_id', False)))
        #     if sale_order.has_one_line() and sale_order.check_available_sale():
        #         product_id = sale_order.has_one_line().product_id
        #         available_purchase_lines = self.env['purchase.order.line'].search([('product_id', '=', product_id.id)])
        #         available_purchase_lines = available_purchase_lines.filtered(lambda x: x.order_id.ebt_can_sale_link)
        #         return [('id', '=', available_purchase_lines.ids)]
        #     return [('id', '=', -1)]
        #
        # return ("[('id', '=', context.get('active_id', False))]")
        #
        # def _domain_lot_id(self):
        #     if self.user_has_groups('stock.group_stock_user'):
        #         return ("[] if not context.get('inventory_mode') else"
        #                 " [('product_id', '=', context.get('active_id', False))] if context.get('active_model') == 'product.product' else"
        #                 " [('product_id.product_tmpl_id', '=', context.get('active_id', False))] if context.get('active_model') == 'product.template' else"
        #                 " [('product_id', '=', product_id)]")
        #
        # return "[]"

        # return ("t = self.env['external.item'].search()"
        # " [('id', '=', t.id)]"
        #         )


        # raise ValidationError(str(self.current_id))
        # # self.fetch_values()
        # # raise ValidationError(str(self.env.context) + " " + str(self._context))
        # _logger.error("ACTIVE ID ++++ " + str(self.env.context))
        # _logger.error("ACTIVE ID ++++ " + str(self._context))
        # _logger.error("ACTIVE ID ++++ " + str(self.env.context.get('current_id')))



    # current_id = fields.Text(default=set_default_val, readonly=False)
    def get_active_session(self):
        globals_dict = {}
        locals_dict = {
                **{
                        'env': self.env,
                        }
                }

        # def safe_eval(expr, globals_dict=None, locals_dict=None, mode="eval", nocopy=False, locals_builtins=False,
        #               filename=None):
        res=safe_eval("env['external.item'].search([('id', '=', env.context.get('active_id', False))])",
                      globals_dict=globals_dict,
                  locals_dict=locals_dict)
        return ("[('id', '=', context.get('active_id', False))]")


    def _get_domain(self):
        raise ValidationError(str(self.get_active_session()))
        # locals_dict = {
        #         **{
        #                 'env': self.env,
        #                 }
        #         }
        # raise ValidationError(str(safe_eval("[('id', '=', env.context.get('active_id', False))]",locals_dict=locals_dict))
        #
        #                       )
        return []

    def set_default_item(self):
        # raise ValidationError(str(self.get_active_session()))
        items = self.env['external.item'].search([])
        return items
        # return ("[('id', '=', context.get('active_id', False))]")

    external_item_ids = fields.Many2many('external.item', string="External items", default = set_default_item,
                                         domain=_get_domain)
    #
    # domain = (
    #     "[('product_tmpl_id', '=', context.get('active_id', False))] if context.get('active_model') == 'product.template' else"
    #     " [('id', '=', context.get('default_product_id', False))] if context.get('default_product_id') else"
    #     " [('type', '=', 'product')]"))

    def add_items(self):
        order_id = self.env['meal.order'].browse(self.env.context.get('active_id'))
        #order_id.update({'external_item_ids': [(4, item.id) for item in self.external_item_ids]})
        order_id.external_item_ids = self.external_item_ids
