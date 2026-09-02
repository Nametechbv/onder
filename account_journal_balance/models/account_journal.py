from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # 101 Nolu Hesap Bakiyesi (Banka için)
    x_bank_balance_357 = fields.Monetary(
        string="357 Banka Bakiyesi", 
        compute='_compute_balances', 
        currency_field='currency_id'
    )
    
    # 102 Nolu Hesap Bakiyesi (Kasa için)
    x_bank_balance_350 = fields.Monetary(
        string="350 Kasa Bakiyesi", 
        compute='_compute_balances', 
        currency_field='currency_id'
    )

    @api.depends('company_id')
    def _compute_balances(self):
        for record in self:
            # 101 Nolu Hesabın SQL Sorgusu (Banka)
            record.env.cr.execute("""
                SELECT SUM(debit - credit) 
                FROM account_move_line 
                WHERE account_id = 357 AND parent_state = 'posted'
            """)
            res_357 = record.env.cr.fetchone()
            record.x_bank_balance_101 = res_357[0] if res_357 and res_357[0] else 0.0

            # 102 Nolu Hesabın SQL Sorgusu (Kasa)
            record.env.cr.execute("""
                SELECT SUM(debit - credit) 
                FROM account_move_line 
                WHERE account_id = 350 AND parent_state = 'posted'
            """)
            res_350 = record.env.cr.fetchone()
            record.x_bank_balance_350 = res_350[0] if res_350 and res_350[0] else 0.0