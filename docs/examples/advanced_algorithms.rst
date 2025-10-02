Exemples d'Algorithmes Avancés
=================================

Cette section présente des exemples d'utilisation des algorithmes avancés de Baobab Automata.

Exemple 1 : Optimisation complète d'un automate
------------------------------------------------

**Problème** : Appliquer une série d'optimisations à un automate pour le rendre minimal.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.algorithms import (
       remove_unreachable_states, remove_dead_states, minimize_dfa
   )

   # DFA non-optimisé avec des états redondants
   unoptimized_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q2',
           ('q1', 'a'): 'q3',
           ('q1', 'b'): 'q4',
           ('q2', 'a'): 'q4',
           ('q2', 'b'): 'q5',
           ('q3', 'a'): 'q3',
           ('q3', 'b'): 'q6',
           ('q4', 'a'): 'q6',
           ('q4', 'b'): 'q5'),
           ('q5', 'a'): 'q7',
           ('q5', 'b'): 'q5'),
           ('q6', 'a'): 'q6',
           ('q6', 'b'): 'q7'),
           ('q7', 'a'): 'q7',
           ('q7', 'b'): 'q7'),
       },
       initial_state='q0',
       final_states={'q6', 'q7'}
   )

   print(f"DFA original: {len(unoptimized_dfa.states)} états")

   # Étape 1: Supprimer les états inaccessibles
   step1_dfa = remove_unreachable_states(unoptimized_dfa)
   print(f"Après suppression des états inaccessibles: {len(step1_dfa.states)} états")

   # Étape 2: Supprimer les états morts
   step2_dfa = remove_dead_states(step1_dfa)
   print(f"Après suppression des états morts: {len(step2_dfa.states)} états")

   # Étape 3: Minimiser
   minimal_dfa = minimize_dfa(step2_dfa)
   print(f"Après minimisation: {len(minimal_dfa.states)} états")

   # Vérification que les langages sont identiques
   test_strings = ['aa', 'bb', 'ab', 'ba', 'aab', 'bba', 'abab', 'baba']
   print(f"\nVérification de l'équivalence:")
   for string in test_strings:
       original_result = unoptimized_dfa.accepts(string)
       minimal_result = minimal_dfa.accepts(string)
       print(f"  '{string}': {original_result} == {minimal_result} {'✓' if original_result == minimal_result else '✗'}")

Exemple 2 : Analyse de complexité d'une machine de Turing
---------------------------------------------------------

**Problème** : Analyser la complexité temporelle et spatiale d'une machine de Turing.

**Solution** :

.. code-block:: python

   from baobab_automata import DTM
   from baobab_automata.turing import ComplexityAnalyzer
   import matplotlib.pyplot as plt

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
   input_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
   time_results = []
   space_results = []
   
   for size in input_sizes:
       # Créer une entrée de test
       test_input = ','.join(['1' if i % 2 == 0 else '0' for i in range(size)])
       
       # Analyser la complexité
       result = analyzer.analyze_complexity(sorting_dtm, test_input)
       
       time_results.append(result.time_steps)
       space_results.append(result.space_used)
       
       print(f"Taille {size}: Temps={result.time_steps}, Espace={result.space_used}")

   # Visualisation des résultats
   plt.figure(figsize=(12, 5))
   
   plt.subplot(1, 2, 1)
   plt.plot(input_sizes, time_results, 'bo-', label='Temps d\'exécution')
   plt.xlabel('Taille de l\'entrée')
   plt.ylabel('Nombre d\'étapes')
   plt.title('Complexité Temporelle')
   plt.grid(True)
   plt.legend()
   
   plt.subplot(1, 2, 2)
   plt.plot(input_sizes, space_results, 'ro-', label='Espace utilisé')
   plt.xlabel('Taille de l\'entrée')
   plt.ylabel('Cellules de ruban')
   plt.title('Complexité Spatiale')
   plt.grid(True)
   plt.legend()
   
   plt.tight_layout()
   plt.savefig('complexity_analysis.png', dpi=300, bbox_inches='tight')
   plt.show()

Exemple 3 : Algorithmes de reconnaissance avancés
--------------------------------------------------

**Problème** : Utiliser des algorithmes spécialisés pour la reconnaissance de patterns.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.algorithms import specialized_algorithms

   # DFA pour la reconnaissance de patterns
   pattern_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4'},
       alphabet={'a', 'b', 'c'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q0',
           ('q0', 'c'): 'q0',
           ('q1', 'a'): 'q1'),
           ('q1', 'b'): 'q2',
           ('q1', 'c'): 'q0',
           ('q2', 'a'): 'q3',
           ('q2', 'b'): 'q0',
           ('q2', 'c'): 'q0',
           ('q3', 'a'): 'q4',
           ('q3', 'b'): 'q0',
           ('q3', 'c'): 'q0',
           ('q4', 'a'): 'q4',
           ('q4', 'b'): 'q4',
           ('q4', 'c'): 'q4'),
       },
       initial_state='q0',
       final_states={'q4'}
   )

   # Texte de test
   test_text = "abcabcaabcaabcaabc"
   pattern = "aab"

   # Recherche de toutes les occurrences
   positions = specialized_algorithms.pattern_matching(test_text, pattern, pattern_dfa)
   print(f"Pattern '{pattern}' trouvé aux positions: {positions}")

   # Recherche de la plus longue correspondance
   longest_match, position = specialized_algorithms.longest_match(test_text, pattern_dfa)
   print(f"Plus longue correspondance: '{longest_match}' à la position {position}")

   # Analyse détaillée
   print(f"\nAnalyse du texte '{test_text}':")
   for i, char in enumerate(test_text):
       if i in positions:
           print(f"Position {i}: '{char}' [MATCH]")
       else:
           print(f"Position {i}: '{char}'")

Exemple 4 : Génération d'automates aléatoires
----------------------------------------------

**Problème** : Générer des automates aléatoires pour les tests et benchmarks.

**Solution** :

.. code-block:: python

   from baobab_automata.utils import generation
   from baobab_automata.algorithms import minimize_dfa
   import random

   # Générer des DFA aléatoires de différentes tailles
   sizes = [5, 10, 15, 20]
   alphabet_size = 3
   
   for size in sizes:
       print(f"\nGénération d'un DFA avec {size} états:")
       
       # Générer un DFA aléatoire
       random_dfa = generation.generate_random_dfa(size, alphabet_size)
       
       print(f"  États: {len(random_dfa.states)}")
       print(f"  Transitions: {len(random_dfa.transitions)}")
       print(f"  États finaux: {len(random_dfa.final_states)}")
       
       # Minimiser le DFA
       minimal_dfa = minimize_dfa(random_dfa)
       
       print(f"  Après minimisation: {len(minimal_dfa.states)} états")
       print(f"  Réduction: {len(random_dfa.states) - len(minimal_dfa.states)} états")

   # Générer un automate à partir d'une description de langage
   language_description = "mots contenant exactement deux 'a' consécutifs"
   generated_automaton = generation.generate_from_language(language_description)
   
   print(f"\nAutomate généré pour: {language_description}")
   print(f"Type: {type(generated_automaton).__name__}")
   print(f"États: {len(generated_automaton.states)}")
   
   # Test avec quelques chaînes
   test_strings = ['aa', 'baa', 'aab', 'baab', 'ab', 'a', 'aaa']
   for string in test_strings:
       result = generated_automaton.accepts(string)
       print(f"  '{string}': {result}")

Exemple 5 : Validation avancée d'automates
-------------------------------------------

**Problème** : Valider la cohérence et la complétude d'automates complexes.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA, NFA, DPDA
   from baobab_automata.utils import validation

   # DFA complet
   complete_dfa = DFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q2',
           ('q1', 'a'): 'q1'),
           ('q1', 'b'): 'q2'),
           ('q2', 'a'): 'q1'),
           ('q2', 'b'): 'q2'),
       },
       initial_state='q0',
       final_states={'q1'}
   )

   # DFA incomplet
   incomplete_dfa = DFA(
       states={'q0', 'q1'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1'),
           # Manque les transitions pour 'b' depuis q0
       },
       initial_state='q0',
       final_states={'q1'}
   )

   # Validation des automates
   automata_to_test = [
       ("DFA Complet", complete_dfa),
       ("DFA Incomplet", incomplete_dfa)
   ]

   for name, automaton in automata_to_test:
       print(f"\nValidation de {name}:")
       
       # Validation générale
       validation_result = validation.validate_automaton(automaton)
       print(f"  Validation générale: {'✓' if validation_result.is_valid else '✗'}")
       
       if not validation_result.is_valid:
           print(f"  Erreurs: {validation_result.errors}")
       
       # Vérification de complétude (pour DFA)
       if isinstance(automaton, DFA):
           is_complete = validation.check_completeness(automaton)
           print(f"  Complétude: {'✓' if is_complete else '✗'}")

   # Validation d'un DPDA
   dpda = DPDA(
       states={'q0', 'q1'},
       alphabet={'a', 'b'},
       stack_alphabet={'A', 'Z'},
       transitions={
           ('q0', 'a', 'Z'): ('q0', 'AZ'),
           ('q0', 'b', 'A'): ('q1', ''),
           ('q1', '', 'Z'): ('q1', 'Z'),
       },
       initial_state='q0',
       initial_stack_symbol='Z',
       final_states={'q1'}
   )

   print(f"\nValidation du DPDA:")
   dpda_validation = validation.validate_automaton(dpda)
   print(f"  Validation: {'✓' if dpda_validation.is_valid else '✗'}")
   if not dpda_validation.is_valid:
       print(f"  Erreurs: {dpda_validation.errors}")

Exemple 6 : Benchmark de performance
-------------------------------------

**Problème** : Comparer les performances de différents algorithmes.

**Solution** :

.. code-block:: python

   import time
   import matplotlib.pyplot as plt
   from baobab_automata import DFA, NFA
   from baobab_automata.algorithms import nfa_to_dfa, minimize_dfa
   from baobab_automata.utils import generation

   def benchmark_conversion():
       """Benchmark de la conversion NFA vers DFA."""
       sizes = [5, 10, 15, 20, 25]
       conversion_times = []
       minimization_times = []
       
       for size in sizes:
           print(f"Test avec {size} états...")
           
           # Générer un NFA aléatoire
           nfa = generation.generate_random_dfa(size, 2)  # Utiliser DFA comme NFA pour le test
           
           # Benchmark conversion
           start_time = time.time()
           dfa = nfa_to_dfa(nfa)
           conversion_time = time.time() - start_time
           conversion_times.append(conversion_time)
           
           # Benchmark minimisation
           start_time = time.time()
           minimal_dfa = minimize_dfa(dfa)
           minimization_time = time.time() - start_time
           minimization_times.append(minimization_time)
           
           print(f"  Conversion: {conversion_time:.4f}s")
           print(f"  Minimisation: {minimization_time:.4f}s")
           print(f"  États finaux: {len(minimal_dfa.states)}")

       # Visualisation des résultats
       plt.figure(figsize=(10, 6))
       plt.plot(sizes, conversion_times, 'bo-', label='Conversion NFA→DFA')
       plt.plot(sizes, minimization_times, 'ro-', label='Minimisation DFA')
       plt.xlabel('Nombre d\'états')
       plt.ylabel('Temps (secondes)')
       plt.title('Benchmark des Algorithmes')
       plt.legend()
       plt.grid(True)
       plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
       plt.show()

   def benchmark_recognition():
       """Benchmark de la reconnaissance."""
       # Créer un gros automate
       large_dfa = generation.generate_random_dfa(50, 3)
       
       # Générer des chaînes de test de différentes longueurs
       string_lengths = [10, 50, 100, 500, 1000]
       recognition_times = []
       
       for length in string_lengths:
           # Générer une chaîne aléatoire
           test_string = ''.join(random.choices(['a', 'b', 'c'], k=length))
           
           # Benchmark reconnaissance
           start_time = time.time()
           result = large_dfa.accepts(test_string)
           recognition_time = time.time() - start_time
           recognition_times.append(recognition_time)
           
           print(f"Longueur {length}: {recognition_time:.6f}s")

       # Visualisation
       plt.figure(figsize=(8, 5))
       plt.plot(string_lengths, recognition_times, 'go-')
       plt.xlabel('Longueur de la chaîne')
       plt.ylabel('Temps de reconnaissance (secondes)')
       plt.title('Performance de Reconnaissance')
       plt.grid(True)
       plt.savefig('recognition_performance.png', dpi=300, bbox_inches='tight')
       plt.show()

   # Exécuter les benchmarks
   print("=== Benchmark de Conversion ===")
   benchmark_conversion()
   
   print("\n=== Benchmark de Reconnaissance ===")
   benchmark_recognition()

Exemple 7 : Optimisation de mémoire
------------------------------------

**Problème** : Optimiser l'utilisation mémoire pour de gros automates.

**Solution** :

.. code-block:: python

   import psutil
   import gc
   from baobab_automata import DFA
   from baobab_automata.algorithms import minimize_dfa
   from baobab_automata.utils import generation

   def monitor_memory():
       """Surveille l'utilisation mémoire."""
       process = psutil.Process()
       return process.memory_info().rss / 1024 / 1024  # MB

   def test_memory_optimization():
       """Test d'optimisation mémoire."""
       print("Test d'optimisation mémoire:")
       
       # Mesurer la mémoire initiale
       initial_memory = monitor_memory()
       print(f"Mémoire initiale: {initial_memory:.2f} MB")
       
       # Créer un gros automate
       large_dfa = generation.generate_random_dfa(100, 4)
       after_creation = monitor_memory()
       print(f"Après création: {after_creation:.2f} MB (+{after_creation - initial_memory:.2f} MB)")
       
       # Minimiser l'automate
       minimal_dfa = minimize_dfa(large_dfa)
       after_minimization = monitor_memory()
       print(f"Après minimisation: {after_minimization:.2f} MB (+{after_minimization - after_creation:.2f} MB)")
       
       # Supprimer les références
       del large_dfa
       del minimal_dfa
       gc.collect()
       
       after_cleanup = monitor_memory()
       print(f"Après nettoyage: {after_cleanup:.2f} MB")
       
       # Test avec plusieurs automates
       print(f"\nTest avec plusieurs automates:")
       automata = []
       
       for i in range(10):
           dfa = generation.generate_random_dfa(50, 3)
           automata.append(dfa)
           
           if i % 2 == 0:
               memory = monitor_memory()
               print(f"  {i+1} automates: {memory:.2f} MB")
       
       # Nettoyage final
       del automata
       gc.collect()
       final_memory = monitor_memory()
       print(f"Mémoire finale: {final_memory:.2f} MB")

   # Exécuter le test
   test_memory_optimization()

Conseils d'optimisation
-----------------------

* **Profiling** : Utilisez des outils de profiling pour identifier les goulots d'étranglement
* **Cache** : Mettez en cache les résultats de calculs coûteux
* **Lazy evaluation** : Calculez les propriétés à la demande
* **Mémoire** : Surveillez l'utilisation mémoire pour de gros automates
* **Parallélisation** : Utilisez la parallélisation pour les opérations indépendantes
* **Algorithmes** : Choisissez les algorithmes les plus efficaces selon le contexte
