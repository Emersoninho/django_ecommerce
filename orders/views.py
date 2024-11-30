from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import AddressForm
from cart.cart import Cart
from .utils import process_payment_with_mercadopago, calculate_shipping_cost_fixed

# Tabela de frete fixo por estado (exemplo)
FRETE_FIXO_POR_ESTADO = {
    'SP': 15.00,
    'RJ': 20.00,
    'MG': 18.00,
    'PE': 10.00,
    'OUTROS': 25.00,  # Valor padrão
}

# Função para calcular o frete
def calcular_frete(address):
    estado = address.state
    cidade = address.city.lower()

    # Exemplo de cálculo por estado
    frete = FRETE_FIXO_POR_ESTADO.get(estado, FRETE_FIXO_POR_ESTADO['OUTROS'])

    # Exemplo de ajuste para cidades específicas
    if cidade in ['carpina', 'recife']:
        distancia = 15  # Exemplo de distância fictícia em km
        if distancia <= 10:
            frete = 5.00
        elif distancia <= 20:
            frete = 10.00
        elif distancia <= 50:
            frete = 15.00
        else:
            frete = 20.00

    return frete

# View para criar o pedido
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Salva o endereço
            address = form.save()
            # Cria o pedido
            order = Order.objects.create(address=address)

            # Calcula o frete
            shipping_cost = calculate_shipping_cost_fixed(address.zipcode, '55825000')
            order.shipping_cost = shipping_cost
            

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

            # Verifica o pagamento
            if payment_response and 'id' in payment_response:
                order.paid = True
                order.save()
                cart.clear()
                return redirect('orders:order_created', order_id=order.id)
            else:
                return render(request, 'orders/payment_error.html', {'error': 'Erro ao processar o pagamento'})
    else:
        form = AddressForm()

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

# View para exibir o pedido criado
def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})
