Guide de Développement
========================

Ce guide s'adresse aux développeurs qui souhaitent contribuer au projet Baobab Automata.

Architecture du projet
-----------------------

Structure des modules
~~~~~~~~~~~~~~~~~~~~~~

Le projet suit une architecture modulaire claire :

.. code-block:: text

   src/baobab_automata/
   ├── __init__.py              # Point d'entrée principal
   ├── core/                    # Interfaces et classes de base
   │   ├── __init__.py
   │   └── base.py
   ├── interfaces/              # Définitions d'interfaces
   │   ├── __init__.py
   │   ├── automaton.py
   │   ├── recognizer.py
   │   ├── converter.py
   │   ├── state.py
   │   └── transition.py
   ├── implementations/         # Implémentations concrètes
   │   ├── __init__.py
   │   ├── state.py
   │   └── transition.py
   ├── finite/                  # Automates finis
   │   ├── __init__.py
   │   ├── dfa.py
   │   ├── nfa.py
   │   ├── epsilon_nfa.py
   │   ├── optimization_algorithms.py
   │   ├── conversion_algorithms.py
   │   ├── language_operations.py
   │   └── regex_parser.py
   ├── pushdown/               # Automates à pile
   │   ├── __init__.py
   │   ├── dpda.py
   │   ├── npda.py
   │   ├── conversion_algorithms.py
   │   ├── optimization_algorithms.py
   │   └── grammar_parser.py
   ├── turing/                 # Machines de Turing
   │   ├── __init__.py
   │   ├── dtm.py
   │   ├── ntm.py
   │   ├── multi_tape_tm.py
   │   └── complexity_analysis.py
   ├── algorithms/             # Algorithmes généraux
   │   ├── __init__.py
   │   ├── conversion_algorithms.py
   │   ├── optimization_algorithms.py
   │   └── specialized_algorithms.py
   ├── visualization/           # Outils de visualisation
   │   ├── __init__.py
   │   ├── graphviz_renderer.py
   │   ├── mermaid_generator.py
   │   └── interactive_plot.py
   ├── exceptions/             # Gestion d'erreurs
   │   ├── __init__.py
   │   ├── base.py
   │   ├── finite_exceptions.py
   │   ├── pushdown_exceptions.py
   │   └── turing_exceptions.py
   └── utils/                  # Utilitaires
       ├── __init__.py
       ├── validation.py
       └── generation.py

Conventions de code
--------------------

Style de code
~~~~~~~~~~~~~~

Le projet suit les conventions Python standard :

* **PEP 8** : Style de code Python standard
* **Black** : Formatage automatique (longueur de ligne 88)
* **Type hints** : Annotations de type obligatoires
* **Docstrings** : Documentation Google/NumPy style

**Exemple de style** :

.. code-block:: python

   from typing import Set, Dict, Tuple, Optional, Union
   from abc import ABC, abstractmethod

   class IAutomaton(ABC):
       """Interface de base pour tous les automates.
       
       Cette interface définit les méthodes communes à tous les types
       d'automates dans Baobab Automata.
       
       Attributes:
           states: Ensemble des états de l'automate
           alphabet: Alphabet d'entrée
           transitions: Fonction de transition
           initial_state: État initial
           final_states: États finaux
       """
       
       def __init__(
           self,
           states: Set[str],
           alphabet: Set[str],
           transitions: Dict[Tuple[str, str], Union[str, Set[str]]],
           initial_state: str,
           final_states: Set[str]
       ) -> None:
           """Initialise l'automate.
           
           Args:
               states: Ensemble des états
               alphabet: Alphabet d'entrée
               transitions: Fonction de transition
               initial_state: État initial
               final_states: États finaux
               
           Raises:
               InvalidAutomatonError: Si l'automate est invalide
           """
           self.states = states
           self.alphabet = alphabet
           self.transitions = transitions
           self.initial_state = initial_state
           self.final_states = final_states
           
           if not self.is_valid():
               raise InvalidAutomatonError("Configuration d'automate invalide")
       
       @abstractmethod
       def accepts(self, input_string: str) -> bool:
           """Vérifie si une chaîne est acceptée par l'automate.
           
           Args:
               input_string: La chaîne à tester
               
           Returns:
               True si la chaîne est acceptée, False sinon
               
           Raises:
               RecognitionError: Si une erreur survient pendant la reconnaissance
           """
           pass
       
       def is_valid(self) -> bool:
           """Valide la configuration de l'automate.
           
           Returns:
               True si l'automate est valide, False sinon
           """
           return (
               self.initial_state in self.states and
               self.final_states.issubset(self.states) and
               all(
                   state in self.states and symbol in self.alphabet
                   for (state, symbol) in self.transitions.keys()
               )
           )

Nommage
~~~~~~~~

* **Classes** : PascalCase (ex: `DFA`, `NPDA`)
* **Interfaces** : Préfixe `I` + PascalCase (ex: `IAutomaton`)
* **Fonctions** : snake_case (ex: `nfa_to_dfa`)
* **Variables** : snake_case (ex: `initial_state`)
* **Constantes** : UPPER_CASE (ex: `MAX_STATES`)
* **Modules** : snake_case (ex: `conversion_algorithms`)

Tests
------

Structure des tests
~~~~~~~~~~~~~~~~~~~~

Les tests sont organisés selon la structure du code source :

.. code-block:: text

   tests/
   ├── __init__.py
   ├── conftest.py              # Configuration pytest
   ├── baobab_automata/         # Tests des modules principaux
   │   ├── __init__.py
   │   ├── exceptions/
   │   ├── implementations/
   │   └── interfaces/
   ├── finite/                  # Tests des automates finis
   │   ├── __init__.py
   │   ├── test_dfa.py
   │   ├── test_nfa.py
   │   ├── test_epsilon_nfa.py
   │   ├── test_conversion_algorithms.py
   │   ├── test_optimization_algorithms.py
   │   └── test_language_operations.py
   ├── pushdown/               # Tests des automates à pile
   │   ├── __init__.py
   │   ├── test_dpda.py
   │   ├── test_npda.py
   │   └── test_conversion_algorithms.py
   ├── turing/                 # Tests des machines de Turing
   │   ├── __init__.py
   │   ├── test_dtm.py
   │   ├── test_ntm.py
   │   └── test_multi_tape_tm.py
   ├── integration/            # Tests d'intégration
   │   ├── __init__.py
   │   └── test_integration.py
   ├── performance/            # Tests de performance
   │   ├── __init__.py
   │   └── test_performance.py
   └── unit/                   # Tests unitaires supplémentaires
       ├── __init__.py
       └── test_*.py

Écriture de tests
~~~~~~~~~~~~~~~~~~

**Exemple de test unitaire** :

.. code-block:: python

   import pytest
   from baobab_automata import DFA
   from baobab_automata.exceptions import InvalidAutomatonError

   class TestDFA:
       """Tests pour la classe DFA."""
       
       def test_valid_dfa_creation(self):
           """Test la création d'un DFA valide."""
           dfa = DFA(
               states={'q0', 'q1'},
               alphabet={'a', 'b'},
               transitions={('q0', 'a'): 'q1'},
               initial_state='q0',
               final_states={'q1'}
           )
           
           assert dfa.states == {'q0', 'q1'}
           assert dfa.alphabet == {'a', 'b'}
           assert dfa.initial_state == 'q0'
           assert dfa.final_states == {'q1'}
       
       def test_invalid_initial_state(self):
           """Test la création d'un DFA avec état initial invalide."""
           with pytest.raises(InvalidAutomatonError):
               DFA(
                   states={'q0', 'q1'},
                   alphabet={'a', 'b'},
                   transitions={('q0', 'a'): 'q1'},
                   initial_state='q_invalid',
                   final_states={'q1'}
               )
       
       def test_accepts_valid_string(self):
           """Test la reconnaissance d'une chaîne valide."""
           dfa = DFA(
               states={'q0', 'q1'},
               alphabet={'a', 'b'},
               transitions={('q0', 'a'): 'q1'},
               initial_state='q0',
               final_states={'q1'}
           )
           
           assert dfa.accepts('a')
       
       def test_accepts_invalid_string(self):
           """Test la reconnaissance d'une chaîne invalide."""
           dfa = DFA(
               states={'q0', 'q1'},
               alphabet={'a', 'b'},
               transitions={('q0', 'a'): 'q1'},
               initial_state='q0',
               final_states={'q1'}
           )
           
           assert not dfa.accepts('b')
           assert not dfa.accepts('aa')
       
       @pytest.mark.parametrize("input_string,expected", [
           ('a', True),
           ('b', False),
           ('aa', False),
           ('ab', False),
       ])
       def test_accepts_parametrized(self, input_string, expected):
           """Test paramétré de la reconnaissance."""
           dfa = DFA(
               states={'q0', 'q1'},
               alphabet={'a', 'b'},
               transitions={('q0', 'a'): 'q1'},
               initial_state='q0',
               final_states={'q1'}
           )
           
           assert dfa.accepts(input_string) == expected

**Exemple de test d'intégration** :

.. code-block:: python

   import pytest
   from baobab_automata import NFA, DFA
   from baobab_automata.algorithms import nfa_to_dfa, minimize_dfa

   class TestConversionIntegration:
       """Tests d'intégration pour les conversions."""
       
       def test_nfa_to_dfa_conversion(self):
           """Test la conversion NFA vers DFA."""
           nfa = NFA(
               states={'q0', 'q1', 'q2'},
               alphabet={'a', 'b'},
               transitions={
                   ('q0', 'a'): {'q0', 'q1'},
                   ('q1', 'b'): {'q2'},
               },
               initial_state='q0',
               final_states={'q2'}
           )
           
           dfa = nfa_to_dfa(nfa)
           
           # Vérifier que les langages sont identiques
           test_strings = ['ab', 'aab', 'aaab', 'b', 'ba']
           for string in test_strings:
               assert nfa.accepts(string) == dfa.accepts(string)
       
       def test_minimization_pipeline(self):
           """Test le pipeline de minimisation."""
           dfa = DFA(
               states={'q0', 'q1', 'q2', 'q3'},
               alphabet={'a', 'b'},
               transitions={
                   ('q0', 'a'): 'q1',
                   ('q0', 'b'): 'q2',
                   ('q1', 'a'): 'q3',
                   ('q1', 'b'): 'q2',
                   ('q2', 'a'): 'q1',
                   ('q2', 'b'): 'q3',
                   ('q3', 'a'): 'q3',
                   ('q3', 'b'): 'q3'),
               },
               initial_state='q0',
               final_states={'q3'}
           )
           
           minimal_dfa = minimize_dfa(dfa)
           
           # Vérifier que la minimisation réduit le nombre d'états
           assert len(minimal_dfa.states) <= len(dfa.states)
           
           # Vérifier que les langages sont identiques
           test_strings = ['aa', 'bb', 'ab', 'ba', 'aab', 'bba']
           for string in test_strings:
               assert dfa.accepts(string) == minimal_dfa.accepts(string)

Exécution des tests
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Tests unitaires
   pytest tests/unit/

   # Tests d'intégration
   pytest tests/integration/

   # Tests de performance
   pytest tests/performance/

   # Tests avec couverture
   pytest --cov=baobab_automata --cov-report=html

   # Tests en parallèle
   pytest -n auto

   # Tests avec marqueurs
   pytest -m "not slow"

Qualité du code
----------------

Outils utilisés
~~~~~~~~~~~~~~~~

* **Black** : Formatage automatique
* **Pylint** : Analyse de qualité (score minimum 8.5/10)
* **Flake8** : Vérification du style PEP 8
* **Bandit** : Scan de sécurité
* **MyPy** : Vérification des types statiques
* **Pre-commit** : Hooks de pré-commit

Configuration
~~~~~~~~~~~~~~

**pyproject.toml** :

.. code-block:: toml

   [tool.black]
   line-length = 88
   target-version = ['py311']
   include = '\.pyi?$'

   [tool.pylint.messages_control]
   disable = [
       "C0114",  # missing-module-docstring
       "C0115",  # missing-class-docstring
       "C0116",  # missing-function-docstring
   ]

   [tool.pylint.format]
   max-line-length = 121

   [tool.mypy]
   python_version = "3.11"
   warn_return_any = true
   disallow_untyped_defs = true
   strict_equality = true

Commandes de qualité
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Formatage automatique
   black src/ tests/

   # Analyse de qualité
   pylint src/baobab_automata/

   # Vérification du style
   flake8 src/ tests/

   # Scan de sécurité
   bandit -r src/

   # Vérification des types
   mypy src/baobab_automata/

   # Toutes les vérifications
   make lint

Documentation
--------------

Standards de documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Docstrings** : Style Google/NumPy
* **Type hints** : Obligatoires pour toutes les fonctions publiques
* **Exemples** : Dans les docstrings des fonctions complexes
* **README** : Mis à jour avec chaque nouvelle fonctionnalité

**Exemple de docstring** :

.. code-block:: python

   def nfa_to_dfa(nfa: NFA) -> DFA:
       """Convertit un automate fini non-déterministe en automate fini déterministe.
       
       Cette fonction implémente l'algorithme de construction de sous-ensembles
       pour convertir un NFA en DFA équivalent.
       
       Args:
           nfa: L'automate fini non-déterministe à convertir
           
       Returns:
           Un automate fini déterministe équivalent
           
       Raises:
           ConversionError: Si la conversion échoue
           InvalidAutomatonError: Si le NFA d'entrée est invalide
           
       Example:
           >>> nfa = NFA(
           ...     states={'q0', 'q1'},
           ...     alphabet={'a', 'b'},
           ...     transitions={('q0', 'a'): {'q0', 'q1'}},
           ...     initial_state='q0',
           ...     final_states={'q1'}
           ... )
           >>> dfa = nfa_to_dfa(nfa)
           >>> dfa.accepts('a')
           True
           
       Note:
           La complexité temporelle est O(2^n) où n est le nombre d'états du NFA.
           Pour de gros NFA, considérez l'optimisation préalable.
       """
       if not nfa.is_valid():
           raise InvalidAutomatonError("Le NFA d'entrée est invalide")
       
       # Implémentation de l'algorithme de construction de sous-ensembles
       # ...
       
       return dfa

Génération de documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Génération de la documentation
   make docs

   # Documentation en mode développement
   make dev

   # Vérification des liens
   make linkcheck

   # Vérification orthographique
   make spelling

Workflow de développement
-------------------------

Processus de contribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Fork** du repository
2. **Clone** de votre fork
3. **Création** d'une branche feature
4. **Développement** avec tests
5. **Validation** de la qualité du code
6. **Commit** avec messages descriptifs
7. **Push** vers votre fork
8. **Pull Request** avec description détaillée

**Exemple de workflow** :

.. code-block:: bash

   # Fork et clone
   git clone https://github.com/votre-username/baobab-automata.git
   cd baobab-automata

   # Création d'une branche feature
   git checkout -b feature/nouvelle-fonctionnalite

   # Développement
   # ... modifications du code ...

   # Tests
   pytest tests/

   # Qualité du code
   make lint

   # Commit
   git add .
   git commit -m "feat: ajouter nouvelle fonctionnalité

   - Implémentation de la fonctionnalité X
   - Ajout de tests unitaires
   - Mise à jour de la documentation
   
   Fixes #123"

   # Push
   git push origin feature/nouvelle-fonctionnalite

   # Créer une Pull Request sur GitHub

Conventions de commit
~~~~~~~~~~~~~~~~~~~~~~

Utilisez le format Conventional Commits :

* **feat** : Nouvelle fonctionnalité
* **fix** : Correction de bug
* **docs** : Documentation
* **style** : Formatage, point-virgules manquants, etc.
* **refactor** : Refactoring du code
* **test** : Ajout de tests
* **chore** : Maintenance

**Exemples** :

.. code-block:: bash

   feat: ajouter support des automates probabilistes
   fix: corriger bug dans la minimisation DFA
   docs: mettre à jour la documentation API
   test: ajouter tests pour la conversion NFA->DFA
   refactor: optimiser l'algorithme de reconnaissance
   chore: mettre à jour les dépendances

Gestion des versions
---------------------

Versioning sémantique
~~~~~~~~~~~~~~~~~~~~~~

Le projet suit le versioning sémantique (SemVer) :

* **MAJOR** : Changements incompatibles
* **MINOR** : Nouvelles fonctionnalités compatibles
* **PATCH** : Corrections de bugs compatibles

**Exemples** :
* `1.0.0` → `2.0.0` : Changement majeur (breaking changes)
* `1.0.0` → `1.1.0` : Nouvelle fonctionnalité
* `1.0.0` → `1.0.1` : Correction de bug

Changelog
~~~~~~~~~~

Le fichier `CHANGELOG.md` suit le format Keep a Changelog :

.. code-block:: markdown

   ## [1.1.0] - 2024-02-15

   ### Ajouté
   - Support des automates probabilistes
   - Nouvelle API de visualisation interactive
   - Algorithmes d'optimisation avancés

   ### Modifié
   - Amélioration des performances de reconnaissance
   - Refactoring de l'API de conversion

   ### Corrigé
   - Correction du bug de minimisation DFA
   - Résolution des fuites mémoire dans la visualisation

Déploiement
------------

Pipeline CI/CD
~~~~~~~~~~~~~~~

Le projet utilise GitHub Actions pour :

* **Tests** : Exécution automatique des tests
* **Qualité** : Vérification de la qualité du code
* **Documentation** : Génération et déploiement de la documentation
* **Release** : Publication automatique des versions

**Exemple de workflow** :

.. code-block:: yaml

   name: CI/CD Pipeline

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main ]

   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: [3.11, 3.12]
       
       steps:
       - uses: actions/checkout@v3
       - name: Set up Python ${{ matrix.python-version }}
         uses: actions/setup-python@v3
         with:
           python-version: ${{ matrix.python-version }}
       
       - name: Install dependencies
         run: |
           pip install -e .[dev]
       
       - name: Run tests
         run: |
           pytest --cov=baobab_automata --cov-report=xml
       
       - name: Upload coverage
         uses: codecov/codecov-action@v3

     quality:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       - name: Set up Python
         uses: actions/setup-python@v3
         with:
           python-version: 3.11
       
       - name: Install dependencies
         run: |
           pip install -e .[dev]
       
       - name: Run linting
         run: |
           black --check src/ tests/
           flake8 src/ tests/
           pylint src/baobab_automata/
           mypy src/baobab_automata/

     docs:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       - name: Set up Python
         uses: actions/setup-python@v3
         with:
           python-version: 3.11
       
       - name: Install dependencies
         run: |
           pip install -e .[dev]
       
       - name: Build documentation
         run: |
           cd docs
           make docs
       
       - name: Deploy to GitHub Pages
         uses: peaceiris/actions-gh-pages@v3
         with:
           github_token: ${{ secrets.GITHUB_TOKEN }}
           publish_dir: docs/_build/html

Publication
~~~~~~~~~~~~

**Processus de release** :

1. **Mise à jour** du version dans `pyproject.toml`
2. **Mise à jour** du `CHANGELOG.md`
3. **Création** d'un tag Git
4. **Publication** sur PyPI
5. **Mise à jour** de la documentation

**Commandes** :

.. code-block:: bash

   # Mise à jour de la version
   bump2version patch  # ou minor, major

   # Création du tag
   git tag v1.1.0
   git push origin v1.1.0

   # Publication sur PyPI
   python -m build
   twine upload dist/*

Débogage
---------

Outils de débogage
~~~~~~~~~~~~~~~~~~~

* **pdb** : Débogueur Python intégré
* **ipdb** : Version améliorée de pdb
* **pytest-debugging** : Intégration avec pytest
* **logging** : Logging structuré

**Exemple de débogage** :

.. code-block:: python

   import logging
   from baobab_automata import DFA

   # Configuration du logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   logger = logging.getLogger(__name__)

   def debug_automaton(automaton, input_string):
       """Fonction de débogage pour les automates."""
       logger.debug(f"Test de '{input_string}' sur l'automate")
       logger.debug(f"États: {automaton.states}")
       logger.debug(f"Alphabet: {automaton.alphabet}")
       logger.debug(f"Transitions: {automaton.transitions}")
       
       try:
           result = automaton.accepts(input_string)
           logger.debug(f"Résultat: {result}")
           return result
       except Exception as e:
           logger.error(f"Erreur: {e}")
           raise

Profiling
~~~~~~~~~~

**Outils de profiling** :

* **cProfile** : Profiling de performance
* **memory_profiler** : Profiling mémoire
* **line_profiler** : Profiling ligne par ligne

**Exemple** :

.. code-block:: python

   import cProfile
   from baobab_automata.algorithms import nfa_to_dfa

   def profile_conversion():
       """Profile la conversion NFA vers DFA."""
       # Créer un gros NFA pour le test
       nfa = create_large_nfa()
       
       # Profiling
       profiler = cProfile.Profile()
       profiler.enable()
       
       dfa = nfa_to_dfa(nfa)
       
       profiler.disable()
       profiler.dump_stats('conversion_profile.prof')
       
       # Analyser les résultats
       import pstats
       stats = pstats.Stats('conversion_profile.prof')
       stats.sort_stats('cumulative')
       stats.print_stats(10)

Conseils de développement
-------------------------

* **Commencez petit** : Implémentez d'abord les cas simples
* **Testez tôt** : Écrivez les tests en même temps que le code
* **Documentez** : Documentez vos fonctions et classes
* **Optimisez après** : Concentrez-vous d'abord sur la justesse
* **Réutilisez** : Utilisez les interfaces et classes existantes
* **Validez** : Validez toujours les entrées et sorties
* **Gérez les erreurs** : Implémentez une gestion d'erreurs robuste
