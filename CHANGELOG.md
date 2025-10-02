# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté
- Documentation complète avec Sphinx
- Guide d'installation et configuration
- Exemples d'utilisation pour tous les types d'automates
- API de visualisation avancée
- Support des thèmes de visualisation
- Export vers formats multiples (PNG, SVG, PDF, GIF)
- Visualisation interactive avec Plotly
- Comparaison visuelle d'automates
- Analyse de performance et métriques
- Documentation API complète

### Modifié
- Amélioration du README.md avec exemples détaillés
- Restructuration de la documentation
- Optimisation des algorithmes de visualisation

### Corrigé
- Corrections mineures dans la documentation

## [0.1.0] - 2024-01-15

### Ajouté
- Implémentation complète des automates finis (DFA, NFA, Epsilon-NFA)
- Implémentation des automates à pile (DPDA, NPDA)
- Implémentation des machines de Turing (DTM, NTM, MultiTapeTM)
- Algorithmes de conversion entre types d'automates
- Algorithmes d'optimisation (minimisation, suppression d'états)
- Opérations sur les langages (union, intersection, complément)
- Parser d'expressions régulières
- Parser de grammaires contextuelles
- Système de visualisation avec Graphviz
- Export vers formats Mermaid et JSON
- Gestion complète des exceptions
- Tests unitaires et d'intégration
- Configuration de qualité du code (Black, Pylint, Flake8, Bandit, MyPy)
- Support Python 3.11+

### Fonctionnalités principales

#### Automates finis
- **DFA** : Automate fini déterministe avec reconnaissance rapide
- **NFA** : Automate fini non-déterministe avec support des transitions multiples
- **Epsilon-NFA** : Support des epsilon-transitions pour les expressions régulières

#### Automates à pile
- **DPDA** : Automate à pile déterministe pour les langages contextuels
- **NPDA** : Automate à pile non-déterministe avec analyse de grammaires
- Conversion PDA ↔ Grammaire contextuelle

#### Machines de Turing
- **DTM** : Machine de Turing déterministe
- **NTM** : Machine de Turing non-déterministe
- **MultiTapeTM** : Support des machines multi-rubans
- Analyse de complexité temporelle et spatiale

#### Algorithmes
- Conversion NFA ↔ DFA
- Minimisation d'automates finis
- Suppression d'états inaccessibles et morts
- Opérations sur les langages (union, intersection, complément)
- Parsing d'expressions régulières
- Parsing de grammaires contextuelles

#### Visualisation
- Génération de graphiques avec Graphviz
- Export vers formats multiples (PNG, SVG, PDF)
- Génération de code Mermaid
- Visualisation interactive
- Comparaison d'automates

#### Qualité et tests
- Couverture de tests >= 95%
- Score Pylint >= 8.5/10
- Vérification de sécurité avec Bandit
- Vérification de types avec MyPy
- Formatage automatique avec Black

## [0.0.1] - 2024-01-01

### Ajouté
- Structure initiale du projet
- Interfaces de base pour les automates
- Implémentations de base des états et transitions
- Configuration du projet avec pyproject.toml
- Structure des tests
- Documentation de base

---

## Notes de version

### Version 0.1.0
Cette version marque la première release stable de Baobab Automata avec toutes les fonctionnalités principales implémentées et testées.

**Points forts :**
- Implémentation complète de tous les types d'automates
- API unifiée et cohérente
- Visualisation avancée
- Documentation complète
- Qualité de code élevée

**Compatibilité :**
- Python >= 3.11
- Compatible avec les systèmes Linux, macOS et Windows
- Support Unicode complet

### Version 0.0.1
Version de développement initiale avec la structure de base du projet.

---

## Roadmap

### Version 0.2.0 (Prévue pour Q2 2024)
- [ ] Support des automates probabilistes
- [ ] Algorithmes d'apprentissage automatique
- [ ] Interface web interactive
- [ ] Support des automates temporisés
- [ ] Optimisations de performance avancées

### Version 0.3.0 (Prévue pour Q3 2024)
- [ ] Support des automates hybrides
- [ ] Intégration avec des bases de données
- [ ] API REST
- [ ] Support des automates quantiques
- [ ] Outils de débogage avancés

### Version 1.0.0 (Prévue pour Q4 2024)
- [ ] API stable et finalisée
- [ ] Documentation complète
- [ ] Support commercial
- [ ] Intégrations tierces
- [ ] Performance optimisée pour la production

---

## Contribution

Pour contribuer au projet :

1. Consultez le fichier `CONTRIBUTING.md`
2. Suivez les conventions de code définies
3. Ajoutez des tests pour les nouvelles fonctionnalités
4. Mettez à jour la documentation
5. Soumettez une pull request

## Support

- **Documentation** : [https://baobab-automata.readthedocs.io/](https://baobab-automata.readthedocs.io/)
- **Issues** : [https://github.com/baobab-automata/baobab-automata/issues](https://github.com/baobab-automata/baobab-automata/issues)
- **Discussions** : [https://github.com/baobab-automata/baobab-automata/discussions](https://github.com/baobab-automata/baobab-automata/discussions)

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
