from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import AddressForm
from cart.cart import Cart
from .utils import process_payment_with_mercadopago
from django.conf import settings

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            order = Order.objects.create(address=address)

            # verificar se a cidade do endereço é a mesma da loja
            if address.city == 'Paudalho':
                order.shipping_cost = 0.00 # frete grátis
            else:
                order.shipping_cost = 5.00 # frete cobrado

            
            # Criação dos itens do pedido
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            payment_method = request.POST.get('payment_method')
            payment_response = process_payment_with_mercadopago(order, payment_method)

            if "id" in payment_response:
                order.paid = True
                order.save()
                cart.clear()
                return redirect('orders:order_created', order_id=order.id)
            else:
                return render(request, 'orders/payment_error.html', {'error': 'Erro ao processar o pagamento'})
    else:
        form = AddressForm()

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})