import mercadopago  # type: ignore
from django.conf import settings

def process_payment_with_mercadopago(order, payment_method):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    # Calcular total
    total = sum(item.get_cost() for item in order.items.all())

    # URL base do site
    site_url = settings.SITE_URL

    # Criação da preferência de pagamento
    preference_data = {
        'items': [
            {
                'title': f'Order #{order.id}',
                'quantity': 1,
                'unit_price': float(total),
                'currency_id': 'BRL',
            }
        ],
        'payer': {
            'email': 'emersoneletrotecnico2016@gmail.com',
        },
        'payment_methods': {
            'excluded_payment_types': [],
            'installments': 1,  # Parcelas
        },
        'back_urls': {
            'success': f'{site_url}/orders/created/{order.id}/',
            'failure': f'{site_url}/orders/create/',
            'pending': f'{site_url}/orders/created/{order.id}',
        },
        'auto_return': 'approved', # retorna automaticamente para a url de sucesso
    }

    # Condições para tipos de pagamento excluídos
    if payment_method == 'boleto':
        preference_data['payment_methods']['excluded_payment_types'] = [{'id': 'credit_card'}]
    elif payment_method == 'pix':
        preference_data['payment_methods']['excluded_payment_types'] = [{'id': 'ticket'}, {'id': 'credit_card'}]

    # Criação da preferência no Mercado Pago
    preference_response = sdk.preference().create(preference_data)
    
    # Verificar se a criação da preferência foi bem-sucedida
    if preference_response['status'] == 201:
        # Redirecionar para a URL de pagamento gerada pela preferência
        payment_url = preference_response['response']['init_point']
        return payment_url
    else:
        # Caso a criação da preferência falhe
        return None
