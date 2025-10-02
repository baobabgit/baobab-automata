Guide de Démarrage Rapide
==========================

Ce guide vous permet de commencer rapidement avec Baobab Automata en quelques minutes.

Concepts de base
----------------

Baobab Automata organise les automates selon une hiérarchie claire :

* **Interfaces** : Définitions abstraites des comportements
* **Implémentations** : Classes concrètes pour chaque type d'automate
* **Algorithmes** : Fonctions de conversion, optimisation et analyse
* **Visualisation** : Outils pour représenter graphiquement les automates

Automates finis
---------------

Création d'un DFA
~~~~~~~~~~~~~~~~~~

Un automate fini déterministe (DFA) reconnaît un langage régulier :

.. code-block:: python

   from baobab_automata import DFA

   # DFA qui reconnaît les chaînes se terminant par 'ab'
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

Création d'un NFA
~~~~~~~~~~~~~~~~~~

Un automate fini non-déterministe (NFA) peut avoir plusieurs transitions pour le même symbole :

.. code-block:: python

   from baobab_automata import NFA

   # NFA qui reconnaît les chaînes contenant 'aa' ou 'bb'
   nfa = NFA(
       states={'q0', 'q1', 'q2', 'q3'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): {'q0', 'q1'},
           ('q0', 'b'): {'q0', 'q2'},
           ('q1', 'a'): {'q3'},
           ('q2', 'b'): {'q3'},
       },
       initial_state='q0',
       final_states={'q3'}
   )

   print(nfa.accepts('aa'))    # True
   print(nfa.accepts('bb'))    # True
   print(nfa.accepts('ab'))    # False

Conversion DFA ↔ NFA
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.algorithms import nfa_to_dfa, dfa_to_nfa

   # Conversion NFA vers DFA
   dfa_from_nfa = nfa_to_dfa(nfa)
   
   # Conversion DFA vers NFA
   nfa_from_dfa = dfa_to_nfa(dfa)

Automates à pile
----------------

Création d'un DPDA
~~~~~~~~~~~~~~~~~~

Un automate à pile déterministe (DPDA) reconnaît les langages contextuels :

.. code-block:: python

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
   print(dpda.accepts('ab'))    # True
   print(dpda.accepts('aab'))   # False

Machines de Turing
------------------

Création d'une DTM
~~~~~~~~~~~~~~~~~~~

Une machine de Turing déterministe (DTM) peut résoudre des problèmes décidables :

.. code-block:: python

   from baobab_automata import DTM

   # DTM qui reconnaît le palindrome sur {a, b}
   dtm = DTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'},
       alphabet={'a', 'b'},
       tape_alphabet={'a', 'b', 'B'},  # B = symbole blanc
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

Visualisation
--------------

Génération de graphiques
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Visualisation d'un DFA
   dfa.visualize('dfa_example.png', format='png')
   
   # Visualisation avec options
   dfa.visualize(
       'dfa_detailed.png',
       format='png',
       dpi=300,
       show_labels=True,
       layout='dot'
   )

   # Génération de code Mermaid
   mermaid_code = dfa.to_mermaid()
   print(mermaid_code)

Algorithmes avancés
-------------------

Optimisation d'automates
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.algorithms import minimize_dfa, remove_unreachable_states

   # Minimisation d'un DFA
   minimized_dfa = minimize_dfa(dfa)
   
   # Suppression des états inaccessibles
   cleaned_dfa = remove_unreachable_states(dfa)

Analyse de langages
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.algorithms import language_operations

   # Union de deux langages
   union_dfa = language_operations.union(dfa1, dfa2)
   
   # Intersection de deux langages
   intersection_dfa = language_operations.intersection(dfa1, dfa2)
   
   # Complément d'un langage
   complement_dfa = language_operations.complement(dfa)

Parsing d'expressions régulières
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.algorithms import regex_to_nfa

   # Conversion d'une expression régulière en NFA
   regex = "(a|b)*abb"
   nfa_from_regex = regex_to_nfa(regex)

Gestion des erreurs
-------------------

Baobab Automata fournit des exceptions spécifiques :

.. code-block:: python

   from baobab_automata.exceptions import (
       InvalidAutomatonError,
       InvalidStateError,
       InvalidTransitionError,
       RecognitionError
   )

   try:
       result = dfa.accepts('invalid_input')
   except RecognitionError as e:
       print(f"Erreur de reconnaissance : {e}")

Prochaines étapes
------------------

Maintenant que vous connaissez les bases :

* Consultez :doc:`../examples/index` pour des exemples plus avancés
* Explorez :doc:`index` pour la documentation API complète
* Découvrez les algorithmes spécialisés dans :doc:`algorithms`

Conseils de performance
------------------------

* Utilisez les algorithmes optimisés pour de gros automates
* Activez le cache pour les visualisations répétées
* Considérez la parallélisation pour les opérations sur plusieurs automates
