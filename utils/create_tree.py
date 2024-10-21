"""
create_tree.py

Este módulo contém uma função para criar uma estrutura de diretórios e arquivos
baseada em uma lista de caminhos de arquivo, excluindo certas pastas especificadas.

Funções:
    create_file_structure(files: List[str], exclude_folders: List[str] = None) -> Dict[str, Any]:
        Cria uma estrutura de diretórios e arquivos baseada na lista de arquivos fornecida,
        excluindo as pastas especificadas.

Exemplo de uso:
    from create_tree import create_file_structure

    files = ['dir1/file1.txt', 'dir1/subdir/file2.txt', 'dir2/file3.txt', 'node_modules/package.json']
    exclude_folders = ['node_modules', 'dist', 'venv', 'examples']
    structure = create_file_structure(files, exclude_folders)
    print(structure)

    # Saída:
    # {
    #     'dir1': {
    #         'files': ['file1.txt'],
    #         'subdir': {
    #             'files': ['file2.txt']
    #         }
    #     },
    #     'dir2': {
    #         'files': ['file3.txt']
    #     }
    # }
"""

import os
from typing import List, Dict, Any

def create_file_structure(files: List[str], exclude_folders: List[str] = None) -> Dict[str, Any]:
    """
    Cria uma estrutura de diretórios e arquivos baseada na lista de arquivos fornecida,
    excluindo as pastas especificadas.

    Args:
        files (List[str]): Uma lista de strings, onde cada string é o caminho de um arquivo.
        exclude_folders (List[str], optional): Uma lista de nomes de pastas a serem excluídas.

    Returns:
        Dict[str, Any]: Um dicionário representando a estrutura de diretórios e arquivos.
    """
    if exclude_folders is None:
        exclude_folders = []

    result = {}
    for file_path in files:
        parts = file_path.split(os.sep)
        if any(folder in parts for folder in exclude_folders):
            continue

        current = result
        for part in parts[:-1]:
            if isinstance(current, list):
                # Se current é uma lista, transforme-o em um dicionário
                current = {'files': current}
            if part not in current:
                current[part] = {}
            current = current[part]
        if isinstance(current, dict):
            current.setdefault('files', []).append(parts[-1])
        elif isinstance(current, list):
            current.append(parts[-1])
        else:
            # Se current não é nem dict nem list, crie uma nova lista
            current = [parts[-1]]
    return result