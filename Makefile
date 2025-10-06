.PHONY: test test-unit test-integration test-performance test-coverage test-all test-watch clean

# Variables
PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
COVERAGE := $(VENV)/bin/coverage

# Installation des dépendances
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	$(PIP) install pytest pytest-cov pytest-watch black pylint flake8 bandit

# Tests
test:
	$(PYTEST)

test-unit:
	$(PYTEST) -m unit

test-integration:
	$(PYTEST) -m integration

test-performance:
	$(PYTEST) -m performance

test-slow:
	$(PYTEST) -m slow

test-coverage:
	$(PYTEST) --cov=baobab_automata --cov-report=html:docs/coverage

test-all:
	$(PYTEST) -m "unit or integration or performance"

test-watch:
	$(PYTEST) --watch

# Qualité du code
format:
	$(VENV)/bin/black src/ tests/

lint:
	$(VENV)/bin/pylint src/ tests/

flake8:
	$(VENV)/bin/flake8 src/ tests/

security:
	$(VENV)/bin/bandit -r src/ -f json -o docs/bandit/bandit_report.json

quality: format lint flake8 security

# Nettoyage
clean:
	rm -rf $(VENV)
	rm -rf docs/coverage/
	rm -rf docs/bandit/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Développement
dev: install
	@echo "Environnement de développement prêt!"
	@echo "Utilisez 'make test' pour exécuter les tests"
	@echo "Utilisez 'make quality' pour vérifier la qualité du code"

# Spécifications
specs-list:
	$(PYTHON) scripts/list_specifications.py

specs-stats:
	$(PYTHON) scripts/list_specifications.py --stats

specs-phase:
	@echo "Usage: make specs-phase PHASE=<numéro>"
	@echo "Exemple: make specs-phase PHASE=002"
	$(PYTHON) scripts/list_specifications.py --phase $(PHASE)

# Aide
help:
	@echo "Commandes disponibles:"
	@echo "  install      - Installe les dépendances"
	@echo "  test         - Exécute tous les tests"
	@echo "  test-unit    - Exécute les tests unitaires"
	@echo "  test-integration - Exécute les tests d'intégration"
	@echo "  test-performance - Exécute les tests de performance"
	@echo "  test-slow    - Exécute les tests lents"
	@echo "  test-coverage - Exécute les tests avec couverture"
	@echo "  test-all     - Exécute tous les types de tests"
	@echo "  test-watch   - Exécute les tests en mode watch"
	@echo "  format       - Formate le code avec Black"
	@echo "  lint         - Vérifie le code avec Pylint"
	@echo "  flake8       - Vérifie le code avec Flake8"
	@echo "  security     - Vérifie la sécurité avec Bandit"
	@echo "  quality      - Exécute tous les contrôles de qualité"
	@echo "  clean        - Nettoie les fichiers temporaires"
	@echo "  dev          - Configure l'environnement de développement"
	@echo "  specs-list   - Liste toutes les spécifications par priorité"
	@echo "  specs-stats  - Affiche les statistiques des spécifications"
	@echo "  specs-phase  - Liste les spécifications d'une phase (PHASE=<numéro>)"
	@echo "  help         - Affiche cette aide"