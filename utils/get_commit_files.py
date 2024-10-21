"""
get_commit_files.py

Este módulo contém uma função para obter a lista de arquivos alterados
no último commit do repositório Git.

Funções:
    get_last_commit_files() -> List[str]:
        Obtém a lista de arquivos alterados no último commit do repositório Git.

Exemplo de uso:
    from get_commit_files import get_last_commit_files

    try:
        changed_files = get_last_commit_files()
        print("Arquivos alterados no último commit:")
        for file in changed_files:
            print(f"- {file}")
    except SystemExit:
        print("Não foi possível obter a lista de arquivos do último commit.")

    # Saída (exemplo):
    # Arquivos alterados no último commit:
    # - path/to/file1.py
    # - path/to/file2.txt
"""

import subprocess
import sys
from typing import List

def get_last_commit_files() -> List[str]:
    """
    Obtém a lista de arquivos alterados no último commit do repositório Git.

    Returns:
        List[str]: Uma lista de strings, onde cada string é o caminho de um arquivo alterado.

    Raises:
        SystemExit: Se não for possível obter a lista de arquivos do último commit.
    """
    try:
        result = subprocess.run(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        print("Erro: Não foi possível obter a lista de arquivos do último commit.")
        sys.exit(1)