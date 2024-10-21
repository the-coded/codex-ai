"""
git_changes.py

Este módulo contém funções para obter informações sobre as mudanças no último commit do Git,
separando os arquivos alterados e removidos.

Funções:
    get_git_changes() -> Tuple[List[str], List[str]]:
        Retorna duas listas: uma com os arquivos alterados e outra com os arquivos removidos no último commit.

Exemplo de uso:
    from utils.git_changes import get_git_changes

    changed_files, removed_files = get_git_changes()
    print("Arquivos alterados:", changed_files)
    print("Arquivos removidos:", removed_files)
"""

import subprocess
from typing import List, Tuple

def get_git_changes() -> Tuple[List[str], List[str]]:
    """
    Obtém as mudanças do último commit do Git, separando os arquivos alterados e removidos.

    Returns:
        Tuple[List[str], List[str]]: Uma tupla contendo duas listas:
            - A primeira lista contém os caminhos dos arquivos alterados.
            - A segunda lista contém os caminhos dos arquivos removidos.

    Raises:
        subprocess.CalledProcessError: Se ocorrer um erro ao executar o comando git.
    """
    try:
        # Obtém as mudanças do último commit
        result = subprocess.run(['git', 'show', '--name-status', '--format=', 'HEAD'],
                                capture_output=True, text=True, check=True)
        
        changed_files = []
        removed_files = []

        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    status, file_path = parts[0], parts[-1]
                    if status == 'D':
                        removed_files.append(file_path)
                    else:
                        changed_files.append(file_path)

        return changed_files, removed_files

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando git: {e}")
        return [], []