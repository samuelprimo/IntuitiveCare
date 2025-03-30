# 🏥 **Sistema de Processamento de Dados ANS** 

*Solução completa para coleta, transformação e análise de dados da Agência Nacional de Saúde Suplementar*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-brightgreen?logo=django)](https://djangoproject.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)](https://mysql.com)


## 📂 **Teste 1 - Web Scraping de Documentos ANS**

### 🎯 **Objetivo**
Automatizar o download dos Anexos I e II (PDFs) do portal da ANS e compactá-los em um único arquivo ZIP.

### ⚙️ **Tecnologias Utilizadas**
- **Python 3.8+**
- Bibliotecas:
  - `requests` (requisições HTTP)
  - `BeautifulSoup` (parseamento HTML)
  - `zipfile` (compactação)
  - `os` (manipulação de arquivos)

## 🛠️ Como Executar o Web Scraper

O projeto utiliza um sistema de gerenciamento via command line. Para executar o scraper:

```bash
python manage.py download_ans_pdfs --url "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos" --output "arquivos.zip"
````
## 🛠 **Teste 2 - Transformação de Dados**

### 📋 **Objetivo**
Extrair dados tabulares do PDF (Anexo I) baixado no Teste 1, transformá-los em CSV estruturado e compactar o resultado.

### 📥 **Entrada**
- Arquivo PDF `Anexo_I.pdf` (baixado via Teste 1)

### 📤 **Saída**
- Arquivo CSV com dados estruturados
- Arquivo ZIP contendo o CSV (`Teste_[Nome].zip`)

## ⚙️ Parâmetros

| Argumento    | Descrição                          | Obrigatório | Valor Padrão       |
|--------------|------------------------------------|-------------|--------------------|
| `--url`      | URL do site contendo os PDFs       | Sim         | -                  |
| `--output`   | Nome do arquivo ZIP de saída       | Não         | `pdfs_coletados.zip` |

## 📊 Extração de Tabelas de PDF

Para extrair tabelas de arquivos PDF, utilize o seguinte comando:

```bash
python manage.py extrair_tabela_pdf --pdf [CAMINHO_PDF] --output [NOME_SAIDA]
```
## ⚙️ Parâmetros 

| Argumento   | Descrição                          | Obrigatório  | Valor Padrão         |
|-------------|-----------------------------------|-------------|---------------------|
| `--pdf`     | Caminho completo do arquivo PDF   | Sim         | -                   |
| `--output`  | Nome do arquivo CSV de saída      | Não         | `dados_extraidos.csv` |

### Observações:
- A extensão `.csv` será adicionada automaticamente se não for especificada

### 🎯 **Objetivos**
1. Estruturar e popular banco de dados com informações das operadoras
2. Realizar análises sobre despesas médicas
3. Identificar as 10 operadoras com maiores gastos em sinistros hospitalares

## 💻 Exemplos de Uso

### Extraindo de um arquivo específico
```bash
python manage.py extrair_tabela_pdf --pdf "C:/documentos/anexo1.pdf" --output "planilha_final"

```

### 🛠 **Tecnologias Utilizadas**
| Componente | Tecnologia |
|------------|------------|
| Banco de Dados | MySQL 8.0 |
| ORM | Django Models |
| Interface | HeidiSQL |
| Linguagem | Python/SQL |

### 📊 **Modelagem de Dados**
```python
# models.py
class Operadora(models.Model):
    registro_ans = models.BigIntegerField(primary_key=True)
    cnpj = models.CharField(max_length=18)
    razao_social = models.TextField()
    # ... outros campos cadastrais

class DemonstracaoContabil(models.Model):
    data = models.DateField()
    registro_ans = models.BigIntegerField(db_index=True)
    descricao = models.CharField(max_length=150)
    vl_saldo_final = models.DecimalField(max_digits=15, decimal_places=2)
```
## 🗃 Banco de Dados: Queries SQL**

### 📥 **1. Importação de Dados**

#### **Operadoras Ativas**
```sql
LOAD DATA LOCAL INFILE 'operadoras.csv'
INTO TABLE api_operadora
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    registro_ans, cnpj, razao_social, nome_fantasia, modalidade, 
    logradouro, numero, complemento, bairro, cidade, 
    estado, cep, ddd, telefone, fax,
    endereco_eletronico, representante, cargo_representante, 
    regiao_de_comercializacao, data_registro_ans
)
SET
    numero = NULLIF(@numero, ''),
    nome_fantasia = NULLIF(@nome_fantasia, ''),
    fax = NULLIF(@fax, '');
    regiao_de_comercializacao = NULLIF(TRIM(@regiao_de_comercializacao), '') + 0;

```
***Demonstrações Contábeis***

```
LOAD DATA LOCAL INFILE 'C:/Users/samuc/Downloads/1T2024/1T2024.csv'
INTO TABLE api_demonstracaocontabil
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final
)
SET
    data = CASE 
        WHEN @data LIKE '__-__-____' THEN STR_TO_DATE(@data, '%y-%m-%d')
        WHEN @data LIKE '__/__/____' THEN STR_TO_DATE(@data, '%d/%m/%Y')
        WHEN @data LIKE '____-__-__' THEN STR_TO_DATE(@data, '%Y-%m-%d')
    END,
    vl_saldo_inicial = REPLACE(@vl_saldo_inicial, ',', '.'),
    vl_saldo_final = REPLACE(@vl_saldo_final, ',', '.');

    

```

## 🔍 2. Consultas Analíticas

### **Top 10 Operadoras - Último Trimestre**

```sql
SELECT 
    op.registro_ans, 
    COALESCE(op.nome_fantasia, op.razao_social) AS nome_operadora, 
    SUM(dc.vl_saldo_final) AS total_despesas
FROM 
    api_demonstracaocontabil dc
JOIN 
    api_operadora op ON dc.registro_ans = op.registro_ans
WHERE 
    dc.descricao LIKE '%SINISTROS%'
GROUP BY 
    op.registro_ans, nome_operadora
ORDER BY 
    total_despesas DESC
LIMIT 10;
```
***Top 10 Operadoras - Último Ano***
```sql
SELECT 
    op.registro_ans, 
    COALESCE(op.nome_fantasia, op.razao_social) AS nome_operadora, 
    SUM(dc.vl_saldo_final) AS total_despesas
FROM 
    api_demonstracaocontabil dc
JOIN 
    api_operadora op ON dc.registro_ans = op.registro_ans
WHERE 
    dc.descricao LIKE '%SINISTROS%'
    AND dc.data >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY 
    op.registro_ans, op.nome_fantasia
ORDER BY 
    total_despesas DESC
LIMIT 10;
```
- Todas as queries usam LIKE para capturar variações no texto dos sinistros

- Conversão explícita de:

- Datas (STR_TO_DATE)

- Valores monetários (substituição de , por .)

- Funções de agregação (SUM) com GROUP BY para consolidação

- COALESCE para tratamento de nomes fantasia nulos

## 📊 **Exemplos de Saída**

### **Top Operadoras (Último Ano)**

| Posição | Operadora       | Despesas (R$)    |
|---------|-----------------|------------------|
| 1       | UNIMED RJ       | 28.450.000,00    |
| 2       | AMIL SAÚDE      | 25.300.000,00    |
| 3       | SULAMÉRICA      | 18.750.000,00    |
| 4       | HAPVIDA         | 15.200.000,00    |
| 5       | NOTRE DAME      | 12.800.000,00    |

**Legenda:**
- Valores representam o somatório anual de despesas com "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS"
- Dados formatados no padrão brasileiro (ponto para milhar, vírgula para decimal)
- Fonte: ANS - Dados Abertos (2023)


## 🚀 Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/samuelprimo/IntuitiveCare.git
cd IntuitiveCare/backend

python -m venv venv

# Ativar no Linux/Mac:
source venv/bin/activate

# Ativar no Windows:
.\venv\Scripts\activate
```
## 📦 Instalação de Dependências

Execute o seguinte comando para instalar todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

## 🔧 Configurar Variáveis de Ambiente

1. Na raiz do projeto (`/backend`), crie um arquivo chamado `.env`
2. Adicione as seguintes configurações:

```ini
# Configurações Django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1 (...)

# Configurações CORS
CORS_ALLOW_ALL_ORIGINS=True

# Configurações do Banco de Dados
DB_ENGINE=django.db.backends.mysql
DB_NAME=sistema_ans
DB_USER=samuc
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
```
## 🛠️ Execução do Projeto

### 5. Aplicar Migrações do Banco de Dados
```bash
python manage.py migrate
```
- Cria todas as tabelas necessárias no banco de dados configurado

- Aplica as migrações pendentes

- Prepara a estrutura do banco para o funcionamento da aplicação
```bash
python manage.py runserver
```
- Servidor disponível em: http://localhost:8000

