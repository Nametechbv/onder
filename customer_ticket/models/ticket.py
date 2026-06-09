from odoo import models, fields, api


class CustomerTicket(models.Model):
    _name = 'customer.ticket'
    _description = 'Customer Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject', required=True, tracking=True)
    description = fields.Html(string='Description', required=True)

    # 'urgency' alanı boolean olarak güncellendi
    is_urgent = fields.Boolean(string='Is Urgent', default=False, tracking=True)

    # 'stage' alanı güncellendi: 'change' eklendi, 'cancel' iptal anlamını taşıyacak
    stage = fields.Selection([
        ('draft', 'New'),
        ('process', 'In Progress'),
        ('review', 'Under Review'),
        ('delivery', 'Delivered'),
        ('change', 'Change Requested'),
        ('done', 'Approved'),
        ('cancel', 'Cancelled')
    ], string='Stage', default='draft', tracking=True, readonly=True)

    central_task_id = fields.Integer(string='Central Task ID', readonly=True)
    ticket_number = fields.Char(string='Ticket No', readonly=True, copy=False, default='New')

    @api.model
    def create(self, vals_list):
        # Eğer vals_list bir liste ise, her bir sözlük için döngüye gir
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get('ticket_number', 'New') == 'New':
                vals['ticket_number'] = self.env['ir.sequence'].next_by_code('customer.ticket') or 'TCK-000'

        return super(CustomerTicket, self).create(vals_list)

    def action_approve(self):
        """Trigger to send approval to Central Odoo"""
        self.write({'stage': 'done'})
        # Integration code will be added in Step 4

    def action_request_change(self):
        """Trigger to send change request to Central Odoo"""
        self.write({'stage': 'change'})
        # Integration code will be added in Step 4

    def action_cancel(self):
        """Trigger to cancel the ticket"""
        self.write({'stage': 'cancel'})
        # Integration code will be added in Step 4