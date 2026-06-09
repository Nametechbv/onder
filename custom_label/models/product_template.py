from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_ingredient = fields.Char(string='Ingredients', store=True)
    x_nutrition = fields.Char(string='Nutritional Values', store=True)
    x_shelf = fields.Integer(string='Shelf Life(Days)', default=20, store=True )
