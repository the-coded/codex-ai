# 🛠️ Scripts

Este diretório contém scripts utilitários para o projeto.

## ⚙️ Environment Setup

### 🐍 start.sh
Configura o ambiente Python, criando e ativando um ambiente virtual.

**Uso**:
```bash
source bin/start.sh
```

## 📝 Git Log Scripts

### 📋 git_log_detailed.sh
Script para visualizar log detalhado do último commit do Git, incluindo patches e informações completas.

**Output**: `.tmp/git_log_detailed.txt`

**Uso**:
```bash
./bin/git_log_detailed.sh
```

### 🔍 git_log_simple.sh
Script para visualizar log simplificado do último commit do Git, útil quando o log é muito grande.

**Output**: `.tmp/git_log_simple.txt`

**Uso**:
```bash
./bin/git_log_simple.sh
```

## 🌳 Tree Generation Scripts

### 🚀 tree_generate_all.sh
Script principal que executa todos os scripts de geração de estrutura na ordem correta:
1. tree_project.sh
2. tree_git_changes.sh
3. tree_git_siblings.sh

**Uso**:
```bash
./bin/tree_generate_all.sh
```

### 📂 tree_project.sh
Gera estrutura completa do projeto em JSON.

**Output**: `.tmp/tree_project.json`

**Uso**:
```bash
./bin/tree_project.sh <caminho_inicial> <arquivo_saida>
```

### 🔄 tree_git_changes.sh
Gera estrutura JSON das mudanças do Git.

**Output**:
- `.tmp/tree_git_changed.json`
- `.tmp/tree_git_removed.json`
- `.tmp/tree_git_all.json`

**Uso**:
```bash
./bin/tree_git_changes.sh
```

### 🔗 tree_git_siblings.sh
Gera estrutura JSON dos arquivos irmãos (no mesmo diretório) dos arquivos alterados.

**Dependências**:
- ⚡ Requer `tree_project.sh` executado antes (usa .tmp/tree_project.json)
- ⚡ Requer `tree_git_changes.sh` executado antes (usa .tmp/tree_git_changed.json)

**Output**: `.tmp/tree_git_siblings.json`

**Uso**:
```bash
./bin/tree_git_siblings.sh
```

## 📦 Outputs

Todos os arquivos gerados são salvos no diretório `.tmp/`:

### 📊 Git Logs
- `git_log_detailed.txt`: Log detalhado do último commit
- `git_log_simple.txt`: Log simplificado do último commit

### 🗂️ Tree Structures
- `tree_project.json`: Estrutura completa do projeto
- `tree_git_all.json`: Todas as mudanças do Git
- `tree_git_changed.json`: Arquivos alterados
- `tree_git_removed.json`: Arquivos removidos
- `tree_git_siblings.json`: Arquivos irmãos dos alterados

## 🔄 Ordem de Execução

Alguns scripts dependem dos outputs de outros scripts. Aqui está a ordem correta de execução:

1. 🚀 `start.sh` (se precisar do ambiente Python)
2. 📂 `tree_project.sh` (gera tree_project.json)
3. 🔄 `tree_git_changes.sh` (gera tree_git_changed.json e outros)
4. 🔗 `tree_git_siblings.sh` (usa outputs dos scripts anteriores)

💡 **Dica**: Use `tree_generate_all.sh` que executa os scripts na ordem correta automaticamente.

⚡ Os scripts de log (`git_log_detailed.sh` e `git_log_simple.sh`) são independentes e podem ser executados a qualquer momento.
