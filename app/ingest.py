import pandas as pd
import psycopg2
from psycopg2 import sql

# Variáveis de conexão com o banco
DB_NAME="nome-do-meu-banco",
DB_USER="nome-do-meu-usuario",
DB_PASS="minha-senha",
DB_HOST="endereco-do-host",
DB_PORT="porta"

# Função para conectar ao banco de dados
def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Função para criar tabelas
def create_tables(conn):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS leads (
            lead_id UUID PRIMARY KEY,
            data_entrada DATE,
            etapa_atual VARCHAR(50),
            data_transicao_prospecao DATE,
            data_transicao_qualificacao DATE,
            data_transicao_proposta DATE,
            data_transicao_fechamento DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS clientes (
            cliente_id UUID PRIMARY KEY,
            data_aquisicao DATE,
            receita_mensal NUMERIC,
            data_cancelamento DATE,
            industria VARCHAR(50),
            lead_id UUID REFERENCES leads(lead_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS transacoes (
            transacao_id UUID PRIMARY KEY,
            cliente_id UUID REFERENCES clientes(cliente_id),
            tipo_transacao VARCHAR(50),
            valor_transacao NUMERIC,
            data_transacao DATE
        )
        """
    ]
    with conn.cursor() as cursor:
        for query in queries:
            cursor.execute(query)
        conn.commit()

# Função para inserir dados em uma tabela
def insert_data(conn, table_name, df):
    # Substituir NaN por None
    df = df.where(pd.notnull(df), None)
    
    with conn.cursor() as cursor:
        for i, row in df.iterrows():
            columns = list(row.index)
            values = [row[col] for col in columns]
            insert_stmt = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )
            cursor.execute(insert_stmt, values)
        conn.commit()

# Função principal
def main():
    # Conectar ao banco de dados
    conn = connect_to_db()
    
    # Criar tabelas
    create_tables(conn)
    
    # Ler dados dos arquivos CSV
    leads_df = pd.read_csv('leads_fake_data.csv')
    clientes_df = pd.read_csv('clientes_fake_data.csv')
    transacoes_df = pd.read_csv('transacoes_fake_data.csv')

    # Inserir dados nas tabelas
    insert_data(conn, 'leads', leads_df)
    insert_data(conn, 'clientes', clientes_df)
    insert_data(conn, 'transacoes', transacoes_df)
    
    # Fechar conexão
    conn.close()

if __name__ == "__main__":
    main()
