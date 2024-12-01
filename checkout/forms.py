from django import forms

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Cartão de Crédito'),
        ('pix', 'Pix'),
        ('boleto', 'Boleto Bancário'),
    ]

    full_name = forms.CharField(label='Nome Completo', max_length=100)
    email = forms.EmailField(label='E-mail')
    address = forms.CharField(label='Endereço Completo', max_length=255)
    postal_code = forms.CharField(label='CEP', max_length=20)
    city = forms.CharField(label='Cidade', max_length=100)
    payment_method = forms.ChoiceField(label='Método de Pagamento', choices=PAYMENT_CHOICES)
