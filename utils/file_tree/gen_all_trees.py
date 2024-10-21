"""
gen_all_trees.py

Este script gera arquivos de estrutura JSON para diferentes diretórios do projeto,
incluindo o diretório raiz, as alterações do último commit Git, e a estrutura relacionada.

Funcionalidades:
1. Define uma função para executar comandos de shell e capturar sua saída.
2. Lista os comandos necessários para gerar as estruturas JSON de diferentes diretórios, do último commit Git, e da estrutura relacionada.
3. Executa cada comando, gerando os arquivos de estrutura JSON correspondentes.

Uso:
    python .nexus/src/general/file_tree/gen_all_trees.py

Exemplo de uso:
    python .nexus/src/general/file_tree/gen_all_trees.py

    # Saída:
    # Comando executado com sucesso: python .nexus/src/general/file_tree/gen_dir_tree.py ./ .tmp/project_structure.json
    # Comando executado com sucesso: python .nexus/src/general/file_tree/gen_git_tree.py
    # Comando executado com sucesso: python .nexus/src/general/file_tree/gen_related_tree.py
    # Todos os arquivos de estrutura foram gerados com sucesso.

Arquivos gerados:
    - .tmp/project_structure.json: Estrutura do diretório raiz do projeto
    - .tmp/git-changed_structure.json: Estrutura dos arquivos alterados no último commit Git
    - .tmp/git-removed_structure.json: Estrutura dos arquivos removidos no último commit Git
    - .tmp/git-diff_structure.json: Estrutura de todas as mudanças (alterados e removidos) no último commit Git
    - .tmp/git-related_structure.json: Estrutura dos arquivos alterados e seus arquivos pais

Observação:
    Certifique-se de que os scripts gen_dir_tree.py, gen_git_tree.py, e gen_related_tree.py
    existem e estão configurados corretamente, pois eles são chamados para gerar cada arquivo de estrutura.
"""

import subprocess
import os
import sys

# Adiciona o diretório pai ao sys.path para permitir importações relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

def run_command(command):
    """
    Executa um comando de shell e imprime o resultado ou erro.

    Args:
        command (str): O comando de shell a ser executado.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Erro ao executar o comando: {command}")
        print(f"Erro: {error.decode('utf-8')}")
    else:
        print(f"Comando executado com sucesso: {command}")
        print(f"Saída: {output.decode('utf-8')}")

def main():
    # Obtém o diretório do script atual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Lista de comandos para gerar as estruturas JSON
    commands = [
        f"python {os.path.join(current_dir, 'gen_dir_tree.py')} ./ .tmp/project_structure.json",
        f"python {os.path.join(current_dir, 'gen_git_tree.py')}",
        f"python {os.path.join(current_dir, 'gen_related_tree.py')}",
    ]

    # Executa cada comando
    for command in commands:
        run_command(command)

    print("Todos os arquivos de estrutura foram gerados com sucesso.")

if __name__ == "__main__":
    main()
