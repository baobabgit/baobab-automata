API des Algorithmes
=====================

Cette section documente l'API des algorithmes disponibles dans Baobab Automata.

Vue d'ensemble
--------------

Baobab Automata fournit une collection complète d'algorithmes pour la manipulation, la conversion et l'optimisation des automates.

Algorithmes de conversion
-------------------------

Conversion entre automates finis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.algorithms.conversion_algorithms
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: nfa_to_dfa(nfa: NFA) -> DFA

   Convertit un automate fini non-déterministe en automate fini déterministe équivalent.

   :param nfa: L'automate fini non-déterministe à convertir
   :return: Un automate fini déterministe équivalent
   :raises ConversionError: Si la conversion échoue

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import NFA
      from baobab_automata.algorithms import nfa_to_dfa

      nfa = NFA(
          states={'q0', 'q1', 'q2'},
          alphabet={'a', 'b'},
          transitions={
              ('q0', 'a'): {'q0', 'q1'},
              ('q0', 'b'): {'q1'},
              ('q1', 'a'): {'q2'},
              ('q1', 'b'): {'q2'},
          },
          initial_state='q0',
          final_states={'q2'}
      )

      dfa = nfa_to_dfa(nfa)
      print(f"États NFA: {len(nfa.states)}")
      print(f"États DFA: {len(dfa.states)}")

.. py:function:: dfa_to_nfa(dfa: DFA) -> NFA

   Convertit un automate fini déterministe en automate fini non-déterministe équivalent.

   :param dfa: L'automate fini déterministe à convertir
   :return: Un automate fini non-déterministe équivalent

.. py:function:: epsilon_nfa_to_nfa(epsilon_nfa: EpsilonNFA) -> NFA

   Convertit un automate fini non-déterministe avec epsilon-transitions en automate fini non-déterministe équivalent.

   :param epsilon_nfa: L'automate epsilon-NFA à convertir
   :return: Un automate fini non-déterministe équivalent

Conversion d'automates à pile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.pushdown.conversion_algorithms
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: pda_to_cfg(pda: Union[DPDA, NPDA]) -> Dict[str, List[List[str]]]

   Convertit un automate à pile en grammaire contextuelle équivalente.

   :param pda: L'automate à pile à convertir
   :return: Une grammaire contextuelle sous forme de dictionnaire
   :raises ConversionError: Si la conversion échoue

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DPDA
      from baobab_automata.pushdown import ConversionAlgorithms

      dpda = DPDA(...)  # Définition de l'automate
      converter = ConversionAlgorithms()
      cfg = converter.pda_to_cfg(dpda)
      
      print("Grammaire contextuelle générée:")
      for non_terminal, productions in cfg.items():
          print(f"{non_terminal} -> {' | '.join([' '.join(prod) for prod in productions])}")

.. py:function:: cfg_to_pda(cfg: Dict[str, List[List[str]]]) -> NPDA

   Convertit une grammaire contextuelle en automate à pile équivalent.

   :param cfg: La grammaire contextuelle à convertir
   :return: Un automate à pile non-déterministe équivalent

Algorithmes d'optimisation
---------------------------

Optimisation des automates finis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.finite.optimization_algorithms
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: minimize_dfa(dfa: DFA) -> DFA

   Minimise un automate fini déterministe en supprimant les états équivalents.

   :param dfa: L'automate fini déterministe à minimiser
   :return: Un automate fini déterministe minimal équivalent
   :raises OptimizationError: Si l'optimisation échoue

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DFA
      from baobab_automata.algorithms import minimize_dfa

      # DFA non-minimal
      dfa = DFA(
          states={'q0', 'q1', 'q2', 'q3', 'q4'},
          alphabet={'a', 'b'},
          transitions={
              ('q0', 'a'): 'q1',
              ('q0', 'b'): 'q2',
              ('q1', 'a'): 'q3',
              ('q1', 'b'): 'q4',
              ('q2', 'a'): 'q4',
              ('q2', 'b'): 'q3',
              ('q3', 'a'): 'q3',
              ('q3', 'b'): 'q4',
              ('q4', 'a'): 'q4',
              ('q4', 'b'): 'q3',
          },
          initial_state='q0',
          final_states={'q3'}
      )

      print(f"États avant minimisation: {len(dfa.states)}")
      minimal_dfa = minimize_dfa(dfa)
      print(f"États après minimisation: {len(minimal_dfa.states)}")

.. py:function:: remove_unreachable_states(automaton: Union[DFA, NFA, EpsilonNFA]) -> Union[DFA, NFA, EpsilonNFA]

   Supprime les états inaccessibles d'un automate fini.

   :param automaton: L'automate à optimiser
   :return: L'automate avec les états inaccessibles supprimés

.. py:function:: remove_dead_states(automaton: Union[DFA, NFA, EpsilonNFA]) -> Union[DFA, NFA, EpsilonNFA]

   Supprime les états morts d'un automate fini.

   :param automaton: L'automate à optimiser
   :return: L'automate avec les états morts supprimés

Optimisation des automates à pile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.pushdown.optimization_algorithms
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: minimize_pda(pda: Union[DPDA, NPDA]) -> Union[DPDA, NPDA]

   Minimise un automate à pile en supprimant les états et transitions redondants.

   :param pda: L'automate à pile à minimiser
   :return: Un automate à pile minimal équivalent

Opérations sur les langages
-----------------------------

.. automodule:: baobab_automata.algorithms.language_operations
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: union(automaton1: Union[DFA, NFA], automaton2: Union[DFA, NFA]) -> Union[DFA, NFA]

   Calcule l'union de deux langages reconnus par des automates finis.

   :param automaton1: Premier automate
   :param automaton2: Deuxième automate
   :return: Un automate reconnaissant l'union des deux langages
   :raises LanguageOperationError: Si l'opération échoue

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DFA
      from baobab_automata.algorithms import language_operations

      # DFA pour les mots contenant 'aa'
      dfa_aa = DFA(
          states={'q0', 'q1', 'q2'},
          alphabet={'a', 'b'},
          transitions={
              ('q0', 'a'): 'q1',
              ('q0', 'b'): 'q0',
              ('q1', 'a'): 'q2',
              ('q1', 'b'): 'q0',
              ('q2', 'a'): 'q2',
              ('q2', 'b'): 'q2',
          },
          initial_state='q0',
          final_states={'q2'}
      )

      # DFA pour les mots contenant 'bb'
      dfa_bb = DFA(
          states={'q0', 'q1', 'q2'},
          alphabet={'a', 'b'},
          transitions={
              ('q0', 'a'): 'q0',
              ('q0', 'b'): 'q1',
              ('q1', 'a'): 'q0',
              ('q1', 'b'): 'q2',
              ('q2', 'a'): 'q2',
              ('q2', 'b'): 'q2',
          },
          initial_state='q0',
          final_states={'q2'}
      )

      # Union : mots contenant 'aa' OU 'bb'
      union_dfa = language_operations.union(dfa_aa, dfa_bb)

.. py:function:: intersection(automaton1: Union[DFA, NFA], automaton2: Union[DFA, NFA]) -> Union[DFA, NFA]

   Calcule l'intersection de deux langages reconnus par des automates finis.

   :param automaton1: Premier automate
   :param automaton2: Deuxième automate
   :return: Un automate reconnaissant l'intersection des deux langages

.. py:function:: complement(automaton: DFA) -> DFA

   Calcule le complément d'un langage reconnu par un automate fini déterministe.

   :param automaton: L'automate fini déterministe
   :return: Un automate reconnaissant le complément du langage

.. py:function:: concatenation(automaton1: Union[DFA, NFA], automaton2: Union[DFA, NFA]) -> Union[DFA, NFA]

   Calcule la concaténation de deux langages reconnus par des automates finis.

   :param automaton1: Premier automate
   :param automaton2: Deuxième automate
   :return: Un automate reconnaissant la concaténation des deux langages

Parsing et génération
---------------------

Parsing d'expressions régulières
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.finite.regex_parser
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: regex_to_nfa(regex: str) -> NFA

   Convertit une expression régulière en automate fini non-déterministe équivalent.

   :param regex: L'expression régulière à parser
   :return: Un automate fini non-déterministe équivalent
   :raises RegexParseError: Si le parsing échoue

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.algorithms import regex_to_nfa

      # Expression régulière pour les mots se terminant par 'ing'
      regex = "(a|b)*ing"
      nfa = regex_to_nfa(regex)
      
      # Test
      assert nfa.accepts('singing')
      assert nfa.accepts('running')
      assert not nfa.accepts('cat')

.. py:function:: nfa_to_regex(nfa: NFA) -> str

   Convertit un automate fini non-déterministe en expression régulière équivalente.

   :param nfa: L'automate fini non-déterministe
   :return: Une expression régulière équivalente

Parsing de grammaires contextuelles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.pushdown.grammar_parser
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: parse_cfg(grammar_text: str) -> Dict[str, List[List[str]]]

   Parse une grammaire contextuelle à partir d'un texte.

   :param grammar_text: Le texte de la grammaire
   :return: Une grammaire contextuelle sous forme de dictionnaire
   :raises GrammarParseError: Si le parsing échoue

Algorithmes spécialisés
------------------------

Algorithmes de reconnaissance avancés
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.algorithms.specialized_algorithms
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: pattern_matching(text: str, pattern: str, automaton: Union[DFA, NFA]) -> List[int]

   Trouve toutes les occurrences d'un pattern dans un texte en utilisant un automate.

   :param text: Le texte dans lequel chercher
   :param pattern: Le pattern à rechercher
   :param automaton: L'automate pour la reconnaissance
   :return: Liste des positions des occurrences

.. py:function:: longest_match(text: str, automaton: Union[DFA, NFA]) -> Tuple[str, int]

   Trouve la plus longue correspondance d'un automate dans un texte.

   :param text: Le texte à analyser
   :param automaton: L'automate pour la reconnaissance
   :return: Tuple (match, position) de la plus longue correspondance

Algorithmes de complexité
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.turing.complexity_analysis
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: analyze_time_complexity(tm: Union[DTM, NTM], input_size: int) -> ComplexityResult

   Analyse la complexité temporelle d'une machine de Turing.

   :param tm: La machine de Turing à analyser
   :param input_size: La taille de l'entrée
   :return: Résultat de l'analyse de complexité

.. py:function:: analyze_space_complexity(tm: Union[DTM, NTM], input_size: int) -> ComplexityResult

   Analyse la complexité spatiale d'une machine de Turing.

   :param tm: La machine de Turing à analyser
   :param input_size: La taille de l'entrée
   :return: Résultat de l'analyse de complexité

Utilitaires
-----------

Validation d'automates
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.utils.validation
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: validate_automaton(automaton: IAutomaton) -> ValidationResult

   Valide la cohérence d'un automate.

   :param automaton: L'automate à valider
   :return: Résultat de la validation

.. py:function:: check_completeness(automaton: Union[DFA, DPDA, DTM]) -> bool

   Vérifie si un automate déterministe est complet.

   :param automaton: L'automate à vérifier
   :return: True si l'automate est complet, False sinon

Génération d'automates
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.utils.generation
   :members:
   :undoc-members:
   :show-inheritance:

.. py:function:: generate_random_dfa(num_states: int, alphabet_size: int) -> DFA

   Génère un automate fini déterministe aléatoire.

   :param num_states: Nombre d'états
   :param alphabet_size: Taille de l'alphabet
   :return: Un automate fini déterministe aléatoire

.. py:function:: generate_from_language(language_description: str) -> Union[DFA, NFA]

   Génère un automate à partir d'une description de langage.

   :param language_description: Description du langage
   :return: Un automate reconnaissant le langage décrit

Exemples d'utilisation avancée
-------------------------------

Pipeline de conversion complet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata import EpsilonNFA, NFA, DFA
   from baobab_automata.algorithms import (
       epsilon_nfa_to_nfa, nfa_to_dfa, minimize_dfa
   )

   # Pipeline: Epsilon-NFA -> NFA -> DFA -> DFA minimal
   epsilon_nfa = EpsilonNFA(...)
   nfa = epsilon_nfa_to_nfa(epsilon_nfa)
   dfa = nfa_to_dfa(nfa)
   minimal_dfa = minimize_dfa(dfa)
   
   print(f"États finaux: {len(minimal_dfa.states)}")

Optimisation en cascade
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.algorithms import (
       remove_unreachable_states, remove_dead_states, minimize_dfa
   )

   # Optimisation en cascade
   dfa = DFA(...)
   
   # Étape 1: Supprimer les états inaccessibles
   dfa = remove_unreachable_states(dfa)
   
   # Étape 2: Supprimer les états morts
   dfa = remove_dead_states(dfa)
   
   # Étape 3: Minimiser
   minimal_dfa = minimize_dfa(dfa)
   
   print(f"Optimisation terminée: {len(minimal_dfa.states)} états")

Analyse de performance
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from baobab_automata import DFA
   from baobab_automata.algorithms import minimize_dfa

   # Mesure de performance
   dfa = DFA(...)  # Gros automate
   
   start_time = time.time()
   minimal_dfa = minimize_dfa(dfa)
   end_time = time.time()
   
   print(f"Minimisation terminée en {end_time - start_time:.2f} secondes")
   print(f"Réduction: {len(dfa.states)} -> {len(minimal_dfa.states)} états")

Conseils d'utilisation
-----------------------

* **Ordre des opérations** : Appliquez les optimisations dans l'ordre logique
* **Validation** : Validez toujours les résultats des conversions
* **Performance** : Utilisez les algorithmes optimisés pour de gros automates
* **Mémoire** : Surveillez l'utilisation mémoire lors de conversions complexes
* **Tests** : Testez les automates convertis avec des cas représentatifs
