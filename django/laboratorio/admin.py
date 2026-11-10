from django.contrib import admin
from .models import PedidoContacto

@admin.register(PedidoContacto)
class PedidoContactoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'laboratorio', 'email', 'telefone', 'criado_em')
    search_fields = ('nome', 'laboratorio', 'email')
    readonly_fields = ('criado_em',)
