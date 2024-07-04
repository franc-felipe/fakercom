import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar a semente para reprodutibilidade
random.seed(42)
np.random.seed(42)

# Inicializar o Faker
fake = Faker()

# Carregar o arquivo clientes_fake_data.csv
clientes_df = pd.read_csv('clientes_fake_data.csv')

# Função para gerar uma data aleatória dentro de um intervalo
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Inicializar uma lista para armazenar as transações
transacoes = []

# Gerar transações para cada cliente
for idx, row in clientes_df.iterrows():
    cliente_id = row['cliente_id']
    data_aquisicao = pd.Timestamp(row['data_aquisicao'])
    data_cancelamento = pd.Timestamp(row['data_cancelamento']) if pd.notnull(row['data_cancelamento']) else None
    receita_mensal = row['receita_mensal']

    # Adicionar a transação inicial (nova venda)
    transacoes.append([fake.uuid4(), cliente_id, 'nova venda', receita_mensal, data_aquisicao])
    
    # Gerar transações mensais
    data_atual = data_aquisicao + pd.DateOffset(months=1)
    while data_atual <= datetime(2023, 12, 31):
        if data_cancelamento and data_atual > data_cancelamento:
            break

        tipo_transacao = 'recorrente'
        valor_transacao = receita_mensal

        # Definir tipo de transação e ajustar valor conforme necessário
        if random.random() < 0.25:
            tipo_transacao = 'upsell'
            valor_transacao = receita_mensal * 1.1
            receita_mensal = valor_transacao
        elif random.random() < 0.10:
            tipo_transacao = 'downsell'
            valor_transacao = receita_mensal * 0.9
            receita_mensal = valor_transacao
        elif random.random() < 0.05:
            tipo_transacao = 'cross-sell'
            valor_transacao = receita_mensal * 0.5

        # Adicionar a transação
        transacoes.append([fake.uuid4(), cliente_id, tipo_transacao, valor_transacao, data_atual])

        # Incrementar para o próximo mês
        data_atual += pd.DateOffset(months=1)

# Criar DataFrame
transacoes_df = pd.DataFrame(transacoes, columns=['transacao_id', 'cliente_id', 'tipo_transacao', 'valor_transacao', 'data_transacao'])

# Exibir os primeiros registros
print(transacoes_df.head())

# Salvar em um arquivo CSV
transacoes_df.to_csv('transacoes_fake_data.csv', index=False)
