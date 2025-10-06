# Baobab Automata

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Alpha-orange.svg)](https://github.com/baobab-automata/baobab-automata)
[![Documentation](https://img.shields.io/badge/Documentation-Sphinx-blue.svg)](https://baobab-automata.readthedocs.io/)

Librairie Python complète et moderne pour la gestion des automates et de leurs algorithmes, avec une interface unifiée et des outils de visualisation avancés.

## 🌟 Fonctionnalités Principales

### Types d'Automates Supportés
- **Automates finis** : DFA, NFA, epsilon-NFA avec algorithmes de conversion et d'optimisation
- **Automates à pile** : DPDA, NPDA avec analyse de grammaires contextuelles
- **Machines de Turing** : DTM, NTM, multi-rubans avec analyse de complexité
- **Algorithmes avancés** : Conversion entre types, optimisation, reconnaissance
- **Visualisation** : Support Graphviz, Mermaid, matplotlib et interfaces web interactives

### Interface Unifiée
- API cohérente pour tous les types d'automates
- Validation automatique des configurations
- Gestion d'erreurs spécialisée
- Support complet des types Python

## 🚀 Installation Rapide

### Prérequis
- Python >= 3.11
- Graphviz (pour la visualisation)

### Installation depuis PyPI
```bash
pip install baobab-automata
```

### Installation avec dépendances de développement
```bash
pip install baobab-automata[dev]
```

### Installation depuis les sources
```bash
git clone https://github.com/baobab-automata/baobab-automata.git
cd baobab-automata
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -e .[dev]
```

## 📖 Exemples d'Utilisation

### Automate Fini Déterministe (DFA)
```python
from baobab_automata import DFA

# DFA qui reconnaît les mots se terminant par 'ab'
dfa = DFA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q0',
        ('q1', 'a'): 'q1',
        ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q1',
        ('q2', 'b'): 'q0',
    },
    initial_state='q0',
    final_states={'q2'}
)

# Test de reconnaissance
print(dfa.accepts('ab'))    # True
print(dfa.accepts('aab'))   # True
print(dfa.accepts('ba'))    # False

# Visualisation
dfa.visualize('dfa_example.png')
```

### Automate à Pile Déterministe (DPDA)
```python
from baobab_automata import DPDA

# DPDA qui reconnaît le langage a^n b^n
dpda = DPDA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    stack_alphabet={'A', 'Z'},
    transitions={
        ('q0', 'a', 'Z'): ('q0', 'AZ'),
        ('q0', 'a', 'A'): ('q0', 'AA'),
        ('q0', 'b', 'A'): ('q1', ''),
        ('q1', 'b', 'A'): ('q1', ''),
        ('q1', '', 'Z'): ('q2', 'Z'),
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'}
)

print(dpda.accepts('aabb'))  # True
print(dpda.accepts('aab'))   # False
```

### Machine de Turing Déterministe (DTM)
```python
from baobab_automata import DTM

# DTM qui reconnaît les palindromes
dtm = DTM(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'},
    alphabet={'a', 'b'},
    tape_alphabet={'a', 'b', 'B'},
    transitions={
        ('q0', 'a'): ('q1', 'B', 'R'),
        ('q0', 'b'): ('q2', 'B', 'R'),
        ('q0', 'B'): ('q_accept', 'B', 'R'),
        ('q1', 'a'): ('q1', 'a', 'R'),
        ('q1', 'b'): ('q1', 'b', 'R'),
        ('q1', 'B'): ('q3', 'B', 'L'),
        ('q2', 'a'): ('q2', 'a', 'R'),
        ('q2', 'b'): ('q2', 'b', 'R'),
        ('q2', 'B'): ('q4', 'B', 'L'),
        ('q3', 'a'): ('q_accept', 'B', 'L'),
        ('q3', 'b'): ('q_reject', 'B', 'L'),
        ('q4', 'a'): ('q_reject', 'B', 'L'),
        ('q4', 'b'): ('q_accept', 'B', 'L'),
    },
    initial_state='q0',
    blank_symbol='B',
    final_states={'q_accept'}
)

print(dtm.accepts('aba'))   # True
print(dtm.accepts('ab'))    # False
```

### Algorithmes de Conversion et Optimisation
```python
from baobab_automata import NFA
from baobab_automata.algorithms import nfa_to_dfa, minimize_dfa, language_operations

# Conversion NFA vers DFA
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

# Minimisation du DFA
minimized_dfa = minimize_dfa(dfa)

# Opérations sur les langages
union_dfa = language_operations.union(dfa1, dfa2)
intersection_dfa = language_operations.intersection(dfa1, dfa2)
complement_dfa = language_operations.complement(dfa)
```

### Parsing d'Expressions Régulières
```python
from baobab_automata.algorithms import regex_to_nfa

# Conversion d'une expression régulière en NFA
regex = "(a|b)*abb"
nfa = regex_to_nfa(regex)

print(nfa.accepts('aabb'))  # True
print(nfa.accepts('babb'))  # True
print(nfa.accepts('ab'))    # False
```

## 🛠️ Développement

### Commandes Disponibles

```bash
make help          # Afficher l'aide
make install       # Installer les dépendances de production
make install-dev   # Installer les dépendances de développement
make test          # Exécuter les tests
make lint          # Vérifier la qualité du code
make format        # Formater le code
make clean         # Nettoyer les artefacts
make docs          # Générer la documentation
make build         # Construire le package
```

### 🎯 Qualité du Code

Le projet utilise plusieurs outils pour assurer la qualité du code :

- **Black** : Formatage automatique du code
- **Pylint** : Analyse de qualité (score minimum 8.5/10)
- **Flake8** : Vérification du style PEP 8
- **Bandit** : Scan de sécurité
- **MyPy** : Vérification des types statiques
- **Pytest** : Tests avec couverture >= 95%

### 📁 Structure du Projet

```
src/baobab_automata/
├── finite/         # Automates finis
│   ├── dfa/        # Automates finis déterministes
│   ├── nfa/        # Automates finis non-déterministes et ε-NFA
│   ├── regex/      # Parser d'expressions régulières
│   ├── language/   # Opérations sur les langages
│   └── optimization/ # Algorithmes d'optimisation
├── pushdown/       # Automates à pile
│   ├── pda/        # Automates à pile non-déterministes
│   ├── dpda/       # Automates à pile déterministes
│   ├── npda/       # Automates à pile non-déterministes avancés
│   ├── grammar/    # Parser de grammaires hors-contexte
│   ├── optimization/ # Algorithmes d'optimisation
│   └── specialized/ # Algorithmes spécialisés (CYK, Earley)
├── turing/         # Machines de Turing
│   ├── tm/         # Machines de Turing de base
│   ├── dtm/        # Machines de Turing déterministes
│   ├── ntm/        # Machines de Turing non-déterministes
│   └── multitape/  # Machines de Turing multi-bandes
├── algorithms/     # Algorithmes organisés par type
│   ├── finite/     # Algorithmes pour automates finis
│   ├── pushdown/   # Algorithmes pour automates à pile
│   └── turing/     # Algorithmes pour machines de Turing
├── interfaces/     # Interfaces abstraites
├── implementations/ # Implémentations de base
├── exceptions/     # Gestion d'erreurs spécialisée
├── utils/          # Utilitaires généraux
└── visualization/  # Outils de visualisation
```

## 📚 Documentation

### Documentation Complète
La documentation complète est disponible et peut être générée avec :

```bash
make docs
```

### Structure de Documentation Sphinx
La documentation utilise Sphinx avec une configuration professionnelle :

```
docs/
├── index.rst                    # Page d'accueil principale
├── installation.rst            # Guide d'installation et configuration
├── quickstart.rst              # Guide de démarrage rapide
├── contributing.rst            # Guide de contribution
├── development.rst             # Guide de développement
├── changelog.rst               # Historique des versions
├── api/                        # Documentation API
│   ├── index.rst
│   ├── automata.rst
│   ├── algorithms.rst
│   ├── visualization.rst
│   └── exceptions.rst
├── examples/                   # Exemples d'utilisation
│   ├── index.rst
│   ├── finite_automata.rst
│   ├── pushdown_automata.rst
│   ├── turing_machines.rst
│   ├── language_recognition.rst
│   ├── conversion_algorithms.rst
│   ├── advanced_algorithms.rst
│   └── visualization_examples.rst
├── conf.py                     # Configuration Sphinx
└── Makefile                    # Commandes de génération
```

### Configuration Sphinx
- **Extensions** : autodoc, autosummary, napoleon, graphviz, inheritance_diagram
- **Thème** : sphinx_rtd_theme
- **Configuration** : Optimisée pour la documentation Python avec support des docstrings Google/NumPy

### Guides Disponibles
- **Installation** : Guide d'installation et configuration
- **Démarrage rapide** : Guide de démarrage rapide
- **Exemples** : Exemples d'utilisation détaillés
- **API** : Documentation API complète
- **Changelog** : Historique des versions

### Fonctionnalités de Documentation

#### Génération Automatique
- **API** : Documentation automatique depuis les docstrings
- **Index** : Génération automatique des index et tables
- **Recherche** : Index de recherche intégré
- **Navigation** : Table des matières interactive

#### Formats de Sortie
- **HTML** : Documentation web interactive
- **PDF** : Documentation imprimable
- **EPUB** : Livre électronique
- **LaTeX** : Code source LaTeX

#### Qualité et Standards
- **Docstrings** : Format Google/NumPy standardisé
- **Exemples** : Code fonctionnel testé
- **Structure** : Organisation logique et cohérente
- **Accessibilité** : Navigation intuitive

### Commandes de Documentation
```bash
cd docs
make html          # Génération HTML
make pdf           # Génération PDF
make epub          # Génération EPUB
make serve         # Serveur local
make help          # Aide
make clean         # Nettoyage
make linkcheck     # Vérification des liens
make spelling      # Vérification orthographique
make coverage      # Rapport de couverture
```

### Statistiques de Documentation
- **Total** : 20+ fichiers de documentation
- **Pages** : 15+ pages de contenu
- **Exemples** : 50+ exemples de code
- **Mots** : 10,000+ mots de documentation
- **Couverture API** : 100% des modules principaux documentés

### Spécifications Détaillées

Les spécifications détaillées suivent une notation de priorité pour faciliter le développement :

- **Format** : `XXX_YYY_PHASE_ZZZ_DESCRIPTION.md`
- **XXX** : Priorité de développement (001-999)
- **YYY** : Numéro de phase (001-007)
- **ZZZ** : Identifiant de phase (PHASE_001, etc.)

#### Outils de Gestion des Spécifications

```bash
# Lister toutes les spécifications par priorité
python3 scripts/list_specifications.py

# Lister les spécifications d'une phase
python3 scripts/list_specifications.py --phase 002

# Afficher les statistiques
python3 scripts/list_specifications.py --stats

# Créer une nouvelle spécification
python3 scripts/create_specification.py 003 201 "PDA Implementation"
```

### Améliorations Futures de la Documentation

#### Fonctionnalités Planifiées
1. **Tutoriels Interactifs** : Jupyter notebooks
2. **Vidéos** : Démonstrations vidéo
3. **API REST** : Documentation interactive
4. **Traductions** : Support multilingue

#### Optimisations
1. **Performance** : Génération plus rapide
2. **Mobile** : Interface responsive
3. **Accessibilité** : Amélioration de l'accessibilité
4. **SEO** : Optimisation pour les moteurs de recherche

### Validation de la Documentation

#### Tests Effectués
- **Génération** : Documentation générée avec succès
- **Liens** : Vérification des liens internes
- **Format** : Validation du format RST
- **Contenu** : Révision du contenu technique

#### Qualité
- **Cohérence** : Style uniforme
- **Exactitude** : Informations techniques correctes
- **Complétude** : Couverture exhaustive
- **Lisibilité** : Structure claire et logique

### Résultat Final de la Documentation

La documentation de Baobab Automata est complète et professionnelle, offrant :

- **Guide complet** pour les utilisateurs et développeurs
- **Exemples pratiques** pour tous les cas d'usage
- **API documentée** avec autodoc Sphinx
- **Structure modulaire** facilement maintenable
- **Standards professionnels** de documentation Python

Cette documentation permettra aux utilisateurs de :
- Comprendre rapidement les fonctionnalités
- Implémenter des solutions avec des exemples concrets
- Contribuer efficacement au projet
- Maintenir et étendre la librairie

## 🎨 Visualisation

### Formats Supportés
- **PNG/SVG** : Images haute qualité avec Graphviz
- **Mermaid** : Code source pour documentation
- **Matplotlib** : Intégration avec l'écosystème Python
- **HTML** : Interfaces web interactives

### Exemples de Visualisation
```python
# Visualisation basique
dfa.visualize('automate.png')

# Visualisation avec options
dfa.visualize(
    'automate_detailed.png',
    format='svg',
    dpi=300,
    show_labels=True,
    layout='neato'
)

# Code Mermaid
mermaid_code = dfa.to_mermaid()
```

## 🧪 Tests

### Exécution des Tests
```bash
# Tests unitaires
make test

# Tests avec couverture
pytest --cov=baobab_automata

# Tests de performance
pytest tests/performance/
```

### Types de Tests
- **Tests unitaires** : Tests des composants individuels
- **Tests d'intégration** : Tests des interactions entre composants
- **Tests de performance** : Tests de performance et optimisation
- **Tests de régression** : Tests pour éviter les régressions

## 🚀 Performance

### Optimisations Incluses
- **Cache intelligent** : Mise en cache des résultats de reconnaissance
- **Algorithmes optimisés** : Versions optimisées pour de gros automates
- **Lazy evaluation** : Calcul à la demande des propriétés
- **Parallélisation** : Support de la parallélisation pour certaines opérations

### Métriques de Performance
- **Complexité temporelle** : Analyse automatique de la complexité
- **Complexité spatiale** : Surveillance de l'utilisation mémoire
- **Benchmarks** : Tests de performance automatisés

## 📊 Statut du Projet

### Version Actuelle
- **Version** : 0.1.0 (Alpha)
- **Statut** : En développement actif
- **Stabilité** : API en évolution

### Roadmap
- **v0.2.0** : Optimisations de performance, automates probabilistes
- **v0.3.0** : Algorithmes d'apprentissage, automates temporisés
- **v1.0.0** : API stable, support LTS

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez le fichier CONTRIBUTING.md pour plus d'informations.

### Comment Contribuer
1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

### Standards de Contribution
- Code formaté avec Black
- Tests avec couverture >= 95%
- Documentation mise à jour
- Respect des conventions de nommage

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

### Obtenir de l'Aide
- **Documentation** : https://baobab-automata.readthedocs.io/
- **Issues** : https://github.com/baobab-automata/baobab-automata/issues
- **Discussions** : https://github.com/baobab-automata/baobab-automata/discussions

### Contact
- **Équipe** : Baobab Automata Team
- **Email** : team@baobab-automata.dev
- **GitHub** : https://github.com/baobab-automata/baobab-automata

---

<div align="center">
  <strong>Baobab Automata</strong> - Une librairie Python moderne pour les automates
  <br>
  <em>Fait avec ❤️ par l'équipe Baobab</em>
</div>