API des Automates
==================

Cette section documente l'API des différents types d'automates disponibles dans Baobab Automata.

Interfaces de base
-------------------

.. automodule:: baobab_automata.interfaces.automaton
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: baobab_automata.interfaces.recognizer
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: baobab_automata.interfaces.converter
   :members:
   :undoc-members:
   :show-inheritance:

Automates finis
---------------

DFA (Automate Fini Déterministe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.finite.dfa.DFA
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DFA

      # DFA qui reconnaît les mots se terminant par 'ab'
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
      assert dfa.accepts('ab')
      assert dfa.accepts('aab')
      assert not dfa.accepts('ba')

NFA (Automate Fini Non-déterministe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.finite.nfa.NFA
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import NFA

      # NFA qui reconnaît les mots contenant 'aa' ou 'bb'
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

      # Test de reconnaissance
      assert nfa.accepts('aa')
      assert nfa.accepts('bb')
      assert not nfa.accepts('ab')

Epsilon-NFA (Automate Fini Non-déterministe avec Epsilon-transitions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.finite.epsilon_nfa.EpsilonNFA
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import EpsilonNFA

      # Epsilon-NFA pour l'expression régulière (a|b)*abb
      epsilon_nfa = EpsilonNFA(
          states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
          alphabet={'a', 'b'},
          transitions={
              ('q0', ''): {'q1', 'q2'},
              ('q1', 'a'): {'q1'},
              ('q1', 'b'): {'q1'},
              ('q1', ''): {'q2'},
              ('q2', 'a'): {'q3'},
              ('q3', 'b'): {'q4'},
              ('q4', 'b'): {'q5'},
          },
          initial_state='q0',
          final_states={'q5'}
      )

Automates à pile
----------------

DPDA (Automate à Pile Déterministe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.pushdown.dpda.DPDA
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemple d'utilisation** :

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

      # Test de reconnaissance
      assert dpda.accepts('ab')
      assert dpda.accepts('aabb')
      assert not dpda.accepts('aab')

NPDA (Automate à Pile Non-déterministe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.pushdown.npda.NPDA
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import NPDA

      # NPDA qui reconnaît les palindromes
      npda = NPDA(
          states={'q0', 'q1', 'q2'},
          alphabet={'a', 'b'},
          stack_alphabet={'A', 'B', 'Z'},
          transitions={
              ('q0', 'a', 'Z'): ('q0', 'AZ'),
              ('q0', 'a', 'A'): ('q0', 'AA'),
              ('q0', 'a', 'B'): ('q0', 'AB'),
              ('q0', 'b', 'Z'): ('q0', 'BZ'),
              ('q0', 'b', 'A'): ('q0', 'BA'),
              ('q0', 'b', 'B'): ('q0', 'BB'),
              ('q0', 'a', 'A'): ('q1', 'A'),
              ('q0', 'b', 'B'): ('q1', 'B'),
              ('q0', '', 'Z'): ('q1', 'Z'),
              ('q1', 'a', 'A'): ('q1', ''),
              ('q1', 'b', 'B'): ('q1', ''),
              ('q1', '', 'Z'): ('q2', 'Z'),
          },
          initial_state='q0',
          initial_stack_symbol='Z',
          final_states={'q2'}
      )

Machines de Turing
------------------

DTM (Machine de Turing Déterministe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.turing.dtm.DTM
   :members:
   :undoc-members:
   :show-inheritance:

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DTM

      # DTM qui reconnaît les palindromes
      dtm = DTM(
          states={'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'},
          alphabet={'a', 'b'},
          tape_alphabet={'a', 'b', 'B'},
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

NTM (Machine de Turing Non-déterministe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.turing.ntm.NTM
   :members:
   :undoc-members:
   :show-inheritance:

MultiTapeTM (Machine de Turing Multi-rubans)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.turing.multi_tape_tm.MultiTapeTM
   :members:
   :undoc-members:
   :show-inheritance:

Méthodes communes
------------------

Tous les automates héritent des méthodes suivantes :

.. py:method:: accepts(input_string: str) -> bool

   Vérifie si une chaîne d'entrée est acceptée par l'automate.

   :param input_string: La chaîne à tester
   :return: True si la chaîne est acceptée, False sinon
   :raises RecognitionError: Si une erreur survient pendant la reconnaissance

.. py:method:: simulate(input_string: str, step_by_step: bool = False) -> Union[bool, List[Configuration]]

   Simule l'exécution de l'automate sur une chaîne d'entrée.

   :param input_string: La chaîne à traiter
   :param step_by_step: Si True, retourne la liste des configurations
   :return: Résultat de la reconnaissance ou liste des configurations
   :raises RecognitionError: Si une erreur survient pendant la simulation

.. py:method:: visualize(filename: str, format: str = 'png', **kwargs) -> None

   Génère une visualisation de l'automate.

   :param filename: Nom du fichier de sortie
   :param format: Format de sortie ('png', 'svg', 'pdf')
   :param kwargs: Options supplémentaires pour la visualisation
   :raises VisualizationError: Si une erreur survient pendant la visualisation

.. py:method:: to_mermaid() -> str

   Génère le code Mermaid pour la visualisation.

   :return: Code Mermaid représentant l'automate

.. py:method:: to_graphviz() -> str

   Génère le code Graphviz pour la visualisation.

   :return: Code Graphviz représentant l'automate

.. py:method:: to_json() -> str

   Exporte l'automate au format JSON.

   :return: Représentation JSON de l'automate

Propriétés communes
-------------------

.. py:attribute:: states

   Ensemble des états de l'automate.

.. py:attribute:: alphabet

   Alphabet d'entrée de l'automate.

.. py:attribute:: transitions

   Fonction de transition de l'automate.

.. py:attribute:: initial_state

   État initial de l'automate.

.. py:attribute:: final_states

   Ensemble des états finaux de l'automate.

Validation
-----------

Tous les automates valident automatiquement leur cohérence lors de l'instanciation :

* Vérification que l'état initial appartient à l'ensemble des états
* Vérification que les états finaux sont des sous-ensembles des états
* Vérification que les transitions utilisent des états et symboles valides
* Vérification de la complétude des transitions (pour les DFA/DPDA/DTM)

Exemples avancés
----------------

Automate avec états multiples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # DFA avec plusieurs états finaux
   multi_final_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q2',
           ('q1', 'a'): 'q3',
           ('q1', 'b'): 'q0',
           ('q2', 'a'): 'q0',
           ('q2', 'b'): 'q3',
           ('q3', 'a'): 'q1',
           ('q3', 'b'): 'q2',
       },
       initial_state='q0',
       final_states={'q1', 'q2'}  # États finaux multiples
   )

Automate avec alphabet étendu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # DFA avec alphabet Unicode
   unicode_dfa = DFA(
       states={'q0', 'q1'},
       alphabet={'α', 'β', 'γ'},
       transitions={
           ('q0', 'α'): 'q1',
           ('q1', 'β'): 'q0',
       },
       initial_state='q0',
       final_states={'q1'}
   )

Performance et optimisation
----------------------------

* Les automates finis sont optimisés pour la reconnaissance rapide
* Les algorithmes de simulation utilisent des optimisations de mémoire
* La visualisation peut être mise en cache pour améliorer les performances
* Les gros automates peuvent nécessiter des paramètres de configuration spécifiques
