"""
list_files.py

Este módulo contém uma função para listar todos os arquivos em um diretório e seus subdiretórios.

Funções:
    list_files(start_path: str) -> List[str]:
        Lista todos os arquivos e diretórios a partir do caminho especificado.

Exemplo de uso:
    from list_files import list_files

    start_path = '/caminho/para/diretorio'
    files = list_files(start_path)
    for file in files:
        print(file)

    # Saída (exemplo):
    # arquivo1.txt
    # subdiretorio/arquivo2.py
    # subdiretorio/arquivo3.json
"""

import os
from typing import List

def list_files(start_path: str) -> List[str]:
    """
    Lista todos os arquivos e diretórios a partir do caminho especificado.

    Args:
        start_path (str): O caminho do diretório a ser analisado.

    Returns:
        List[str]: Uma lista de caminhos de arquivos relativos ao start_path.
    """
    file_list = []
    for root, _, files in os.walk(start_path):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), start_path)
            file_list.append(file_path)
    return file_list