# Geração de Dados Fictícios para Análise de Dados

Este projeto visa gerar dados fictícios para simular um ambiente de análise de dados contendo informações de: leads, clientes e transações.

## Estrutura das tabelas

### Tabela `leads`

Esta tabela contém dados de possíveis clientes. São pessoas que, de alguma maneira, entraram em contato conosco ou abordamos de forma ativa. Este processo de `lead` possui algumas etapas e segue um `workflow: prospecção -> qualificação -> proposta -> fechamento`, podendo haver o abandono/desistência a qualquer momento. Quando o `lead` chega em `fechamento` ele se torna um cliente. 

- `lead_id`: Identificador único do lead.
- `data_entrada`: Data de entrada do lead no funil.
- `data_transicao_prospecao`: Data de transição para a etapa de Prospecção.
- `data_transicao_qualificacao`: Data de transição para a etapa de Qualificação.
- `data_transicao_proposta`: Data de transição para a etapa de Proposta.
- `data_transicao_fechamento`: Data de transição para a etapa de Fechamento.
- `etapa_atual`: Etapa atual do lead no funil.

### Tabela `clientes`

Esta tabela contém dados de clientes. São pessoas que de fato efetuaram uma compra.

- `cliente_id`: Identificador único do cliente.
- `data_aquisicao`: Data da primeira compra.
- `receita_mensal`: Valor da mensalidade paga.
- `data_cancelamento`: Data de cancelamento do cliente (se aplicável).
- `industria`: Segmento do cliente.

### Tabela `transacoes`

Esta tabela contém dados de pagamentos dos clientes referente o serviço prestado. O serviço em si, possui recorrência mensal de pagamento (mensalidades).

- `transacao_id`: Identificador único da transação.
- `cliente_id`: Identificador do cliente relacionado à transação.
- `tipo_transacao`: Tipo de transação (nova venda, upsell, downsell, cross-sell, recorrente).
- `valor_transacao`: Valor da transação.
- `data_transacao`: Data da transação.

Sobre o atributo `tipo_transacao`:

Este atributo qualifica a transação, sendo: 
- `nova venda`: primeira compra do cliente.
- `upsell`: aumento (R$) de plano de um produto contratado.
- `downsell`: redução (R$) de plano de um produto contratado.
- `cross-sell`: aquisição de um novo produto.
- `recorrente`:  mensalidade comum (no caso, manteve o mesmo formato de contratação do mês anterior.)

## Pré-requisitos

Para executar este projeto, foi utilizado a versão `3.12.3` do Python e  você precisará das seguintes bibliotecas:

- pandas
- numpy
- faker

Essas bibliotecas estão listadas no arquivo requirements.txt e podem ser instaladas conforme explicado nas seções seguintes.

## Instalação

1. Clone o repositório:

```sh
git clone https://github.com/franc-felipe/fakercom.git
cd fakercom
```

2. Crie e ative um ambiente virtual:

```sh
python -m venv .venv
source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`
```

3. Instale as dependências:

```sh
pip install -r requirements.txt
```

## Estrutura do código

São 4 arquivos python que encontram-se na pasta `app`.

```lua
app
├── clientes.py
├── leads.py
├── ingest.py
└── transacoes.py
```

## Executando o Projeto

Para gerar os dados fictícios e salvá-los em arquivos CSV, siga os passos abaixo:

1. Execute o arquivo `leads.py`:

```sh
python leads.py
```

2. Execute o arquivo `clientes.py`:

```sh
python clientes.py
```

3. Execute o arquivo `transacoes.py`:

```sh
python transacoes.py
```

4. Este passo é opcional. O objetivo do arquivo `ingest.py` é fazer a carga destes dados em csv, num banco de dados. Para isso, você necessita editar os dados de acesso no arquivo (linhas 6 à 10).

Após a edição, execute:

```sh
python ingest.py
```




