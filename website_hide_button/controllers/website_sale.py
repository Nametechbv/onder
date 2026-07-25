# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2026-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    """class to hide price, add to cart and quantity"""

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/
        page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0,
             max_price=0.0, ppg=False, **post):
        """Method for finding log in user or not in shop page """
        res = super().shop(page, category, search, min_price,
                           max_price, ppg, **post)

        # Ayarları veritabanından güvenli bir şekilde çekiyoruz. (Odoo'da get_param string dönebilir)
        hide_cart_setting = request.env['ir.config_parameter'].sudo().get_param(
            'website_hide_button.hide_cart') == 'True'
        hide_price_setting = request.env['ir.config_parameter'].sudo().get_param(
            'website_hide_button.hide_price') == 'True'

        res.qcontext.update({
            # Eğer kullanıcı misafirse VE gizleme ayarı açıksa True döner (Uyarıyı gösterir)
            'login_user': True if request.env.user._is_public() and hide_cart_setting else False,

            # Eğer fiyat gizleme ayarı KAPALIYSA True döner (XML'deki show_price artık buna bakacak)
            'show_price': not hide_price_setting
        })
        return res

    def _prepare_product_values(self, product, category,**kwargs):
        """Method for finding log in user or not in product page """
        res = super(WebsiteSaleInherit, self)._prepare_product_values(product,
                                                                      category,
                                                                      **kwargs)
        hide_cart_setting = request.env['ir.config_parameter'].sudo().get_param(
            'website_hide_button.hide_cart') == 'True'
        hide_price_setting = request.env['ir.config_parameter'].sudo().get_param(
            'website_hide_button.hide_price') == 'True'

        res['login_user'] = True if request.env.user._is_public() and hide_cart_setting else False
        res['show_price'] = not hide_price_setting
        return res

    @http.route()
    def shop_payment(self, **post):
        """  Restrict public visitors from accessing payment page so that SO
        creation will be disabled   """
        user = http.request.env.user
        hide_cart_setting = request.env['ir.config_parameter'].sudo().get_param(
            'website_hide_button.hide_cart') == 'True'

        if (not user._is_public() or (user._is_public() and not hide_cart_setting)) and \
                (user.has_group('base.group_portal') or user.has_group('base.group_user')):
            return super(WebsiteSaleInherit, self).shop_payment(**post)
        return request.redirect("/")
