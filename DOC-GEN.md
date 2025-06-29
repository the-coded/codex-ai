# 🚀 DOC-GEN - Plano de Implementação YAGNI

**Comando de documentação genérica para qualquer projeto/linguagem**

---

## 🎯 **VISÃO GERAL**

### **Objetivo:**
Criar comando `doc-gen` para documentar projetos de forma genérica, diferente do `doc-ui` que é específico para React/Sass/Storybook.

### **Diferenças Chave:**
| **Aspecto** | **doc-ui** | **doc-gen** |
|-------------|------------|-------------|
| **Escopo** | React/Sass/Storybook específicos | Qualquer projeto/linguagem |
| **Detecção** | Patterns específicos (.tsx, .scss, .stories) | Extensões genéricas + estrutura de pastas |
| **Output** | `docs/react/`, `docs/sass/` | `docs/` espelhando estrutura do projeto |
| **Lógica** | Cross-triggers (component → storybook) | Hierarquia de pastas (pasta → arquivos) |
| **Prompts** | Templates específicos para UI | Templates genéricos para código/docs |

### **Modos de Documentação:**
- **Simple**: README.md por pasta explicando conteúdo
- **Detailed**: README.md + [filename].md para cada arquivo

### **🎯 ABORDAGEM YAGNI:**
1. **Criar infraestrutura core/** modular
2. **Criar doc-gen.py** usando módulos core/
3. **Testar completamente** standalone
4. **[Opcional] Migrar doc-ui.py** para usar mesmos módulos

---

## 📋 **COMANDOS E FLAGS COMPLETOS**

### **🎯 Comando Base:**
```bash
codex-ai doc-gen [OPTIONS]
```

### **📝 Argumentos Obrigatórios:**
- `--mode {simple,detailed}` - Tipo de documentação a gerar

### **📁 Controle de Arquivos:**
- `--path PATH` - Pasta específica para documentar (padrão: projeto inteiro)
- `--shallow` - Não recursivo, só a pasta específica (padrão: recursivo)

### **🗂️ Controle de Output:**
- `--docs-dir DIRECTORY` - Diretório de output (padrão: `docs/`)
  - `docs/` = Separado (docs/src/utils/)
  - `./docs/` = Inline (src/utils/docs/)
- `--strip-prefix PREFIX1,PREFIX2` - Remover prefixos dos paths (padrão: `src/`)

### **🎛️ Filtros de Arquivos:**
- `--preset {python,javascript}` - Preset específico (padrão: merge python+javascript+generic)
- `--ext .EXT1,.EXT2` - Extensões customizadas (ex: `.py,.js,.md`)
- `--exclude PATTERN1,PATTERN2` - Exclusões customizadas (ex: `*.pyc,node_modules`)

### **🔄 Modos Git:**
- `--local` - Forçar modo local (staged/modified files)
- `--since COMMIT` - Arquivos mudados desde este commit (implica --pipeline)
- `--pipeline` - Forçar modo pipeline (padrão: origin/main se sem --since)

### **🔧 Debug e Preview:**
- `--dry-run` - Preview sem AI calls (sem custos)
- `--help` - Mostrar ajuda completa

**Nota**: `--verbose` é flag global do codex-ai: `codex-ai --verbose doc-gen`

### **📊 Exemplos Completos:**
```bash
# Básico
codex-ai doc-gen --mode simple
codex-ai doc-gen --mode detailed

# Com path específico
codex-ai doc-gen --path src/ --mode detailed
codex-ai doc-gen --path src/utils/ --shallow --mode simple

# Controle de output
codex-ai doc-gen --mode detailed --docs-dir docs/
codex-ai doc-gen --mode detailed --docs-dir ./docs/
codex-ai doc-gen --mode detailed --docs-dir docs/ --strip-prefix src/,lib/

# Filtros
codex-ai doc-gen --mode detailed --preset python
codex-ai doc-gen --mode detailed --ext .py,.js,.md
codex-ai doc-gen --mode detailed --exclude *.pyc,node_modules,__pycache__

# Git modes
codex-ai doc-gen --mode detailed --local
codex-ai doc-gen --mode detailed --since HEAD~5

# Debug
codex-ai --verbose doc-gen --mode detailed --dry-run
```

### **🎛️ Presets Disponíveis:**
```python
# Default (sem --preset): python + javascript + generic (merge automático)

# --preset python (inclui generic automaticamente)
extensions: .py, .pyi, .yaml, .toml  # + generic extensions
exclude: *.pyc, __pycache__, .pytest_cache, build, dist, *.egg-info  # + generic excludes

# --preset javascript (inclui generic automaticamente)  
extensions: .js, .ts, .jsx, .tsx, .json, .mjs  # + generic extensions
exclude: node_modules, *.min.js, *.min.css, *.map, build, dist, .next  # + generic excludes

# generic (sempre incluído)
extensions: .md, .txt, .yaml, .yml, .json, .sh, .bash
exclude: .git, .tmp, *.log, .DS_Store, Thumbs.db, .vscode, .idea
```

**Lógica de Merge:**
- **Default**: python + javascript + generic (todas extensões e excludes)
- **--preset python**: python + generic (sem extensões JS específicas)
- **--preset javascript**: javascript + generic (sem extensões Python específicas)

---

## 📝 **CONSTANTES NECESSÁRIAS**

### **✅ Checklist - Constantes no commands/doc_gen.py:**

#### **📝 C1: DOC_GEN_PRESETS**
```python
DOC_GEN_PRESETS = {
    "python": {
        "extensions": [".py", ".pyi", ".yaml", ".toml"],
        "exclude": ["*.pyc", "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info"]
    },
    "javascript": {
        "extensions": [".js", ".ts", ".jsx", ".tsx", ".json", ".mjs"],
        "exclude": ["node_modules", "*.min.js", "*.min.css", "*.map", "build", "dist", ".next"]
    },
    "generic": {
        "extensions": [".md", ".txt", ".yaml", ".yml", ".json", ".sh", ".bash"],
        "exclude": [".git", ".tmp", "*.log", ".DS_Store", "Thumbs.db", ".vscode", ".idea"]
    }
}
```
- [ ] **C1.1**: Definir preset python com extensões e excludes
- [ ] **C1.2**: Definir preset javascript com extensões e excludes
- [ ] **C1.3**: Definir preset generic com extensões e excludes

#### **📝 C2: DOC_GEN_DEFAULTS**
```python
DOC_GEN_DEFAULTS = {
    "docs_dir": "docs/",
    "strip_prefixes": ["src/"],
    "pipeline_default_branches": [
        "origin/main",
        "origin/master", 
        "main",
        "master",
        "HEAD~1"
    ],
    "mode": "simple"
}
```
- [ ] **C2.1**: Definir docs_dir padrão
- [ ] **C2.2**: Definir strip_prefixes padrão
- [ ] **C2.3**: Definir pipeline_default_branches com fallbacks
- [ ] **C2.4**: Definir mode padrão

#### **📝 C3: DOC_GEN_TEMPLATES**
```python
DOC_GEN_TEMPLATES = {
    "folder_readme": "templates/prompts/doc_gen_folder_readme_prompt.md",
    "folder_index": "templates/prompts/doc_gen_folder_index_prompt.md",
    "file_detailed": "templates/prompts/doc_gen_file_detailed_prompt.md"
}
```
- [ ] **C3.1**: Definir path para template folder_readme
- [ ] **C3.2**: Definir path para template folder_index
- [ ] **C3.3**: Definir path para template file_detailed

#### **📝 C4: DOC_GEN_CLI_CHOICES**
```python
DOC_GEN_CLI_CHOICES = {
    "modes": ["simple", "detailed"],
    "presets": ["python", "javascript"]  # generic sempre incluído automaticamente
}
```
- [ ] **C4.1**: Definir choices para --mode
- [ ] **C4.2**: Definir choices para --preset

#### **📝 C5: DOC_GEN_VALIDATION**
```python
DOC_GEN_VALIDATION = {
    "max_files_per_run": 100,  # Evitar requests excessivos
    "supported_extensions": [
        ".py", ".pyi", ".js", ".ts", ".jsx", ".tsx", ".json", ".mjs",
        ".md", ".txt", ".yaml", ".yml", ".sh", ".bash", ".toml"
    ]
}
```
- [ ] **C5.1**: Definir max_files_per_run
- [ ] **C5.2**: Definir supported_extensions

### **✅ Checklist - Adicionar em constants/ai.py:**

#### **📝 C6: DOC_GEN Template no AIDER_COMMAND_TEMPLATES**
```python
# Adicionar no AIDER_COMMAND_TEMPLATES existente:
"DOC_GEN": {
    "additional_flags": [
        ["--no-git"],
        ["--thinking-tokens", "4k"]
    ],
    "pattern": "aider {base_flags} --model {model} --read {context_files} --message-file {prompt_file} --file {output_file}"
}
```
- [ ] **C6.1**: Adicionar DOC_GEN no AIDER_COMMAND_TEMPLATES
- [ ] **C6.2**: Definir additional_flags para doc-gen
- [ ] **C6.3**: Definir pattern para comando aider

### **✅ Checklist - Imports de constants/ existentes:**

#### **📝 C7: Imports de constants.git**
```python
from constants.git import (
    EXCLUDE_PATTERNS,           # Padrões de exclusão Git
    GIT_STATUS_COMMANDS,        # Comandos de status Git  
    GIT_DIFF_COMMANDS,          # Comandos de diff Git
    build_exclude_pathspec,     # Helper para pathspec
    format_git_command          # Helper para formatar comandos
)
```
- [ ] **C7.1**: Import EXCLUDE_PATTERNS
- [ ] **C7.2**: Import GIT_STATUS_COMMANDS
- [ ] **C7.3**: Import GIT_DIFF_COMMANDS
- [ ] **C7.4**: Import helpers (build_exclude_pathspec, format_git_command)

#### **📝 C8: Imports de constants.output**
```python
from constants.output import (
    EMOJIS,                     # Emojis para feedback (✅ ❌ 🔍 📁)
    SEMANTIC_COLORS,            # Cores semânticas para terminal
    format_with_emoji,          # Helper para emojis
    colorize                    # Helper para cores
)
```
- [ ] **C8.1**: Import EMOJIS
- [ ] **C8.2**: Import SEMANTIC_COLORS
- [ ] **C8.3**: Import helpers (format_with_emoji, colorize)

#### **📝 C9: Imports de constants.ai**
```python
from constants.ai import (
    AI_MODELS,                  # Modelos disponíveis
    TOKEN_STRATEGY,             # Estratégia de tokens
    AIDER_BASE_FLAGS,           # Flags base do aider
    select_model_by_tokens,     # Selecionar modelo por tokens
    get_effective_token_limit,  # Limite efetivo de tokens
    build_aider_command,        # Construir comando aider (usa DOC_GEN template)
    get_default_model_name      # Modelo padrão
)
```
- [ ] **C9.1**: Import AI_MODELS
- [ ] **C9.2**: Import TOKEN_STRATEGY
- [ ] **C9.3**: Import AIDER_BASE_FLAGS
- [ ] **C9.4**: Import helpers AI (select_model_by_tokens, get_effective_token_limit, etc.)

### **✅ Checklist - Criar Arquivos com Constantes:**

#### **📝 C10: Criar commands/doc_gen.py (só constantes)**
- [ ] **C10.1**: Criar arquivo `commands/doc_gen.py`
- [ ] **C10.2**: Adicionar todas constantes C1-C5
- [ ] **C10.3**: Adicionar imports C7-C9
- [ ] **C10.4**: Adicionar docstrings e type hints
- [ ] **C10.5**: Testar imports: `python -c "from commands.doc_gen import DOC_GEN_PRESETS; print('OK')"`

### **✅ Validação Constantes:**
- [ ] **VC1**: Todas constantes definidas em doc_gen.py
- [ ] **VC2**: DOC_GEN template adicionado em constants/ai.py
- [ ] **VC3**: Todos imports funcionam
- [ ] **VC4**: Presets validados com extensões corretas
- [ ] **VC5**: Defaults testados

---

## 🏗️ **FASE 1: INFRAESTRUTURA CORE (Risk-Free)**

### **✅ Checklist - Criar core/git/ Modular:**

#### **📝 1.1: Adicionar funções ao core/git/changes_tracker.py**
- [ ] **1.1.1**: Copiar `auto_detect_mode()` do doc_ui.py para final do changes_tracker.py
- [ ] **1.1.2**: Copiar `get_files_for_mode()` do doc_ui.py para final do changes_tracker.py
- [ ] **1.1.3**: Copiar `get_files_for_path()` do doc_ui.py para final do changes_tracker.py
- [ ] **1.1.4**: Adicionar parâmetro `shallow=False` em `get_files_for_path()`
- [ ] **1.1.5**: Importar dependências necessárias (`os`, `Path`, `Optional`, `List`)
- [ ] **1.1.6**: Manter docstrings e type hints

#### **📝 1.2: Atualizar core/git/__init__.py**
- [ ] **1.2.1**: Adicionar `auto_detect_mode` nos imports do changes_tracker
- [ ] **1.2.2**: Adicionar `get_files_for_mode` nos imports do changes_tracker
- [ ] **1.2.3**: Adicionar `get_files_for_path` nos imports do changes_tracker
- [ ] **1.2.4**: Adicionar as 3 funções no `__all__` list

#### **📝 1.3: Testar Imports (SEM tocar doc_ui.py)**
- [ ] **1.3.1**: `python -c "from core.git import auto_detect_mode; print('OK')"`
- [ ] **1.3.2**: `python -c "from core.git import get_files_for_mode; print('OK')"`
- [ ] **1.3.3**: `python -c "from core.git import get_files_for_path; print('OK')"`

### **✅ Checklist - Criar utils/filesystem.py:**

#### **📝 1.4: Criar utils/filesystem.py**
- [ ] **1.4.1**: Criar arquivo `utils/filesystem.py`
- [ ] **1.4.2**: Implementar `cleanup_tmp_directory()` - limpar e recriar .tmp/
- [ ] **1.4.3**: Implementar `create_output_directories(paths: List[str])` - criar dirs
- [ ] **1.4.4**: Implementar `ensure_directory_exists(path: str)` - helper
- [ ] **1.4.5**: Adicionar imports (`os`, `shutil`, `Path`, `List`)
- [ ] **1.4.6**: Adicionar docstrings e type hints

#### **📝 1.5: Atualizar utils/__init__.py**
- [ ] **1.5.1**: Adicionar imports das funções filesystem
- [ ] **1.5.2**: Adicionar no `__all__` list
- [ ] **1.5.3**: Testar: `python -c "from utils.filesystem import cleanup_tmp_directory; print('OK')"`

### **✅ Validação Fase 1:**
- [ ] **V1.1**: Todos imports core/git/ funcionam
- [ ] **V1.2**: Todos imports utils/filesystem funcionam
- [ ] **V1.3**: doc_ui.py ainda funciona: `python -m cli doc-ui --help`

---

## 📝 **FASE 2: TEMPLATES E PRESETS**

### **✅ Checklist - Templates de Prompts:**

#### **📝 2.1: doc_gen_folder_readme_prompt.md**
- [ ] **2.1.1**: Criar `templates/prompts/doc_gen_folder_readme_prompt.md`
- [ ] **2.1.2**: Template para README.md de pastas
- [ ] **2.1.3**: Seção para docs separadas (docs/) - overview + índice incorporado
- [ ] **2.1.4**: Seção para docs inline (./docs/) - overview simples + link INDEX.md
- [ ] **2.1.5**: Instruções para análise de arquivos da pasta

#### **📝 2.2: doc_gen_folder_index_prompt.md**
- [ ] **2.2.1**: Criar `templates/prompts/doc_gen_folder_index_prompt.md`
- [ ] **2.2.2**: Template para INDEX.md (só modo inline)
- [ ] **2.2.3**: Navegação para documentação técnica
- [ ] **2.2.4**: Categorização e links organizados

#### **📝 2.3: doc_gen_file_detailed_prompt.md**
- [ ] **2.3.1**: Criar `templates/prompts/doc_gen_file_detailed_prompt.md`
- [ ] **2.3.2**: Template para docs individuais
- [ ] **2.3.3**: Seções obrigatórias (purpose, functions, dependencies, usage)
- [ ] **2.3.4**: Exemplos de código e notas de implementação

#### **📝 2.4: Atualizar templates/__init__.py**
- [ ] **2.4.1**: Adicionar imports dos novos templates
- [ ] **2.4.2**: Atualizar `__all__` list

### **✅ Validação Fase 2:**
- [ ] **V2.1**: Templates criados e acessíveis
- [ ] **V2.2**: Presets já definidos em CONSTANTES (seção anterior)

---

## 🚀 **FASE 3: DOC-GEN.PY COMPLETO**

### **✅ Checklist - Criar commands/doc_gen.py:**

#### **📝 3.1: Estrutura Básica**
- [ ] **3.1.1**: Criar arquivo `commands/doc_gen.py`
- [ ] **3.1.2**: Imports de `core.git` (auto_detect_mode, get_files_for_mode, get_files_for_path)
- [ ] **3.1.3**: Imports de `utils.filesystem` (cleanup_tmp_directory, create_output_directories)
- [ ] **3.1.4**: Imports de `core.ai` (get_default_model, count_tokens, load_prompt)
- [ ] **3.1.5**: Definir DOC_GEN_PRESETS no arquivo

#### **📝 3.2: Funções Específicas**
- [ ] **3.2.1**: `get_default_filters()` - merge todos presets
- [ ] **3.2.2**: `get_preset_filters(preset_name)` - preset específico
- [ ] **3.2.3**: `detect_doc_gen_files()` - filtrar arquivos baseado em presets
- [ ] **3.2.4**: `determine_output_strategy()` - separated vs inline
- [ ] **3.2.5**: `map_output_paths()` - mapear input para output paths
- [ ] **3.2.6**: `generate_folder_documentation()` - README.md + INDEX.md
- [ ] **3.2.7**: `generate_file_documentation()` - docs individuais

#### **📝 3.3: Função Principal**
- [ ] **3.3.1**: `run_doc_gen()` - função principal
- [ ] **3.3.2**: Argumentos: mode, path, shallow, docs_dir, preset, ext, exclude
- [ ] **3.3.3**: Auto-detect git mode usando `auto_detect_mode()`
- [ ] **3.3.4**: Listar arquivos usando `get_files_for_mode()` ou `get_files_for_path()`
- [ ] **3.3.5**: Filtrar arquivos usando `detect_doc_gen_files()`
- [ ] **3.3.6**: Mapear output paths usando `map_output_paths()`
- [ ] **3.3.7**: Gerar documentação usando funções de geração

#### **📝 3.4: CLI Arguments**
- [ ] **3.4.1**: `add_doc_gen_arguments()` - definir argumentos CLI
- [ ] **3.4.2**: `--mode {simple,detailed}` - tipo de documentação
- [ ] **3.4.3**: `--path PATH` - pasta específica
- [ ] **3.4.4**: `--shallow` - não recursivo
- [ ] **3.4.5**: `--docs-dir` - diretório de output (docs/ ou ./docs/)
- [ ] **3.4.6**: `--strip-prefix` - remover prefixos
- [ ] **3.4.7**: `--preset {python,javascript,generic}` - preset específico
- [ ] **3.4.8**: `--ext` - extensões customizadas
- [ ] **3.4.9**: `--exclude` - exclusões customizadas
- [ ] **3.4.10**: `--dry-run` - preview sem AI calls
- [ ] **3.4.11**: `--verbose` - output detalhado

#### **📝 3.5: Handler CLI**
- [ ] **3.5.1**: `doc_gen_command(args)` - handler para CLI
- [ ] **3.5.2**: Chamar `run_doc_gen()` com argumentos parseados

### **✅ Checklist - Integração CLI:**

#### **📝 3.6: Atualizar commands/__init__.py**
- [ ] **3.6.1**: Adicionar import de doc_gen
- [ ] **3.6.2**: Exportar funções necessárias

#### **📝 3.7: Atualizar cli.py**
- [ ] **3.7.1**: Import `run_doc_gen_command` de commands.doc_gen
- [ ] **3.7.2**: Adicionar subparser para 'doc-gen'
- [ ] **3.7.3**: Registrar `add_doc_gen_arguments`
- [ ] **3.7.4**: Registrar handler `doc_gen_command`
- [ ] **3.7.5**: Atualizar help text principal

### **✅ Checklist - Testes Standalone:**

#### **📝 3.8: Testes Básicos**
- [ ] **3.8.1**: `python -m cli doc-gen --help` (deve funcionar)
- [ ] **3.8.2**: `python -m cli doc-gen --dry-run --verbose` (deve mostrar preview)
- [ ] **3.8.3**: `python -m cli doc-gen --mode simple --dry-run` (deve funcionar)
- [ ] **3.8.4**: `python -m cli doc-gen --mode detailed --dry-run` (deve funcionar)
- [ ] **3.8.5**: `python -m cli doc-gen --preset python --dry-run` (deve funcionar)

#### **📝 3.9: Testes de Filtros**
- [ ] **3.9.1**: Testar merge de todos presets (default)
- [ ] **3.9.2**: Testar preset específico
- [ ] **3.9.3**: Testar extensões customizadas
- [ ] **3.9.4**: Testar exclusões customizadas

#### **📝 3.10: Testes de Output**
- [ ] **3.10.1**: Testar estratégia separated (--docs-dir docs/)
- [ ] **3.10.2**: Testar estratégia inline (--docs-dir ./docs/)
- [ ] **3.10.3**: Testar strip prefixes
- [ ] **3.10.4**: Testar path mapping

### **✅ Validação Fase 3:**
- [ ] **V3.1**: doc-gen.py funciona completamente standalone
- [ ] **V3.2**: CLI reconhece comando doc-gen
- [ ] **V3.3**: Dry-run mostra preview correto
- [ ] **V3.4**: Filtros funcionam corretamente
- [ ] **V3.5**: Output paths são mapeados corretamente

---

## 🔄 **FASE 4: MIGRAR DOC-UI.PY (Opcional)**

### **✅ Checklist - Adaptar doc_ui.py:**

#### **📝 4.1: Substituir Funções Duplicadas**
- [ ] **4.1.1**: Remover `auto_detect_mode()` do doc_ui.py
- [ ] **4.1.2**: Remover `get_files_for_mode()` do doc_ui.py
- [ ] **4.1.3**: Remover `get_files_for_path()` do doc_ui.py
- [ ] **4.1.4**: Adicionar import: `from core.git import auto_detect_mode, get_files_for_mode, get_files_for_path`

#### **📝 4.2: Usar utils/filesystem.py**
- [ ] **4.2.1**: Remover código inline de .tmp/ management
- [ ] **4.2.2**: Adicionar import: `from utils.filesystem import cleanup_tmp_directory, create_output_directories`
- [ ] **4.2.3**: Substituir chamadas inline por funções utils

#### **📝 4.3: Validar doc_ui.py**
- [ ] **4.3.1**: `python -m cli doc-ui --help` (deve funcionar)
- [ ] **4.3.2**: `python -m cli doc-ui --dry-run` (deve funcionar)
- [ ] **4.3.3**: `python tests/commands_doc_ui.py` (deve passar)
- [ ] **4.3.4**: Verificar que .tmp/ ainda é criado corretamente

### **✅ Validação Fase 4:**
- [ ] **V4.1**: doc_ui.py ainda funciona após migração
- [ ] **V4.2**: Código não duplicado entre doc_ui.py e doc_gen.py
- [ ] **V4.3**: Ambos comandos funcionam independentemente

---

## 🧪 **TESTES FINAIS**

### **✅ Checklist - Criar tests/commands_doc_gen.py:**
- [ ] **T1**: Testes de CLI arguments
- [ ] **T2**: Testes de filtros e presets
- [ ] **T3**: Testes de output paths
- [ ] **T4**: Testes de git integration
- [ ] **T5**: Mock de AI interface

### **✅ Checklist - Atualizar tests/run_all.py:**
- [ ] **T6**: Adicionar commands_doc_gen.py na lista de testes

---

## 📖 **DOCUMENTAÇÃO**

### **✅ Checklist - commands/doc_gen.md:**
- [ ] **D1**: Criar help do comando
- [ ] **D2**: Exemplos de uso básicos
- [ ] **D3**: Explicação de modos e estratégias
- [ ] **D4**: Documentação de presets

---

## ✅ **VALIDAÇÃO FINAL COMPLETA**

### **✅ Funcionalidade:**
- [ ] **F1**: `codex-ai doc-gen --help` funciona
- [ ] **F2**: Dry-run mostra preview correto
- [ ] **F3**: Modo simple gera README.md por pasta
- [ ] **F4**: Modo detailed gera README.md + docs individuais
- [ ] **F5**: Filtros funcionam corretamente

### **✅ Integração:**
- [ ] **I1**: CLI reconhece comando doc-gen
- [ ] **I2**: doc_ui.py ainda funciona (se Fase 4 executada)
- [ ] **I3**: Todos os testes passam
- [ ] **I4**: Imports de core/ funcionam
- [ ] **I5**: Utils funcionam

### **✅ Output Quality:**
- [ ] **Q1**: Estratégia separated funciona
- [ ] **Q2**: Estratégia inline funciona
- [ ] **Q3**: Strip prefixes funciona
- [ ] **Q4**: Links entre docs funcionam
- [ ] **Q5**: Estrutura de pastas correta

---

## 🎯 **COMANDOS CLI FINAIS**

### **📋 Comandos Básicos:**
```bash
# Documentar projeto inteiro
codex-ai doc-gen --mode simple              # README.md por pasta
codex-ai doc-gen --mode detailed            # README.md + docs individuais

# Path específico
codex-ai doc-gen --path src/ --mode detailed             # recursivo (padrão)
codex-ai doc-gen --path src/ --shallow --mode simple     # só src/

# Preview sem custos
codex-ai doc-gen --dry-run --verbose
```

### **🗂️ Output Control:**
```bash
# Separado (padrão)
codex-ai doc-gen --docs-dir docs/                        # docs/src/utils/

# Inline  
codex-ai doc-gen --docs-dir ./docs/                      # src/utils/docs/

# Strip prefixes
codex-ai doc-gen --docs-dir docs/ --strip-prefix src/,lib/
```

### **🎛️ Filtros:**
```bash
# Default: todos os presets (python + javascript + generic)
codex-ai doc-gen --mode detailed

# Preset específico
codex-ai doc-gen --preset python
codex-ai doc-gen --preset javascript

# Custom
codex-ai doc-gen --ext .py,.js,.md
codex-ai doc-gen --exclude node_modules,*.pyc,__pycache__
```

---

## 🏗️ **ESTRUTURAS DE OUTPUT**

### **📁 Separado (--docs-dir docs/):**
```
projeto/
├── src/utils/
│   ├── helpers.py
│   └── database.py
└── docs/                    # ← Área separada
    └── src/utils/
        ├── README.md        # ← Overview + índice incorporado
        ├── helpers.md       # ← Doc técnica
        └── database.md      # ← Doc técnica
```

### **📁 Inline (--docs-dir ./docs/):**
```
projeto/
└── src/utils/
    ├── README.md            # ← Overview da pasta
    ├── docs/                # ← Subpasta para docs técnicas
    │   ├── INDEX.md         # ← Navegação
    │   ├── helpers.md       # ← Doc técnica
    │   └── database.md      # ← Doc técnica
    ├── helpers.py
    └── database.py
```

---

## 📊 **MÉTRICAS DE SUCESSO**

- [ ] **Funcionalidade**: Todos os comandos CLI funcionam
- [ ] **Qualidade**: Docs geradas são úteis e bem estruturadas
- [ ] **Performance**: Dry-run rápido, filtros eficientes
- [ ] **Manutenibilidade**: Código modular, testes passando
- [ ] **Usabilidade**: Comandos intuitivos, help claro
- [ ] **YAGNI**: Zero over-engineering, implementação incremental

---

**🎯 Status Atual: PLANO YAGNI REFORMULADO**
**📅 Próximo Passo: Implementar Fase 1 - Infraestrutura Core**
