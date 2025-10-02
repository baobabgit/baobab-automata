Baobab Automata Documentation
==============================

.. image:: https://img.shields.io/badge/Python-3.11%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://img.shields.io/badge/Status-Alpha-orange.svg
   :target: https://github.com/baobab-automata/baobab-automata
   :alt: Status

Baobab Automata est une librairie Python moderne et complète qui fournit une interface unifiée pour travailler avec différents types d'automates et leurs algorithmes associés.

Fonctionnalités principales
----------------------------

* **Automates finis** : DFA, NFA, epsilon-NFA avec algorithmes de conversion et d'optimisation
* **Automates à pile** : DPDA, NPDA avec analyse de grammaires contextuelles
* **Machines de Turing** : DTM, NTM, multi-rubans avec analyse de complexité
* **Algorithmes avancés** : Conversion entre types d'automates, optimisation, reconnaissance
* **Visualisation** : Support Graphviz, Mermaid, et interfaces web interactives
* **Interface unifiée** : API cohérente pour tous les types d'automates

Installation rapide
-------------------

.. code-block:: bash

   pip install baobab-automata

Exemple d'utilisation
---------------------

.. code-block:: python

   from baobab_automata import DFA, NFA, TuringMachine

   # Créer un automate fini déterministe
   dfa = DFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q1', 'b'): 'q2',
       },
       initial_state='q0',
       final_states={'q2'}
   )

   # Vérifier si une chaîne est acceptée
   result = dfa.accepts('ab')
   print(result)  # True

   # Visualiser l'automate
   dfa.visualize('dfa_example.png')

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Guide d'utilisation

   api/installation
   api/quickstart
   examples/index
   api/index

.. toctree::
   :maxdepth: 2
   :caption: Référence API

   api/automata
   api/algorithms
   api/visualization
   api/exceptions

.. toctree::
   :maxdepth: 1
   :caption: Développement

   changelog
   api/contributing
   api/development

Indices et tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
