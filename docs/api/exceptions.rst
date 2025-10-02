API des Exceptions
===================

Cette section documente l'API des exceptions disponibles dans Baobab Automata.

Vue d'ensemble
--------------

Baobab Automata utilise une hiérarchie d'exceptions bien structurée pour gérer les erreurs de manière appropriée et fournir des messages d'erreur informatifs.

Hiérarchie des exceptions
-------------------------

.. automodule:: baobab_automata.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Exception de base
~~~~~~~~~~~~~~~~~~

.. autoclass:: baobab_automata.exceptions.BaobabAutomataError
   :members:
   :undoc-members:
   :show-inheritance:

   Exception de base pour toutes les erreurs de Baobab Automata.

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.exceptions import BaobabAutomataError

      try:
          # Opération sur un automate
          result = automaton.accepts('input')
      except BaobabAutomataError as e:
          print(f"Erreur Baobab Automata: {e}")

Exceptions d'automates
-----------------------

.. autoclass:: baobab_automata.exceptions.InvalidAutomatonError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'un automate est invalide ou mal formé.

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DFA
      from baobab_automata.exceptions import InvalidAutomatonError

      try:
          # DFA avec état initial invalide
          dfa = DFA(
              states={'q0', 'q1'},
              alphabet={'a', 'b'},
              transitions={('q0', 'a'): 'q1'},
              initial_state='q_invalid',  # État inexistant
              final_states={'q1'}
          )
      except InvalidAutomatonError as e:
          print(f"Automate invalide: {e}")

.. autoclass:: baobab_automata.exceptions.InvalidStateError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'un état est invalide ou n'appartient pas à l'automate.

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.exceptions import InvalidStateError

      try:
          # Tentative d'utiliser un état invalide
          automaton.get_state('invalid_state')
      except InvalidStateError as e:
          print(f"État invalide: {e}")

.. autoclass:: baobab_automata.exceptions.InvalidTransitionError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'une transition est invalide ou mal définie.

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.exceptions import InvalidTransitionError

      try:
          # Transition avec état de destination invalide
          automaton.add_transition('q0', 'a', 'invalid_state')
      except InvalidTransitionError as e:
          print(f"Transition invalide: {e}")

Exceptions de reconnaissance
-----------------------------

.. autoclass:: baobab_automata.exceptions.RecognitionError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'une erreur survient pendant la reconnaissance d'un langage.

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.exceptions import RecognitionError

      try:
          # Reconnaissance avec symbole non défini
          result = automaton.accepts('invalid_symbol')
      except RecognitionError as e:
          print(f"Erreur de reconnaissance: {e}")

Exceptions de conversion
-----------------------

.. autoclass:: baobab_automata.exceptions.ConversionError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'une erreur survient pendant la conversion entre automates.

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.algorithms import nfa_to_dfa
      from baobab_automata.exceptions import ConversionError

      try:
          # Conversion d'un automate invalide
          dfa = nfa_to_dfa(invalid_nfa)
      except ConversionError as e:
          print(f"Erreur de conversion: {e}")

Exceptions spécialisées
-----------------------

Exceptions des automates finis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.finite.optimization_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.finite.optimization_exceptions.OptimizationError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'une erreur survient pendant l'optimisation d'un automate fini.

Exceptions des automates à pile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.pushdown.dpda_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.pushdown.dpda_exceptions.DPDAError
   :members:
   :undoc-members:
   :show-inheritance:

   Exception spécifique aux automates à pile déterministes.

.. automodule:: baobab_automata.pushdown.npda_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.pushdown.npda_exceptions.NPDAError
   :members:
   :undoc-members:
   :show-inheritance:

   Exception spécifique aux automates à pile non-déterministes.

Exceptions des machines de Turing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.exceptions.dtm_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.exceptions.dtm_exceptions.DTMError
   :members:
   :undoc-members:
   :show-inheritance:

   Exception spécifique aux machines de Turing déterministes.

.. automodule:: baobab_automata.exceptions.ntm_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.exceptions.ntm_exceptions.NTMError
   :members:
   :undoc-members:
   :show-inheritance:

   Exception spécifique aux machines de Turing non-déterministes.

Exceptions de visualisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.visualization.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.visualization.exceptions.VisualizationError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'une erreur survient pendant la visualisation d'un automate.

Exceptions de parsing
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: baobab_automata.finite.regex_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: baobab_automata.finite.regex_exceptions.RegexParseError
   :members:
   :undoc-members:
   :show-inheritance:

   Levée lorsqu'une erreur survient pendant le parsing d'une expression régulière.

Gestion des erreurs
-------------------

Bonnes pratiques
~~~~~~~~~~~~~~~~

1. **Capture spécifique** : Capturez les exceptions les plus spécifiques en premier
2. **Messages informatifs** : Utilisez les messages d'erreur pour diagnostiquer les problèmes
3. **Logging** : Enregistrez les erreurs pour le débogage
4. **Récupération** : Implémentez des stratégies de récupération appropriées

**Exemple de gestion d'erreurs complète** :

.. code-block:: python

   import logging
   from baobab_automata import DFA
   from baobab_automata.exceptions import (
       InvalidAutomatonError,
       RecognitionError,
       ConversionError
   )

   def safe_automaton_operation(automaton, input_string):
       """Opération sécurisée sur un automate."""
       try:
           # Validation de l'automate
           if not automaton.is_valid():
               raise InvalidAutomatonError("L'automate n'est pas valide")
           
           # Reconnaissance
           result = automaton.accepts(input_string)
           return result
           
       except InvalidAutomatonError as e:
           logging.error(f"Automate invalide: {e}")
           raise
           
       except RecognitionError as e:
           logging.warning(f"Erreur de reconnaissance pour '{input_string}': {e}")
           return False
           
       except ConversionError as e:
           logging.error(f"Erreur de conversion: {e}")
           raise
           
       except Exception as e:
           logging.error(f"Erreur inattendue: {e}")
           raise

Validation d'entrée
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.exceptions import InvalidStateError, InvalidTransitionError

   def validate_automaton_input(states, alphabet, transitions, initial_state, final_states):
       """Valide les entrées pour la création d'un automate."""
       errors = []
       
       # Validation des états
       if initial_state not in states:
           errors.append(f"État initial '{initial_state}' n'appartient pas aux états")
       
       if not final_states.issubset(states):
           invalid_states = final_states - states
           errors.append(f"États finaux invalides: {invalid_states}")
       
       # Validation des transitions
       for (state, symbol), target in transitions.items():
           if state not in states:
               errors.append(f"État source '{state}' invalide dans la transition")
           if symbol not in alphabet:
               errors.append(f"Symbole '{symbol}' invalide dans la transition")
           if isinstance(target, str) and target not in states:
               errors.append(f"État cible '{target}' invalide dans la transition")
       
       if errors:
           raise InvalidAutomatonError(f"Erreurs de validation: {'; '.join(errors)}")

Gestion des erreurs de conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.algorithms import nfa_to_dfa
   from baobab_automata.exceptions import ConversionError

   def safe_nfa_to_dfa_conversion(nfa):
       """Conversion sécurisée NFA vers DFA."""
       try:
           # Vérification préalable
           if not nfa.is_valid():
               raise ConversionError("Le NFA n'est pas valide")
           
           # Conversion
           dfa = nfa_to_dfa(nfa)
           
           # Vérification post-conversion
           if not dfa.is_valid():
               raise ConversionError("Le DFA résultant n'est pas valide")
           
           return dfa
           
       except ConversionError as e:
           logging.error(f"Échec de la conversion NFA->DFA: {e}")
           raise
       except Exception as e:
           raise ConversionError(f"Erreur inattendue pendant la conversion: {e}")

Gestion des erreurs de visualisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata.visualization.exceptions import VisualizationError

   def safe_visualization(automaton, filename):
       """Visualisation sécurisée d'un automate."""
       try:
           # Vérification des prérequis
           if not automaton.is_valid():
               raise VisualizationError("L'automate n'est pas valide")
           
           # Tentative de visualisation
           automaton.visualize(filename)
           
       except VisualizationError as e:
           logging.error(f"Erreur de visualisation: {e}")
           # Fallback vers une visualisation simplifiée
           try:
               automaton.visualize(filename, format='svg', layout='dot')
           except Exception as fallback_error:
               logging.error(f"Fallback échoué: {fallback_error}")
               raise VisualizationError(f"Impossible de visualiser l'automate: {e}")

Messages d'erreur personnalisés
--------------------------------

.. code-block:: python

   from baobab_automata.exceptions import BaobabAutomataError

   class CustomAutomatonError(BaobabAutomataError):
       """Exception personnalisée pour des cas spécifiques."""
       
       def __init__(self, message, automaton_type=None, context=None):
           super().__init__(message)
           self.automaton_type = automaton_type
           self.context = context
       
       def __str__(self):
           base_message = super().__str__()
           if self.automaton_type:
               base_message += f" (Type: {self.automaton_type})"
           if self.context:
               base_message += f" (Contexte: {self.context})"
           return base_message

   # Utilisation
   try:
       # Opération qui peut échouer
       pass
   except CustomAutomatonError as e:
       print(f"Erreur personnalisée: {e}")
       print(f"Type d'automate: {e.automaton_type}")
       print(f"Contexte: {e.context}")

Logging et débogage
-------------------

Configuration du logging
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging

   # Configuration du logger pour Baobab Automata
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   # Logger spécifique
   baobab_logger = logging.getLogger('baobab_automata')
   baobab_logger.setLevel(logging.DEBUG)

   # Handler pour les erreurs
   error_handler = logging.FileHandler('baobab_errors.log')
   error_handler.setLevel(logging.ERROR)
   baobab_logger.addHandler(error_handler)

Débogage des exceptions
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import traceback
   from baobab_automata.exceptions import BaobabAutomataError

   def debug_automaton_error(automaton, operation, *args, **kwargs):
       """Fonction de débogage pour les erreurs d'automates."""
       try:
           return operation(*args, **kwargs)
       except BaobabAutomataError as e:
           print(f"Erreur Baobab Automata: {e}")
           print(f"Type d'exception: {type(e).__name__}")
           print(f"Automate: {automaton}")
           print(f"Opération: {operation.__name__}")
           print(f"Arguments: {args}")
           print(f"Arguments nommés: {kwargs}")
           print("Traceback complet:")
           traceback.print_exc()
           raise

Tests d'exceptions
------------------

.. code-block:: python

   import pytest
   from baobab_automata import DFA
   from baobab_automata.exceptions import InvalidAutomatonError

   def test_invalid_automaton():
       """Test que les automates invalides lèvent les bonnes exceptions."""
       with pytest.raises(InvalidAutomatonError):
           DFA(
               states={'q0'},
               alphabet={'a'},
               transitions={},
               initial_state='q_invalid',  # État inexistant
               final_states={'q0'}
           )

   def test_exception_message():
       """Test que les messages d'erreur sont informatifs."""
       try:
           DFA(
               states={'q0'},
               alphabet={'a'},
               transitions={},
               initial_state='q_invalid',
               final_states={'q0'}
           )
       except InvalidAutomatonError as e:
           assert 'q_invalid' in str(e)
           assert 'initial_state' in str(e).lower()

Conseils d'utilisation
-----------------------

* **Spécificité** : Utilisez les exceptions les plus spécifiques possibles
* **Messages** : Rendez les messages d'erreur informatifs et actionables
* **Logging** : Enregistrez les erreurs pour faciliter le débogage
* **Récupération** : Implémentez des stratégies de récupération appropriées
* **Tests** : Testez la gestion des erreurs dans vos tests unitaires
* **Documentation** : Documentez les exceptions que vos fonctions peuvent lever
