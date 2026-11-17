"""Repositório de livros: ÚNICA camada que acessa a coleção do acervo.

Se no futuro o acervo passar para um banco de dados, apenas este arquivo
precisará mudar; o serviço e a API continuam iguais.
"""

from modelos import Livro  # Modelo usado para representar cada livro.

# Acervo didático armazenado em memória.
# O "_" no início indica que a variável é privada deste módulo:
# os demais arquivos devem usar as funções abaixo, nunca o dicionário direto.
# Usamos um dicionário indexado pelo id para a busca ser direta (O(1)).
_LIVROS: dict[int, Livro] = {
    1: Livro(id=1, titulo="Dom Casmurro", autor="Machado de Assis", ano_publicacao=1899, disponivel=True),
    2: Livro(id=2, titulo="O Cortiço", autor="Aluísio Azevedo", ano_publicacao=1890, disponivel=False),
    3: Livro(id=3, titulo="Vidas Secas", autor="Graciliano Ramos", ano_publicacao=1938, disponivel=True),
    4: Livro(id=4, titulo="Grande Sertão: Veredas", autor="João Guimarães Rosa", ano_publicacao=1956, disponivel=True),
    5: Livro(id=5, titulo="A Hora da Estrela", autor="Clarice Lispector", ano_publicacao=1977, disponivel=False),
    6: Livro(id=6, titulo="Capitães da Areia", autor="Jorge Amado", ano_publicacao=1937, disponivel=True),
}


def listar_todos() -> list[Livro]:
    """Retorna todos os livros do acervo (lista vazia se não houver nenhum)."""
    # Devolvemos CÓPIAS para que quem chamou não altere os objetos guardados.
    return [livro.model_copy() for livro in _LIVROS.values()]


def buscar_por_id(livro_id: int) -> Livro | None:
    """Retorna o livro com o id informado ou None se ele não existir."""
    livro = _LIVROS.get(livro_id)  # None indica ausência.
    # A cópia impede que o chamador altere o objeto guardado no acervo.
    return livro.model_copy() if livro is not None else None
