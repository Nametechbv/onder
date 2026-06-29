from odoo import models, fields, api

# models/product_template.py
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_vergi = fields.Char(string="Vergi", readonly=True, store=True, compute='_computed_vergi') #
    x_tadim = fields.Boolean(string="Tadım Ürünü mü?") #

    @api.depends('taxes_id') #
    def _computed_vergi(self):
        for rec in self:
            rec.x_vergi = rec.taxes_id

# models/res_users.py
class ResUsers(models.Model):
    _inherit = 'res.users'

    x_tum_musteri = fields.Boolean(string="Tadim") #
    x_tedarik_depo = fields.Many2one('stock.location', string="Tedarik Depo", ondelete='set null') #
    x_tadim = fields.Boolean(string="Tadim mi") #
    x_picking_type = fields.Many2one('stock.picking.type', string="Picking Type", ondelete='set null') #
    x_iskonto = fields.Integer(string="Iskonto") #
    x_in_route = fields.Boolean(string="Rota dışı satış") #
    x_discount_limit = fields.Float(string="Discount") #
    x_depo = fields.Many2one('stock.location', string="Depo", ondelete='set null') #


# models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_toplam_iskonto = fields.Float(string="Iskonto") #
    x_offer = fields.Boolean(string="Offer") #
    x_iskonto = fields.Float(string="Iskonto") #


# models/sale_order_line.py
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_pallettype = fields.Selection([ #
        ('euro', 'Euro Palet'),
        ('plastic', 'Plastik Palet'),
        ('wood', 'Ahşap Palet')
    ], string="Pallet Type")
    x_pallet = fields.Float(string="Pallet") #
    x_iskonto = fields.Float(string="Iskonto") #
    x_count = fields.Float(string="Count") #
    x_birim = fields.Float(string="Birim Fiyat") #


# models/res_partner.py
class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_price_list = fields.Integer( #
        string="Price List",
        readonly=True,
        related='property_product_pricelist.id'
    )
    x_partner_code = fields.Char(string="Partner Code") #
    x_iskonto = fields.Integer(string="Iskonto") #
    x_invoice_limit = fields.Integer(string="Limit") #
    x_frequency = fields.Integer(string="Ziyaret") #


# models/stock_picking.py
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_paket1 = fields.Float(string="Paket", readonly=True) #
    x_paket = fields.Integer(string="Paket", readonly=True) #


# models/account_move.py
class AccountMove(models.Model):
    _inherit = 'account.move'

    # to_check = fields.Boolean(string="Parcali Iade", default=False)

    x_partner_user = fields.Many2one( #
        'res.users', string="Müşteri Satış Temsilcisi",
        readonly=True,
        store=True,
        ondelete='set null',
        compute='_compute_partner_user',
        tracking=True
    )
    x_inroute = fields.Boolean(string="Route İçi mi") #
    x_box = fields.Integer(string="Total Box", compute='_compute_x_box', store=True)   #

    def _compute_partner_user(self):
        for record in self:
            record.x_partner_user = record.partner_id.user_id

    @api.depends('invoice_line_ids.quantity')
    def _compute_x_box(self):
        for rec in self:
            total = 0
            for line in rec.invoice_line_ids:
                total += line.quantity
            rec.x_box = total


# models/account_move_line.py
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_count = fields.Float(string="Box", readonly=True, related='product_id.base_unit_count') #
    x_birim = fields.Float(string="Unit Price", readonly=True, store=True, compute='_compute_x_birim') #

    @api.depends('x_count', 'price_unit')
    def _compute_x_birim(self):
        for rec in self:
            if rec.x_count > 0:
                rec.x_birim = rec.price_unit / rec.x_count

# models/res_company.py
class ResCompany(models.Model):
    _inherit = 'res.company'

    x_fatura_logo = fields.Binary(string="Fatura Logo") #