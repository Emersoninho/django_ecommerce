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
            # Salva o endereço do cliente
            address = form.save()
            order = Order.objects.create(address=address)

            # Simula o cálculo da distância (usando um valor fixo por enquanto, como exemplo)
            origin = 'Paudalho, PE'  # Endereço da loja
            destination = f'{address.address_line}, {address.city}, {address.state}'  # Endereço do cliente

            # Calcular a distância (exemplo com valores simulados)
            # Vamos simular que a distância seja calculada entre os dois pontos.
            # Para fins de exemplo, vamos assumir algumas distâncias fictícias.
            # Isso deve ser substituído por um cálculo real (API de geolocalização ou outro método).
            distance = 15  # Simulando uma distância de 15 km
            if distance is not None:
                if distance <= 10:
                    shipping_cost = 5.00
                elif distance <= 20:
                    shipping_cost = 10.00
                else:
                    shipping_cost = 15.00
            else:
                shipping_cost = 20.00  # Valor padrão em caso de erro

            # Atribui o custo de entrega ao pedido
            order.shipping_cost = shipping_cost
            order.save()

            # Adiciona os itens do carrinho ao pedido
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Processo de pagamento
            payment_method = request.POST.get('payment_method')
            payment_response = process_payment_with_mercadopago(order, payment_method)

            if 'id' in payment_response:
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
