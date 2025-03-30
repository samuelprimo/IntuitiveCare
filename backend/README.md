# 🏥 **Sistema de Processamento de Dados ANS** 

*Solução completa para coleta, transformação e análise de dados da Agência Nacional de Saúde Suplementar*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-brightgreen?logo=django)](https://djangoproject.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)](https://mysql.com)

## 📌 **Sumário**
1. [Funcionalidades](#-funcionalidades)
2. [Tecnologias](#-tecnologias)
3. [Estrutura do Projeto](#-estrutura-do-projeto)
4. [Modelagem do Banco](#-modelagem-do-banco)
5. [Como Executar](#-como-executar)
6. [Queries SQL](#%EF%B8%8F-queries-sql-chave)
7. [Exemplos de Saída](#-exemplos-de-saída)

## 🚀 **Funcionalidades**

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

### 📜 **Código Principal**
```python
import requests
from bs4 import BeautifulSoup
import zipfile
import os

def baixar_pdfs(url_alvo, arquivo_saida):
    # Configura headers para evitar bloqueio
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Faz requisição ao site
        resposta = requests.get(url_alvo, headers=headers)
        resposta.raise_for_status()
        
        # Parseia o HTML
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Encontra todos os links de PDF
        links_pdf = [
            a['href'] for a in soup.find_all('a', href=True) 
            if a['href'].lower().endswith('.pdf')
        ]
        
        # Cria ZIP com os arquivos
        with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
            for link in links_pdf:
                nome_arquivo = link.split('/')[-1]
                conteudo_pdf = requests.get(link).content
                zipf.writestr(nome_arquivo, conteudo_pdf)
                
        return f"Arquivo {arquivo_saida} criado com sucesso!"
        
    except Exception as e:
        return f"Erro: {str(e)}"
````
## 🛠 **Teste 2 - Transformação de Dados**

### 📋 **Objetivo**
Extrair dados tabulares do PDF (Anexo I) baixado no Teste 1, transformá-los em CSV estruturado e compactar o resultado.

### 📥 **Entrada**
- Arquivo PDF `Anexo_I.pdf` (baixado via Teste 1)

### 📤 **Saída**
- Arquivo CSV com dados estruturados
- Arquivo ZIP contendo o CSV (`Teste_[Nome].zip`)

### 🧠 **Lógica Implementada**
```python
def extract_tables_from_pdf(file_path):
    data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                for row in tables:
                    clean_row = [cell for cell in row if cell and not cell.isdigit()]
                    data.append(clean_row)
    
    df = pd.DataFrame(data)
    df.rename(columns={"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)
    return df
```
## 🗃 **Teste 3 - Banco de Dados e Análise de Dados**

### 🎯 **Objetivos**
1. Estruturar e popular banco de dados com informações das operadoras
2. Realizar análises sobre despesas médicas
3. Identificar as 10 operadoras com maiores gastos em sinistros hospitalares

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
