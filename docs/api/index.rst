Documentation API
==================

Cette section contient la documentation complète de l'API de Baobab Automata.

Vue d'ensemble
--------------

Baobab Automata fournit une API unifiée pour travailler avec différents types d'automates. L'architecture suit le pattern d'interfaces et d'implémentations, permettant une flexibilité maximale.

Structure de l'API
-------------------

.. toctree::
   :maxdepth: 2

   automata
   algorithms
   visualization
   exceptions

Interfaces principales
-----------------------

Les interfaces définissent les contrats que doivent respecter toutes les implémentations :

* :class:`IAutomaton` - Interface de base pour tous les automates
* :class:`IRecognizer` - Interface pour la reconnaissance de langages
* :class:`IConverter` - Interface pour les conversions entre automates
* :class:`IState` - Interface pour les états d'automates
* :class:`ITransition` - Interface pour les transitions

Types d'automates
------------------

Automates finis
~~~~~~~~~~~~~~~

* :class:`DFA` - Automate fini déterministe
* :class:`NFA` - Automate fini non-déterministe
* :class:`EpsilonNFA` - Automate fini non-déterministe avec epsilon-transitions

Automates à pile
~~~~~~~~~~~~~~~~

* :class:`DPDA` - Automate à pile déterministe
* :class:`NPDA` - Automate à pile non-déterministe

Machines de Turing
~~~~~~~~~~~~~~~~~~

* :class:`DTM` - Machine de Turing déterministe
* :class:`NTM` - Machine de Turing non-déterministe
* :class:`MultiTapeTM` - Machine de Turing multi-rubans

Algorithmes
-----------

Conversion
~~~~~~~~~~

* :func:`nfa_to_dfa` - Conversion NFA vers DFA
* :func:`dfa_to_nfa` - Conversion DFA vers NFA
* :func:`epsilon_nfa_to_nfa` - Conversion epsilon-NFA vers NFA
* :func:`pda_to_cfg` - Conversion PDA vers grammaire contextuelle

Optimisation
~~~~~~~~~~~~

* :func:`minimize_dfa` - Minimisation d'un DFA
* :func:`remove_unreachable_states` - Suppression des états inaccessibles
* :func:`remove_dead_states` - Suppression des états morts

Opérations sur les langages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :func:`union` - Union de deux langages
* :func:`intersection` - Intersection de deux langages
* :func:`complement` - Complément d'un langage
* :func:`concatenation` - Concatenation de deux langages

Parsing
~~~~~~~

* :func:`regex_to_nfa` - Conversion d'expression régulière vers NFA
* :func:`cfg_to_pda` - Conversion de grammaire contextuelle vers PDA

Visualisation
-------------

* :func:`visualize` - Génération de graphiques d'automates
* :func:`to_mermaid` - Génération de code Mermaid
* :func:`to_graphviz` - Génération de code Graphviz
* :func:`export_json` - Export au format JSON

Gestion des erreurs
-------------------

* :class:`BaobabAutomataError` - Exception de base
* :class:`InvalidAutomatonError` - Automate invalide
* :class:`InvalidStateError` - État invalide
* :class:`InvalidTransitionError` - Transition invalide
* :class:`RecognitionError` - Erreur de reconnaissance
* :class:`ConversionError` - Erreur de conversion

Conventions de nommage
-----------------------

Classes et interfaces
~~~~~~~~~~~~~~~~~~~~~~

* Les interfaces commencent par ``I`` (ex: ``IAutomaton``)
* Les classes concrètes utilisent des acronymes (ex: ``DFA``, ``NPDA``)
* Les exceptions se terminent par ``Error``

Méthodes
~~~~~~~~

* ``accepts(input_string)`` - Vérifie si une chaîne est acceptée
* ``simulate(input_string)`` - Simule l'exécution de l'automate
* ``visualize(filename)`` - Génère une visualisation
* ``to_<format>()`` - Conversion vers un format spécifique

Paramètres
~~~~~~~~~~

* ``states`` - Ensemble des états
* ``alphabet`` - Alphabet d'entrée
* ``transitions`` - Fonction de transition
* ``initial_state`` - État initial
* ``final_states`` - États finaux

Exemples d'utilisation
-----------------------

Création d'un automate
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata import DFA

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

Reconnaissance de langage
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   result = dfa.accepts('ab')
   print(result)  # True

Conversion d'automate
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.algorithms import nfa_to_dfa

   nfa = NFA(...)
   dfa = nfa_to_dfa(nfa)

Visualisation
~~~~~~~~~~~~~

.. code-block:: python

   dfa.visualize('automaton.png')
   mermaid_code = dfa.to_mermaid()

Gestion des erreurs
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.exceptions import RecognitionError

   try:
       result = dfa.accepts('invalid')
   except RecognitionError as e:
       print(f"Erreur: {e}")

Bonnes pratiques
-----------------

* Utilisez des noms d'états descriptifs
* Documentez vos automates avec des commentaires
* Testez avec des cas limites (chaînes vides, symboles non définis)
* Utilisez la visualisation pour comprendre le comportement
* Préférez les interfaces aux implémentations concrètes
* Gérez les exceptions appropriées

Performance
-----------

* Les automates finis sont optimisés pour la reconnaissance rapide
* Les algorithmes de conversion utilisent des optimisations
* La visualisation peut être mise en cache
* Les gros automates peuvent nécessiter des paramètres de configuration

Compatibilité
-------------

* Python >= 3.11
* Compatible avec les standards Unicode
* Support des caractères spéciaux dans les alphabets
* Export/import de formats standards (JSON, Graphviz, Mermaid)
