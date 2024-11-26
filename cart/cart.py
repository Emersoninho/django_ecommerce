from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        """Inicializa o carrinho."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Salva um carrinho vazio na sessão
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Adiciona um produto ao carrinho ou atualiza sua quantidade."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Marca a sessão como modificada."""
        self.session.modified = True

    def remove(self, product):
        """Remove um produto do carrinho."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Itera pelos itens no carrinho e obtém os produtos do banco de dados."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Conta o número total de itens no carrinho."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calcula o preço total dos itens no carrinho."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Esvazia o carrinho."""
        del self.session[settings.CART_SESSION_ID]
        self.save()