import mercadopago # type: ignore
from django.conf import settings

def process_payment_with_mercadopago(order, payment_method):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    # Calcular total
    total = sum(item.get_cost() for item in order.items.all())

    #Cria preferência de pagamento
    preference_data = {
        'items':[
            {
                'title':f'Order #{order.id}',
                'quantity': 1,
                'unit_price': float(total),
                'currency_id': 'BRL',
            }
        ],
        'payer': {
            'email': order.address.email,
        },
        'payment_methods': {
            'excluded_payment_types': [],
            'installments': 1, #Parcelas
        }
    }

    if payment_method == 'boleto':
        preference_data['payment_methods']['excluded_payment_types'] = [{'id':'credit_card'}]
    elif payment_method == 'pix':
        preference_data['payment_methods']['excluded_payment_types'] = [{'id': 'ticket'}, {'id': 'credit_card'}]

    preference_response = sdk.preference().create(preference_data)
    return preference_response['response']   