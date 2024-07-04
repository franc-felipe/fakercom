import pandas as pd
import numpy as np
from faker import Faker
import random

# Configurar a semente para reprodutibilidade
random.seed(42)
np.random.seed(42)

# Inicializar o Faker
fake = Faker()

# Carregar o arquivo leads_fake_data.csv
leads_df = pd.read_csv('leads_fake_data.csv')

# Filtrar os leads que se tornaram clientes
clientes_df = leads_df[leads_df['etapa_atual'] == 'Fechamento'].copy()

# Gerar dados para a tabela de clientes
clientes_df['cliente_id'] = [fake.uuid4() for _ in range(len(clientes_df))]
clientes_df['data_aquisicao'] = clientes_df['data_transicao_fechamento']
clientes_df['receita_mensal'] = [random.choice(range(350, 1901, 10)) for _ in range(len(clientes_df))]

# Gerar data de cancelamento para até 20% dos clientes
num_cancelamentos = int(0.2 * len(clientes_df))
cancelamento_indices = random.sample(list(clientes_df.index), num_cancelamentos)

# Concentrar 20% dos cancelamentos em Jan/23
jan_23_cancelamentos = int(0.2 * num_cancelamentos)
for idx in cancelamento_indices[:jan_23_cancelamentos]:
    data_aquisicao = pd.Timestamp(clientes_df.loc[idx, 'data_aquisicao'])
    if data_aquisicao < pd.Timestamp('2023-01-01'):
        data_cancelamento = fake.date_between_dates(date_start=pd.Timestamp('2023-01-01'), date_end=pd.Timestamp('2023-01-31'))
    else:
        try:
            data_cancelamento = fake.date_between_dates(date_start=data_aquisicao + pd.DateOffset(days=1), date_end=pd.Timestamp('2023-01-31'))
        except ValueError:
            data_cancelamento = pd.Timestamp('9999-12-01')
    clientes_df.loc[idx, 'data_cancelamento'] = data_cancelamento

# Restante dos cancelamentos em datas aleatórias, posteriores à data de aquisição
for idx in cancelamento_indices[jan_23_cancelamentos:]:
    data_aquisicao = pd.Timestamp(clientes_df.loc[idx, 'data_aquisicao'])
    try:
        data_cancelamento = fake.date_between_dates(date_start=data_aquisicao + pd.DateOffset(days=1), date_end=pd.Timestamp('2023-12-31'))
    except ValueError:
        data_cancelamento = pd.Timestamp('9999-12-01')
    clientes_df.loc[idx, 'data_cancelamento'] = data_cancelamento

# Adicionar indústria
industrias = ['Tecnologia', 'Saúde', 'Finanças', 'Educação', 'Varejo']
clientes_df['industria'] = [random.choice(industrias) for _ in range(len(clientes_df))]

# Selecionar e renomear colunas
clientes_df = clientes_df[['cliente_id', 'data_aquisicao', 'receita_mensal', 'data_cancelamento', 'industria', 'lead_id']]

# Exibir os primeiros registros
print(clientes_df.head())

# Salvar em um arquivo CSV
clientes_df.to_csv('clientes_fake_data.csv', index=False)
