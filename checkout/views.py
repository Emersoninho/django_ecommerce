from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import CheckoutForm
from django.contrib import messages
import logging

def checkout(request):
    """Exibe o checkout e processa a compra."""
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Aqui você deve processar o pagamento real
            payment_successful = True  # Aqui deve ir a lógica de pagamento real
            logging.debug(f'Pagamento bem sucedido: {payment_successful}')
            if payment_successful:
                # Processar o pedido, salvar no banco de dados, etc.
                messages.success(request, 'Compra realizada com sucesso!')
                cart.clear()  # Limpa o carrinho após a compra
                logging.debug('Redirecionando para o sucesso!')
                return redirect('checkout:success')  # Redireciona para a página de sucesso
            else:
                messages.error(request, 'Erro no pagamento. Tente novamente.')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CheckoutForm()
    return render(request, 'checkout/cart_checkout.html', {'cart': cart, 'form': form})

def success(request):
    """Página de sucesso após a compra."""
    return render(request, 'checkout/checkout_success.html')
