import mercadopago
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
        'auto_return': 'approved',  # Retorna automaticamente para a URL de sucesso
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
        print(f'Erro ao criar preferência: {preference_response}')
        return None

def calculate_shipping_cost_fixed(origin_cep, destination_cep):
    """
    Calcula o custo do frete com base em uma lógica fixa.

    :param origin_cep: CEP de origem
    :param destination_cep: CEP de destino
    :return: Preço do frete
    """
    # Exemplo de lógica de frete com base em prefixos de CEP
    if origin_cep[:2] == destination_cep[:2]:  # Mesmo estado
        return 10.00
    elif origin_cep[:1] == destination_cep[:1]:  # Regiões próximas
        return 20.00
    else:  # Outras regiões
        return 30.00
