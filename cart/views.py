from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from django.contrib import messages


def cart_add(request, product_id):
    """Adiciona um produto ao carrinho."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    messages.success(request, f'Produto {product.name} adicionado ao carrinho com sucesso!')
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    """Remove um produto do carrinho."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Produto {product.name} removido do carrinho.')
    return redirect('cart:cart_detail')

def cart_detail(request):
    """Exibe os detalhes do carrinho."""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_clear(request):
    """Esvazia o carrinho."""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Carrinho esvaziado com sucesso!')
    return redirect('cart:cart_detail')


