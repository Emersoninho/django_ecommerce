from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from django.contrib import messages
from decimal import Decimal

def calcular_frete(estado):
    fretes = {
        'SP': Decimal(10.00),
        'RJ': Decimal(15.00),
        'MG': Decimal(20.00),
        'PE': Decimal(5.00),
    }
    return float(fretes.get(estado, Decimal(30.00)))  # Retorna como float diretamente

def checkout(request):
    """Exibe o checkout e processa a compra."""
    cart = Cart(request)
    freight = 0.00
    total_price = float(cart.get_total_price())  # Garante que o total seja float

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            freight = calcular_frete(state)  # Calcula o frete
            total_price += freight  # Calcula o total com frete

            # Cria o pedido
            order = Order.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
                state=state,
                payment_method=form.cleaned_data['payment_method'],
                freight=Decimal(freight),  # Salva como Decimal no banco
                total_price=Decimal(total_price),  # Salva como Decimal no banco
            )

            # Adiciona itens do carrinho ao pedido
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            # Limpa o carrinho e redireciona para sucesso
            cart.clear()
            messages.success(request, 'Compra realizada com sucesso!')
            return redirect('checkout:success')

        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')

    else:
        form = CheckoutForm()

    # Envia os valores ao template
    return render(
        request,
        'checkout/cart_checkout.html',
        {
            'cart': cart,
            'form': form,
            'freight': freight,  # Valor já é float
            'total_price': total_price,  # Valor já é float
        },
    )

def success(request):
    """Página de sucesso após a compra."""
    return render(request, 'checkout/checkout_success.html')
