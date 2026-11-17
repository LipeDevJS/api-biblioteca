"""Testes automatizados da API. Execute com: python -m pytest"""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import livro_repositorio
from livros import app
from modelos import Livro

cliente = TestClient(app)


def test_listar_livros_retorna_200_e_lista():
    resposta = cliente.get("/livros")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
    assert len(resposta.json()) >= 5  # Requisito: pelo menos cinco livros.


def test_listar_livros_acervo_vazio_retorna_lista_vazia(monkeypatch):
    # Simula um acervo vazio sem alterar o código da aplicação.
    monkeypatch.setattr(livro_repositorio, "_LIVROS", {})
    resposta = cliente.get("/livros")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_consultar_livro_existente_retorna_200():
    resposta = cliente.get("/livros/1")
    assert resposta.status_code == 200
    assert resposta.json() == {
        "id": 1,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano_publicacao": 1899,
        "disponivel": True,
    }


def test_consultar_livro_inexistente_retorna_404():
    resposta = cliente.get("/livros/999")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Livro não encontrado"}


@pytest.mark.parametrize("id_invalido", ["0", "-1", "abc", "1.5"])
def test_consultar_livro_com_id_invalido_retorna_422(id_invalido):
    resposta = cliente.get(f"/livros/{id_invalido}")
    assert resposta.status_code == 422


@pytest.mark.parametrize(
    "dados",
    [
        {"id": 0, "titulo": "X", "autor": "Y", "ano_publicacao": 2000, "disponivel": True},
        {"id": 1, "titulo": "", "autor": "Y", "ano_publicacao": 2000, "disponivel": True},
        {"id": 1, "titulo": "X", "autor": "   ", "ano_publicacao": 2000, "disponivel": True},
        {"id": 1, "titulo": "X", "autor": "Y", "ano_publicacao": 0, "disponivel": True},
        {"id": 1, "titulo": "X", "autor": "Y", "ano_publicacao": 2000, "disponivel": "sim"},
    ],
)
def test_modelo_livro_rejeita_dados_invalidos(dados):
    with pytest.raises(ValidationError):
        Livro(**dados)
