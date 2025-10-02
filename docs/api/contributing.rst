Guide de Contribution
======================

Merci de votre intérêt pour contribuer à Baobab Automata ! Ce guide vous aidera à comprendre comment contribuer efficacement au projet.

Types de contributions
-----------------------

Nous accueillons plusieurs types de contributions :

Nouvelles fonctionnalités
~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Nouveaux types d'automates** : Automates probabilistes, temporisés, etc.
* **Algorithmes avancés** : Nouveaux algorithmes de conversion ou d'optimisation
* **Outils de visualisation** : Nouvelles méthodes de visualisation
* **Intégrations** : Support de nouvelles bibliothèques ou formats

Corrections de bugs
~~~~~~~~~~~~~~~~~~~~

* **Bugs de reconnaissance** : Problèmes dans la reconnaissance de langages
* **Bugs de conversion** : Erreurs dans les algorithmes de conversion
* **Bugs de visualisation** : Problèmes d'affichage ou de rendu
* **Bugs de performance** : Optimisations nécessaires

Améliorations de la documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Exemples** : Nouveaux exemples d'utilisation
* **Tutoriels** : Guides pas à pas
* **Documentation API** : Amélioration de la documentation des fonctions
* **Traductions** : Traduction de la documentation

Tests et qualité
~~~~~~~~~~~~~~~~~

* **Tests unitaires** : Couverture de nouveaux cas
* **Tests d'intégration** : Tests de l'interaction entre composants
* **Tests de performance** : Benchmarks et optimisations
* **Amélioration de la qualité** : Refactoring et nettoyage du code

Comment contribuer
-------------------

Processus étape par étape
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Fork le repository**
   * Allez sur https://github.com/baobab-automata/baobab-automata
   * Cliquez sur "Fork" en haut à droite

2. **Clone votre fork**
   .. code-block:: bash

      git clone https://github.com/votre-username/baobab-automata.git
      cd baobab-automata

3. **Configurez l'environnement de développement**
   .. code-block:: bash

      # Créez un environnement virtuel
      python -m venv .venv
      source .venv/bin/activate  # Linux/Mac
      # ou
      .venv\Scripts\activate  # Windows

      # Installez les dépendances de développement
      pip install -e .[dev]

4. **Créez une branche pour votre contribution**
   .. code-block:: bash

      git checkout -b feature/nom-de-votre-fonctionnalite
      # ou
      git checkout -b fix/description-du-bug

5. **Développez votre contribution**
   * Écrivez le code
   * Ajoutez des tests
   * Mettez à jour la documentation
   * Respectez les conventions de code

6. **Testez votre contribution**
   .. code-block:: bash

      # Tests unitaires
      pytest tests/

      # Qualité du code
      make lint

      # Documentation
      make docs

7. **Commitez vos changements**
   .. code-block:: bash

      git add .
      git commit -m "feat: ajouter nouvelle fonctionnalité

      - Description détaillée des changements
      - Référence aux issues si applicable

      Fixes #123"

8. **Poussez vers votre fork**
   .. code-block:: bash

      git push origin feature/nom-de-votre-fonctionnalite

9. **Créez une Pull Request**
   * Allez sur votre fork sur GitHub
   * Cliquez sur "New Pull Request"
   * Remplissez le template de PR

Standards de code
------------------

Style de code
~~~~~~~~~~~~~~

Le projet suit les conventions Python standard :

* **PEP 8** : Style de code Python
* **Black** : Formatage automatique (longueur de ligne 88)
* **Type hints** : Annotations de type obligatoires
* **Docstrings** : Documentation Google/NumPy style

**Exemple de style** :

.. code-block:: python

   from typing import Set, Dict, Tuple, Optional, Union
   from abc import ABC, abstractmethod

   class NouvelleClasse(ABC):
       """Classe exemple suivant les conventions du projet.
       
       Cette classe montre les conventions de style utilisées
       dans Baobab Automata.
       
       Attributes:
           states: Ensemble des états
           alphabet: Alphabet d'entrée
       """
       
       def __init__(
           self,
           states: Set[str],
           alphabet: Set[str],
           **kwargs: Optional[Dict[str, Union[str, int]]]
       ) -> None:
           """Initialise la classe.
           
           Args:
               states: Ensemble des états
               alphabet: Alphabet d'entrée
               **kwargs: Arguments optionnels
               
           Raises:
               ValueError: Si les paramètres sont invalides
           """
           self.states = states
           self.alphabet = alphabet
           
           if not self._validate_inputs():
               raise ValueError("Paramètres invalides")
       
       @abstractmethod
       def process(self, input_data: str) -> bool:
           """Traite les données d'entrée.
           
           Args:
               input_data: Données à traiter
               
           Returns:
               True si le traitement réussit, False sinon
               
           Raises:
               ProcessingError: Si une erreur survient
           """
           pass
       
       def _validate_inputs(self) -> bool:
           """Valide les entrées.
           
           Returns:
               True si les entrées sont valides, False sinon
           """
           return (
               isinstance(self.states, set) and
               isinstance(self.alphabet, set) and
               len(self.states) > 0 and
               len(self.alphabet) > 0
           )

Tests
~~~~~~

**Couverture minimale** : 95%

**Types de tests requis** :

* **Tests unitaires** : Pour chaque fonction/méthode
* **Tests d'intégration** : Pour les interactions entre composants
* **Tests de régression** : Pour éviter les régressions
* **Tests de performance** : Pour les algorithmes critiques

**Exemple de test** :

.. code-block:: python

   import pytest
   from baobab_automata import NouvelleClasse
   from baobab_automata.exceptions import ProcessingError

   class TestNouvelleClasse:
       """Tests pour NouvelleClasse."""
       
       def test_initialization_valid(self):
           """Test l'initialisation avec des paramètres valides."""
           instance = NouvelleClasse(
               states={'q0', 'q1'},
               alphabet={'a', 'b'}
           )
           
           assert instance.states == {'q0', 'q1'}
           assert instance.alphabet == {'a', 'b'}
       
       def test_initialization_invalid(self):
           """Test l'initialisation avec des paramètres invalides."""
           with pytest.raises(ValueError):
               NouvelleClasse(
                   states=set(),  # Ensemble vide
                   alphabet={'a', 'b'}
               )
       
       @pytest.mark.parametrize("input_data,expected", [
           ('valid_input', True),
           ('invalid_input', False),
           ('', False),
       ])
       def test_process_parametrized(self, input_data, expected):
           """Test paramétré de la méthode process."""
           instance = NouvelleClasse(
               states={'q0', 'q1'},
               alphabet={'a', 'b'}
           )
           
           result = instance.process(input_data)
           assert result == expected

Documentation
~~~~~~~~~~~~~~

**Standards de documentation** :

* **Docstrings** : Obligatoires pour toutes les fonctions publiques
* **Type hints** : Obligatoires pour toutes les signatures
* **Exemples** : Dans les docstrings des fonctions complexes
* **README** : Mis à jour avec les nouvelles fonctionnalités

**Exemple de docstring** :

.. code-block:: python

   def nouvelle_fonction(
       param1: str,
       param2: Optional[int] = None,
       **kwargs: Dict[str, Any]
   ) -> Tuple[bool, str]:
       """Effectue une opération complexe.
       
       Cette fonction implémente un algorithme sophistiqué pour
       traiter les données d'entrée et retourner un résultat.
       
       Args:
           param1: Premier paramètre obligatoire
           param2: Deuxième paramètre optionnel
           **kwargs: Arguments supplémentaires
           
       Returns:
           Tuple contenant:
               - bool: True si l'opération réussit
               - str: Message de statut
               
       Raises:
           ValueError: Si param1 est vide
           ProcessingError: Si l'opération échoue
           
       Example:
           >>> result, message = nouvelle_fonction("test", 42)
           >>> print(f"Résultat: {result}, Message: {message}")
           Résultat: True, Message: Opération réussie
           
       Note:
           Cette fonction a une complexité temporelle O(n log n)
           où n est la taille de param1.
       """
       if not param1:
           raise ValueError("param1 ne peut pas être vide")
       
       # Implémentation...
       
       return True, "Opération réussie"

Workflow de développement
-------------------------

Branches
~~~~~~~~~

* **main** : Branche principale stable
* **develop** : Branche de développement
* **feature/*** : Nouvelles fonctionnalités
* **fix/*** : Corrections de bugs
* **docs/*** : Améliorations de documentation
* **test/*** : Améliorations de tests

**Convention de nommage des branches** :

.. code-block:: bash

   feature/support-automates-probabilistes
   fix/bug-minimisation-dfa
   docs/amelioration-guide-installation
   test/couverture-algorithmes-conversion

Commits
~~~~~~~~

**Format Conventional Commits** :

.. code-block:: bash

   feat: ajouter support des automates probabilistes
   fix: corriger bug dans la minimisation DFA
   docs: mettre à jour la documentation API
   test: ajouter tests pour la conversion NFA->DFA
   refactor: optimiser l'algorithme de reconnaissance
   chore: mettre à jour les dépendances

**Types de commits** :

* **feat** : Nouvelle fonctionnalité
* **fix** : Correction de bug
* **docs** : Documentation
* **style** : Formatage, point-virgules manquants, etc.
* **refactor** : Refactoring du code
* **test** : Ajout de tests
* **chore** : Maintenance

Pull Requests
~~~~~~~~~~~~~~~

**Template de Pull Request** :

.. code-block:: markdown

   ## Description
   
   Brève description des changements apportés.
   
   ## Type de changement
   
   - [ ] Correction de bug
   - [ ] Nouvelle fonctionnalité
   - [ ] Amélioration de la documentation
   - [ ] Refactoring
   - [ ] Amélioration des tests
   
   ## Tests
   
   - [ ] Tests unitaires ajoutés/mis à jour
   - [ ] Tests d'intégration ajoutés/mis à jour
   - [ ] Tous les tests passent
   - [ ] Couverture de tests >= 95%
   
   ## Documentation
   
   - [ ] Documentation mise à jour
   - [ ] Exemples ajoutés si nécessaire
   - [ ] Changelog mis à jour
   
   ## Checklist
   
   - [ ] Code formaté avec Black
   - [ ] Tests passent
   - [ ] Qualité du code vérifiée (Pylint, Flake8)
   - [ ] Types vérifiés avec MyPy
   - [ ] Sécurité vérifiée avec Bandit
   - [ ] Documentation générée sans erreurs
   
   ## Issues liées
   
   Fixes #123
   Related to #456

Processus de review
--------------------

Critères de review
~~~~~~~~~~~~~~~~~~~

**Code** :
* Respect des conventions de style
* Qualité et lisibilité du code
* Performance et efficacité
* Gestion d'erreurs appropriée

**Tests** :
* Couverture de tests suffisante
* Qualité des tests
* Cas de test représentatifs
* Tests de régression

**Documentation** :
* Docstrings complètes
* Exemples d'utilisation
* Documentation mise à jour
* Clarté et précision

**Fonctionnalité** :
* Correspondance avec les spécifications
* Compatibilité avec l'API existante
* Pas de régression
* Performance acceptable

Processus de review
~~~~~~~~~~~~~~~~~~~~

1. **Review automatique** : CI/CD vérifie la qualité du code
2. **Review par les pairs** : Au moins un reviewer
3. **Tests** : Tous les tests doivent passer
4. **Approbation** : Au moins une approbation requise
5. **Merge** : Merge après approbation

**Commentaires de review** :

* **Constructifs** : Proposer des améliorations
* **Spécifiques** : Pointer des lignes précises
* **Respectueux** : Maintenir un ton professionnel
* **Actionables** : Donner des suggestions concrètes

Gestion des issues
-------------------

Types d'issues
~~~~~~~~~~~~~~~

* **Bug** : Problème à corriger
* **Enhancement** : Amélioration de fonctionnalité existante
* **Feature Request** : Nouvelle fonctionnalité
* **Documentation** : Amélioration de la documentation
* **Question** : Question ou demande d'aide

**Template d'issue** :

.. code-block:: markdown

   ## Description
   
   Description claire et concise du problème ou de la demande.
   
   ## Type d'issue
   
   - [ ] Bug
   - [ ] Enhancement
   - [ ] Feature Request
   - [ ] Documentation
   - [ ] Question
   
   ## Environnement
   
   - OS: [ex: Ubuntu 20.04]
   - Python: [ex: 3.11.0]
   - Version Baobab Automata: [ex: 0.1.0]
   
   ## Étapes pour reproduire (si bug)
   
   1. Aller à '...'
   2. Cliquer sur '...'
   3. Voir l'erreur
   
   ## Comportement attendu
   
   Description du comportement attendu.
   
   ## Comportement actuel
   
   Description du comportement actuel.
   
   ## Informations supplémentaires
   
   Screenshots, logs, etc.

Labels
~~~~~~~

* **bug** : Problème à corriger
* **enhancement** : Amélioration
* **feature** : Nouvelle fonctionnalité
* **documentation** : Documentation
* **good first issue** : Bon pour les débutants
* **help wanted** : Aide recherchée
* **priority:high** : Priorité élevée
* **priority:medium** : Priorité moyenne
* **priority:low** : Priorité faible

Milestones
~~~~~~~~~~~

* **v0.2.0** : Prochaine version mineure
* **v0.3.0** : Version suivante
* **v1.0.0** : Version stable
* **Backlog** : Fonctionnalités futures

Communauté
-----------

Code de conduite
~~~~~~~~~~~~~~~~~~

Nous nous engageons à fournir un environnement accueillant et inclusif pour tous les contributeurs. 

**Comportement attendu** :
* Utilisation d'un langage accueillant et inclusif
* Respect des différents points de vue et expériences
* Acceptation gracieuse des critiques constructives
* Focus sur ce qui est le mieux pour la communauté
* Empathie envers les autres membres de la communauté

**Comportement inacceptable** :
* Langage ou images sexualisés
* Trolling, commentaires insultants ou désobligeants
* Harcèlement public ou privé
* Publication d'informations privées sans permission
* Autre comportement inapproprié dans un contexte professionnel

**Signalement** : Contactez l'équipe à team@baobab-automata.dev

Communication
~~~~~~~~~~~~~~

**Canaux de communication** :

* **GitHub Issues** : Bugs et demandes de fonctionnalités
* **GitHub Discussions** : Questions et discussions générales
* **Pull Requests** : Review et discussion du code
* **Email** : team@baobab-automata.dev pour les questions privées

**Bonnes pratiques** :

* Soyez respectueux et constructif
* Utilisez des titres clairs et descriptifs
* Fournissez suffisamment de contexte
* Répondez aux questions et commentaires
* Remerciez les contributeurs

Reconnaissance
~~~~~~~~~~~~~~~

Nous reconnaissons les contributions de plusieurs façons :

* **Contributeurs** : Liste dans le README
* **Release notes** : Mention des contributions importantes
* **Badges** : Badges de contribution sur GitHub
* **Communauté** : Reconnaissance dans la communauté

Ressources
-----------

Documentation
~~~~~~~~~~~~~~

* **Guide de démarrage** : :doc:`quickstart`
* **Documentation API** : :doc:`index`
* **Exemples** : :doc:`../examples/index`
* **Guide de développement** : :doc:`development`

Outils
~~~~~~~

* **Git** : Contrôle de version
* **Python 3.11+** : Langage de programmation
* **Pytest** : Framework de tests
* **Black** : Formatage de code
* **Pylint** : Analyse de qualité
* **Sphinx** : Documentation

Liens utiles
~~~~~~~~~~~~~

* **Repository** : https://github.com/baobab-automata/baobab-automata
* **Documentation** : https://baobab-automata.readthedocs.io/
* **Issues** : https://github.com/baobab-automata/baobab-automata/issues
* **Discussions** : https://github.com/baobab-automata/baobab-automata/discussions

Questions fréquentes
---------------------

**Comment commencer à contribuer ?**
Commencez par regarder les issues marquées "good first issue" ou "help wanted". Ce sont des tâches idéales pour les nouveaux contributeurs.

**Quel est le processus de review ?**
Toutes les contributions passent par une review par les pairs. Le processus inclut des vérifications automatiques et une review manuelle.

**Comment proposer une nouvelle fonctionnalité ?**
Ouvrez une issue avec le label "feature request" et décrivez votre idée. L'équipe discutera de la faisabilité et de l'intégration.

**Que faire si je trouve un bug ?**
Ouvrez une issue avec le label "bug" et fournissez autant de détails que possible pour reproduire le problème.

**Comment obtenir de l'aide ?**
Utilisez GitHub Discussions pour poser des questions ou contactez l'équipe à team@baobab-automata.dev.

Merci de contribuer à Baobab Automata ! 🎉
