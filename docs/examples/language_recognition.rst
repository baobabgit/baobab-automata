Exemples de Reconnaissance de Langages
=======================================

Cette section présente des exemples pratiques de reconnaissance de langages avec différents types d'automates.

Exemple 1 : Reconnaissance de mots anglais
--------------------------------------------

**Problème** : Créer un automate qui reconnaît les mots anglais courants.

**Solution avec DFA** :

.. code-block:: python

   from baobab_automata import DFA

   # DFA pour les mots anglais courants
   english_words_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'},
       alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
       transitions={
           # Transitions pour "cat"
           ('q0', 'c'): 'q1',
           ('q1', 'a'): 'q2',
           ('q2', 't'): 'q3',
           
           # Transitions pour "dog"
           ('q0', 'd'): 'q4',
           ('q4', 'o'): 'q5',
           ('q5', 'g'): 'q6',
           
           # Transitions pour "run"
           ('q0', 'r'): 'q7',
           ('q7', 'u'): 'q8',
           ('q8', 'n'): 'q9',
           
           # Transitions pour "fly"
           ('q0', 'f'): 'q10',
           ('q10', 'l'): 'q11',
           ('q11', 'y'): 'q12',
       },
       initial_state='q0',
       final_states={'q3', 'q6', 'q9', 'q12'}
   )

   # Tests
   test_words = ['cat', 'dog', 'run', 'fly', 'car', 'bat', 'log']
   for word in test_words:
       result = english_words_dfa.accepts(word)
       print(f"'{word}' -> {result}")

Exemple 2 : Reconnaissance de nombres décimaux
-----------------------------------------------

**Problème** : Créer un automate qui reconnaît les nombres décimaux valides.

**Solution avec DFA** :

.. code-block:: python

   from baobab_automata import DFA

   # DFA pour les nombres décimaux
   decimal_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
       alphabet={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-'},
       transitions={
           # Signe optionnel
           ('q0', '+'): 'q1',
           ('q0', '-'): 'q1',
           ('q0', '0'): 'q2', ('q0', '1'): 'q2', ('q0', '2'): 'q2',
           ('q0', '3'): 'q2', ('q0', '4'): 'q2', ('q0', '5'): 'q2',
           ('q0', '6'): 'q2', ('q0', '7'): 'q2', ('q0', '8'): 'q2',
           ('q0', '9'): 'q2',
           
           # Chiffres après signe
           ('q1', '0'): 'q2', ('q1', '1'): 'q2', ('q1', '2'): 'q2',
           ('q1', '3'): 'q2', ('q1', '4'): 'q2', ('q1', '5'): 'q2',
           ('q1', '6'): 'q2', ('q1', '7'): 'q2', ('q1', '8'): 'q2',
           ('q1', '9'): 'q2',
           
           # Chiffres entiers
           ('q2', '0'): 'q2', ('q2', '1'): 'q2', ('q2', '2'): 'q2',
           ('q2', '3'): 'q2', ('q2', '4'): 'q2', ('q2', '5'): 'q2',
           ('q2', '6'): 'q2', ('q2', '7'): 'q2', ('q2', '8'): 'q2',
           ('q2', '9'): 'q2',
           ('q2', '.'): 'q3',
           
           # Chiffres décimaux
           ('q3', '0'): 'q4', ('q3', '1'): 'q4', ('q3', '2'): 'q4',
           ('q3', '3'): 'q4', ('q3', '4'): 'q4', ('q3', '5'): 'q4',
           ('q3', '6'): 'q4', ('q3', '7'): 'q4', ('q3', '8'): 'q4',
           ('q3', '9'): 'q4',
           
           ('q4', '0'): 'q4', ('q4', '1'): 'q4', ('q4', '2'): 'q4',
           ('q4', '3'): 'q4', ('q4', '4'): 'q4', ('q4', '5'): 'q4',
           ('q4', '6'): 'q4', ('q4', '7'): 'q4', ('q4', '8'): 'q4',
           ('q4', '9'): 'q4',
       },
       initial_state='q0',
       final_states={'q2', 'q4'}  # Entiers ou décimaux
   )

   # Tests
   test_numbers = ['123', '+456', '-789', '12.34', '-56.78', '+90.12', '0', '.5', '5.']
   for number in test_numbers:
       result = decimal_dfa.accepts(number)
       print(f"'{number}' -> {result}")

Exemple 3 : Reconnaissance d'adresses email
--------------------------------------------

**Problème** : Créer un automate qui reconnaît les adresses email valides (format simplifié).

**Solution avec NFA** :

.. code-block:: python

   from baobab_automata import NFA

   # NFA pour les adresses email (format simplifié)
   email_nfa = NFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'},
       alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '.'},
       transitions={
           # Nom d'utilisateur (lettres et chiffres)
           ('q0', 'a'): {'q0', 'q1'}, ('q0', 'b'): {'q0', 'q1'}, ('q0', 'c'): {'q0', 'q1'},
           ('q0', 'd'): {'q0', 'q1'}, ('q0', 'e'): {'q0', 'q1'}, ('q0', 'f'): {'q0', 'q1'},
           ('q0', 'g'): {'q0', 'q1'}, ('q0', 'h'): {'q0', 'q1'}, ('q0', 'i'): {'q0', 'q1'},
           ('q0', 'j'): {'q0', 'q1'}, ('q0', 'k'): {'q0', 'q1'}, ('q0', 'l'): {'q0', 'q1'},
           ('q0', 'm'): {'q0', 'q1'}, ('q0', 'n'): {'q0', 'q1'}, ('q0', 'o'): {'q0', 'q1'},
           ('q0', 'p'): {'q0', 'q1'}, ('q0', 'q'): {'q0', 'q1'}, ('q0', 'r'): {'q0', 'q1'},
           ('q0', 's'): {'q0', 'q1'}, ('q0', 't'): {'q0', 'q1'}, ('q0', 'u'): {'q0', 'q1'},
           ('q0', 'v'): {'q0', 'q1'}, ('q0', 'w'): {'q0', 'q1'}, ('q0', 'x'): {'q0', 'q1'},
           ('q0', 'y'): {'q0', 'q1'}, ('q0', 'z'): {'q0', 'q1'},
           ('q0', '0'): {'q0', 'q1'}, ('q0', '1'): {'q0', 'q1'}, ('q0', '2'): {'q0', 'q1'},
           ('q0', '3'): {'q0', 'q1'}, ('q0', '4'): {'q0', 'q1'}, ('q0', '5'): {'q0', 'q1'},
           ('q0', '6'): {'q0', 'q1'}, ('q0', '7'): {'q0', 'q1'}, ('q0', '8'): {'q0', 'q1'},
           ('q0', '9'): {'q0', 'q1'},
           
           # Symbole @
           ('q1', '@'): {'q2'},
           
           # Domaine (lettres et chiffres)
           ('q2', 'a'): {'q2', 'q3'}, ('q2', 'b'): {'q2', 'q3'}, ('q2', 'c'): {'q2', 'q3'},
           ('q2', 'd'): {'q2', 'q3'}, ('q2', 'e'): {'q2', 'q3'}, ('q2', 'f'): {'q2', 'q3'},
           ('q2', 'g'): {'q2', 'q3'}, ('q2', 'h'): {'q2', 'q3'}, ('q2', 'i'): {'q2', 'q3'},
           ('q2', 'j'): {'q2', 'q3'}, ('q2', 'k'): {'q2', 'q3'}, ('q2', 'l'): {'q2', 'q3'},
           ('q2', 'm'): {'q2', 'q3'}, ('q2', 'n'): {'q2', 'q3'}, ('q2', 'o'): {'q2', 'q3'},
           ('q2', 'p'): {'q2', 'q3'}, ('q2', 'q'): {'q2', 'q3'}, ('q2', 'r'): {'q2', 'q3'},
           ('q2', 's'): {'q2', 'q3'}, ('q2', 't'): {'q2', 'q3'}, ('q2', 'u'): {'q2', 'q3'},
           ('q2', 'v'): {'q2', 'q3'}, ('q2', 'w'): {'q2', 'q3'}, ('q2', 'x'): {'q2', 'q3'},
           ('q2', 'y'): {'q2', 'q3'}, ('q2', 'z'): {'q2', 'q3'},
           ('q2', '0'): {'q2', 'q3'}, ('q2', '1'): {'q2', 'q3'}, ('q2', '2'): {'q2', 'q3'},
           ('q2', '3'): {'q2', 'q3'}, ('q2', '4'): {'q2', 'q3'}, ('q2', '5'): {'q2', 'q3'},
           ('q2', '6'): {'q2', 'q3'}, ('q2', '7'): {'q2', 'q3'}, ('q2', '8'): {'q2', 'q3'},
           ('q2', '9'): {'q2', 'q3'},
           
           # Point
           ('q3', '.'): {'q4'},
           
           # Extension (lettres)
           ('q4', 'a'): {'q4', 'q5'}, ('q4', 'b'): {'q4', 'q5'}, ('q4', 'c'): {'q4', 'q5'},
           ('q4', 'd'): {'q4', 'q5'}, ('q4', 'e'): {'q4', 'q5'}, ('q4', 'f'): {'q4', 'q5'},
           ('q4', 'g'): {'q4', 'q5'}, ('q4', 'h'): {'q4', 'q5'}, ('q4', 'i'): {'q4', 'q5'},
           ('q4', 'j'): {'q4', 'q5'}, ('q4', 'k'): {'q4', 'q5'}, ('q4', 'l'): {'q4', 'q5'},
           ('q4', 'm'): {'q4', 'q5'}, ('q4', 'n'): {'q4', 'q5'}, ('q4', 'o'): {'q4', 'q5'},
           ('q4', 'p'): {'q4', 'q5'}, ('q4', 'q'): {'q4', 'q5'}, ('q4', 'r'): {'q4', 'q5'},
           ('q4', 's'): {'q4', 'q5'}, ('q4', 't'): {'q4', 'q5'}, ('q4', 'u'): {'q4', 'q5'},
           ('q4', 'v'): {'q4', 'q5'}, ('q4', 'w'): {'q4', 'q5'}, ('q4', 'x'): {'q4', 'q5'},
           ('q4', 'y'): {'q4', 'q5'}, ('q4', 'z'): {'q4', 'q5'},
       },
       initial_state='q0',
       final_states={'q5'}
   )

   # Tests
   test_emails = ['user@domain.com', 'test123@example.org', 'admin@site.net', 
                  'invalid@', '@domain.com', 'user@', 'user@domain']
   for email in test_emails:
       result = email_nfa.accepts(email)
       print(f"'{email}' -> {result}")

Exemple 4 : Reconnaissance de langages contextuels
----------------------------------------------------

**Problème** : Créer un automate à pile qui reconnaît le langage des expressions bien parenthésées.

**Solution avec DPDA** :

.. code-block:: python

   from baobab_automata import DPDA

   # DPDA pour les expressions bien parenthésées
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

Exemple 5 : Reconnaissance de palindromes
------------------------------------------

**Problème** : Créer une machine de Turing qui reconnaît les palindromes.

**Solution avec DTM** :

.. code-block:: python

   from baobab_automata import DTM

   # DTM pour les palindromes sur {a, b}
   palindrome_dtm = DTM(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q_accept', 'q_reject'},
       alphabet={'a', 'b'},
       tape_alphabet={'a', 'b', 'B', 'X', 'Y'},
       transitions={
           # Phase 1 : Marquer le premier symbole
           ('q0', 'a'): ('q1', 'X', 'R'),
           ('q0', 'b'): ('q2', 'Y', 'R'),
           ('q0', 'B'): ('q_accept', 'B', 'R'),  # Chaîne vide
           
           # Phase 2 : Aller à la fin
           ('q1', 'a'): ('q1', 'a', 'R'),
           ('q1', 'b'): ('q1', 'b', 'R'),
           ('q1', 'B'): ('q3', 'B', 'L'),
           
           ('q2', 'a'): ('q2', 'a', 'R'),
           ('q2', 'b'): ('q2', 'b', 'R'),
           ('q2', 'B'): ('q4', 'B', 'L'),
           
           # Phase 3 : Vérifier le dernier symbole
           ('q3', 'a'): ('q5', 'B', 'L'),
           ('q3', 'b'): ('q_reject', 'B', 'L'),
           ('q3', 'X'): ('q_accept', 'B', 'R'),
           
           ('q4', 'a'): ('q_reject', 'B', 'L'),
           ('q4', 'b'): ('q5', 'B', 'L'),
           ('q4', 'Y'): ('q_accept', 'B', 'R'),
           
           # Phase 4 : Retour au début
           ('q5', 'a'): ('q5', 'a', 'L'),
           ('q5', 'b'): ('q5', 'b', 'L'),
           ('q5', 'X'): ('q0', 'X', 'R'),
           ('q5', 'Y'): ('q0', 'Y', 'R'),
       },
       initial_state='q0',
       blank_symbol='B',
       final_states={'q_accept'}
   )

   # Tests
   test_strings = ['', 'a', 'b', 'aa', 'bb', 'aba', 'bab', 'abba', 'ab', 'abc']
   for string in test_strings:
       result = palindrome_dtm.accepts(string)
       print(f"'{string}' -> {result}")

Exemple 6 : Reconnaissance avec expressions régulières
------------------------------------------------------

**Problème** : Utiliser des expressions régulières pour reconnaître des patterns complexes.

**Solution** :

.. code-block:: python

   from baobab_automata.algorithms import regex_to_nfa

   # Expression régulière pour les numéros de téléphone français
   # Format: 0X XX XX XX XX (simplifié)
   phone_regex = "0[1-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2}"
   
   # Conversion en NFA
   phone_nfa = regex_to_nfa(phone_regex)

   # Tests
   test_phones = [
       '01 23 45 67 89',  # Valide
       '06 12 34 56 78',  # Valide
       '09 99 88 77 66',  # Valide
       '00 12 34 56 78',  # Invalide (commence par 00)
       '01 234 56 78',    # Invalide (format incorrect)
       '01 23 45 67',     # Invalide (trop court)
   ]
   
   for phone in test_phones:
       result = phone_nfa.accepts(phone)
       print(f"'{phone}' -> {result}")

Exemple 7 : Reconnaissance multi-langages
------------------------------------------

**Problème** : Créer un système qui reconnaît plusieurs langages simultanément.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.algorithms import language_operations

   # DFA pour les mots se terminant par 'ing'
   ing_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3'},
       alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
       transitions={
           # Transitions pour 'ing'
           ('q0', 'i'): 'q1',
           ('q1', 'n'): 'q2',
           ('q2', 'g'): 'q3',
           # Autres lettres
           ('q0', 'a'): 'q0', ('q0', 'b'): 'q0', ('q0', 'c'): 'q0', ('q0', 'd'): 'q0',
           ('q0', 'e'): 'q0', ('q0', 'f'): 'q0', ('q0', 'g'): 'q0', ('q0', 'h'): 'q0',
           ('q0', 'j'): 'q0', ('q0', 'k'): 'q0', ('q0', 'l'): 'q0', ('q0', 'm'): 'q0',
           ('q0', 'o'): 'q0', ('q0', 'p'): 'q0', ('q0', 'q'): 'q0', ('q0', 'r'): 'q0',
           ('q0', 's'): 'q0', ('q0', 't'): 'q0', ('q0', 'u'): 'q0', ('q0', 'v'): 'q0',
           ('q0', 'w'): 'q0', ('q0', 'x'): 'q0', ('q0', 'y'): 'q0', ('q0', 'z'): 'q0',
           ('q1', 'a'): 'q0', ('q1', 'b'): 'q0', ('q1', 'c'): 'q0', ('q1', 'd'): 'q0',
           ('q1', 'e'): 'q0', ('q1', 'f'): 'q0', ('q1', 'g'): 'q0', ('q1', 'h'): 'q0',
           ('q1', 'i'): 'q1', ('q1', 'j'): 'q0', ('q1', 'k'): 'q0', ('q1', 'l'): 'q0',
           ('q1', 'm'): 'q0', ('q1', 'o'): 'q0', ('q1', 'p'): 'q0', ('q1', 'q'): 'q0',
           ('q1', 'r'): 'q0', ('q1', 's'): 'q0', ('q1', 't'): 'q0', ('q1', 'u'): 'q0',
           ('q1', 'v'): 'q0', ('q1', 'w'): 'q0', ('q1', 'x'): 'q0', ('q1', 'y'): 'q0',
           ('q1', 'z'): 'q0',
           ('q2', 'a'): 'q0', ('q2', 'b'): 'q0', ('q2', 'c'): 'q0', ('q2', 'd'): 'q0',
           ('q2', 'e'): 'q0', ('q2', 'f'): 'q0', ('q2', 'h'): 'q0', ('q2', 'i'): 'q1',
           ('q2', 'j'): 'q0', ('q2', 'k'): 'q0', ('q2', 'l'): 'q0', ('q2', 'm'): 'q0',
           ('q2', 'n'): 'q2', ('q2', 'o'): 'q0', ('q2', 'p'): 'q0', ('q2', 'q'): 'q0',
           ('q2', 'r'): 'q0', ('q2', 's'): 'q0', ('q2', 't'): 'q0', ('q2', 'u'): 'q0',
           ('q2', 'v'): 'q0', ('q2', 'w'): 'q0', ('q2', 'x'): 'q0', ('q2', 'y'): 'q0',
           ('q2', 'z'): 'q0',
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

   # DFA pour les mots se terminant par 'ed'
   ed_dfa = DFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
       transitions={
           ('q0', 'e'): 'q1',
           ('q1', 'd'): 'q2',
           # Autres lettres (simplifié)
           ('q0', 'a'): 'q0', ('q0', 'b'): 'q0', ('q0', 'c'): 'q0', ('q0', 'd'): 'q0',
           ('q0', 'f'): 'q0', ('q0', 'g'): 'q0', ('q0', 'h'): 'q0', ('q0', 'i'): 'q0',
           ('q0', 'j'): 'q0', ('q0', 'k'): 'q0', ('q0', 'l'): 'q0', ('q0', 'm'): 'q0',
           ('q0', 'n'): 'q0', ('q0', 'o'): 'q0', ('q0', 'p'): 'q0', ('q0', 'q'): 'q0',
           ('q0', 'r'): 'q0', ('q0', 's'): 'q0', ('q0', 't'): 'q0', ('q0', 'u'): 'q0',
           ('q0', 'v'): 'q0', ('q0', 'w'): 'q0', ('q0', 'x'): 'q0', ('q0', 'y'): 'q0',
           ('q0', 'z'): 'q0',
           ('q1', 'a'): 'q0', ('q1', 'b'): 'q0', ('q1', 'c'): 'q0', ('q1', 'd'): 'q0',
           ('q1', 'e'): 'q1', ('q1', 'f'): 'q0', ('q1', 'g'): 'q0', ('q1', 'h'): 'q0',
           ('q1', 'i'): 'q0', ('q1', 'j'): 'q0', ('q1', 'k'): 'q0', ('q1', 'l'): 'q0',
           ('q1', 'm'): 'q0', ('q1', 'n'): 'q0', ('q1', 'o'): 'q0', ('q1', 'p'): 'q0',
           ('q1', 'q'): 'q0', ('q1', 'r'): 'q0', ('q1', 's'): 'q0', ('q1', 't'): 'q0',
           ('q1', 'u'): 'q0', ('q1', 'v'): 'q0', ('q1', 'w'): 'q0', ('q1', 'x'): 'q0',
           ('q1', 'y'): 'q0', ('q1', 'z'): 'q0',
           ('q2', 'a'): 'q0', ('q2', 'b'): 'q0', ('q2', 'c'): 'q0', ('q2', 'd'): 'q0',
           ('q2', 'e'): 'q1', ('q2', 'f'): 'q0', ('q2', 'g'): 'q0', ('q2', 'h'): 'q0',
           ('q2', 'i'): 'q0', ('q2', 'j'): 'q0', ('q2', 'k'): 'q0', ('q2', 'l'): 'q0',
           ('q2', 'm'): 'q0', ('q2', 'n'): 'q0', ('q2', 'o'): 'q0', ('q2', 'p'): 'q0',
           ('q2', 'q'): 'q0', ('q2', 'r'): 'q0', ('q2', 's'): 'q0', ('q2', 't'): 'q0',
           ('q2', 'u'): 'q0', ('q2', 'v'): 'q0', ('q2', 'w'): 'q0', ('q2', 'x'): 'q0',
           ('q2', 'y'): 'q0', ('q2', 'z'): 'q0',
       },
       initial_state='q0',
       final_states={'q2'}
   )

   # Union des deux langages
   combined_dfa = language_operations.union(ing_dfa, ed_dfa)

   # Tests
   test_words = ['running', 'walked', 'singing', 'played', 'cat', 'dog', 'working']
   for word in test_words:
       ing_result = ing_dfa.accepts(word)
       ed_result = ed_dfa.accepts(word)
       combined_result = combined_dfa.accepts(word)
       print(f"'{word}' -> ing:{ing_result}, ed:{ed_result}, combined:{combined_result}")

Conseils d'implémentation
--------------------------

* **Conception** : Commencez par identifier les patterns dans le langage
* **Optimisation** : Utilisez les algorithmes de minimisation pour réduire la taille
* **Tests** : Testez avec des cas représentatifs et des cas limites
* **Validation** : Validez toujours les automates avant utilisation
* **Documentation** : Documentez les automates complexes avec des commentaires
