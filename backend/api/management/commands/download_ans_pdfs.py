import requests
from bs4 import BeautifulSoup
import zipfile
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Baixa todos os PDFs de uma URL especificada e salva em um arquivo ZIP'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            required=True,
            help='URL para buscar os PDFs (obrigatório)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='Anexos.zip',
            help='Nome do arquivo ZIP de saída (padrão: Anexos.zip)'
        )

    def handle(self, *args, **options):
        url_alvo = options['url']
        arquivo_saida = options['output']

        try:
            self.stdout.write(self.style.SUCCESS(
                f'Iniciando download de PDFs de {url_alvo}...'))

            dir_temp = os.path.join(settings.BASE_DIR, 'pdfs_temporarios')
            os.makedirs(dir_temp, exist_ok=True)

            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                resposta = requests.get(url_alvo, headers=headers)
                resposta.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro ao acessar {url_alvo}: {e}")
                raise

            soup = BeautifulSoup(resposta.text, 'html.parser')

            links_pdf = [
                a['href'] for a in soup.find_all('a', href=True)
                if a['href'].lower().endswith('.pdf')
            ]

            if not links_pdf:
                self.stdout.write(self.style.WARNING(
                    'Nenhum link de PDF encontrado!'))
                return

            self.stdout.write(
                f'Encontrados {len(links_pdf)} arquivos PDF para download')

            arquivos_pdf = []
            for link in links_pdf:
                try:
                    nome_base = link.split('/')[-1]
                    nome_arquivo = os.path.join(dir_temp, nome_base)

                    contador = 1
                    while os.path.exists(nome_arquivo):
                        nome_arquivo = os.path.join(
                            dir_temp, f"{contador}_{nome_base}")
                        contador += 1

                    with open(nome_arquivo, 'wb') as f:
                        resposta = requests.get(link, headers=headers)
                        resposta.raise_for_status()
                        f.write(resposta.content)
                    arquivos_pdf.append(nome_arquivo)
                    self.stdout.write(f'Baixado: {nome_arquivo}')
                except Exception as e:
                    logger.error(f"Erro ao baixar {link}: {e}")
                    continue

            with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
                for arquivo in arquivos_pdf:
                    zipf.write(arquivo, os.path.basename(arquivo))

            self.stdout.write(self.style.SUCCESS(
                f'Arquivo ZIP criado com sucesso: {arquivo_saida}'))

            shutil.rmtree(dir_temp, ignore_errors=True)

        except Exception as e:
            logger.error(f"Ocorreu um erro: {e}")
            raise
