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
