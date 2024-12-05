from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('credit_card', 'Cartão de Crédito'),
        ('pix', 'Pix'),
        ('boleto', 'Boleto Bancário'),
    ]

    STATE_CHOICES = [
        ('SP', 'São Paulo'),
        ('RJ', 'Rio de Janeiro'),
        ('MG', 'Minas Gerais'),
        ('PE', 'Pernambuco'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Método de Pagamento')
    state = forms.ChoiceField(choices=STATE_CHOICES, label='Estado')  # Novo campo de estado
    freight = forms.DecimalField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'postal_code', 'city', 'state', 'payment_method', 'freight']
