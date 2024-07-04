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

# Função para gerar uma data aleatória dentro de um intervalo
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Intervalo de datas
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)

# Gerar dados
data = []
months = pd.date_range(start_date, end_date, freq='MS')

for month in months:
    num_leads = random.randint(20, 30)
    if month == datetime(2022, 12, 1):
        num_leads = 100
    
    for _ in range(num_leads):
        lead_id = fake.uuid4()
        data_entrada = random_date(month, month + timedelta(days=30))
        etapa_atual = random.choice(['Prospecção', 'Qualificação', 'Proposta', 'Fechamento'])
        
        data_transicao_prospecao = data_entrada if etapa_atual in ['Prospecção', 'Qualificação', 'Proposta', 'Fechamento'] else None
        data_transicao_qualificacao = random_date(data_transicao_prospecao, data_transicao_prospecao + timedelta(days=30)) if etapa_atual in ['Qualificação', 'Proposta', 'Fechamento'] else None
        data_transicao_proposta = random_date(data_transicao_qualificacao, data_transicao_qualificacao + timedelta(days=30)) if etapa_atual in ['Proposta', 'Fechamento'] else None
        data_transicao_fechamento = random_date(data_transicao_proposta, data_transicao_proposta + timedelta(days=30)) if etapa_atual == 'Fechamento' else None
        
        data.append([lead_id, data_entrada, etapa_atual, data_transicao_prospecao, data_transicao_qualificacao, data_transicao_proposta, data_transicao_fechamento])

# Criar DataFrame
columns = ['lead_id', 'data_entrada', 'etapa_atual', 'data_transicao_prospecao', 'data_transicao_qualificacao', 'data_transicao_proposta', 'data_transicao_fechamento']
leads_df = pd.DataFrame(data, columns=columns)

# Exibir os primeiros registros
print(leads_df.head())

# Opcional: Salvar em um arquivo CSV
leads_df.to_csv('leads_fake_data.csv', index=False)
