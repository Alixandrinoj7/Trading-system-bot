import random
from datetime import datetime

def gerar_sinal_inteligente():
    pares = ['EUR/USD', 'GBP/JPY', 'USD/JPY', 'AUD/USD', 'EUR/GBP']
    tipo_operacao = random.choice(['CALL', 'PUT'])
    moeda = random.choice(pares)
    preco_base = round(random.uniform(1.0900, 1.1000), 4)

    if tipo_operacao == 'CALL':
        preco_entrada = preco_base
        preco_saida = round(preco_base + random.uniform(0.0010, 0.0030), 4)
    else:
        preco_entrada = preco_base
        preco_saida = round(preco_base - random.uniform(0.0010, 0.0030), 4)

    sinal = {
        'moeda': moeda,
        'tipo': tipo_operacao,
        'expiracao': 1,
        'horario': datetime.now().strftime('%H:%M:%S'),
        'preco_entrada': preco_entrada,
        'preco_saida': preco_saida,
        'assertividade': round(random.uniform(70, 95), 2)
    }

    return sinal
