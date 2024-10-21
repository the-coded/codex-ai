"""
load_json.py

Este módulo contém uma função para carregar arquivos JSON.

Funções:
    load_json(file_path: str) -> Dict[str, Any]:
        Carrega um arquivo JSON e retorna seu conteúdo como um dicionário.

Exemplo de uso:
    from utils.load_json import load_json

    json_data = load_json('caminho/para/arquivo.json')
    print(json_data)
"""

import json
from typing import Dict, Any

def load_json(file_path: str) -> Dict[str, Any]:
    """
    Carrega um arquivo JSON e retorna seu conteúdo como um dicionário.

    Args:
        file_path (str): O caminho para o arquivo JSON a ser carregado.

    Returns:
        Dict[str, Any]: O conteúdo do arquivo JSON como um dicionário.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        json.JSONDecodeError: Se o arquivo não for um JSON válido.
    """
    with open(file_path, 'r') as file:
        return json.load(file)