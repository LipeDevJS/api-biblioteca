"""Modelos de dados (contratos) da API da biblioteca.

Este módulo define apenas a ESTRUTURA e as REGRAS DE VALIDAÇÃO dos dados.
Ele não sabe onde os livros estão guardados nem como chegam via HTTP.
"""

from pydantic import BaseModel, Field  # Modelos e regras de validação.


class Livro(BaseModel):  # Contrato dos dados de um livro do acervo.
    # strict=True impede conversões implícitas (ex.: "1" virar 1),
    # garantindo que o acervo só tenha dados do tipo correto.
    id: int = Field(gt=0, strict=True, description="Identificador positivo do livro")

    # min_length=1 rejeita textos vazios; str_strip_whitespace (abaixo)
    # remove espaços nas pontas antes da validação, então "   " também é rejeitado.
    titulo: str = Field(min_length=1, description="Título do livro (não pode ser vazio)")
    autor: str = Field(min_length=1, description="Autor do livro (não pode ser vazio)")

    ano_publicacao: int = Field(gt=0, strict=True, description="Ano de publicação (maior que zero)")

    # strict=True evita que valores como "sim" ou 1 sejam aceitos como booleano.
    disponivel: bool = Field(strict=True, description="Indica se está disponível para empréstimo")

    # Configuração do modelo: remove espaços extras das strings automaticamente.
    model_config = {"str_strip_whitespace": True}
