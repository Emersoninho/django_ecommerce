from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import AddressForm
from cart.cart import Cart
from .utils import process_payment_with_mercadopago

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            order = Order.objects.create(address=address)
            
            # Criação dos itens do pedido
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            payment_method = request.POST.get('payment_method')
            # Processa o pagamento com Mercado Pago
            payment_url = process_payment_with_mercadopago(order, payment_method)
            
            if payment_url:
                # Redireciona para a URL de pagamento do Mercado Pago
                return redirect(payment_url)
            else:
                # Exibe erro se algo deu errado
                return render(request, 'orders/payment_error.html', {'error': 'Erro ao processar o pagamento'})

    else:
        form = AddressForm()

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})