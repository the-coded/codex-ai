"""
gen_git_tree.py

Este script cria arquivos JSON contendo a estrutura de diretórios e arquivos
que foram alterados e removidos no último commit do repositório Git.

Funcionalidades:
1. Obtém a lista de arquivos alterados e removidos no último commit usando o comando git.
2. Cria estruturas de diretórios e arquivos baseadas nas alterações.
3. Salva as estruturas em arquivos JSON separados.

Uso:
    python .nexus/src/general/file_tree/gen_git_tree.py [caminho_alterados] [caminho_removidos] [caminho_diff]

    Se nenhum caminho for especificado, os arquivos serão salvos em:
    - .tmp/git-changed_structure.json (para arquivos alterados)
    - .tmp/git-removed_structure.json (para arquivos removidos)
    - .tmp/git-diff_structure.json (para todas as mudanças)

Exemplos de uso:
    # Usando os caminhos de saída padrão
    python .nexus/src/general/file_tree/gen_git_tree.py

    # Especificando caminhos de saída personalizados
    python .nexus/src/general/file_tree/gen_git_tree.py .tmp/custom-changed.json .tmp/custom-removed.json .tmp/custom-diff.json

Observação:
    Certifique-se de executar este script na raiz do repositório Git.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.utils.git_changes import get_git_changes
from src.utils.create_tree import create_file_structure
from src.utils.save_tree_to_json import save_structure_to_json

def main():
    default_output_changed = '.tmp/git-changed_structure.json'
    default_output_removed = '.tmp/git-removed_structure.json'
    default_output_diff = '.tmp/git-diff_structure.json'
    
    if len(sys.argv) > 4:
        print(f"Uso: python {sys.argv[0]} [caminho_alterados] [caminho_removidos] [caminho_diff]")
        print(f"Se nenhum caminho for especificado, os arquivos serão salvos em {default_output_changed}, {default_output_removed} e {default_output_diff}")
        sys.exit(1)

    output_changed = sys.argv[1] if len(sys.argv) > 1 else default_output_changed
    output_removed = sys.argv[2] if len(sys.argv) > 2 else default_output_removed
    output_diff = sys.argv[3] if len(sys.argv) > 3 else default_output_diff

    changed_files, removed_files = get_git_changes()

    changed_structure = create_file_structure(changed_files)
    removed_structure = create_file_structure(removed_files)
    diff_structure = create_file_structure(changed_files + removed_files)

    save_structure_to_json(changed_structure, output_changed)
    save_structure_to_json(removed_structure, output_removed)
    save_structure_to_json(diff_structure, output_diff)

if __name__ == "__main__":
    main()
