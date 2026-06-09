import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)
alias = "onder"

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

        tickets = super(CustomerTicket, self).create(vals_list)
        central_url = self.env['ir.config_parameter'].sudo().get_param('central_odoo.url',
                                                                       'https://rubixb2.com/api/ticket/create')
        api_token = self.env['ir.config_parameter'].sudo().get_param('central_odoo.token', 'Ticket2026')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_token}'
        }

        for ticket in tickets:
            # Payload wrapped in 'params' for Odoo JSON-RPC routing
            payload = {
                "params": {
                    "title": ticket.name,
                    "description": ticket.description,
                    "is_urgent": ticket.is_urgent,
                    "customer_ref": alias,
                    "remote_ticket_id": ticket.id
                }
            }
            try:
                response = requests.post(central_url, json=payload, headers=headers, timeout=10)
                if response.status_code == 200:
                    result = response.json().get('result', {})
                    if result.get('status') == 'success':
                        ticket.central_task_id = result.get('central_task_id')
                    else:
                        _logger.error(f"Central Odoo API Error: {result.get('message')}")
            except Exception as e:
                _logger.error(f"Failed to push ticket to Central Odoo: {str(e)}")

        return tickets


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