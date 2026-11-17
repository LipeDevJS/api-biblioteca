"""Serviço (regras de negócio) do acervo.

Fica entre a API e o repositório. Não conhece HTTP: sinaliza problemas
com exceções do próprio domínio, que a camada da API traduz para HTTP.
"""

import livro_repositorio  # Centraliza o acesso aos dados do acervo.
from modelos import Livro  # Tipo retornado pelas consultas.


class LivroNaoEncontrado(Exception):
    """Erro de domínio: não existe livro com o identificador informado.

    Não depende do FastAPI de propósito; assim o serviço pode ser reutilizado
    em outros contextos (scripts, testes, outra interface) sem mudanças.
    """

    def __init__(self, livro_id: int) -> None:
        self.livro_id = livro_id  # Guarda o id para diagnóstico/log.
        super().__init__(f"Livro {livro_id} não encontrado")


def listar_livros() -> list[Livro]:
    """Retorna o acervo completo. Acervo vazio resulta em lista vazia (não é erro)."""
    return livro_repositorio.listar_todos()


def consultar_livro(livro_id: int) -> Livro:
    """Retorna o livro pelo id ou lança LivroNaoEncontrado se ele não existir."""
    livro = livro_repositorio.buscar_por_id(livro_id)
    if livro is None:  # Ausência é tratada como erro de domínio.
        raise LivroNaoEncontrado(livro_id)
    return livro
