"""
save_tree_to_json.py

Este módulo contém uma função para salvar uma estrutura de arquivos em formato JSON.

Funções:
    save_structure_to_json(structure: Dict[str, Any], output_file: str) -> None:
        Salva a estrutura de arquivos em um arquivo JSON.

Exemplo de uso:
    from save_tree_to_json import save_structure_to_json

    structure = {
        'dir1': {
            'files': ['file1.txt'],
            'subdir': {
                'files': ['file2.txt']
            }
        },
        'dir2': {
            'files': ['file3.txt']
        }
    }
    save_structure_to_json(structure, 'output.json')

    # Saída:
    # Estrutura de arquivos salva em output.json
"""

import json
import os
from typing import Dict, Any

def save_structure_to_json(structure: Dict[str, Any], output_file: str) -> None:
    """
    Salva a estrutura de arquivos em um arquivo JSON.

    Args:
        structure (Dict[str, Any]): A estrutura de arquivos a ser salva.
        output_file (str): O caminho do arquivo de saída JSON.
    """
    # Cria o diretório de saída, se não existir
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(structure, f, indent=2)
    print(f"Estrutura de arquivos salva em {output_file}")