"""
gen_related_tree.py

Este script cria um arquivo JSON contendo a estrutura de arquivos relacionados
aos arquivos alterados, baseando-se na estrutura completa do projeto.

Funcionalidades:
1. Lê a estrutura de arquivos alterados do .tmp/git-changed_structure.json.
2. Lê a estrutura completa do projeto do .tmp/project_structure.json.
3. Para cada arquivo alterado, inclui todos os arquivos do mesmo diretório na estrutura do projeto.
4. Salva a nova estrutura em .tmp/git-related_structure.json.

Uso:
    python .nexus/src/general/file_tree/gen_related_tree.py

Exemplo de uso:
    python .nexus/src/general/file_tree/gen_related_tree.py

    # Saída:
    # Estrutura de arquivos relacionados salva em .tmp/git-related_structure.json

Observação:
    Certifique-se de que os arquivos .tmp/git-changed_structure.json e
    .tmp/project_structure.json existem antes de executar este script.
"""

import json
from typing import Dict, Any, List
import os
import sys

# Adiciona o diretório pai ao sys.path para permitir importações relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.utils.load_json import load_json
from src.utils.save_tree_to_json import save_structure_to_json

def find_related_files(structure: Dict[str, Any], target_file: str, current_path: List[str] = []) -> List[str]:
    """
    Encontra todos os arquivos relacionados a um arquivo alvo na estrutura do projeto.

    Args:
        structure (Dict[str, Any]): A estrutura do projeto.
        target_file (str): O arquivo alvo.
        current_path (List[str]): O caminho atual na estrutura (usado para recursão).

    Returns:
        List[str]: Lista de arquivos relacionados.
    """
    for key, value in structure.items():
        if key == "files" and target_file in value:
            return value
        elif isinstance(value, dict):
            result = find_related_files(value, target_file, current_path + [key])
            if result:
                return result
    return []

def create_related_structure(changed_structure: Dict[str, Any], project_structure: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cria uma nova estrutura incluindo todos os arquivos relacionados aos arquivos alterados.

    Args:
        changed_structure (Dict[str, Any]): A estrutura de arquivos alterados.
        project_structure (Dict[str, Any]): A estrutura completa do projeto.

    Returns:
        Dict[str, Any]: A nova estrutura com arquivos relacionados.
    """
    related_structure = {}

    def process_structure(structure: Dict[str, Any], current_path: List[str] = []):
        for key, value in structure.items():
            if key == "files":
                for file in value:
                    related_files = find_related_files(project_structure, file)
                    if related_files:
                        current = related_structure
                        for folder in current_path:
                            current = current.setdefault(folder, {})
                        current["files"] = related_files
            elif isinstance(value, dict):
                process_structure(value, current_path + [key])

    process_structure(changed_structure)
    return related_structure

def main():
    changed_structure = load_json('.tmp/git-changed_structure.json')
    project_structure = load_json('.tmp/project_structure.json')

    related_structure = create_related_structure(changed_structure, project_structure)
    save_structure_to_json(related_structure, '.tmp/git-related_structure.json')

if __name__ == "__main__":
    main()
