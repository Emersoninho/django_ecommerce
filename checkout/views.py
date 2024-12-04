from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from django.contrib import messages

def calcular_frete(estado):
    fretes = {
        'SP': 10.00,
        'RJ': 15.00,
        'MG': 20.00,
        'PE': 5.00,
    }
    return fretes.get(estado, 30.00) # frete sem estado definido


def checkout(request):
    """Exibe o checkout e processa a compra."""
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            freight = calcular_frete(state)

            # calcular o total do campo, incluindo o frete
            total_price = cart.get_total_price() + freight

            # Cria um pedido manualmente usando os dados do formulário
            order = Order.objects.create(
                full_name = form.cleaned_data['full_name'],
                email = form.cleaned_data['email'],
                address = form.cleaned_data['address'],
                postal_code = form.cleaned_data['postal_code'],
                city = form.cleaned_data['city'],
                state = state,
                payment_method = form.cleaned_data['payment_method'],
                freight = freight,
                total_price = total_price,
            )
            
            # Adiciona os itens do carrinho ao pedido
            for item in cart:
                OrderItem.objects.create(order=order, 
                    product=item['product'], 
                    price=item['price'], 
                    quantity=item['quantity'],
                )
                
            # Mensagem de sucesso e redireciona para a página de sucesso
            cart.clear()

            # redericiona para a página de sucesso
            messages.success(request, 'Compra realizada com sucesso!')
            return redirect('checkout:success')  # Redireciona para a página de sucesso
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CheckoutForm()
    return render(request, 'checkout/cart_checkout.html', {'cart': cart, 'form': form})

def success(request):
    """Página de sucesso após a compra."""
    return render(request, 'checkout/checkout_success.html')
