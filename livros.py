"""Camada da API (HTTP) do acervo da biblioteca.

Responsável apenas por: receber a requisição, validar o identificador da URL,
chamar o serviço e converter o resultado (ou o erro) em resposta HTTP.
"""

from typing import Annotated  # Associa o tipo à validação do parâmetro.

from fastapi import FastAPI, HTTPException, Path, status  # Recursos HTTP.

from modelos import Livro  # Contrato das respostas.
from servico_livros import LivroNaoEncontrado, consultar_livro, listar_livros

app = FastAPI(
    title="API da Biblioteca",
    description="Consulta ao acervo de livros da biblioteca.",
    version="1.0.0",
)


@app.get(
    "/livros",
    response_model=list[Livro],  # Garante que a resposta é uma lista de livros.
    status_code=status.HTTP_200_OK,
    summary="Lista todos os livros do acervo",
)
def obter_livros() -> list[Livro]:
    # Acervo vazio retorna [] com status 200: "nenhum livro" não é um erro.
    return listar_livros()


@app.get(
    "/livros/{livro_id}",
    response_model=Livro,  # Define o formato do JSON de resposta.
    status_code=status.HTTP_200_OK,
    summary="Consulta um livro pelo identificador",
    responses={404: {"description": "Livro não encontrado"}},
)
def obter_livro(
    # Path(gt=0): o FastAPI responde 422 automaticamente se o id for
    # zero, negativo ou não for um número inteiro (ex.: "abc").
    livro_id: Annotated[int, Path(gt=0, description="Identificador do livro (inteiro > 0)")],
) -> Livro:
    try:
        return consultar_livro(livro_id)  # Delega a consulta ao serviço.
    except LivroNaoEncontrado as erro:
        # Conversão do erro de domínio em HTTP fica SOMENTE nesta camada.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # id válido, mas inexistente.
            detail="Livro não encontrado",  # Mensagem pública para o cliente.
        ) from erro  # Preserva a causa original para diagnóstico.
