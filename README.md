# API da Biblioteca (FastAPI)

API para consulta ao acervo de uma biblioteca, desenvolvida em Python com FastAPI.
Permite listar todos os livros ou buscar um livro pelo identificador.

## Estrutura do projeto (separação de responsabilidades)

| Arquivo | Camada | Responsabilidade |
|---|---|---|
| `modelos.py` | Modelo | Define o contrato `Livro` e valida os campos (Pydantic). |
| `livro_repositorio.py` | Repositório | Único lugar que acessa a coleção de livros (em memória). |
| `servico_livros.py` | Serviço | Regras de consulta e a exceção de domínio `LivroNaoEncontrado`. |
| `livros.py` | API | Rotas HTTP, validação do id da URL e conversão da exceção em HTTP 404. |
| `test_livros.py` | Testes | Testes automatizados das rotas e das validações. |

Fluxo de uma requisição: `livros.py` (API) → `servico_livros.py` (serviço) → `livro_repositorio.py` (dados).

## Modelo `Livro`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | inteiro | maior que zero |
| `titulo` | texto | não pode ser vazio |
| `autor` | texto | não pode ser vazio |
| `ano_publicacao` | inteiro | maior que zero |
| `disponivel` | booleano | disponível para empréstimo |

## Como executar

Requisito: Python 3.10 ou superior.

1. Abrir o terminal na pasta do projeto.
2. Criar o ambiente virtual (apenas na primeira vez):
   ```bash
   python -m venv .venv
   ```
3. Ativar o ambiente virtual:
   - Windows: `.venv\Scripts\activate.bat` (no PowerShell: `.venv\Scripts\Activate.ps1`)
   - Linux ou Mac: `source .venv/bin/activate`
4. Instalar as dependências (apenas na primeira vez):
   ```bash
   pip install -r requirements.txt
   ```
5. Iniciar a API:
   ```bash
   python -m uvicorn livros:app --host 127.0.0.1 --port 8001 --reload
   ```
6. Acessar no navegador:
   - Lista de livros: http://127.0.0.1:8001/livros
   - Um livro: http://127.0.0.1:8001/livros/1
   - Documentação interativa (Swagger): http://127.0.0.1:8001/docs

## Rotas

### `GET /livros`
Retorna `200` com a lista de livros. Se o acervo estiver vazio, retorna `200` com `[]`.

### `GET /livros/{livro_id}`

| Situação | Exemplo | Status |
|---|---|---|
| Livro encontrado | `/livros/1` | `200` |
| Id válido, mas inexistente | `/livros/999` | `404` – `{"detail": "Livro não encontrado"}` |
| Id inválido (zero, negativo ou texto) | `/livros/0`, `/livros/-1`, `/livros/abc` | `422` |

Exemplo de resposta (`/livros/1`):
```json
{
  "id": 1,
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano_publicacao": 1899,
  "disponivel": true
}
```

## Decisões de implementação

- **Repositório isolado:** a coleção `_LIVROS` é privada do módulo `livro_repositorio.py`; as demais camadas usam apenas `listar_todos()` e `buscar_por_id()`. Trocar a memória por um banco de dados exigiria mudar só esse arquivo.
- **Cópias dos objetos:** o repositório devolve cópias (`model_copy()`) para que ninguém altere o acervo por acidente.
- **Exceção de domínio sem HTTP:** `LivroNaoEncontrado` não depende do FastAPI; a conversão para `404` acontece apenas em `livros.py`.
- **Validação do id na URL:** `Path(gt=0)` faz o FastAPI responder `422` automaticamente para zero, negativos e textos.
- **Validação do modelo:** `strict=True` evita conversões implícitas (ex.: `"sim"` como booleano) e `str_strip_whitespace` faz textos só com espaços serem rejeitados.
- **Modelos de resposta:** cada rota declara `response_model`, o que garante o formato do JSON e documenta a API no `/docs`.

## Testes automatizados

Com o ambiente virtual ativado:
```bash
python -m pytest -v
```
