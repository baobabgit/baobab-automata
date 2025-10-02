Exemples d'Algorithmes de Conversion
=======================================

Cette section présente des exemples pratiques d'algorithmes de conversion entre différents types d'automates.

Exemple 1 : Conversion NFA vers DFA avec Construction de Sous-ensembles
-----------------------------------------------------------------------

**Problème** : Convertir un NFA en DFA équivalent en utilisant la construction de sous-ensembles.

**Solution** :

.. code-block:: python

   from baobab_automata import NFA
   from baobab_automata.algorithms import nfa_to_dfa

   # NFA original
   nfa = NFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): {'q0', 'q1'},
           ('q0', 'b'): {'q0'},
           ('q1', 'a'): {'q2'},
           ('q1', 'b'): {'q2'},
       },
       initial_state='q0',
       final_states={'q2'}
   )

   print("NFA original :")
   print(f"États : {nfa.states}")
   print(f"Transitions : {nfa.transitions}")
   print(f"États finaux : {nfa.final_states}")

   # Conversion vers DFA
   dfa = nfa_to_dfa(nfa)

   print("\nDFA converti :")
   print(f"États : {dfa.states}")
   print(f"Transitions : {dfa.transitions}")
   print(f"États finaux : {dfa.final_states}")

   # Vérification de l'équivalence
   test_strings = ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb']
   print("\nVérification de l'équivalence :")
   for string in test_strings:
       nfa_result = nfa.accepts(string)
       dfa_result = dfa.accepts(string)
       print(f"'{string}' -> NFA: {nfa_result}, DFA: {dfa_result}")

Exemple 2 : Conversion Epsilon-NFA vers NFA
----------------------------------------------

**Problème** : Convertir un epsilon-NFA en NFA équivalent en supprimant les epsilon-transitions.

**Solution** :

.. code-block:: python

   from baobab_automata import EpsilonNFA
   from baobab_automata.algorithms import epsilon_nfa_to_nfa

   # Epsilon-NFA original
   epsilon_nfa = EpsilonNFA(
       states={'q0', 'q1', 'q2', 'q3'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', ''): {'q1'},      # epsilon-transition
           ('q1', 'a'): {'q2'},
           ('q2', ''): {'q3'},      # epsilon-transition
           ('q3', 'b'): {'q3'},
       },
       initial_state='q0',
       final_states={'q3'}
   )

   print("Epsilon-NFA original :")
   print(f"États : {epsilon_nfa.states}")
   print(f"Transitions : {epsilon_nfa.transitions}")
   print(f"États finaux : {epsilon_nfa.final_states}")

   # Conversion vers NFA
   nfa = epsilon_nfa_to_nfa(epsilon_nfa)

   print("\nNFA converti :")
   print(f"États : {nfa.states}")
   print(f"Transitions : {nfa.transitions}")
   print(f"États finaux : {nfa.final_states}")

   # Vérification de l'équivalence
   test_strings = ['a', 'b', 'ab', 'abb', 'aab', 'aaab']
   print("\nVérification de l'équivalence :")
   for string in test_strings:
       epsilon_result = epsilon_nfa.accepts(string)
       nfa_result = nfa.accepts(string)
       print(f"'{string}' -> ε-NFA: {epsilon_result}, NFA: {nfa_result}")

Exemple 3 : Conversion DPDA vers Grammaire Contextuelle
--------------------------------------------------------

**Problème** : Convertir un DPDA en grammaire contextuelle équivalente.

**Solution** :

.. code-block:: python

   from baobab_automata import DPDA
   from baobab_automata.algorithms import dpda_to_grammar

   # DPDA pour le langage a^n b^n
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

   print("DPDA original :")
   print(f"États : {dpda.states}")
   print(f"Alphabet : {dpda.alphabet}")
   print(f"Alphabet de pile : {dpda.stack_alphabet}")
   print(f"Transitions : {dpda.transitions}")

   # Conversion vers grammaire
   grammar = dpda_to_grammar(dpda)

   print("\nGrammaire générée :")
   print(f"Variables : {grammar.variables}")
   print(f"Terminaux : {grammar.terminals}")
   print(f"Symbole de départ : {grammar.start_symbol}")
   print("Règles de production :")
   for variable, productions in grammar.productions.items():
       for production in productions:
           print(f"  {variable} -> {production}")

   # Test de la grammaire
   test_strings = ['', 'ab', 'aabb', 'aaabbb', 'aab', 'abb']
   print("\nTest de la grammaire :")
   for string in test_strings:
       dpda_result = dpda.accepts(string)
       grammar_result = grammar.derives(string)
       print(f"'{string}' -> DPDA: {dpda_result}, Grammaire: {grammar_result}")

Exemple 4 : Conversion Grammaire vers NPDA
--------------------------------------------

**Problème** : Convertir une grammaire contextuelle en NPDA équivalent.

**Solution** :

.. code-block:: python

   from baobab_automata import Grammar
   from baobab_automata.algorithms import grammar_to_npda

   # Grammaire pour le langage a^n b^n c^n
   grammar = Grammar(
       variables={'S', 'A', 'B'},
       terminals={'a', 'b', 'c'},
       productions={
           'S': ['aAB', 'aB'],
           'A': ['aAB', 'aB'],
           'B': ['bC'],
           'C': ['bC', 'c'],
       },
       start_symbol='S'
   )

   print("Grammaire originale :")
   print(f"Variables : {grammar.variables}")
   print(f"Terminaux : {grammar.terminals}")
   print(f"Symbole de départ : {grammar.start_symbol}")
   print("Règles de production :")
   for variable, productions in grammar.productions.items():
       for production in productions:
           print(f"  {variable} -> {production}")

   # Conversion vers NPDA
   npda = grammar_to_npda(grammar)

   print("\nNPDA généré :")
   print(f"États : {npda.states}")
   print(f"Alphabet : {npda.alphabet}")
   print(f"Alphabet de pile : {npda.stack_alphabet}")
   print(f"État initial : {npda.initial_state}")
   print(f"Symbole initial de pile : {npda.initial_stack_symbol}")
   print(f"États finaux : {npda.final_states}")

   # Test du NPDA
   test_strings = ['abc', 'aabbcc', 'aaabbbccc', 'aabb', 'abcc', 'aabcc']
   print("\nTest du NPDA :")
   for string in test_strings:
       grammar_result = grammar.derives(string)
       npda_result = npda.accepts(string)
       print(f"'{string}' -> Grammaire: {grammar_result}, NPDA: {npda_result}")

Exemple 5 : Conversion Expression Régulière vers NFA
------------------------------------------------------

**Problème** : Convertir une expression régulière en NFA en utilisant la construction de Thompson.

**Solution** :

.. code-block:: python

   from baobab_automata.algorithms import regex_to_nfa

   # Expressions régulières à convertir
   regexes = [
       'a*',           # Répétition de 'a'
       'a|b',          # Union de 'a' et 'b'
       'ab',           # Concaténation de 'a' et 'b'
       '(a|b)*',       # Répétition de l'union
       'a+b',          # Un ou plusieurs 'a' suivis de 'b'
       '(ab)*',        # Répétition de la concaténation
   ]

   for regex in regexes:
       print(f"\nExpression régulière : {regex}")
       
       try:
           nfa = regex_to_nfa(regex)
           print(f"NFA généré avec {len(nfa.states)} états")
           print(f"Alphabet : {nfa.alphabet}")
           print(f"État initial : {nfa.initial_state}")
           print(f"États finaux : {nfa.final_states}")
           
           # Tests avec des chaînes appropriées
           if regex == 'a*':
               test_strings = ['', 'a', 'aa', 'aaa', 'b']
           elif regex == 'a|b':
               test_strings = ['a', 'b', 'ab', 'aa', 'bb']
           elif regex == 'ab':
               test_strings = ['ab', 'a', 'b', 'aba', 'abb']
           elif regex == '(a|b)*':
               test_strings = ['', 'a', 'b', 'ab', 'ba', 'aa', 'bb']
           elif regex == 'a+b':
               test_strings = ['ab', 'aab', 'aaab', 'b', 'bb']
           elif regex == '(ab)*':
               test_strings = ['', 'ab', 'abab', 'ababab', 'a', 'b']
           
           print("Tests de reconnaissance :")
           for string in test_strings:
               result = nfa.accepts(string)
               print(f"  '{string}' -> {result}")
               
       except Exception as e:
           print(f"Erreur lors de la conversion : {e}")

Exemple 6 : Conversion DTM vers DFA (pour Langages Réguliers)
--------------------------------------------------------------

**Problème** : Convertir une DTM qui reconnaît un langage régulier en DFA équivalent.

**Solution** :

.. code-block:: python

   from baobab_automata import DTM
   from baobab_automata.algorithms import dtm_to_dfa

   # DTM qui reconnaît les mots de longueur paire
   dtm = DTM(
       states={'q0', 'q1', 'q_accept', 'q_reject'},
       alphabet={'a', 'b'},
       tape_alphabet={'a', 'b', 'B'},
       transitions={
           ('q0', 'a'): ('q1', 'a', 'R'),
           ('q0', 'b'): ('q1', 'b', 'R'),
           ('q0', 'B'): ('q_accept', 'B', 'R'),  # Mot vide
           ('q1', 'a'): ('q0', 'a', 'R'),
           ('q1', 'b'): ('q0', 'b', 'R'),
           ('q1', 'B'): ('q_accept', 'B', 'R'),  # Longueur paire
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   print("DTM original :")
   print(f"États : {dtm.states}")
   print(f"Alphabet : {dtm.alphabet}")
   print(f"Alphabet de ruban : {dtm.tape_alphabet}")
   print(f"État initial : {dtm.initial_state}")
   print(f"Symbole blanc : {dtm.blank_symbol}")
   print(f"États finaux : {dtm.final_states}")

   # Conversion vers DFA
   try:
       dfa = dtm_to_dfa(dtm)
       
       print("\nDFA converti :")
       print(f"États : {dfa.states}")
       print(f"Alphabet : {dfa.alphabet}")
       print(f"État initial : {dfa.initial_state}")
       print(f"États finaux : {dfa.final_states}")
       print(f"Transitions : {dfa.transitions}")

       # Vérification de l'équivalence
       test_strings = ['', 'a', 'b', 'ab', 'ba', 'aa', 'bb', 'aba', 'abb', 'aab', 'bab']
       print("\nVérification de l'équivalence :")
       for string in test_strings:
           dtm_result = dtm.accepts(string)
           dfa_result = dfa.accepts(string)
           print(f"'{string}' -> DTM: {dtm_result}, DFA: {dfa_result}")
           
   except Exception as e:
       print(f"Conversion impossible : {e}")
       print("Le langage reconnu par cette DTM n'est pas régulier")

Exemple 7 : Conversion avec Optimisation
------------------------------------------

**Problème** : Effectuer une conversion avec optimisation pour réduire la taille de l'automate résultant.

**Solution** :

.. code-block:: python

   from baobab_automata import NFA
   from baobab_automata.algorithms import nfa_to_dfa, minimize_dfa, remove_unreachable_states

   # NFA complexe
   nfa = NFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): {'q1', 'q2'},
           ('q0', 'b'): {'q0'},
           ('q1', 'a'): {'q3'},
           ('q1', 'b'): {'q4'},
           ('q2', 'a'): {'q3'},
           ('q2', 'b'): {'q5'},
           ('q3', 'a'): {'q3'},
           ('q3', 'b'): {'q3'},
           ('q4', 'a'): {'q3'},
           ('q4', 'b'): {'q3'},
           ('q5', 'a'): {'q3'},
           ('q5', 'b'): {'q3'},
       },
       initial_state='q0',
       final_states={'q3'}
   )

   print("NFA original :")
   print(f"États : {len(nfa.states)}")
   print(f"Transitions : {len(nfa.transitions)}")

   # Conversion vers DFA
   dfa = nfa_to_dfa(nfa)
   print(f"\nDFA après conversion :")
   print(f"États : {len(dfa.states)}")
   print(f"Transitions : {len(dfa.transitions)}")

   # Suppression des états inaccessibles
   cleaned_dfa = remove_unreachable_states(dfa)
   print(f"\nDFA après nettoyage :")
   print(f"États : {len(cleaned_dfa.states)}")
   print(f"Transitions : {len(cleaned_dfa.transitions)}")

   # Minimisation
   minimized_dfa = minimize_dfa(cleaned_dfa)
   print(f"\nDFA après minimisation :")
   print(f"États : {len(minimized_dfa.states)}")
   print(f"Transitions : {len(minimized_dfa.transitions)}")

   # Vérification de l'équivalence
   test_strings = ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb']
   print("\nVérification de l'équivalence :")
   for string in test_strings:
       original_result = nfa.accepts(string)
       final_result = minimized_dfa.accepts(string)
       print(f"'{string}' -> NFA: {original_result}, DFA final: {final_result}")

Exemple 8 : Conversion en Cascade
-----------------------------------

**Problème** : Effectuer une série de conversions en cascade pour transformer un automate complexe.

**Solution** :

.. code-block:: python

   from baobab_automata import EpsilonNFA
   from baobab_automata.algorithms import (
       epsilon_nfa_to_nfa,
       nfa_to_dfa,
       minimize_dfa
   )

   # Epsilon-NFA complexe
   epsilon_nfa = EpsilonNFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', ''): {'q1', 'q2'},     # epsilon-transitions
           ('q1', 'a'): {'q3'},
           ('q2', 'b'): {'q4'},
           ('q3', ''): {'q5'},           # epsilon-transition
           ('q4', ''): {'q5'},           # epsilon-transition
           ('q5', 'a'): {'q5'},
           ('q5', 'b'): {'q5'},
       },
       initial_state='q0',
       final_states={'q5'}
   )

   print("Conversion en cascade :")
   print(f"1. Epsilon-NFA original : {len(epsilon_nfa.states)} états")

   # Étape 1 : Epsilon-NFA vers NFA
   nfa = epsilon_nfa_to_nfa(epsilon_nfa)
   print(f"2. NFA après suppression des ε-transitions : {len(nfa.states)} états")

   # Étape 2 : NFA vers DFA
   dfa = nfa_to_dfa(nfa)
   print(f"3. DFA après construction de sous-ensembles : {len(dfa.states)} états")

   # Étape 3 : Minimisation du DFA
   minimized_dfa = minimize_dfa(dfa)
   print(f"4. DFA après minimisation : {len(minimized_dfa.states)} états")

   # Vérification de l'équivalence à chaque étape
   test_strings = ['a', 'b', 'ab', 'ba', 'aa', 'bb', 'aba', 'abb', 'aab', 'bab']
   print("\nVérification de l'équivalence :")
   for string in test_strings:
       epsilon_result = epsilon_nfa.accepts(string)
       nfa_result = nfa.accepts(string)
       dfa_result = dfa.accepts(string)
       minimized_result = minimized_dfa.accepts(string)
       
       print(f"'{string}' -> ε-NFA: {epsilon_result}, NFA: {nfa_result}, "
             f"DFA: {dfa_result}, DFA min: {minimized_result}")

Exercices Pratiques
--------------------

1. **Convertir un NFA complexe** en DFA et analyser la croissance du nombre d'états
2. **Implémenter la conversion** d'une grammaire LL(1) en NPDA
3. **Optimiser les conversions** en supprimant les états inutiles à chaque étape
4. **Comparer les performances** de différentes méthodes de conversion
5. **Créer des outils de validation** pour vérifier l'équivalence des automates convertis

Conseils d'Implémentation
--------------------------

* **Validation** : Toujours valider l'équivalence après conversion
* **Optimisation** : Appliquez les optimisations à chaque étape
* **Tests** : Testez avec des cas limites et des automates complexes
* **Performance** : Surveillez la complexité des conversions
* **Documentation** : Documentez clairement les algorithmes utilisés
