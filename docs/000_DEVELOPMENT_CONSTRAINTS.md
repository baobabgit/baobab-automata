# Contraintes de développement

## Technologie

- **Version Python** : Python >= 3.11
- **Environnement virtuel** : Placé dans le dossier `.venv`
- **Architecture orientée objet** : Un fichier = une classe
- **Structure des sources** : Dossier `src/` pour le code source
- **Structure des tests** : Dossier `tests/` pour les tests unitaires
- **Correspondance tests/sources** : Une classe = une classe de tests unitaires
- **Tests des classes abstraites** : Utilisation de classes concrètes pour tester les classes abstraites

## Documentation

- **Format des docstrings** : reStructuredText pour toutes les fonctions, classes et modules
- **Contenu des docstrings** : Documentation complète des paramètres, valeurs de retour et exceptions
- **Exemples d'utilisation** : Inclus dans les docstrings
- **Génération automatique** : Documentation générée avec Sphinx

## Journal de développement

- **Fichier de journal** : `docs/000_DEV_DIARY.md`
- **Contenu obligatoire** : Pour chaque modification du code :
  - Description de la modification
  - Justification (pourquoi)
  - Méthode (comment)
  - Date et heure
- **Fréquence** : À chaque modification du code

## Gestion des environnements

- **Fichier de configuration** : `pyproject.toml`
- **Environnements définis** :
  - Développement
  - Production

## Architecture des dossiers

### Dossier `docs/`

- **Notation des fichiers** : Nombre sur 3 chiffres suivi d'un underscore
- **Reprise de numérotation** : À chaque sous-dossier, la numérotation reprend à 001
- **Format des spécifications** : Markdown pour cahier des charges, phases, spécifications et spécifications détaillées

### Cahier des charges

- **Emplacement** : `docs/SPECIFICATIONS.md`
- **Contenu** : Cahier des charges exhaustif
- **Format** : Markdown

### Phases de développement

- **Emplacement** : `docs/phases/`
- **Notation** : `XXX_PHASE_YYY.md` où XXX est le numéro de fichier et YYY le numéro de phase (3 digits)
- **Contenu** : Spécifications à implémenter et méthodes d'implémentation

### Spécifications détaillées

- **Emplacement** : `docs/detailed_specifications/`
- **Notation** : `XXX_PHASE_YYY_` suivi du nom de la spécification détaillée
- **Cible** : Agents IA de développement
- **Focus** : Un détail spécifique par agent
- **Objectif** : Fonctionnement indépendant et parallèle des agents
- **Interfaces** : Classes interfaces pour les dépendances entre agents

### Dossiers spécialisés

- **Couverture de code** : `docs/coverage/`
- **Fichiers de configuration** : `conf/` (avec sous-dossiers autorisés)
- **Scripts** : `scripts/` (avec sous-dossiers autorisés)

## Formatage et qualité du code

### Outils de formatage

- **Black** : Formatage automatique du code
- **Pylint** : Analyse de la qualité du code
  - Score minimum requis : 8.5/10
- **Flake8** : Vérification du style de code et détection d'erreurs de syntaxe
- **Configuration** : Règles de codage strictes (PEP 8)

### Environnement virtuel

- **Utilisation obligatoire** : Toujours utiliser l'environnement virtuel Python
- **Emplacement** : `.venv/`
- **Création automatique** : Si l'environnement n'existe pas, le créer

### Sécurité

- **Bandit** : Scan de sécurité pour détecter les vulnérabilités communes en Python
- **Tolérance** : Aucune vulnérabilité critique ou haute tolérée
- **Gestion sécurisée** : Chemins de fichiers et entrées utilisateur sécurisés

## Structure de fichiers requise

```
/workspace/
├── .venv/                          # Environnement virtuel Python
├── src/                            # Code source (une classe par fichier)
├── tests/                          # Tests unitaires (structure miroir de src/)
├── docs/                           # Documentation
│   ├── 000_DEV_DIARY.md           # Journal de développement
│   ├── SPECIFICATIONS.md          # Cahier des charges
│   ├── phases/                     # Phases de développement
│   ├── detailed_specifications/   # Spécifications détaillées
│   └── coverage/                   # Rapports de couverture de code
├── conf/                           # Fichiers de configuration
├── scripts/                        # Scripts utilitaires
└── pyproject.toml                  # Configuration des environnements
```

## Règles de développement

1. **Une classe par fichier** : Respect strict de la règle un fichier = une classe
2. **Tests obligatoires** : Chaque classe doit avoir sa classe de test correspondante
3. **Documentation complète** : Toutes les fonctions, classes et modules doivent être documentés
4. **Journal de développement** : Toute modification doit être loggée
5. **Qualité du code** : Score Pylint minimum de 8.5/10
6. **Sécurité** : Aucune vulnérabilité critique ou haute
7. **Environnement virtuel** : Utilisation obligatoire de l'environnement virtuel
8. **Formatage** : Code formaté avec Black et conforme à PEP 8