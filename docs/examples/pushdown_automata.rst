Exemples d'Automates à Pile
============================

Cette section présente des exemples pratiques d'utilisation des automates à pile (PDA) avec Baobab Automata.

Exemple 1 : DPDA pour le langage a^n b^n
-----------------------------------------

**Problème** : Créer un DPDA qui reconnaît le langage L = {a^n b^n | n ≥ 0}.

**Solution** :

.. code-block:: python

   from baobab_automata import DPDA

   # DPDA pour a^n b^n
   anbn_dpda = DPDA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       stack_alphabet={'A', 'Z'},
       transitions={
           # Lecture des 'a' et empilement
           ('q0', 'a', 'Z'): ('q0', 'AZ'),
           ('q0', 'a', 'A'): ('q0', 'AA'),
           
           # Transition vers lecture des 'b'
           ('q0', 'b', 'A'): ('q1', ''),
           
           # Lecture des 'b' et dépilement
           ('q1', 'b', 'A'): ('q1', ''),
           
           # Acceptation si pile vide
           ('q1', '', 'Z'): ('q2', 'Z'),
       },
       initial_state='q0',
       initial_stack_symbol='Z',
       final_states={'q2'}
   )

   # Tests
   test_strings = ['', 'ab', 'aabb', 'aaabbb', 'a', 'b', 'abb', 'aab']
   for string in test_strings:
       result = anbn_dpda.accepts(string)
       print(f"'{string}' -> {result}")

   # Visualisation
   anbn_dpda.visualize('anbn_dpda.png')

**Résultats attendus** :

::

   '' -> True
   'ab' -> True
   'aabb' -> True
   'aaabbb' -> True
   'a' -> False
   'b' -> False
   'abb' -> False
   'aab' -> False

Exemple 2 : NPDA pour les palindromes
--------------------------------------

**Problème** : Créer un NPDA qui reconnaît les palindromes sur l'alphabet {a, b}.

**Solution** :

.. code-block:: python

   from baobab_automata import NPDA

   # NPDA pour les palindromes
   palindrome_npda = NPDA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       stack_alphabet={'A', 'B', 'Z'},
       transitions={
           # Phase 1 : Lecture et empilement (deviner le milieu)
           ('q0', 'a', 'Z'): ('q0', 'AZ'),
           ('q0', 'a', 'A'): ('q0', 'AA'),
           ('q0', 'a', 'B'): ('q0', 'AB'),
           ('q0', 'b', 'Z'): ('q0', 'BZ'),
           ('q0', 'b', 'A'): ('q0', 'BA'),
           ('q0', 'b', 'B'): ('q0', 'BB'),
           
           # Transition non-déterministe vers phase 2
           ('q0', 'a', 'A'): ('q1', 'A'),  # 'a' au milieu
           ('q0', 'b', 'B'): ('q1', 'B'),  # 'b' au milieu
           ('q0', '', 'Z'): ('q1', 'Z'),   # chaîne vide
           
           # Phase 2 : Vérification palindrome
           ('q1', 'a', 'A'): ('q1', ''),
           ('q1', 'b', 'B'): ('q1', ''),
           ('q1', '', 'Z'): ('q2', 'Z'),
       },
       initial_state='q0',
       initial_stack_symbol='Z',
       final_states={'q2'}
   )

   # Tests
   test_strings = ['', 'a', 'b', 'aa', 'bb', 'aba', 'bab', 'abba', 'ab', 'abc']
   for string in test_strings:
       result = palindrome_npda.accepts(string)
       print(f"'{string}' -> {result}")

Exemple 3 : Analyse de grammaire contextuelle
-----------------------------------------------

**Problème** : Analyser une grammaire contextuelle simple avec un PDA.

**Solution** :

.. code-block:: python

   from baobab_automata import NPDA
   from baobab_automata.pushdown import GrammarParser

   # Grammaire : S -> aSb | ab
   grammar_rules = {
       'S': [['a', 'S', 'b'], ['a', 'b']]
   }

   # Parser de grammaire
   parser = GrammarParser(grammar_rules)
   
   # Conversion en NPDA
   grammar_npda = parser.to_npda()

   # Tests
   test_strings = ['ab', 'aabb', 'aaabbb', 'a', 'b', 'abb']
   for string in test_strings:
       result = grammar_npda.accepts(string)
       print(f"'{string}' -> {result}")

Exemple 4 : DPDA pour les expressions bien parenthésées
--------------------------------------------------------

**Problème** : Créer un DPDA qui vérifie si une expression est bien parenthésée.

**Solution** :

.. code-block:: python

   from baobab_automata import DPDA

   # DPDA pour expressions bien parenthésées
   parentheses_dpda = DPDA(
       states={'q0', 'q1'},
       alphabet={'(', ')', '[', ']', '{', '}'},
       stack_alphabet={'(', '[', '{', 'Z'},
       transitions={
           # Empilement des parenthèses ouvrantes
           ('q0', '(', 'Z'): ('q0', '(Z'),
           ('q0', '(', '('): ('q0', '(('),
           ('q0', '(', '['): ('q0', '(['),
           ('q0', '(', '{'): ('q0', '({'),
           
           ('q0', '[', 'Z'): ('q0', '[Z'),
           ('q0', '[', '('): ('q0', '[('),
           ('q0', '[', '['): ('q0', '[['),
           ('q0', '[', '{'): ('q0', '[{'),
           
           ('q0', '{', 'Z'): ('q0', '{Z'),
           ('q0', '{', '('): ('q0', '{('),
           ('q0', '{', '['): ('q0', '{['),
           ('q0', '{', '{'): ('q0', '{{'),
           
           # Dépilement des parenthèses fermantes
           ('q0', ')', '('): ('q0', ''),
           ('q0', ']', '['): ('q0', ''),
           ('q0', '}', '{'): ('q0', ''),
           
           # Acceptation si pile vide
           ('q0', '', 'Z'): ('q1', 'Z'),
       },
       initial_state='q0',
       initial_stack_symbol='Z',
       final_states={'q1'}
   )

   # Tests
   test_expressions = [
       '()', '[]', '{}', '([])', '[()]', '{[]}',
       '((()))', '[()()]', '{[()]}',
       '(', ')', '([)]', '[(])', '([)]'
   ]
   
   for expr in test_expressions:
       result = parentheses_dpda.accepts(expr)
       print(f"'{expr}' -> {result}")

Exemple 5 : Conversion PDA vers CFG
------------------------------------

**Problème** : Convertir un PDA en grammaire contextuelle équivalente.

**Solution** :

.. code-block:: python

   from baobab_automata import DPDA
   from baobab_automata.pushdown import ConversionAlgorithms

   # DPDA simple
   simple_dpda = DPDA(
       states={'q0', 'q1'},
       alphabet={'a', 'b'},
       stack_alphabet={'A', 'Z'},
       transitions={
           ('q0', 'a', 'Z'): ('q0', 'AZ'),
           ('q0', 'a', 'A'): ('q0', 'AA'),
           ('q0', 'b', 'A'): ('q1', ''),
           ('q1', 'b', 'A'): ('q1', ''),
           ('q1', '', 'Z'): ('q1', 'Z'),
       },
       initial_state='q0',
       initial_stack_symbol='Z',
       final_states={'q1'}
   )

   # Conversion en grammaire contextuelle
   converter = ConversionAlgorithms()
   cfg = converter.pda_to_cfg(simple_dpda)
   
   print("Grammaire contextuelle générée :")
   for non_terminal, productions in cfg.items():
       print(f"{non_terminal} -> {' | '.join([' '.join(prod) for prod in productions])}")

Exemple 6 : Optimisation d'un PDA
-----------------------------------

**Problème** : Optimiser un PDA en supprimant les états inutiles et les transitions redondantes.

**Solution** :

.. code-block:: python

   from baobab_automata import DPDA
   from baobab_automata.pushdown import OptimizationAlgorithms

   # PDA non-optimisé
   unoptimized_dpda = DPDA(
       states={'q0', 'q1', 'q2', 'q3', 'q4'},
       alphabet={'a', 'b'},
       stack_alphabet={'A', 'B', 'Z'},
       transitions={
           ('q0', 'a', 'Z'): ('q1', 'AZ'),
           ('q1', 'a', 'A'): ('q1', 'AA'),
           ('q1', 'b', 'A'): ('q2', ''),
           ('q2', 'b', 'A'): ('q2', ''),
           ('q2', '', 'Z'): ('q3', 'Z'),
           ('q3', '', 'Z'): ('q4', 'Z'),  # Transition inutile
       },
       initial_state='q0',
       initial_stack_symbol='Z',
       final_states={'q4'}
   )

   print(f"États avant optimisation : {len(unoptimized_dpda.states)}")
   print(f"Transitions avant optimisation : {len(unoptimized_dpda.transitions)}")

   # Optimisation
   optimizer = OptimizationAlgorithms()
   optimized_dpda = optimizer.remove_unreachable_states(unoptimized_dpda)
   optimized_dpda = optimizer.remove_dead_states(optimized_dpda)
   optimized_dpda = optimizer.minimize_transitions(optimized_dpda)

   print(f"États après optimisation : {len(optimized_dpda.states)}")
   print(f"Transitions après optimisation : {len(optimized_dpda.transitions)}")

   # Vérification que les langages sont identiques
   test_strings = ['', 'ab', 'aabb', 'aaabbb', 'a', 'b']
   for string in test_strings:
       original_result = unoptimized_dpda.accepts(string)
       optimized_result = optimized_dpda.accepts(string)
       assert original_result == optimized_result, f"Différence pour '{string}'"
       print(f"'{string}' -> {original_result}")

Exemple 7 : Simulation pas à pas
---------------------------------

**Problème** : Simuler l'exécution d'un PDA pas à pas pour comprendre son comportement.

**Solution** :

.. code-block:: python

   from baobab_automata import DPDA

   # DPDA pour simulation
   simulation_dpda = DPDA(
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

   # Simulation pas à pas
   def simulate_step_by_step(pda, input_string):
       print(f"Simulation de '{input_string}' :")
       print("=" * 50)
       
       configurations = pda.simulate(input_string, step_by_step=True)
       
       for i, config in enumerate(configurations):
           print(f"Étape {i+1}:")
           print(f"  État: {config.state}")
           print(f"  Entrée restante: '{config.remaining_input}'")
           print(f"  Pile: {config.stack}")
           print(f"  Transition: {config.transition}")
           print()

   # Test avec différentes entrées
   test_strings = ['ab', 'aabb', 'a']
   for string in test_strings:
       simulate_step_by_step(simulation_dpda, string)
       print("\n" + "="*60 + "\n")

Exercices pratiques
--------------------

1. **Créer un DPDA** qui reconnaît le langage {a^n b^m c^n | n, m ≥ 0}
2. **Implémenter un NPDA** pour les expressions arithmétiques avec parenthèses
3. **Analyser une grammaire** plus complexe avec plusieurs règles
4. **Optimiser un PDA** avec de nombreux états redondants
5. **Simuler pas à pas** l'exécution d'un PDA complexe

Conseils d'implémentation
--------------------------

* **Conception** : Commencez par identifier les phases de traitement
* **Stack management** : Utilisez des symboles distincts pour chaque contexte
* **Non-déterminisme** : Exploitez le non-déterminisme pour simplifier la conception
* **Tests** : Testez avec des cas limites (chaînes vides, symboles non définis)
* **Visualisation** : Utilisez la visualisation pour comprendre le comportement
