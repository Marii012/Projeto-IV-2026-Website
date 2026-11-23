"""Operações de negócio que envolvem várias tabelas (numa só transação)."""
from fastapi import HTTPException

from app.config import ESTADO_ATIVO, ESTADO_PENDENTE, TIPO_CLIENTE, TIPO_COLABORADOR
from app.repositories import cliente, morada, utilizador


def _erro(msg):
    return HTTPException(status_code=400, detail=msg)


def validar_registo(d):
    nome, email = d.nome.strip(), d.email.strip()
    telefone, nif = d.telefone.strip(), d.nif.strip()
    moradas = [m.strip() for m in d.moradas if m and m.strip()]

    if not nome or not email or not telefone or not nif:
        raise _erro("Preenche todos os campos obrigatórios.")
    if len(email) > 150:
        raise _erro("O email não pode ultrapassar 150 caracteres.")
    if len(telefone) > 20:
        raise _erro("O telefone não pode ultrapassar 20 algarismos.")
    if not d.password or not d.confirmar_password:
        raise _erro("Preenche os campos da palavra-passe.")
    if d.password != d.confirmar_password:
        raise _erro("As palavras-passe não coincidem.")
    if len(d.password) < 8:
        raise _erro("A palavra-passe deve ter pelo menos 8 caracteres.")
    if not nif.isdigit() or len(nif) != 9:
        raise _erro("O NIF deve conter exatamente 9 algarismos.")
    if not moradas:
        raise _erro("Adiciona pelo menos uma morada.")
    if len(moradas) > 4:
        raise _erro("Podes adicionar no máximo 4 moradas.")
    return nome, email, telefone, nif, moradas


def registar_cliente(cur, d):
    """Registo público: utilizador + cliente + moradas. Fica pendente de aprovação."""
    nome, email, telefone, nif, moradas = validar_registo(d)

    id_utilizador = utilizador.inserir(
        cur, nome, email, d.password, None, TIPO_CLIENTE, ESTADO_PENDENTE)
    c = cliente.tabela.inserir(cur, {
        "nome": nome, "nif": nif, "telefone": telefone,
        "data_aprovacao": None, "id_utilizador": id_utilizador})
    for m in moradas:
        morada.tabela.inserir(cur, {
            "nome_clinica": nome, "morada": m, "id_cliente": c["id"]})
    return id_utilizador


def criar_utilizador_admin(cur, d):
    """Criação de cliente ou colaborador por um administrador (conta ativa)."""
    nome, email = d.nome.strip(), d.email.strip()
    if d.tipo not in ("cliente", "colaborador"):
        raise _erro("Tipo de utilizador inválido.")
    if not nome or not email:
        raise _erro("Preenche todos os campos obrigatórios.")

    if d.tipo == "cliente":
        nif = (d.nif or "").strip()
        telefone = (d.telefone or "").strip()
        morada_txt = (d.morada or "").strip()
        if not nif or not telefone or not morada_txt:
            raise _erro("Preenche o NIF, telefone e morada.")
        if not nif.isdigit():
            raise _erro("O NIF só pode conter algarismos.")
        if len(nif) != 9:
            raise _erro("O NIF deve conter exatamente 9 algarismos.")
        if not telefone.isdigit():
            raise _erro("O telefone só pode conter algarismos.")
        if len(telefone) > 20:
            raise _erro("O telefone não pode ultrapassar 20 algarismos.")

    id_tipo = TIPO_CLIENTE if d.tipo == "cliente" else TIPO_COLABORADOR
    id_utilizador = utilizador.inserir(
        cur, nome, email, None, None, id_tipo, ESTADO_ATIVO)

    if d.tipo == "cliente":
        c = cliente.tabela.inserir(cur, {
            "nome": nome, "nif": nif, "telefone": telefone,
            "data_aprovacao": None, "id_utilizador": id_utilizador})
        morada.tabela.inserir(cur, {
            "nome_clinica": nome, "morada": morada_txt, "id_cliente": c["id"]})
    return id_utilizador
