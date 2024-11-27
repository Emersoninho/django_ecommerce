from django.shortcuts import render, redirect
from .models import Order, OrderItem, Address
from .forms import AddressForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            order = Order.objects.create(address=address)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # limpar o carrinho após o pedido
            cart.clear()
            return redirect('orders:order_create', order_id=order.id)
    else:
        form = AddressForm()
        return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})
        
def order_created(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})