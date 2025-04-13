from django.db import models

class ProfissionalSaude(models.Model):
    nome_social = models.CharField(max_length=255)
    profissao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_social

class Consulta(models.Model):
    data = models.DateTimeField(max_length=255)
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.CASCADE, related_name='consultas')

    def __str__(self):
        return f"{self.profissional.nome_socil} - {self.data}"
