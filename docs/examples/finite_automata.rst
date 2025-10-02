Exemples d'Automates Finis
===========================

Cette section présente des exemples pratiques d'utilisation des automates finis avec Baobab Automata.

Exemple 1 : Reconnaissance de mots se terminant par "ing"
---------------------------------------------------------

**Problème** : Créer un DFA qui reconnaît tous les mots anglais se terminant par "ing".

**Solution** :

.. code-block:: python

   from baobab_automata import DFA

   # DFA pour les mots se terminant par "ing"
   ing_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3'},
       alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
       transitions={
           # Transitions depuis q0
           ('q0', 'i'): 'q1',
           ('q0', 'a'): 'q0', ('q0', 'b'): 'q0', ('q0', 'c'): 'q0', ('q0', 'd'): 'q0',
           ('q0', 'e'): 'q0', ('q0', 'f'): 'q0', ('q0', 'g'): 'q0', ('q0', 'h'): 'q0',
           ('q0', 'j'): 'q0', ('q0', 'k'): 'q0', ('q0', 'l'): 'q0', ('q0', 'm'): 'q0',
           ('q0', 'n'): 'q0', ('q0', 'o'): 'q0', ('q0', 'p'): 'q0', ('q0', 'q'): 'q0',
           ('q0', 'r'): 'q0', ('q0', 's'): 'q0', ('q0', 't'): 'q0', ('q0', 'u'): 'q0',
           ('q0', 'v'): 'q0', ('q0', 'w'): 'q0', ('q0', 'x'): 'q0', ('q0', 'y'): 'q0',
           ('q0', 'z'): 'q0',
           
           # Transitions depuis q1
           ('q1', 'n'): 'q2',
           ('q1', 'a'): 'q0', ('q1', 'b'): 'q0', ('q1', 'c'): 'q0', ('q1', 'd'): 'q0',
           ('q1', 'e'): 'q0', ('q1', 'f'): 'q0', ('q1', 'g'): 'q0', ('q1', 'h'): 'q0',
           ('q1', 'i'): 'q1', ('q1', 'j'): 'q0', ('q1', 'k'): 'q0', ('q1', 'l'): 'q0',
           ('q1', 'm'): 'q0', ('q1', 'o'): 'q0', ('q1', 'p'): 'q0', ('q1', 'q'): 'q0',
           ('q1', 'r'): 'q0', ('q1', 's'): 'q0', ('q1', 't'): 'q0', ('q1', 'u'): 'q0',
           ('q1', 'v'): 'q0', ('q1', 'w'): 'q0', ('q1', 'x'): 'q0', ('q1', 'y'): 'q0',
           ('q1', 'z'): 'q0',
           
           # Transitions depuis q2
           ('q2', 'g'): 'q3',
           ('q2', 'a'): 'q0', ('q2', 'b'): 'q0', ('q2', 'c'): 'q0', ('q2', 'd'): 'q0',
           ('q2', 'e'): 'q0', ('q2', 'f'): 'q0', ('q2', 'h'): 'q0', ('q2', 'i'): 'q1',
           ('q2', 'j'): 'q0', ('q2', 'k'): 'q0', ('q2', 'l'): 'q0', ('q2', 'm'): 'q0',
           ('q2', 'n'): 'q2', ('q2', 'o'): 'q0', ('q2', 'p'): 'q0', ('q2', 'q'): 'q0',
           ('q2', 'r'): 'q0', ('q2', 's'): 'q0', ('q2', 't'): 'q0', ('q2', 'u'): 'q0',
           ('q2', 'v'): 'q0', ('q2', 'w'): 'q0', ('q2', 'x'): 'q0', ('q2', 'y'): 'q0',
           ('q2', 'z'): 'q0',
           
           # Transitions depuis q3
           ('q3', 'a'): 'q0', ('q3', 'b'): 'q0', ('q3', 'c'): 'q0', ('q3', 'd'): 'q0',
           ('q3', 'e'): 'q0', ('q3', 'f'): 'q0', ('q3', 'g'): 'q0', ('q3', 'h'): 'q0',
           ('q3', 'i'): 'q1', ('q3', 'j'): 'q0', ('q3', 'k'): 'q0', ('q3', 'l'): 'q0',
           ('q3', 'm'): 'q0', ('q3', 'n'): 'q2', ('q3', 'o'): 'q0', ('q3', 'p'): 'q0',
           ('q3', 'q'): 'q0', ('q3', 'r'): 'q0', ('q3', 's'): 'q0', ('q3', 't'): 'q0',
           ('q3', 'u'): 'q0', ('q3', 'v'): 'q0', ('q3', 'w'): 'q0', ('q3', 'x'): 'q0',
           ('q3', 'y'): 'q0', ('q3', 'z'): 'q0',
       },
       initial_state='q0',
       final_states={'q3'}
   )

   # Tests
   test_words = ['sing', 'running', 'playing', 'cat', 'dog', 'interesting']
   for word in test_words:
       result = ing_dfa.accepts(word)
       print(f"'{word}' -> {result}")

   # Visualisation
   ing_dfa.visualize('ing_dfa.png')

**Résultats attendus** :

::

   'sing' -> True
   'running' -> True
   'playing' -> True
   'cat' -> False
   'dog' -> False
   'interesting' -> True

Exemple 2 : NFA pour les nombres binaires pairs
-----------------------------------------------

**Problème** : Créer un NFA qui reconnaît les nombres binaires pairs (se terminant par 0).

**Solution** :

.. code-block:: python

   from baobab_automata import NFA

   # NFA pour les nombres binaires pairs
   binary_even_nfa = NFA(
       states={'q0', 'q1'},
       alphabet={'0', '1'},
       transitions={
           ('q0', '0'): {'q0', 'q1'},
           ('q0', '1'): {'q0'},
           ('q1', '0'): {'q1'},
           ('q1', '1'): {'q1'},
       },
       initial_state='q0',
       final_states={'q1'}
   )

   # Tests
   test_numbers = ['0', '10', '110', '1000', '1010', '1', '11', '101']
   for num in test_numbers:
       result = binary_even_nfa.accepts(num)
       print(f"'{num}' -> {result}")

   # Conversion en DFA
   from baobab_automata.algorithms import nfa_to_dfa
   binary_even_dfa = nfa_to_dfa(binary_even_nfa)
   
   print("\nAprès conversion en DFA :")
   for num in test_numbers:
       result = binary_even_dfa.accepts(num)
       print(f"'{num}' -> {result}")

Exemple 3 : Epsilon-NFA pour les expressions régulières
--------------------------------------------------------

**Problème** : Créer un epsilon-NFA pour l'expression régulière (a|b)*abb.

**Solution** :

.. code-block:: python

   from baobab_automata import EpsilonNFA

   # Epsilon-NFA pour (a|b)*abb
   regex_epsilon_nfa = EpsilonNFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4'},
       alphabet={'a', 'b'},
       transitions={
           # Transitions epsilon
           ('q0', ''): {'q1', 'q2'},
           
           # Boucle (a|b)*
           ('q1', 'a'): {'q1'},
           ('q1', 'b'): {'q1'},
           ('q1', ''): {'q2'},
           
           # Premier 'a'
           ('q2', 'a'): {'q3'},
           
           # Premier 'b'
           ('q3', 'b'): {'q4'},
           
           # Deuxième 'b'
           ('q4', 'b'): {'q5'},
       },
       initial_state='q0',
       final_states={'q5'}
   )

   # Tests
   test_strings = ['abb', 'aabb', 'babb', 'ababb', 'ab', 'aab']
   for string in test_strings:
       result = regex_epsilon_nfa.accepts(string)
       print(f"'{string}' -> {result}")

Exemple 4 : Minimisation d'un DFA
---------------------------------

**Problème** : Minimiser un DFA pour réduire le nombre d'états.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.algorithms import minimize_dfa

   # DFA non-minimal
   non_minimal_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q2',
           ('q1', 'a'): 'q3',
           ('q1', 'b'): 'q4',
           ('q2', 'a'): 'q4',
           ('q2', 'b'): 'q5',
           ('q3', 'a'): 'q3',
           ('q3', 'b'): 'q4',
           ('q4', 'a'): 'q4',
           ('q4', 'b'): 'q5',
           ('q5', 'a'): 'q4',
           ('q5', 'b'): 'q5',
       },
       initial_state='q0',
       final_states={'q3', 'q5'}
   )

   print(f"États avant minimisation : {len(non_minimal_dfa.states)}")

   # Minimisation
   minimal_dfa = minimize_dfa(non_minimal_dfa)
   print(f"États après minimisation : {len(minimal_dfa.states)}")

   # Vérification que les langages sont identiques
   test_strings = ['aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb']
   for string in test_strings:
       original_result = non_minimal_dfa.accepts(string)
       minimal_result = minimal_dfa.accepts(string)
       assert original_result == minimal_result, f"Différence pour '{string}'"
       print(f"'{string}' -> {original_result}")

Exemple 5 : Opérations sur les langages
----------------------------------------

**Problème** : Effectuer des opérations d'union, intersection et complément sur des langages.

**Solution** :

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
   
   # Intersection : mots contenant 'aa' ET 'bb'
   intersection_dfa = language_operations.intersection(dfa_aa, dfa_bb)
   
   # Complément : mots ne contenant ni 'aa' ni 'bb'
   complement_dfa = language_operations.complement(union_dfa)

   # Tests
   test_words = ['aa', 'bb', 'aabb', 'ab', 'ba', 'aab', 'bba']
   
   print("Union (aa OU bb) :")
   for word in test_words:
       result = union_dfa.accepts(word)
       print(f"  '{word}' -> {result}")
   
   print("\nIntersection (aa ET bb) :")
   for word in test_words:
       result = intersection_dfa.accepts(word)
       print(f"  '{word}' -> {result}")
   
   print("\nComplément (ni aa ni bb) :")
   for word in test_words:
       result = complement_dfa.accepts(word)
       print(f"  '{word}' -> {result}")

Exercices pratiques
--------------------

1. **Créer un DFA** qui reconnaît les adresses email valides (format simplifié)
2. **Implémenter un NFA** pour les nombres décimaux avec point décimal
3. **Construire un epsilon-NFA** pour l'expression régulière (ab)*|(ba)*
4. **Minimiser un DFA** avec plus de 10 états
5. **Effectuer des opérations** sur trois langages différents

Solutions et conseils
----------------------

* Utilisez la visualisation pour comprendre le comportement des automates
* Testez toujours vos automates avec plusieurs chaînes d'entrée
* Documentez vos automates avec des commentaires explicatifs
* Considérez les cas limites (chaînes vides, symboles non définis)
