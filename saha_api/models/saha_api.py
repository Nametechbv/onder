from odoo import models, api, fields

class SahaSatisAPI(models.Model):
    _name = 'saha.satis.api'
    _description = 'Mobil Saha Satis API Katmani'

    @api.model
    def get_full_product_catalog_by_location(self, location_id, partner_id=None, limit=50, offset=0):
        """
        Odoo 15 uyumlu: Lokasyon bazlı stok ve dinamik fiyat hesaplama.
        """
        # 1. Müşteri ve Fiyat Listesi Hazırlığı
        partner = self.env['res.partner'].browse(partner_id) if partner_id else self.env['res.partner']
        
        # Odoo 15'te partner üzerinden pricelist'e güvenli erişim
        pricelist = partner.property_product_pricelist
        if not pricelist:
            pricelist = self.env['product.pricelist'].search([], limit=1)

        # 2. Ürünleri Sorgula
        domain = [('sale_ok', '=', True)]
        products = self.env['product.product'].search(domain, limit=limit, offset=offset)

        catalogue = []
        # Stok hesaplaması için context eklenmiş ürün seti
        products_with_loc = products.with_context(location=location_id)

        for product in products_with_loc:
            # 3. Lokasyon Bazlı Stok
            stock = product.qty_available

            # 4. Fiyat Hesaplama (DÜZELTİLDİ: _get_product_price yerine get_product_price)
            if pricelist:
                # Odoo 15 Standart Metodu
                price_unit = pricelist.get_product_price(product, 1.0, partner)
            else:
                price_unit = product.lst_price

            # Vergi Hesaplama
            currency = pricelist.currency_id if pricelist else self.env.company.currency_id
            taxes_res = product.taxes_id.compute_all(
                price_unit=price_unit,
                currency=currency,
                quantity=1.0,
                product=product,
                partner=partner
            )

            # 5. Veri Paketini Birleştir
            catalogue.append({
                'id': product.id,
                'name': product.name,
                'barcode': product.default_code,
                'list_price': price_unit,
                'price_gross': taxes_res['total_included'],
                'x_vergi': sum(tax['amount'] for tax in taxes_res['taxes']),
                'stock': stock,
                'uom': product.uom_id.name,
                'product_piece_count': getattr(product, 'base_unit_count', 0),
                'int_category': product.categ_id.name,
                'web_categories': product.public_categ_ids.mapped('name') if 'public_categ_ids' in product._fields else [],
                'weight': product.weight,
                'volume': product.volume,
                'product_barcode': product.barcode
            })

        return catalogue