from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .cart import Cart

def cart_update(request, product_id, action):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if action == 'increment':
        cart.add(product, quantity=1)
    elif action == 'decrement':
        cart.add(product, quantity=-1)
        # Remove o item se a quantidade for menor ou igual a 0
        if cart.cart[str(product_id)]['quantity'] <= 0:
            cart.remove(product)
    return redirect('cart:cart_detail')

def cart_add(request, product_id):
    """Adiciona um produto ao carrinho."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    
    if quantity > product.stock:
        # Se a quantidade solicitada for maior que a quantidade em estoque
        messages.error(request, f"Desculpe, não temos {quantity} unidades de {product.name} em estoque.")
    else:
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'Produto {product.name} adicionado ao carrinho com sucesso!')
    
    return redirect('cart:cart_detail')  # Redireciona para a página do carrinho

def cart_remove(request, product_id):
    """Remove um produto do carrinho."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Produto {product.name} removido do carrinho.')
    return redirect('cart:cart_detail')  # Redireciona para a página do carrinho

def cart_detail(request):
    """Exibe os detalhes do carrinho."""
    cart = Cart(request)
    return render(request, 'checkout/cart_checkout.html', {'cart': cart})

def cart_clear(request):
    """Esvazia o carrinho."""
    cart = request.session.get('cart', {})
    cart.clear()
    request.session['cart'] = cart
    messages.success(request, 'Carrinho esvaziado com sucesso!')
    return redirect('cart:cart_detail')  # Redireciona para a página do carrinho

