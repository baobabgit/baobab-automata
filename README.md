# Baobab Automata

Librairie Python complète pour la gestion des automates et de leurs algorithmes.

## Description

Baobab Automata est une librairie Python moderne et complète qui fournit une interface unifiée pour travailler avec différents types d'automates :

- **Automates finis** : DFA, NFA, epsilon-NFA
- **Automates à pile** : DPDA, NPDA
- **Machines de Turing** : DTM, NTM, multi-rubans
- **Algorithmes** : Conversion, optimisation, reconnaissance
- **Visualisation** : Graphviz, Mermaid, interfaces web

## Installation

### Prérequis

- Python >= 3.11
- pip

### Installation de développement

```bash
# Cloner le repository
git clone <repository-url>
cd baobab-automata

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances de développement
make install-dev
```

### Installation de production

```bash
pip install baobab-automata
```

## Utilisation

```python
from baobab_automata import DFA, NFA, TuringMachine

# Créer un automate fini déterministe
dfa = DFA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'a'): 'q1',
        ('q1', 'b'): 'q2',
    },
    initial_state='q0',
    final_states={'q2'}
)

# Vérifier si une chaîne est acceptée
result = dfa.accepts('ab')
print(result)  # True
```

## Développement

### Commandes disponibles

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

### Qualité du code

Le projet utilise plusieurs outils pour assurer la qualité du code :

- **Black** : Formatage automatique
- **Pylint** : Analyse de qualité (score minimum 8.5/10)
- **Flake8** : Vérification du style PEP 8
- **Bandit** : Scan de sécurité
- **MyPy** : Vérification des types
- **Pytest** : Tests avec couverture >= 95%

### Structure du projet

```
src/baobab_automata/
├── core/           # Interfaces et classes de base
├── finite/         # Automates finis
├── pushdown/       # Automates à pile
├── turing/         # Machines de Turing
├── algorithms/     # Algorithmes
├── visualization/  # Outils de visualisation
└── utils/          # Utilitaires
```

## Documentation

La documentation complète est disponible dans le dossier `docs/` et peut être générée avec :

```bash
make docs
```

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! Veuillez consulter le fichier CONTRIBUTING.md pour plus d'informations.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur le repository GitHub.