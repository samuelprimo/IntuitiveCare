from django.db import models


class Operadora(models.Model):
    registro_ans = models.BigIntegerField(primary_key=True)
    cnpj = models.CharField(max_length=18)
    razao_social = models.TextField()
    nome_fantasia = models.TextField(null=True, blank=True)
    modalidade = models.TextField()
    logradouro = models.TextField()
    numero = models.CharField(max_length=50)
    complemento = models.TextField(null=True, blank=True)
    bairro = models.TextField()
    cidade = models.TextField()
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    ddd = models.CharField(max_length=3)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    endereco_eletronico = models.EmailField(null=True, blank=True)
    representante = models.TextField()
    cargo_representante = models.TextField()
    regiao_de_comercializacao = models.IntegerField(null=True, blank=True)
    data_registro_ans = models.DateField()

    def __str__(self):
        return self.razao_social


class DemonstracaoContabil(models.Model):
    data = models.DateField()
    registro_ans = models.BigIntegerField(db_index=True)
    cd_conta_contabil = models.BigIntegerField()
    descricao = models.CharField(max_length=150, db_index=True)
    vl_saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2)
    vl_saldo_final = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.descricao
