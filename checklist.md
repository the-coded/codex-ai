# 🚀 Codex-AI - Checklist de Migração

## 📊 Progress Overview
- [x] **Fase 1**: Setup e Migração (100%) ✅
- [ ] **Fase 2**: Core Implementation (0%)  
- [ ] **Fase 3**: Commands Implementation (0%)
- [ ] **Fase 4**: Templates e AI Integration (0%)
- [ ] **Fase 5**: Testing e Validation (0%)
- [ ] **Fase 6**: Documentation e Cleanup (0%)

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
- [x] `requirements.txt` ✅
- [x] `requirements-dev.txt` ✅
- [x] Todos os `__init__.py` dos pacotes ✅
- [x] Sistema de configuração hierárquica ✅
- [x] Tokens específicos por modelo AI ✅
- [x] CLI funcional com comando `uidocs` ✅
- [x] README.md atualizado ✅

---

## ⚙️ **FASE 2: Core Implementation**

### 2.1 Constants
- [ ] `constants/__init__.py`
- [ ] `constants/timetrack.py`
  - [ ] FILE_TYPE_MULTIPLIERS
  - [ ] COMMIT_TYPE_MULTIPLIERS
  - [ ] COMPLEXITY_THRESHOLDS
  - [ ] STRUCTURAL_PATTERNS
  - [ ] ALGORITHMIC_PATTERNS
- [ ] `constants/git.py`
  - [ ] CONVENTIONAL_COMMIT_TYPES
  - [ ] EXCLUDE_PATTERNS
  - [ ] GIT_COMMANDS
  - [ ] GIT_STATUS_COMMANDS (staged, modified, untracked)
  - [ ] GIT_DIFF_COMMANDS (since_commit, branch_range)
- [ ] `constants/files.py`
  - [ ] FILE_CATEGORIES
  - [ ] SPECIAL_EXTENSIONS
  - [ ] LANGUAGE_MAP
- [ ] `constants/ai.py`
  - [ ] AI_MODELS (Sonnet-4, Sonnet-3.7, Sonnet-3.5)
  - [ ] TOKEN_STRATEGY
  - [ ] AIDER_DEFAULTS
- [ ] `constants/output.py`
  - [ ] OUTPUT_FORMATS
  - [ ] EMOJIS
  - [ ] COLORS
  - [ ] REPORT_TEMPLATES

### 2.2 Core Modules
- [ ] `core/__init__.py`
- [ ] `core/git/`
  - [ ] `__init__.py`
  - [ ] `log_analyzer.py` (port de bin/git_log_*.sh)
  - [ ] `release_analyzer.py` (port de bin/git_release_*.sh)
  - [ ] `tree_generator.py` (port de bin/tree_*.sh)
  - [ ] `commit_parser.py`
  - [ ] `changes_tracker.py`
- [ ] `core/time/`
  - [ ] `__init__.py`
  - [ ] `calculator.py` (port do JS timetracker)
  - [ ] `complexity_analyzer.py` (port do JS)
  - [ ] `report_generator.py` (port do JS)
  - [ ] `algorithms.py`
- [ ] `core/ai/`
  - [ ] `__init__.py`
  - [ ] `model_selector.py`
  - [ ] `aider_interface.py`
  - [ ] `token_manager.py`
  - [ ] `prompt_processor.py`
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
  - [ ] `utils/__init__.py`
  - [ ] `utils/get_base_path.py`
  - [ ] `utils/load_json.py`
  - [ ] `utils/load_template.py`
  - [ ] `utils/get_token_count.py`
- [ ] Novos utils:
  - [ ] `utils/logger.py`
  - [ ] `utils/file_utils.py`
  - [ ] `utils/env_loader.py` (.env support)
  - [ ] `utils/subprocess_utils.py`
  - [ ] `utils/path_utils.py`
  - [ ] `utils/validation.py`
  - [ ] `utils/git_utils.py` (git operations for uidocs modes)

---

## 🎯 **FASE 3: Commands Implementation**

### 3.1 Commands Structure
- [ ] `commands/__init__.py`
- [ ] `commands/base.py` (se necessário)

### 3.2 Individual Commands
- [ ] `commands/changelog.py`
  - [ ] Argument parsing
  - [ ] Git log analysis
  - [ ] AI model selection
  - [ ] Aider integration
  - [ ] Output generation
- [ ] `commands/timetrack.py`
  - [ ] Commit analysis (port do JS)
  - [ ] Time calculation
  - [ ] Report generation
  - [ ] Multiple output formats
- [ ] `commands/uidocs.py`
  - [ ] Mode detection (local vs pipeline vs auto)
  - [ ] Local mode: staged/modified files detection
  - [ ] Pipeline mode: git diff analysis
  - [ ] File filtering and type detection
  - [ ] React/Sass/Storybook processing
  - [ ] AI integration
- [ ] `commands/analyze.py`
  - [ ] Project structure analysis (port dos tree_*.sh)
  - [ ] Git changes analysis
  - [ ] Complexity analysis
  - [ ] Report generation

---

## 📝 **FASE 4: Templates e AI Integration**

### 4.1 Markdown Templates
- [ ] `templates/prompts/`
  - [ ] `changelog_prompt.md`
  - [ ] `uidocs_react_prompt.md`
  - [ ] `uidocs_sass_prompt.md`
  - [ ] `uidocs_storybook_prompt.md`
  - [ ] `analysis_prompt.md`
- [ ] `templates/outputs/`
  - [ ] `changelog_template.md`
  - [ ] `timetrack_report_template.md`
  - [ ] `docs_template.md`
- [ ] `templates/README.md`

### 4.2 AI Integration
- [ ] Token counting e management
- [ ] Auto-seleção git_log (detailed vs simple)
- [ ] Model fallback strategy (Sonnet-4 → 3.7 → 3.5)
- [ ] Aider command generation
- [ ] Error handling e retry logic

### 4.3 Output Formatters
- [ ] `formatters/__init__.py`
- [ ] `formatters/time.py`
- [ ] `formatters/git.py`
- [ ] `formatters/docs.py`
- [ ] `formatters/base.py`
- [ ] Support para JSON, YAML, Markdown, HTML

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
- [ ] Update main README.md
- [ ] CLI usage examples
- [ ] Configuration guide (.env + config files)
- [ ] Migration guide (old → new)
- [ ] Troubleshooting guide

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

*Updated: 2025-01-23*  
*Progress: Fase 1 completa - 15/100+ tasks completed (15%)*
