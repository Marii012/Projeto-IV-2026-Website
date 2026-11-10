from django.db import models

class PedidoContacto(models.Model):
    nome = models.CharField(max_length=120)
    laboratorio = models.CharField(max_length=160)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True)
    mensagem = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Pedido de contacto'
        verbose_name_plural = 'Pedidos de contacto'

    def __str__(self):
        return f'{self.nome} — {self.laboratorio}'
