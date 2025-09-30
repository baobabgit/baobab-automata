# Spécification Détaillée - Infrastructure Setup

## Agent IA Cible
Agent de développement spécialisé dans la configuration d'infrastructure et d'environnements de développement Python.

## Objectif
Configurer l'infrastructure complète du projet Baobab Automata selon les contraintes de développement définies.

## Spécifications Techniques

### 1. Configuration pyproject.toml

#### 1.1 Structure de Base
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "baobab-automata"
version = "0.1.0"
description = "Librairie Python complète pour la gestion des automates et de leurs algorithmes"
authors = [{name = "Baobab Team", email = "team@baobab-automata.org"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
```

#### 1.2 Dépendances de Production
```toml
dependencies = [
    "numpy>=1.24.0",
    "graphviz>=0.20.0",
    "matplotlib>=3.7.0",
    "plotly>=5.15.0",
    "pydantic>=2.0.0",
    "typing-extensions>=4.5.0",
]
```

#### 1.3 Dépendances de Développement
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
    "black>=23.0.0",
    "pylint>=2.17.0",
    "flake8>=6.0.0",
    "bandit>=1.7.0",
    "mypy>=1.5.0",
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "pre-commit>=3.3.0",
]
```

#### 1.4 Environnements
```toml
[tool.setuptools]
packages = ["baobab_automata"]

[tool.setuptools.package-dir]
baobab_automata = "src/baobab_automata"
```

### 2. Configuration des Outils de Qualité

#### 2.1 Black (Formatage)
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

#### 2.2 Pylint (Analyse de Qualité)
```toml
[tool.pylint.messages_control]
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
]

[tool.pylint.format]
max-line-length = 88

[tool.pylint.design]
max-args = 10
max-locals = 15
max-branches = 12
max-statements = 50
max-attributes = 10
max-public-methods = 20
max-bool-expr = 5

[tool.pylint.similarities]
min-similarity-lines = 4
ignore-comments = true
ignore-docstrings = true
ignore-imports = false
```

#### 2.3 Flake8 (Style de Code)
```toml
[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "build",
    "dist",
    ".eggs",
    "*.egg-info",
]
per-file-ignores = [
    "__init__.py:F401",
]
```

#### 2.4 Bandit (Sécurité)
```toml
[tool.bandit]
exclude_dirs = ["tests", ".venv"]
skips = ["B101", "B601"]
```

#### 2.5 MyPy (Vérification des Types)
```toml
[tool.mypy]
python_version = "3.11"
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
module = [
    "graphviz.*",
    "matplotlib.*",
    "plotly.*",
    "numpy.*",
]
ignore_missing_imports = true
```

### 3. Configuration des Tests

#### 3.1 Pytest
```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=baobab_automata",
    "--cov-report=term-missing",
    "--cov-report=html:docs/coverage",
    "--cov-report=xml:docs/coverage/coverage.xml",
    "--cov-fail-under=95",
]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "performance: Performance tests",
    "slow: Slow tests",
]
```

### 4. Configuration Sphinx

#### 4.1 conf.py
```python
# Configuration file for the Sphinx documentation builder
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'Baobab Automata'
copyright = '2024, Baobab Team'
author = 'Baobab Team'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}
```

### 5. Structure des Dossiers

#### 5.1 Dossier src/
```
src/
└── baobab_automata/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── interfaces.py
    │   ├── base.py
    │   └── exceptions.py
    ├── finite/
    │   ├── __init__.py
    │   ├── dfa.py
    │   ├── nfa.py
    │   └── epsilon_nfa.py
    ├── pushdown/
    │   ├── __init__.py
    │   ├── pda.py
    │   ├── dpda.py
    │   └── npda.py
    ├── turing/
    │   ├── __init__.py
    │   ├── tm.py
    │   ├── dtm.py
    │   ├── ntm.py
    │   └── multi_tape_tm.py
    ├── algorithms/
    │   ├── __init__.py
    │   ├── conversion.py
    │   ├── optimization.py
    │   └── recognition.py
    ├── visualization/
    │   ├── __init__.py
    │   ├── graphviz.py
    │   ├── mermaid.py
    │   └── web.py
    └── utils/
        ├── __init__.py
        ├── validation.py
        └── helpers.py
```

#### 5.2 Dossier tests/
```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   ├── test_core/
│   ├── test_finite/
│   ├── test_pushdown/
│   ├── test_turing/
│   ├── test_algorithms/
│   ├── test_visualization/
│   └── test_utils/
├── integration/
│   ├── __init__.py
│   └── test_workflows.py
└── performance/
    ├── __init__.py
    └── test_benchmarks.py
```

### 6. Scripts de Développement

#### 6.1 Makefile
```makefile
.PHONY: help install install-dev test lint format clean docs build

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Build documentation"
	@echo "  build        Build package"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	pylint src/ tests/
	flake8 src/ tests/
	bandit -r src/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf docs/_build/
	rm -rf docs/coverage/

docs:
	cd docs && make html

build:
	python -m build
```

### 7. Pre-commit Hooks

#### 7.1 .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## Critères de Validation

### 1. Configuration
- [ ] pyproject.toml valide et complet
- [ ] Tous les outils de qualité configurés
- [ ] Environnement virtuel fonctionnel
- [ ] Dépendances installées correctement

### 2. Structure
- [ ] Structure des dossiers respectée
- [ ] Fichiers __init__.py présents
- [ ] Makefile fonctionnel
- [ ] Pre-commit hooks installés

### 3. Qualité
- [ ] Black formate le code correctement
- [ ] Pylint score >= 8.5/10
- [ ] Flake8 passe sans erreur
- [ ] Bandit ne détecte aucune vulnérabilité critique/haute
- [ ] MyPy valide les types

### 4. Tests
- [ ] Pytest fonctionne
- [ ] Couverture de code >= 95%
- [ ] Tests unitaires passent
- [ ] Configuration de test valide

## Exemples d'Utilisation

### Installation
```bash
# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances de développement
make install-dev
```

### Développement
```bash
# Formater le code
make format

# Lancer les tests
make test

# Lancer le linting
make lint

# Construire la documentation
make docs
```

## Notes d'Implémentation

1. **Environnement virtuel** : Toujours utiliser `.venv/` comme spécifié
2. **Python 3.11+** : Configuration stricte pour la version minimale
3. **Qualité** : Score Pylint >= 8.5/10 obligatoire
4. **Sécurité** : Aucune vulnérabilité Bandit critique/haute
5. **Tests** : Couverture >= 95% obligatoire
6. **Documentation** : Sphinx configuré pour génération automatique