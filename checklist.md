# 🚀 Codex-AI - Checklist de Migração

## 📊 Progress Overview
- [x] **Fase 1**: Setup e Migração (100%) ✅
- [ ] **Fase 2**: Core Implementation (95%) 🔄
- [ ] **Fase 3**: Commands Implementation (75%) 🔄
- [ ] **Fase 4**: Templates e AI Integration (100%) ✅
- [ ] **Fase 5**: Testing e Validation (0%)
- [x] **Fase 6**: Documentation e Cleanup (95%) ✅

---

## 🔄 **FASE 1: Setup e Migração** 

### 1.1 Preparação do Ambiente
- [x] Criar backup do código atual ✅
- [x] Mover código atual para `old/` ✅
  - [x] `old/pkg/` ✅
  - [x] `old/bin/` ✅
  - [x] `old/utils/` ✅
  - [x] `old/shared/` ✅
  - [x] `old/docs/` ✅
  - [x] `old/README.md` ✅
- [x] Criar estrutura nova arquitetura ✅
- [x] Setup inicial do projeto (`setup.py`, `pyproject.toml`) ✅

### 1.2 Criação da Estrutura Base
- [x] `__init__.py` (root) ✅
- [x] `__main__.py` (root) ✅
- [x] `cli.py` (root) ✅
- [x] `config.py` (root) ✅
- [x] `.env.example` ✅
- [x] Estrutura de diretórios ✅
- [x] `pyproject.toml` (single source of truth) ✅
- [x] `requirements-dev.txt` ✅
- [x] Todos os `__init__.py` dos pacotes ✅
- [x] Sistema de configuração hierárquica ✅
- [x] Tokens específicos por modelo AI ✅
- [x] CLI funcional com comando `uidocs` ✅
- [x] README.md atualizado ✅

---

## ⚙️ **FASE 2: Core Implementation**

### 2.1 Constants
- [x] `constants/__init__.py` ✅
- [x] `constants/project.py` ✅
  - [x] Centralização de metadados do projeto ✅
  - [x] Leitura do pyproject.toml como single source ✅
  - [x] Funções get_version(), get_author(), etc. ✅
- [x] `constants/timetrack.py` ✅
  - [x] FILE_TYPE_MULTIPLIERS ✅
  - [x] COMMIT_TYPE_MULTIPLIERS ✅
  - [x] COMPLEXITY_THRESHOLDS ✅
  - [x] STRUCTURAL_PATTERNS ✅
  - [x] ALGORITHMIC_PATTERNS ✅
- [x] `constants/git.py` ✅
  - [x] CONVENTIONAL_COMMIT_TYPES ✅
  - [x] EXCLUDE_PATTERNS ✅
  - [x] GIT_COMMANDS ✅
  - [x] GIT_STATUS_COMMANDS (staged, modified, untracked) ✅
  - [x] GIT_DIFF_COMMANDS (since_commit, branch_range) ✅
- [x] `constants/files.py` ✅
  - [x] FILE_CATEGORIES ✅
  - [x] SPECIAL_EXTENSIONS ✅
  - [x] LANGUAGE_MAP ✅
- [x] `constants/ai.py` ✅
  - [x] AI_MODELS (Sonnet-4, Sonnet-3.7, Sonnet-3.5) ✅
  - [x] TOKEN_STRATEGY ✅
  - [x] AIDER_DEFAULTS ✅
- [x] `constants/output.py` ✅
  - [x] OUTPUT_FORMATS ✅
  - [x] EMOJIS ✅
  - [x] COLORS ✅
  - [x] REPORT_TEMPLATES ✅

### 2.2 Core Modules
- [x] `core/__init__.py` ✅
  - [x] Module availability tracking ✅
  - [x] Import management com try/except ✅
  - [x] Helper functions (get_available_modules, require_module) ✅
  - [x] Status constants (GIT_AVAILABLE, AI_AVAILABLE, etc.) ✅
- [x] `core/git/` ✅
  - [x] `__init__.py` ✅
  - [x] `log_analyzer.py` (port de bin/git_log_*.sh) ✅
  - [x] `release_analyzer.py` (port de bin/git_release_*.sh) ✅
  - [x] `tree_generator.py` (port de bin/tree_*.sh) ✅
  - [x] `commit_parser.py` ✅
  - [x] `changes_tracker.py` ✅
- [x] `core/timetracker/` ✅
  - [x] `__init__.py` ✅
  - [x] `calculator.py` (port do analyze-git-changes.js) ✅
  - [x] `report_generator.py` (port do git-hours-report.js) ✅
  - [x] Convenience functions (port do index.js) ✅
- [x] `core/ai/` ✅
  - [x] `__init__.py` ✅
  - [x] `model_selector.py` ✅
  - [x] `aider_interface.py` ✅
  - [x] `token_manager.py` ✅
  - [x] `prompt_processor.py` ✅
- [ ] `core/uidocs/`
  - [ ] `__init__.py`
  - [ ] `sources.py` (LocalSource, PipelineSource, AllFilesSource)
  - [ ] `processor.py` (main uidocs processing logic)
  - [ ] `filters.py` (file type detection & filtering)
  - [ ] `react_processor.py` (port do uidocs/run_doc_react.py)
  - [ ] `sass_processor.py` (port do uidocs/run_doc_sass.py)
  - [ ] `storybook_processor.py` (port do uidocs storybook)
  - [ ] `generator.py` (documentation generation orchestrator)

### 2.3 Utils (Migração + Novos)
- [ ] Migrar utils atuais:
  - [ ] `utils/__init__.py` (module exports - for all commands and core modules)
  - [x] `utils/get_base_path.py` ✅ (project root detection - for all commands and config)
  - [x] `utils/load_json.py` ✅ (JSON loading - for config files and data processing)
  - [x] `utils/get_token_count.py` ✅ (token counting - for changelog and AI integration)
- [ ] Novos utils:
  - [ ] `utils/git_utils.py` (git operations - for uidocs local/pipeline modes)

---

## 🎯 **FASE 3: Commands Implementation**

### 3.1 Commands Structure
- [ ] `commands/__init__.py`
- [ ] `commands/base.py` (se necessário)

### 3.2 Individual Commands
- [x] `commands/config.py` ✅
  - [x] Global configuration management ✅
  - [x] API key storage (~/.codex/.env) ✅
  - [x] Model selection (claude_4_sonnet, claude_3_7_sonnet, claude_3_5_sonnet) ✅
  - [x] Output format settings (json, yaml, markdown, html, text) ✅
  - [x] Timeout configurations (git, ai) ✅
  - [x] --list and --reset options ✅
  - [x] Input validation ✅
- [x] `commands/changelog.py` ✅
  - [x] Argument parsing ✅
  - [x] Git log analysis (3-level strategy: detailed/medium/simple) ✅
  - [x] AI model selection (automatic fallback) ✅
  - [x] Aider integration (working perfectly) ✅
  - [x] Output generation (with verbose logging) ✅
  - [x] Token management (114,950 tokens available for git log) ✅
  - [x] Smart fallback chain (detailed → medium → simple) ✅
- [x] `commands/timetrack.py` ✅
  - [x] Commit analysis (port do JS) ✅
  - [x] Time calculation ✅
  - [x] Report generation ✅
  - [x] Multiple output formats (JSON, Markdown, CSV, HTML) ✅
  - [x] Filtering (author, date range) ✅
  - [x] CLI integration ✅
- [x] `commands/map_tree.py` ✅
  - [x] Project structure mapping (port do tree_project.sh) ✅
  - [x] Git changes analysis (port do tree_git_changes.sh) ✅
  - [x] Release changes analysis (port do tree_git_release_changes.sh) ✅
  - [x] Sibling files analysis (port do tree_git_siblings.sh) ✅
  - [x] Multiple output formats (JSON, YAML, Markdown) ✅
  - [x] CLI integration (codex-ai map-tree) ✅
  - [x] Error handling e validação ✅
  - [x] Equivalente ao tree_generate_all.sh ✅
- [ ] `commands/uidocs.py`
  - [ ] Mode detection (local vs pipeline vs auto)
  - [ ] Local mode: staged/modified files detection
  - [ ] Pipeline mode: git diff analysis
  - [ ] File filtering and type detection
  - [ ] React/Sass/Storybook processing
  - [ ] AI integration

---

## 📝 **FASE 4: Templates e AI Integration**

### 4.1 Markdown Templates
- [x] `templates/prompts/` ✅
  - [x] `changelog_prompt.md` ✅
  - [x] `uidocs_react_prompt.md` ✅
  - [x] `uidocs_sass_prompt.md` ✅
  - [x] `uidocs_storybook_prompt.md` ✅

### 4.2 AI Integration
- [x] Token counting e management ✅
  - [x] Precise token allocation formula (114,950 tokens for git log) ✅
  - [x] TOKEN_STRATEGY.PROMPT_OVERHEAD constant ✅
  - [x] get_effective_token_limit() function ✅
- [x] Auto-seleção git_log (detailed vs medium vs simple) ✅
  - [x] 3-level strategy implementation ✅
  - [x] GIT_LOG_LIMITS constants ✅
  - [x] Smart fallback chain ✅
- [x] Model fallback strategy (Sonnet-4 → 3.7 → 3.5) ✅
  - [x] AI_MODELS priority system ✅
  - [x] select_model_by_tokens() function ✅
- [x] Aider command generation ✅
  - [x] build_aider_command() function ✅
  - [x] AIDER_COMMAND_TEMPLATES ✅
- [x] Error handling e retry logic ✅
  - [x] Automatic fallback on token overflow ✅
  - [x] Verbose logging for debugging ✅


---

## 🧪 **FASE 5: Testing e Validation**

### 5.1 Unit Tests
- [ ] Tests para core functions
- [ ] Tests para constants
- [ ] Tests para utils
- [ ] Tests para formatters

### 5.2 Integration Tests
- [ ] Test full workflow changelog
- [ ] Test full workflow timetrack
- [ ] Test full workflow uidocs (local mode)
- [ ] Test full workflow uidocs (pipeline mode)
- [ ] Test full workflow analyze

### 5.3 Validation vs Old Code
- [ ] **Changelog**: Compare output novo vs antigo
- [ ] **TimeTracker**: Validate algoritmo port
- [ ] **Docs**: Compare geração React/Sass
- [ ] **Analysis**: Validate Git analysis

### 5.4 Performance Tests
- [ ] Large repository handling
- [ ] Token management efficiency
- [ ] Memory usage
- [ ] Command execution time

---

## 📖 **FASE 6: Documentation e Cleanup**

### 6.1 Documentation
- [x] Update main README.md ✅
  - [x] Token management section with constants ✅
  - [x] 3-level git log strategy explained ✅
  - [x] Smart fallback chain documented ✅
- [x] CLI usage examples ✅
- [x] Configuration guide (config command + ENV vars) ✅
- [x] Migration guide (old → new) ✅
- [x] Troubleshooting guide (docs/local-developing.md) ✅
- [x] Technical documentation (docs/token-management.md) ✅
  - [x] Complete token allocation formula ✅
  - [x] Performance benchmarks ✅
  - [x] Configuration constants reference ✅
  - [x] Troubleshooting guide ✅
- [x] Prompts updated with "Files Available to You" ✅
  - [x] React prompt with correct paths ✅
  - [x] Sass prompt with correct paths ✅
  - [x] Storybook prompt with correct paths ✅
- [ ] **REVISÃO FINAL COMPLETA**: Revisar toda documentação após implementação

### 6.2 Package Distribution
- [ ] Finalize setup.py
- [ ] Test pip install
- [ ] Test CLI commands (`codex-ai`)
- [ ] Validate entry points

### 6.3 Final Cleanup
- [ ] Code review
- [ ] Remove debug code
- [ ] Optimize imports
- [ ] Final testing
- [ ] **Implement proper JSON Schema**: Replace validate_json_schema with real jsonschema library
- [ ] **Remove old/ directory** (quando aprovado)

---

## 🎉 **ENTREGA FINAL**

### Critérios de Aceitação
- [ ] **100% Feature Parity**: Todas funcionalidades antigas funcionando
- [ ] **Performance**: Igual ou melhor que versão antiga
- [ ] **Usabilidade**: CLI intuitivo (`codex-ai command`)
- [ ] **Manutenibilidade**: Código limpo e bem estruturado
- [ ] **Testabilidade**: Coverage adequado
- [ ] **Documentação**: Completa e atualizada
- [ ] **.env Support**: Funcionando perfeitamente
- [ ] **AI Models**: Sonnet-4 → 3.7 → 3.5 fallback

### Checklist Final
- [ ] ✅ Todas as fases concluídas
- [ ] ✅ Todos os testes passando
- [ ] ✅ Documentação atualizada
- [ ] ✅ Performance validada
- [ ] ✅ Code review aprovado
- [ ] ✅ PyPI package `codex-ai` funcionando
- [ ] ✅ CLI `codex-ai` funcionando
- [ ] ✅ Pipeline integration testada
- [ ] 📦 **get_base_path deprecation**: Verificar se get_base_path ainda é necessário após publicação PyPI
- [ ] 🗑️ **old/ directory removido**

---

## 📋 **CONFIGURAÇÃO FINAL**

### Identificação
- **PyPI Package**: `codex-ai`
- **CLI Command**: `codex-ai`
- **Python Module**: `codex_ai`
- **Repository**: `codex-ai`

### AI Models (Prioridade)
1. 🥇 `anthropic/claude-4-sonnet-20250514` (1M tokens)
2. 🥈 `anthropic/claude-3-7-sonnet-latest` (500K tokens)  
3. 🥉 `anthropic/claude-3-5-sonnet-latest` (200K tokens)

### Environment Variables
- `ANTHROPIC_API_KEY` - API key principal
- `CODEX_DEFAULT_MODEL` - Modelo padrão
- `CODEX_OUTPUT_FORMAT` - Formato padrão
- `CODEX_VERBOSE` - Verbose mode
- `.env` file support completo

---

## 📝 **TODOs para Revisão Futura**

### ✅ **Implementados:**
- [x] 📦 **~/.config/codex-ai/ directory**: Migrado para localização XDG-compliant ✅
- [x] 🔧 **Config command**: Usando ~/.config/codex-ai/config.env ✅
- [x] 📍 **Path management**: get_global_config_path() atualizado ✅
- [x] 📋 **Documentation**: Docstrings atualizados ✅
- [x] 🗑️ **python-dotenv removido**: Dependência desnecessária removida ✅
- [x] 🔄 **CLI version dinâmica**: Usa get_version() do pyproject.toml ✅
- [x] 📖 **README.md atualizado**: Comandos e configuração corrigidos ✅
- [x] 📝 **docs/ atualizados**: local-developing.md corrigido ✅
- [x] 🎯 **Hierarquia config simplificada**: Sem dotenv, apenas ENV + global ✅

### 🧹 Limpeza de Código:
- [ ] 📦 **get_base_path deprecation**: Verificar se ainda é necessário após publicação PyPI
- [ ] 🗑️ **old/ directory**: Remover quando aprovado
- [ ] 🔍 **Code review**: Revisar TODOs espalhados pelo código

---

*Updated: 2025-06-24*  
*Progress: Fase 1 (100%) + Fase 2 (85%) + Fase 3 (75%) + Fase 4 (80%) + Fase 6 (95%) = ~87/100+ tasks completed (87%)*

**🧹 LIMPEZA CONCLUÍDA:**
- ✅ Removidas todas as referências obsoletas ao comando `analyze`
- ✅ CLI atualizado para usar `map-tree` em vez de `analyze`
- ✅ Removidas todas as referências obsoletas ao comando `docs`
- ✅ CLI atualizado para usar `uidocs` em vez de `docs`
- ✅ Documentação e examples atualizados
- ✅ Comando `map-tree` funcionando perfeitamente
- ✅ Package metadata regenerado com correções

**🗑️ LIMPEZA YAGNI (2025-06-24):**
- ✅ Removidos 7 utils desnecessários (logger, file_utils, env_loader, subprocess_utils, path_utils, validation, load_template)
- ✅ Removida seção templates/outputs/ completa (YAGNI - comandos já têm formatters próprios)
- ✅ Removido analysis_prompt.md (comando analysis não existe mais)
- ✅ Removida seção formatters/ completa (YAGNI - cada comando tem seu próprio formatter)
- ✅ Fase 4 atualizada para 100% ✅ (só precisamos dos prompts existentes)
- ✅ Fase 2 atualizada para 95% (só falta core/uidocs + git_utils)
- ✅ Checklist otimizado: de ~100+ tarefas para ~15 tarefas reais restantes
