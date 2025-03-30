import os
import zipfile
import pandas as pd
import pdfplumber
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Converts a PDF table to CSV and zips the output"
    HEADER_MAP = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial"
    }

    def add_arguments(self, parser):
        parser.add_argument('--input', type=str, required=True,
                            help='Caminho do arquivo de entrada')
        parser.add_argument('--output', type=str, required=True,
                            help='Nome do arquivo de saída (sem extensão)')

    def handle(self, *args, **options):
        input_path = options['input']
        output_filename = options['output']

        if not os.path.exists(input_path):
            self.stderr.write(self.style.ERROR(
                f"O arquivo {input_path} não existe."))
            return

        df = self.extract_tables_from_pdf(input_path)
        csv_path = f"{output_filename}.csv"
        df.to_csv(csv_path, index=False, header=False,
                  encoding='utf-8', sep=';')

        zip_path = f"{output_filename}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))

        os.remove(csv_path)
        self.stdout.write(self.style.SUCCESS(
            f"Arquivo zipado gerado: {zip_path}"))

    def extract_tables_from_pdf(self, file_path):
        data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_table()
                if tables:
                    for row in tables:

                        clean_row = [
                            cell for cell in row if cell and not cell.isdigit()]
                        data.append(clean_row)

        df = pd.DataFrame(data)
        df.rename(columns=self.HEADER_MAP, inplace=True)
        return df
