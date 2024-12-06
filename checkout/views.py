def checkout(request):
    """Exibe o checkout e processa a compra."""
    cart = Cart(request)
    freight = Decimal('0.00')
    total_price = cart.get_total_price()  # Supondo que isso retorne um Decimal

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            freight = calcular_frete(state)  # Isso deve retornar um Decimal
            total_price += freight

            order = Order.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
                state=state,
                payment_method=form.cleaned_data['payment_method'],
                freight=freight,
                total_price=total_price,
            )
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                
            cart.clear()
            messages.success(request, 'Compra realizada com sucesso!')
            return redirect('checkout:success')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CheckoutForm()
    
    # Armazenando valores na sessão como float
    request.session['freight'] = float(freight)  # Converte para float
    request.session['total_price'] = float(total_price)  # Converte para float

    return render(request, 'checkout/cart_checkout.html', {
        'cart': cart, 
        'form': form, 
        'freight': float(freight), 
        'total_price': float(total_price)
    })