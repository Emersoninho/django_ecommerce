from decimal import Decimal
from django.conf import settings
from products.models import Product

# Definindo constantes para facilitar a manutenção e evitar erros de digitação
QUANTITY = 'quantity'
PRICE = 'price'
PRODUCT = 'product'
TOTAL_PRICE = 'total_price'

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
        
        # Verifica se a quantidade solicitada é maior que o estoque
        if product.stock < quantity:
            return f"Desculpe, só há {product.stock} unidades disponíveis do produto {product.name}."
        
        if product_id not in self.cart:
            self.cart[product_id] = {QUANTITY: 0, PRICE: str(product.price)}
        
        # Atualiza a quantidade de acordo com a flag override_quantity
        if override_quantity:
            self.cart[product_id][QUANTITY] = quantity
        else:
            self.cart[product_id][QUANTITY] += quantity
        
        # Atualiza o preço do produto
        self.cart[product_id][PRICE] = str(product.price)
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
            self.cart[str(product.id)][PRODUCT] = product

        for item in self.cart.values():
            item[PRICE] = Decimal(item[PRICE])  # Garante que o preço seja um Decimal
            item[TOTAL_PRICE] = item[PRICE] * item[QUANTITY]  # Calcula o preço total
            yield item

    def __len__(self):
        """Conta o número total de itens no carrinho."""
        return sum(item[QUANTITY] for item in self.cart.values())

    def get_total_price(self):
        """Calcula o preço total dos itens no carrinho."""
        return sum(Decimal(item[PRICE]) * item[QUANTITY] for item in self.cart.values())

    def clear(self):
        """Esvazia o carrinho."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
