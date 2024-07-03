import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Função para gerar data aleatória
def random_date(start, end):
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Função para converter todas as datas em uma lista para datetime.date
def convert_to_date(dates):
    return [d.date() if isinstance(d, datetime) else d for d in dates]

# Função para gerar dados de clientes
def generate_clientes(leads_df, n):
    clientes = []
    categorias = ['novo', 'upsell', 'downsell', 'cross-sell']
    industrias = ['transportes', 'logística']
    
    leads_df = leads_df[leads_df['etapa_atual'] == 'Fechamento'].sample(n)
    
    for index, lead in leads_df.iterrows():
        cliente_id = lead['lead_id']
        data_aquisicao = lead['data_transicao_fechamento']
        receita_mensal = round(random.uniform(1000, 10000), 2)
        categoria_cliente = random.choice(categorias)
        data_cancelamento = None if random.random() > 0.2 else random_date(data_aquisicao, datetime(2023, 12, 31)).date()
        industria = random.choice(industrias)
        clientes.append([cliente_id, data_aquisicao, receita_mensal, categoria_cliente, data_cancelamento, industria])
    
    return pd.DataFrame(clientes, columns=['cliente_id', 'data_aquisicao', 'receita_mensal', 'categoria_cliente', 'data_cancelamento', 'industria'])

# Função para gerar dados de leads
def generate_leads(n):
    leads = []
    etapas = ['Prospecção', 'Qualificação', 'Proposta', 'Fechamento']
    
    for i in range(n):
        lead_id = i + 1
        data_entrada = random_date(datetime(2020, 1, 1), datetime(2022, 12, 31))
        data_transicoes = [data_entrada]
        for _ in range(3):
            data_transicoes.append(random_date(data_transicoes[-1], datetime(2023, 12, 31)))
        data_transicoes = convert_to_date(data_transicoes)
        etapa_index = min(len([d for d in data_transicoes if d < datetime(2024, 1, 1).date()]), len(etapas) - 1)
        etapa_atual = etapas[etapa_index]
        leads.append([lead_id, data_entrada] + data_transicoes + [etapa_atual])
    
    return pd.DataFrame(leads, columns=['lead_id', 'data_entrada', 'data_transicao_prospecao', 'data_transicao_qualificacao', 'data_transicao_proposta', 'data_transicao_fechamento', 'etapa_atual'])

# Função para gerar dados de transações
def generate_transacoes(clientes_df):
    transacoes = []
    tipos = ['nova venda', 'upsell', 'downsell', 'cross-sell']
    
    for index, cliente in clientes_df.iterrows():
        cliente_id = cliente['cliente_id']
        data_aquisicao = cliente['data_aquisicao']
        data_cancelamento = cliente['data_cancelamento']
        receita_mensal = cliente['receita_mensal']
        
        if data_cancelamento:
            data_fim = data_cancelamento
        else:
            data_fim = datetime(2023, 12, 31).date()
        
        current_date = data_aquisicao
        while current_date <= data_fim:
            transacao_id = len(transacoes) + 1
            tipo_transacao = 'nova venda' if current_date == data_aquisicao else 'recorrente'
            valor_transacao = receita_mensal
            transacoes.append([transacao_id, cliente_id, tipo_transacao, valor_transacao, current_date])
            current_date += timedelta(days=30)
    
    return pd.DataFrame(transacoes, columns=['transacao_id', 'cliente_id', 'tipo_transacao', 'valor_transacao', 'data_transacao'])

# Gerar os dados
num_clientes = 100
num_leads = 1000

leads_df = generate_leads(num_leads)
clientes_df = generate_clientes(leads_df, num_clientes)
transacoes_df = generate_transacoes(clientes_df)

# Salvar em CSV
clientes_df.to_csv('clientes.csv', index=False)
leads_df.to_csv('leads.csv', index=False)
transacoes_df.to_csv('transacoes.csv', index=False)
