Exemples de Machines de Turing
===============================

Cette section présente des exemples pratiques d'utilisation des machines de Turing avec Baobab Automata.

Exemple 1 : DTM pour l'addition binaire
----------------------------------------

**Problème** : Créer une DTM qui additionne deux nombres binaires.

**Solution** :

.. code-block:: python

   from baobab_automata import DTM

   # DTM pour l'addition binaire (format: a+b=)
   binary_addition_dtm = DTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q_accept', 'q_reject'},
       alphabet={'0', '1', '+', '='},
       tape_alphabet={'0', '1', '+', '=', 'B', 'X', 'Y'},
       transitions={
           # Phase 1 : Aller à la fin du premier nombre
           ('q0', '0'): ('q0', '0', 'R'),
           ('q0', '1'): ('q0', '1', 'R'),
           ('q0', '+'): ('q1', '+', 'R'),
           
           # Phase 2 : Aller à la fin du deuxième nombre
           ('q1', '0'): ('q1', '0', 'R'),
           ('q1', '1'): ('q1', '1', 'R'),
           ('q1', '='): ('q2', '=', 'L'),
           
           # Phase 3 : Addition de droite à gauche
           ('q2', '0'): ('q3', 'X', 'L'),
           ('q2', '1'): ('q4', 'Y', 'L'),
           ('q2', '+'): ('q8', '+', 'L'),
           
           # Cas : 0 + 0 = 0
           ('q3', '0'): ('q3', '0', 'L'),
           ('q3', '1'): ('q3', '1', 'L'),
           ('q3', '+'): ('q5', '+', 'L'),
           ('q5', '0'): ('q5', '0', 'L'),
           ('q5', '1'): ('q5', '1', 'L'),
           ('q5', 'B'): ('q6', '0', 'R'),
           ('q6', '0'): ('q6', '0', 'R'),
           ('q6', '1'): ('q6', '1', 'R'),
           ('q6', '+'): ('q6', '+', 'R'),
           ('q6', '='): ('q6', '=', 'R'),
           ('q6', 'X'): ('q2', '0', 'L'),
           
           # Cas : 0 + 1 = 1 ou 1 + 0 = 1
           ('q4', '0'): ('q4', '0', 'L'),
           ('q4', '1'): ('q4', '1', 'L'),
           ('q4', '+'): ('q7', '+', 'L'),
           ('q7', '0'): ('q7', '0', 'L'),
           ('q7', '1'): ('q7', '1', 'L'),
           ('q7', 'B'): ('q6', '1', 'R'),
           ('q6', 'Y'): ('q2', '1', 'L'),
           
           # Cas : 1 + 1 = 10 (avec retenue)
           ('q4', '1'): ('q4', '1', 'L'),
           ('q4', '+'): ('q7', '+', 'L'),
           ('q7', '1'): ('q7', '1', 'L'),
           ('q7', 'B'): ('q6', '0', 'R'),
           ('q6', 'Y'): ('q2', '0', 'L'),
           
           # Finalisation
           ('q8', '0'): ('q8', '0', 'L'),
           ('q8', '1'): ('q8', '1', 'L'),
           ('q8', 'B'): ('q9', 'B', 'R'),
           ('q9', '0'): ('q9', '0', 'R'),
           ('q9', '1'): ('q9', '1', 'R'),
           ('q9', '+'): ('q9', '+', 'R'),
           ('q9', '='): ('q9', '=', 'R'),
           ('q9', 'B'): ('q_accept', 'B', 'R'),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Tests (format simplifié pour la démonstration)
   test_cases = ['10+1=', '11+1=', '101+10=']
   for case in test_cases:
       print(f"Test: {case}")
       # Note: Cette implémentation est simplifiée pour l'exemple
       # Une implémentation complète nécessiterait plus de transitions

Exemple 2 : NTM pour le problème de satisfiabilité (SAT)
---------------------------------------------------------

**Problème** : Créer une NTM qui résout le problème SAT pour des formules en forme normale conjonctive (CNF).

**Solution** :

.. code-block:: python

   from baobab_automata import NTM

   # NTM pour SAT (exemple simplifié avec 2 variables)
   sat_ntm = NTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q_accept', 'q_reject'},
       alphabet={'0', '1', '(', ')', '&', '|', '~', 'x', 'y'},
       tape_alphabet={'0', '1', '(', ')', '&', '|', '~', 'x', 'y', 'B', 'T', 'F'},
       transitions={
           # Phase 1 : Non-déterministe - choisir une assignation
           ('q0', 'x'): ('q1', 'T', 'R'),  # x = True
           ('q0', 'x'): ('q2', 'F', 'R'),  # x = False
           ('q0', 'y'): ('q3', 'T', 'R'),  # y = True
           ('q0', 'y'): ('q4', 'F', 'R'),  # y = False
           
           # Phase 2 : Évaluer la formule
           ('q1', 'T'): ('q1', 'T', 'R'),
           ('q1', 'F'): ('q1', 'F', 'R'),
           ('q1', '&'): ('q5', '&', 'R'),
           ('q1', '|'): ('q5', '|', 'R'),
           ('q1', ')'): ('q6', ')', 'R'),
           
           # Évaluation des clauses
           ('q5', 'T'): ('q5', 'T', 'R'),
           ('q5', 'F'): ('q5', 'F', 'R'),
           ('q5', '&'): ('q5', '&', 'R'),
           ('q5', '|'): ('q5', '|', 'R'),
           ('q5', ')'): ('q6', ')', 'R'),
           
           # Acceptation si formule satisfaite
           ('q6', 'B'): ('q_accept', 'B', 'R'),
           
           # Rejet si formule non satisfaite
           ('q6', 'F'): ('q_reject', 'F', 'R'),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Test avec une formule simple : (x | y) & (~x | y)
   # Format simplifié pour la démonstration
   test_formula = "(x|y)&(~x|y)"
   print(f"Test SAT pour: {test_formula}")

Exemple 3 : Machine de Turing multi-rubans
--------------------------------------------

**Problème** : Créer une machine de Turing multi-rubans pour la multiplication binaire.

**Solution** :

.. code-block:: python

   from baobab_automata import MultiTapeTM

   # Machine multi-rubans pour multiplication binaire
   multiplication_mtm = MultiTapeTM(
       num_tapes=3,  # Ruban 1: multiplicande, Ruban 2: multiplicateur, Ruban 3: résultat
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q_accept', 'q_reject'},
       alphabet={'0', '1'},
       tape_alphabet={'0', '1', 'B', 'X', 'Y'},
       transitions={
           # Initialisation : copier le multiplicande sur le ruban 3
           ('q0', ('1', 'B', 'B')): ('q1', ('1', 'B', '1'), ('R', 'S', 'R')),
           ('q0', ('0', 'B', 'B')): ('q1', ('0', 'B', '0'), ('R', 'S', 'R')),
           
           # Phase de multiplication
           ('q1', ('1', '1', 'B')): ('q2', ('1', '1', '1'), ('S', 'R', 'R')),
           ('q1', ('0', '1', 'B')): ('q2', ('0', '1', '0'), ('S', 'R', 'R')),
           ('q1', ('1', '0', 'B')): ('q2', ('1', '0', '0'), ('S', 'R', 'R')),
           ('q1', ('0', '0', 'B')): ('q2', ('0', '0', '0'), ('S', 'R', 'R')),
           
           # Finalisation
           ('q2', ('B', 'B', 'B')): ('q_accept', ('B', 'B', 'B'), ('S', 'S', 'S')),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Test de multiplication : 11 * 10 = 110
   print("Test multiplication multi-rubans:")
   print("11 * 10 = 110")

Exemple 4 : Simulation pas à pas d'une DTM
-------------------------------------------

**Problème** : Simuler l'exécution d'une DTM pas à pas pour comprendre son comportement.

**Solution** :

.. code-block:: python

   from baobab_automata import DTM

   # DTM simple pour inversion de chaîne binaire
   reverse_dtm = DTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'},
       alphabet={'0', '1'},
       tape_alphabet={'0', '1', 'B', 'X', 'Y'},
       transitions={
           # Phase 1 : Marquer la fin
           ('q0', '0'): ('q0', '0', 'R'),
           ('q0', '1'): ('q0', '1', 'R'),
           ('q0', 'B'): ('q1', 'B', 'L'),
           
           # Phase 2 : Inversion
           ('q1', '0'): ('q2', 'X', 'L'),
           ('q1', '1'): ('q3', 'Y', 'L'),
           ('q1', 'X'): ('q1', 'X', 'L'),
           ('q1', 'Y'): ('q1', 'Y', 'L'),
           ('q1', 'B'): ('q4', 'B', 'R'),
           
           # Remplacer X par 0 et Y par 1
           ('q2', 'X'): ('q2', 'X', 'L'),
           ('q2', 'Y'): ('q2', 'Y', 'L'),
           ('q2', 'B'): ('q4', '0', 'R'),
           
           ('q3', 'X'): ('q3', 'X', 'L'),
           ('q3', 'Y'): ('q3', 'Y', 'L'),
           ('q3', 'B'): ('q4', '1', 'R'),
           
           # Phase 3 : Finalisation
           ('q4', 'X'): ('q4', '0', 'R'),
           ('q4', 'Y'): ('q4', '1', 'R'),
           ('q4', 'B'): ('q_accept', 'B', 'R'),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Simulation pas à pas
   def simulate_tm_step_by_step(tm, input_string):
       print(f"Simulation de '{input_string}' :")
       print("=" * 60)
       
       configurations = tm.simulate(input_string, step_by_step=True)
       
       for i, config in enumerate(configurations):
           print(f"Étape {i+1}:")
           print(f"  État: {config.state}")
           print(f"  Ruban: {config.tape}")
           print(f"  Position: {config.head_position}")
           print(f"  Transition: {config.transition}")
           print()

   # Test avec différentes entrées
   test_strings = ['01', '110', '1010']
   for string in test_strings:
       simulate_tm_step_by_step(reverse_dtm, string)
       print("\n" + "="*60 + "\n")

Exemple 5 : Analyse de complexité
----------------------------------

**Problème** : Analyser la complexité temporelle et spatiale d'une machine de Turing.

**Solution** :

.. code-block:: python

   from baobab_automata import DTM
   from baobab_automata.turing import ComplexityAnalyzer

   # DTM pour le tri de nombres binaires
   sorting_dtm = DTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q_accept'},
       alphabet={'0', '1', ','},
       tape_alphabet={'0', '1', ',', 'B', 'X', 'Y'},
       transitions={
           # Algorithme de tri à bulles simplifié
           ('q0', '0'): ('q0', '0', 'R'),
           ('q0', '1'): ('q0', '1', 'R'),
           ('q0', ','): ('q0', ',', 'R'),
           ('q0', 'B'): ('q1', 'B', 'L'),
           
           # Phase de tri
           ('q1', '1'): ('q2', 'X', 'L'),
           ('q1', '0'): ('q1', '0', 'L'),
           ('q1', ','): ('q1', ',', 'L'),
           ('q1', 'B'): ('q6', 'B', 'R'),
           
           ('q2', '0'): ('q3', 'Y', 'R'),
           ('q2', '1'): ('q2', '1', 'L'),
           ('q2', ','): ('q2', ',', 'L'),
           
           ('q3', 'X'): ('q3', 'X', 'R'),
           ('q3', 'Y'): ('q3', 'Y', 'R'),
           ('q3', 'B'): ('q4', 'B', 'L'),
           
           ('q4', 'Y'): ('q4', '0', 'L'),
           ('q4', 'X'): ('q4', '1', 'L'),
           ('q4', ','): ('q5', ',', 'L'),
           
           ('q5', '0'): ('q5', '0', 'L'),
           ('q5', '1'): ('q5', '1', 'L'),
           ('q5', 'B'): ('q1', 'B', 'R'),
           
           ('q6', '0'): ('q6', '0', 'R'),
           ('q6', '1'): ('q6', '1', 'R'),
           ('q6', ','): ('q6', ',', 'R'),
           ('q6', 'B'): ('q_accept', 'B', 'R'),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Analyse de complexité
   analyzer = ComplexityAnalyzer()
   
   # Test avec différentes tailles d'entrée
   test_inputs = ['1,0', '1,0,1', '1,0,1,0', '1,0,1,0,1']
   
   for input_str in test_inputs:
       print(f"Analyse pour '{input_str}':")
       
       # Simulation avec métriques
       result = analyzer.analyze_complexity(sorting_dtm, input_str)
       
       print(f"  Temps d'exécution: {result.time_steps} étapes")
       print(f"  Espace utilisé: {result.space_used} cellules")
       print(f"  Complexité temporelle: O({result.time_complexity})")
       print(f"  Complexité spatiale: O({result.space_complexity})")
       print()

Exemple 6 : Machine de Turing universelle (simplifiée)
-------------------------------------------------------

**Problème** : Créer une machine de Turing qui peut simuler d'autres machines de Turing.

**Solution** :

.. code-block:: python

   from baobab_automata import UniversalTM

   # Machine de Turing universelle simplifiée
   universal_tm = UniversalTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q_accept', 'q_reject'},
       alphabet={'0', '1', '#', ';'},
       tape_alphabet={'0', '1', '#', ';', 'B', 'X', 'Y', 'Z'},
       transitions={
           # Phase 1 : Parser la description de la machine
           ('q0', '0'): ('q0', '0', 'R'),
           ('q0', '1'): ('q0', '1', 'R'),
           ('q0', '#'): ('q1', '#', 'R'),
           ('q0', ';'): ('q2', ';', 'R'),
           
           # Phase 2 : Simuler la machine décrite
           ('q1', '0'): ('q3', 'X', 'R'),
           ('q1', '1'): ('q4', 'Y', 'R'),
           ('q1', 'B'): ('q5', 'B', 'R'),
           
           # Simulation des transitions
           ('q3', 'X'): ('q3', 'X', 'R'),
           ('q3', 'Y'): ('q3', 'Y', 'R'),
           ('q3', 'B'): ('q6', 'B', 'L'),
           
           ('q4', 'X'): ('q4', 'X', 'R'),
           ('q4', 'Y'): ('q4', 'Y', 'R'),
           ('q4', 'B'): ('q7', 'B', 'L'),
           
           # Finalisation
           ('q6', 'X'): ('q6', '0', 'L'),
           ('q6', 'Y'): ('q6', '1', 'L'),
           ('q6', 'B'): ('q_accept', 'B', 'R'),
           
           ('q7', 'X'): ('q7', '0', 'L'),
           ('q7', 'Y'): ('q7', '1', 'L'),
           ('q7', 'B'): ('q_accept', 'B', 'R'),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Test avec une description simplifiée d'une machine
   # Format: description#entrée
   machine_description = "01#101"  # Machine simple qui accepte les chaînes avec '01'
   print(f"Simulation universelle de: {machine_description}")

Exercices pratiques
--------------------

1. **Créer une DTM** qui multiplie deux nombres binaires
2. **Implémenter une NTM** pour le problème du voyageur de commerce
3. **Construire une machine multi-rubans** pour la division binaire
4. **Analyser la complexité** d'une machine de tri
5. **Simuler pas à pas** l'exécution d'une machine complexe

Conseils d'implémentation
--------------------------

* **Conception** : Divisez le problème en phases logiques
* **États** : Utilisez des noms d'états descriptifs
* **Transitions** : Documentez chaque transition avec des commentaires
* **Tests** : Testez avec des cas simples avant des cas complexes
* **Optimisation** : Minimisez le nombre d'états et de transitions
* **Visualisation** : Utilisez la visualisation pour comprendre le comportement
