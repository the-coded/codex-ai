"""
gen_dir_tree.py

Este script cria um arquivo JSON contendo a estrutura de diretórios e arquivos
de um diretório especificado, excluindo certas pastas.

Funcionalidades:
1. Percorre recursivamente o diretório especificado.
2. Cria uma estrutura de diretórios e arquivos, excluindo pastas especificadas.
3. Salva a estrutura em um arquivo JSON.

Uso:
    python .nexus/src/general/file_tree/gen_dir_tree.py <start_path> <output_file>

Exemplos de uso:
    # Gerar estrutura para o diretório raiz do projeto
    python .nexus/src/general/file_tree/gen_dir_tree.py ./ .tmp/project_structure.json

    # Gerar estrutura para o diretório react/src
    python .nexus/src/general/file_tree/gen_dir_tree.py react/src .tmp/react_structure.json

    # Gerar estrutura para o diretório docs
    python .nexus/src/general/file_tree/gen_dir_tree.py docs .tmp/docs_structure.json

    # Gerar estrutura para o diretório sass/src
    python .nexus/src/general/file_tree/gen_dir_tree.py sass/src .tmp/sass_structure.json

    # Exemplo genérico
    python .nexus/src/general/file_tree/gen_dir_tree.py /caminho/para/diretorio output.json

    # Saída para cada exemplo:
    # Estrutura de diretórios salva em .tmp/project_structure.json
    # Estrutura de diretórios salva em .tmp/react_structure.json
    # Estrutura de diretórios salva em .tmp/docs_structure.json
    # Estrutura de diretórios salva em .tmp/sass_structure.json
    # Estrutura de diretórios salva em output.json

Observação:
    O <start_path> deve ser um diretório válido.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.list_files import list_files
from utils.create_tree import create_file_structure
from utils.save_tree_to_json import save_structure_to_json

# Lista de pastas a serem excluídas
EXCLUDE_FOLDERS = [
                    'dist', 
                    'node_modules', 
                    'venv', 
                    'examples', 
                    '.git', 
                    '.vscode', 
                    '.tmp', 
                    '.github', 
                    '.aider.tags.cache.v3'
                ]

def main():
    if len(sys.argv) != 3:
        print(f"Uso: python {sys.argv[0]} <start_path> <output_file>")
        sys.exit(1)

    start_path = sys.argv[1]
    output_file = sys.argv[2]

    # Converter o caminho relativo para absoluto
    start_path = os.path.abspath(start_path)

    if not os.path.isdir(start_path):
        print(f"Erro: {start_path} não é um diretório válido.")
        sys.exit(1)

    files = list_files(start_path)
    file_structure = create_file_structure(files, EXCLUDE_FOLDERS)
    save_structure_to_json(file_structure, output_file)
    print(f"Estrutura de diretórios salva em {output_file}")

if __name__ == "__main__":
    main()
