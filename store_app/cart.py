from decimal import Decimal

from django.conf import settings

from store_app.models import Product


class Cart(object):
    '''Корзина продуктов'''

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        '''Перебираем товары в корзине и получаем товары из базы данных'''
        product_ids = self.cart.keys()
        # получаем товары и добавляем их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = item['price']
            item['total_price'] = float(item['price']) * float(item['quantity'])
            yield item

    def __len__(self):
        '''Количество товаров в корзине'''
        return sum(i['quantity'] for i in self.cart.values())

    def add(self, product, quantity=1):
        '''Добавление товара в корзину'''
        product_id = str(product.id)
        self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}

    def save(self):
        '''Сохранение товара'''
        self.session.modified = True

    def remove(self, product):
        '''Удаление товара'''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        '''Очистка корзины в сессии'''
        del self.session[settings.CART_SESSION_ID]
        self.save()
