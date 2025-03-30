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

### **Teste 1 - Web Scraping**
```python
python manage.py download_pdfs --url "https://www.gov.br/ans/..." --output "Anexos.zip"

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
