# 🎨 Poetry Migration Guide - Codex-AI

<div align="center">

**Guia completo para migração de setuptools para Poetry**  
*Modernizando o gerenciamento de dependências do Codex-AI*

[![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=flat&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 📋 Table of Contents

- [🎯 Por que Poetry?](#-por-que-poetry)
- [📊 Setuptools vs Poetry](#-setuptools-vs-poetry)
- [🔧 Preparação](#-preparação)
- [🚀 Migração Passo a Passo](#-migração-passo-a-passo)
- [📚 Referência de Comandos](#-referência-de-comandos)
- [🏗️ Novo pyproject.toml](#️-novo-pyprojecttoml)
- [✅ Validação](#-validação)
- [🔮 Roadmap](#-roadmap)

---

## 🎯 Por que Poetry?

### **📈 Status do Mercado (2024)**

| Métrica | Setuptools | Poetry | Tendência |
|---------|------------|--------|-----------|
| **Novos Projetos** | 40% | 45% | 📈 Poetry crescendo |
| **Projetos Enterprise** | 70% | 25% | 🔄 Migração gradual |
| **Startups/Scale-ups** | 20% | 65% | 🚀 Poetry dominando |
| **Open Source** | 50% | 35% | 📊 Equilibrado |

### **🏢 Quem Usa Poetry (2024)**

#### **✅ Projetos Famosos com Poetry:**
- **FastAPI** - Framework web mais popular
- **Pydantic** - Validação de dados
- **Starlette** - Framework ASGI
- **Typer** - CLI framework
- **Httpx** - Cliente HTTP moderno
- **Ruff** - Linter super rápido

#### **🔄 Migrando para Poetry:**
- **Django** - Considerando migração
- **Requests** - Avaliando Poetry
- **Pandas** - Testando em projetos menores

### **🎯 Benefícios Principais**

#### **1. 🔒 Dependency Resolution Inteligente**
```bash
# Setuptools (manual)
pip install requests==2.28.0
pip install urllib3==1.26.0  # ❌ Conflito! requests precisa urllib3>=1.21.1,<1.27

# Poetry (automático)
poetry add requests@2.28.0   # ✅ Resolve automaticamente urllib3 compatível
```

#### **2. 📦 Lock Files (Reprodutibilidade)**
```bash
# Node.js tem package-lock.json
# Poetry tem poetry.lock

# Setuptools
pip freeze > requirements.txt  # ❌ Manual, incompleto

# Poetry  
poetry install                 # ✅ Usa poetry.lock automaticamente
```

#### **3. 🛠️ Comandos Mais Simples**
```bash
# Setuptools
pip install requests
echo "requests>=2.28.0" >> requirements.txt
pip install -e .

# Poetry
poetry add requests            # ✅ Tudo em um comando
```

#### **4. ⚡ Virtual Environment Automático**
```bash
# Setuptools
python -m venv venv
source venv/bin/activate
pip install -e .

# Poetry
poetry install                 # ✅ Cria e ativa venv automaticamente
poetry shell                   # ✅ Ativa venv
```

#### **5. 📊 Build System Moderno**
```bash
# Setuptools
python setup.py sdist bdist_wheel  # ❌ Comando legado

# Poetry
poetry build                       # ✅ Cria wheel + sdist automaticamente
```

---

## 📊 Setuptools vs Poetry

### **🔄 Comparação Detalhada**

| Aspecto | Setuptools | Poetry | Vencedor |
|---------|------------|--------|----------|
| **📦 Dependency Resolution** | Manual | Automático | 🏆 Poetry |
| **🔒 Lock Files** | requirements.txt | poetry.lock | 🏆 Poetry |
| **⚡ Performance** | Lento | Rápido | 🏆 Poetry |
| **🛠️ Ease of Use** | Complexo | Simples | 🏆 Poetry |
| **📚 Documentation** | Extensa | Boa | 🏆 Setuptools |
| **🏢 Enterprise Support** | Maduro | Crescendo | 🏆 Setuptools |
| **🔧 Flexibility** | Alta | Média | 🏆 Setuptools |
| **📈 Future-proof** | Estável | Moderno | 🏆 Poetry |

### **💡 Quando Usar Cada Um**

#### **✅ Use Setuptools se:**
- 🏢 **Projeto enterprise** com muitas extensões C/C++
- 📚 **Equipe experiente** com setuptools
- 🔧 **Casos complexos** de build
- ⏰ **Deadline apertado** (sem tempo para migração)

#### **🚀 Use Poetry se:**
- 🆕 **Projeto novo** ou em desenvolvimento ativo
- 👥 **Equipe pequena/média** focada em produtividade
- 📦 **Dependências Python puras** (sem C/C++)
- 🎯 **Quer modernizar** o workflow

---

## 🔧 Preparação

### **📋 Checklist Pré-Migração**

#### **1. ✅ Backup Completo**
```bash
# Backup do estado atual
cp pyproject.toml pyproject.toml.backup
cp -r . ../codex-ai-backup

# Commit atual
git add .
git commit -m "backup: before poetry migration"
git tag backup-pre-poetry
```

#### **2. ✅ Verificar Compatibilidade**
```bash
# Verificar se todas dependências suportam Poetry
poetry check                    # Verifica pyproject.toml
poetry show --tree             # Mostra árvore de dependências
```

#### **3. ✅ Instalar Poetry**
```bash
# Método oficial (recomendado)
curl -sSL https://install.python-poetry.org | python3 -

# Ou via pip (alternativo)
pip install poetry

# Verificar instalação
poetry --version
```

#### **4. ✅ Configurar Poetry**
```bash
# Configurações recomendadas
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true  # Cria .venv na pasta do projeto
poetry config repositories.pypi-public https://pypi.org/simple/
```

---

## 🚀 Migração Passo a Passo

### **📝 Passo 1: Analisar pyproject.toml Atual**

```toml
# ANTES (setuptools)
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
dependencies = [
    "PyYAML>=6.0.2",
    "GitPython>=3.1.44",
    # ... mais dependências
]

[project.optional-dependencies]
performance = ["ujson>=5.10.0"]
rich = ["rich>=13.7.0"]
```

### **📝 Passo 2: Converter para Poetry**

```bash
# Inicializar Poetry no projeto existente
poetry init --no-interaction

# Ou converter manualmente o pyproject.toml
```

### **📝 Passo 3: Novo pyproject.toml (Poetry)**

```toml
# DEPOIS (Poetry)
[tool.poetry]
name = "codex-ai"
version = "1.0.0"
description = "AI-powered development toolkit for changelog generation, time tracking, and code analysis"
authors = ["Codex-AI Team <gabriel@laplanta.com.br>"]
readme = "README.md"
license = "MIT"
homepage = "https://github.com/the-coded/codex-ai"
repository = "https://github.com/the-coded/codex-ai"
documentation = "https://github.com/the-coded/codex-ai#readme"
keywords = ["ai", "git", "changelog", "documentation", "time-tracking"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Documentation",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[tool.poetry.dependencies]
python = "^3.8"
# ═══ PROCESSAMENTO DE DADOS ═══
PyYAML = "^6.0.2"              # Leitura/escrita YAML (configs, CI/CD)

# ═══ CONTROLE DE VERSÃO ═══  
GitPython = "^3.1.44"          # Interface Python para Git (commits, branches, tags)

# ═══ INTELIGÊNCIA ARTIFICIAL ═══
anthropic = "^0.55.0"          # API oficial Claude (competitor do ChatGPT)
aider-chat = "^0.84.0"         # AI coding assistant (escreve código automaticamente)
tiktoken = "^0.9.0"            # Contador de tokens para APIs de IA

# ═══ TEMPLATES E FORMATAÇÃO ═══
jinja2 = "^3.1.6"              # Engine de templates (como Handlebars/Mustache)

# ═══ UTILIDADES DE DATA/TEMPO ═══
python-dateutil = "^2.9.0"     # Manipulação avançada de datas (como moment.js)

# ═══ TIPAGEM E COMPATIBILIDADE ═══
typing-extensions = "^4.13.0"  # Recursos de tipagem para Python < 3.11
tomli = {version = "^2.2.0", markers = "python_version < '3.11'"}  # Parser TOML

[tool.poetry.group.performance.dependencies]
ujson = "^5.10.0"              # JSON parser mais rápido (C extension)
orjson = "^3.10.0"             # JSON parser ainda mais rápido (Rust)

[tool.poetry.group.rich.dependencies]
rich = "^13.7.0"               # Interface rica no terminal (cores, tabelas, progress)
colorama = "^0.4.6"            # Cores cross-platform (Windows/Unix)

[tool.poetry.group.dev.dependencies]
# Ferramentas de qualidade de código
ruff = "^0.1.0"                # Linter/formatter all-in-one (substitui black+isort+flake8)
mypy = "^1.8.0"                # Type checker estático
pytest = "^7.4.0"             # Framework de testes
pytest-cov = "^4.1.0"         # Coverage para pytest
watchdog = "^3.0.0"           # File watcher para desenvolvimento

[tool.poetry.scripts]
codex-ai = "cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### **📝 Passo 4: Migrar Dependências**

```bash
# Remover instalação setuptools
pip uninstall codex-ai

# Instalar com Poetry
poetry install

# Instalar grupos opcionais
poetry install --with performance,rich,dev

# Ou instalar tudo
poetry install --all-extras
```

### **📝 Passo 5: Gerar Lock File**

```bash
# Gerar poetry.lock
poetry lock

# Verificar dependências
poetry show --tree
poetry show --outdated
```

---

## 📚 Referência de Comandos

### **🔄 Equivalências Setuptools → Poetry**

| Setuptools | Poetry | Descrição |
|------------|--------|-----------|
| `pip install -e .` | `poetry install` | Instalar projeto em modo desenvolvimento |
| `pip install requests` | `poetry add requests` | Adicionar dependência |
| `pip install pytest --dev` | `poetry add --group dev pytest` | Adicionar dependência de desenvolvimento |
| `pip freeze > requirements.txt` | `poetry export -f requirements.txt` | Exportar dependências |
| `python setup.py sdist bdist_wheel` | `poetry build` | Criar distribuição |
| `twine upload dist/*` | `poetry publish` | Publicar no PyPI |
| `pip install -r requirements.txt` | `poetry install` | Instalar dependências |

### **🚀 Comandos Poetry Essenciais**

#### **📦 Gerenciamento de Dependências**
```bash
# Adicionar dependências
poetry add requests                    # Produção
poetry add --group dev pytest         # Desenvolvimento
poetry add --group performance ujson  # Grupo específico
poetry add "requests>=2.28.0"         # Com versão específica

# Remover dependências
poetry remove requests
poetry remove --group dev pytest

# Atualizar dependências
poetry update                          # Todas
poetry update requests                 # Específica
poetry update --group dev             # Grupo específico
```

#### **🏗️ Build e Publicação**
```bash
# Build
poetry build                          # Cria wheel + sdist
poetry build --format wheel          # Só wheel
poetry build --format sdist          # Só source distribution

# Publicação
poetry publish                        # PyPI oficial
poetry publish --repository testpypi  # Test PyPI
poetry publish --dry-run             # Simular publicação
```

#### **🔍 Informações**
```bash
# Informações do projeto
poetry show                           # Listar dependências
poetry show --tree                    # Árvore de dependências
poetry show --outdated               # Dependências desatualizadas
poetry show requests                  # Info específica

# Verificações
poetry check                          # Verificar pyproject.toml
poetry lock --check                   # Verificar se lock está atualizado
```

#### **🌍 Virtual Environment**
```bash
# Gerenciar ambiente virtual
poetry shell                          # Ativar venv
poetry env info                       # Info do venv
poetry env list                       # Listar venvs
poetry env remove python3.11          # Remover venv específico
```

---

## 🏗️ Novo pyproject.toml

### **📋 Estrutura Completa com Poetry**

```toml
[tool.poetry]
name = "codex-ai"
version = "1.0.0"
description = "AI-powered development toolkit for changelog generation, time tracking, and code analysis"
authors = ["Codex-AI Team <gabriel@laplanta.com.br>"]
maintainers = ["Codex-AI Team <gabriel@laplanta.com.br>"]
readme = "README.md"
license = "MIT"
homepage = "https://github.com/the-coded/codex-ai"
repository = "https://github.com/the-coded/codex-ai"
documentation = "https://github.com/the-coded/codex-ai#readme"
keywords = [
    "ai", "artificial-intelligence", "git", "changelog", "documentation", 
    "time-tracking", "development-tools", "claude", "automation", 
    "code-analysis", "project-management", "developer-experience"
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Version Control :: Git",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Environment :: Console",
]
packages = [
    {include = "commands"},
    {include = "core"},
    {include = "constants"},
    {include = "utils"},
    {include = "templates"},
    {include = "cli.py"},
]

[tool.poetry.dependencies]
python = "^3.8"

# ═══ PROCESSAMENTO DE DADOS ═══
PyYAML = "^6.0.2"              # Leitura/escrita YAML - configs, CI/CD, metadados

# ═══ CONTROLE DE VERSÃO ═══  
GitPython = "^3.1.44"          # Interface Python para Git - commits, branches, tags, diffs

# ═══ INTELIGÊNCIA ARTIFICIAL ═══
anthropic = "^0.55.0"          # API oficial Claude (Anthropic) - competitor do ChatGPT
aider-chat = "^0.84.0"         # AI coding assistant - escreve código automaticamente
tiktoken = "^0.9.0"            # Contador de tokens para APIs de IA (OpenAI/Anthropic)

# ═══ TEMPLATES E FORMATAÇÃO ═══
jinja2 = "^3.1.6"              # Engine de templates - como Handlebars/Mustache no Node.js

# ═══ UTILIDADES DE DATA/TEMPO ═══
python-dateutil = "^2.9.0"     # Manipulação avançada de datas - como moment.js/date-fns

# ═══ TIPAGEM E COMPATIBILIDADE ═══
typing-extensions = "^4.13.0"  # Recursos de tipagem para Python < 3.11
tomli = {version = "^2.2.0", markers = "python_version < '3.11'"}  # Parser TOML (built-in no 3.11+)

[tool.poetry.group.performance]
optional = true

[tool.poetry.group.performance.dependencies]
ujson = "^5.10.0"              # JSON parser mais rápido (C extension) - 2-3x faster que json
orjson = "^3.10.0"             # JSON parser ainda mais rápido (Rust) - 5-10x faster que json

[tool.poetry.group.rich]
optional = true

[tool.poetry.group.rich.dependencies]
rich = "^13.7.0"               # Interface rica no terminal - cores, tabelas, progress bars
colorama = "^0.4.6"            # Cores cross-platform (Windows/Unix) - como chalk no Node.js

[tool.poetry.group.dev]
optional = true

[tool.poetry.group.dev.dependencies]
# ═══ QUALIDADE DE CÓDIGO ═══
ruff = "^0.1.0"                # Linter/formatter all-in-one (substitui black+isort+flake8)
mypy = "^1.8.0"                # Type checker estático - como TypeScript

# ═══ TESTES ═══
pytest = "^7.4.0"             # Framework de testes - como Jest no Node.js
pytest-cov = "^4.1.0"         # Coverage para pytest - como jest --coverage

# ═══ DESENVOLVIMENTO ═══
watchdog = "^3.0.0"           # File watcher para desenvolvimento - como nodemon

[tool.poetry.scripts]
codex-ai = "cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# ═══ CONFIGURAÇÕES DE FERRAMENTAS ═══
# (Mantém as mesmas configurações de ruff, mypy, pytest, etc.)

[tool.ruff]
line-length = 88
target-version = "py38"
select = ["E", "F", "W", "I", "N", "UP", "YTT", "S", "BLE", "FBT", "B", "A", "COM", "C4", "DTZ", "T10", "EM", "EXE", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SIM", "TID", "TCH", "ARG", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = ["E501", "S101", "S603", "S607"]
exclude = ["old/", ".venv/", "build/", "dist/"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = ["aider.*", "tiktoken.*", "git.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.coverage.run]
source = [".", "commands", "core", "constants", "utils"]
omit = ["*/tests/*", "*/test_*", "setup.py", "*/old/*", "*/.venv/*", "*/venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

---

## ✅ Validação

### **🧪 Testes Pós-Migração**

#### **1. ✅ Verificar Instalação**
```bash
# Limpar ambiente
poetry env remove --all
rm -rf .venv

# Reinstalar do zero
poetry install --all-extras

# Verificar se CLI funciona
poetry run codex-ai --help
poetry run codex-ai config --list
```

#### **2. ✅ Executar Testes**
```bash
# Testes unitários
poetry run python tests/run_all.py

# Testes específicos
poetry run python tests/run_all.py --category commands

# Com coverage
poetry run pytest --cov=. --cov-report=html
```

#### **3. ✅ Verificar Build**
```bash
# Build local
poetry build

# Verificar arquivos gerados
ls -la dist/
# Deve ter: codex_ai-1.0.0-py3-none-any.whl e codex-ai-1.0.0.tar.gz

# Testar instalação do wheel
pip install dist/codex_ai-1.0.0-py3-none-any.whl
codex-ai --help
pip uninstall codex-ai
```

#### **4. ✅ Verificar Dependências**
```bash
# Verificar árvore de dependências
poetry show --tree

# Verificar conflitos
poetry check

# Verificar se lock está atualizado
poetry lock --check
```

### **🔧 Troubleshooting Comum**

#### **❌ Problema: "No module named 'cli'"**
```bash
# Solução: Verificar packages no pyproject.toml
[tool.poetry]
packages = [
    {include = "cli.py"},  # ← Adicionar se missing
]
```

#### **❌ Problema: "Command 'codex-ai' not found"**
```bash
# Solução: Verificar scripts
[tool.poetry.scripts]
codex-ai = "cli:main"  # ← Verificar se está correto

# Reinstalar
poetry install
```

#### **❌ Problema: Dependências conflitantes**
```bash
# Solução: Resolver conflitos
poetry lock --no-update  # Usar versões atuais
poetry update            # Ou atualizar tudo
```

---

## 🔮 Roadmap

### **📅 Cronograma Sugerido**

#### **🎯 Fase 1: Preparação (1-2 semanas)**
- [ ] ✅ Estudar Poetry e suas vantagens
- [ ] ✅ Fazer backup completo do projeto
- [ ] ✅ Instalar e configurar Poetry
- [ ] ✅ Testar Poetry em projeto de exemplo

#### **🎯 Fase 2: Migração (1 semana)**
- [ ] 🔄 Converter pyproject.toml para Poetry
- [ ] 🔄 Migrar dependências e grupos
- [ ] 🔄 Atualizar scripts de CI/CD
- [ ] 🔄 Testar build e publicação

#### **🎯 Fase 3: Validação (1 semana)**
- [ ] ✅ Executar todos os testes
- [ ] ✅ Verificar compatibilidade
- [ ] ✅ Documentar mudanças
- [ ] ✅ Treinar equipe

#### **🎯 Fase 4: Deploy (1 semana)**
- [ ] 🚀 Atualizar documentação
- [ ] 🚀 Publicar nova versão
- [ ] 🚀 Monitorar feedback
- [ ] 🚀 Ajustes finais

### **⚖️ Considerações de Migração**

#### **✅ Migrar AGORA se:**
- 🆕 **Projeto em desenvolvimento ativo**
- 👥 **Equipe pequena/média** (< 10 pessoas)
- 🎯 **Foco em produtividade** e developer experience
- 📦 **Dependências Python puras** (sem C/C++ complexo)
- 🚀 **Quer estar na vanguarda** tecnológica

#### **⏳ Migrar DEPOIS se:**
- 🏢 **Projeto enterprise** com muitas extensões
- 👥 **Equipe grande** (> 20 pessoas) sem experiência Poetry
- ⏰ **Deadline crítico** nos próximos 2 meses
- 🔧 **Build system complexo** com customizações

#### **🚫 NÃO migrar se:**
- 🏛️ **Projeto legado** em manutenção apenas
- 📚 **Equipe sem tempo** para aprender nova ferramenta
- 🔒 **Restrições corporativas** que impedem Poetry
- ⚡ **Funciona perfeitamente** e não há necessidade

---

## 📚 Recursos Adicionais

### **📖 Documentação Oficial**
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry GitHub](https://github.com/python-poetry/poetry)
- [Poetry FAQ](https://python-poetry.org/docs/faq/)

### **🎓 Tutoriais e Guias**
- [Real Python - Poetry Guide](https://realpython.com/dependency-management-python-poetry/)
- [Poetry vs Pipenv vs pip-tools](https://python-poetry.org/docs/faq/#what-is-the-difference-between-poetry-and-pipenv)
- [Migrating from setuptools](https://python-poetry.org/docs/pyproject/#migrating-from-setuptools)

### **🛠️ Ferramentas Complementares**
- [poetry-plugin-export](https://github.com/python-poetry/poetry-plugin-export) - Exportar requirements.txt
- [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) - Versionamento automático
- [poetry-pre-commit-plugin](https://github.com/python-poetry/poetry-pre-commit-plugin) - Integração com pre-commit

---

## 🎯 Conclusão

A migração para Poetry representa um **investimento no futuro** do Codex-AI:

### **📈 Benefícios Imediatos**
- ⚡ **Instalação mais rápida** de dependências
- 🔒 **Builds reproduzíveis** com poetry.lock
- 🛠️ **Comandos mais simples** e intuitivos
- 📦 **Gerenciamento automático** de virtual environments

### **🚀 Benefícios a Longo Prazo**
- 📊 **Melhor developer experience** para novos contribuidores
- 🔮 **Preparação para o futuro** do ecossistema Python
- 🏢 **Alinhamento com projetos modernos** (FastAPI, Pydantic, etc.)
- 📈 **Facilita contribuições** da comunidade

### **💡 Recomendação Final**

**Recomendamos a migração** para Poetry, especialmente considerando que:
1. ✅ Codex-AI é um projeto **moderno e ativo**
2. ✅ Tem **dependências Python puras** (sem C/C++ complexo)
3. ✅ Beneficiaria da **melhor developer experience**
4. ✅ Alinharia com **tendências do mercado** Python 2024+

**A migração pode ser feita gradualmente, sem pressa, quando a equipe tiver disponibilidade para aprender e testar adequadamente.**

---

<div align="center">

**Made with ❤️ by [laplanta](https://laplanta.com.br)**

*Modernizando o desenvolvimento Python, um projeto por vez* 🚀

</div>
