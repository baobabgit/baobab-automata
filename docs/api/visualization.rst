API de Visualisation
=====================

Cette section documente l'API de visualisation de Baobab Automata.

Vue d'ensemble
--------------

Baobab Automata fournit des outils de visualisation puissants pour représenter graphiquement les automates et leurs comportements.

Modules de visualisation
-------------------------

.. automodule:: baobab_automata.visualization
   :members:
   :undoc-members:
   :show-inheritance:

Visualisation de base
---------------------

.. py:function:: visualize(automaton: IAutomaton, filename: str, format: str = 'png', **kwargs) -> None

   Génère une visualisation d'un automate et l'enregistre dans un fichier.

   :param automaton: L'automate à visualiser
   :param filename: Nom du fichier de sortie
   :param format: Format de sortie ('png', 'svg', 'pdf', 'jpg')
   :param kwargs: Options supplémentaires de visualisation
   :raises VisualizationError: Si la visualisation échoue

   **Options disponibles** :

   * ``dpi`` : Résolution en points par pouce (défaut: 300)
   * ``layout`` : Algorithme de disposition ('dot', 'neato', 'fdp', 'sfdp', 'circo')
   * ``show_labels`` : Afficher les étiquettes des transitions (défaut: True)
   * ``show_weights`` : Afficher les poids des transitions (défaut: False)
   * ``node_size`` : Taille des nœuds (défaut: 'medium')
   * ``edge_color`` : Couleur des arêtes (défaut: 'black')
   * ``node_color`` : Couleur des nœuds (défaut: 'lightblue')
   * ``final_node_color`` : Couleur des nœuds finaux (défaut: 'lightgreen')
   * ``initial_node_color`` : Couleur du nœud initial (défaut: 'lightcoral')

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata import DFA

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

      # Visualisation basique
      dfa.visualize('automaton.png')

      # Visualisation avec options
      dfa.visualize(
          'automaton_detailed.png',
          format='svg',
          dpi=600,
          layout='neato',
          show_labels=True,
          node_size='large',
          edge_color='blue',
          final_node_color='gold'
      )

Génération de code
-------------------

.. py:function:: to_mermaid(automaton: IAutomaton, **kwargs) -> str

   Génère le code Mermaid pour la visualisation d'un automate.

   :param automaton: L'automate à convertir
   :param kwargs: Options de génération
   :return: Code Mermaid représentant l'automate

   **Exemple d'utilisation** :

   .. code-block:: python

      mermaid_code = dfa.to_mermaid()
      print(mermaid_code)

      # Sauvegarder dans un fichier
      with open('automaton.md', 'w') as f:
          f.write(f"```mermaid\n{mermaid_code}\n```")

.. py:function:: to_graphviz(automaton: IAutomaton, **kwargs) -> str

   Génère le code Graphviz pour la visualisation d'un automate.

   :param automaton: L'automate à convertir
   :param kwargs: Options de génération
   :return: Code Graphviz représentant l'automate

   **Exemple d'utilisation** :

   .. code-block:: python

      graphviz_code = dfa.to_graphviz()
      print(graphviz_code)

      # Utiliser avec Graphviz directement
      import subprocess
      with open('automaton.dot', 'w') as f:
          f.write(graphviz_code)
      
      subprocess.run(['dot', '-Tpng', 'automaton.dot', '-o', 'automaton.png'])

Visualisation interactive
-------------------------

.. py:function:: create_interactive_plot(automaton: IAutomaton, **kwargs) -> None

   Crée une visualisation interactive avec Plotly.

   :param automaton: L'automate à visualiser
   :param kwargs: Options de visualisation interactive

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import create_interactive_plot

      # Créer une visualisation interactive
      create_interactive_plot(
          dfa,
          title="Automate Interactif",
          show_tooltips=True,
          enable_zoom=True,
          animation_speed=1000
      )

Visualisation de simulations
-----------------------------

.. py:function:: visualize_simulation(automaton: IAutomaton, input_string: str, **kwargs) -> None

   Visualise l'exécution d'un automate sur une chaîne d'entrée.

   :param automaton: L'automate à simuler
   :param input_string: La chaîne d'entrée
   :param kwargs: Options de visualisation

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import visualize_simulation

      # Visualiser la simulation pas à pas
      visualize_simulation(
          dfa,
          'ab',
          step_by_step=True,
          save_frames=True,
          output_dir='simulation_frames'
      )

Visualisation comparative
--------------------------

.. py:function:: compare_automata(automata: List[IAutomaton], labels: List[str] = None, **kwargs) -> None

   Compare visuellement plusieurs automates côte à côte.

   :param automata: Liste des automates à comparer
   :param labels: Étiquettes pour chaque automate
   :param kwargs: Options de visualisation

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import compare_automata

      # Comparer un NFA et son DFA équivalent
      compare_automata(
          [nfa, dfa],
          labels=['NFA Original', 'DFA Converti'],
          layout='horizontal',
          show_differences=True
      )

Visualisation de métriques
---------------------------

.. py:function:: visualize_metrics(automaton: IAutomaton, **kwargs) -> None

   Visualise les métriques d'un automate (nombre d'états, transitions, etc.).

   :param automaton: L'automate à analyser
   :param kwargs: Options de visualisation

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import visualize_metrics

      # Visualiser les métriques
      visualize_metrics(
          dfa,
          show_statistics=True,
          create_charts=True,
          export_data=True
      )

Thèmes de visualisation
-----------------------

Baobab Automata propose plusieurs thèmes prédéfinis :

.. py:function:: apply_theme(theme_name: str, **kwargs) -> Dict[str, Any]

   Applique un thème de visualisation prédéfini.

   :param theme_name: Nom du thème ('default', 'dark', 'colorful', 'minimal', 'academic')
   :param kwargs: Options supplémentaires
   :return: Dictionnaire des options de visualisation

   **Thèmes disponibles** :

   * ``default`` : Thème par défaut avec couleurs douces
   * ``dark`` : Thème sombre pour les présentations
   * ``colorful`` : Thème coloré pour les démonstrations
   * ``minimal`` : Thème minimaliste en noir et blanc
   * ``academic`` : Thème académique pour les publications

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import apply_theme

      # Appliquer le thème académique
      theme_options = apply_theme('academic')
      
      dfa.visualize(
          'academic_automaton.png',
          **theme_options
      )

Export et import
----------------

.. py:function:: export_visualization(automaton: IAutomaton, format: str, **kwargs) -> bytes

   Exporte une visualisation dans différents formats.

   :param automaton: L'automate à exporter
   :param format: Format d'export ('png', 'svg', 'pdf', 'jpg', 'gif')
   :param kwargs: Options d'export
   :return: Données binaires de l'image

.. py:function:: create_gif_animation(automaton: IAutomaton, input_strings: List[str], **kwargs) -> None

   Crée une animation GIF montrant l'exécution sur plusieurs chaînes.

   :param automaton: L'automate à animer
   :param input_strings: Liste des chaînes d'entrée
   :param kwargs: Options d'animation

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import create_gif_animation

      # Créer une animation
      create_gif_animation(
          dfa,
          ['a', 'ab', 'abb', 'abbb'],
          filename='automaton_animation.gif',
          duration=1000,
          loop=True
      )

Visualisation avancée
---------------------

Diagrammes de classes
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: create_class_diagram(automata_classes: List[type], **kwargs) -> None

   Crée un diagramme de classes pour les types d'automates.

   :param automata_classes: Liste des classes d'automates
   :param kwargs: Options de visualisation

Diagrammes de séquence
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: create_sequence_diagram(automaton: IAutomaton, input_string: str, **kwargs) -> None

   Crée un diagramme de séquence montrant l'exécution d'un automate.

   :param automaton: L'automate à analyser
   :param input_string: La chaîne d'entrée
   :param kwargs: Options de visualisation

Visualisation de performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: visualize_performance(automaton: IAutomaton, test_cases: List[str], **kwargs) -> None

   Visualise les performances d'un automate sur différents cas de test.

   :param automaton: L'automate à analyser
   :param test_cases: Liste des cas de test
   :param kwargs: Options de visualisation

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import visualize_performance

      # Analyser les performances
      test_cases = ['a' * i for i in range(1, 100)]
      visualize_performance(
          dfa,
          test_cases,
          show_execution_time=True,
          show_memory_usage=True,
          create_benchmark_chart=True
      )

Configuration avancée
---------------------

Styles personnalisés
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: create_custom_style(style_config: Dict[str, Any]) -> Dict[str, Any]

   Crée un style de visualisation personnalisé.

   :param style_config: Configuration du style
   :return: Options de visualisation

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import create_custom_style

      # Créer un style personnalisé
      custom_style = create_custom_style({
          'node_color': '#FF6B6B',
          'edge_color': '#4ECDC4',
          'final_node_color': '#45B7D1',
          'initial_node_color': '#96CEB4',
          'font_family': 'Arial',
          'font_size': 14,
          'edge_width': 2,
          'node_size': 0.8
      })
      
      dfa.visualize('custom_style.png', **custom_style)

Layouts personnalisés
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: create_custom_layout(automaton: IAutomaton, layout_function: Callable) -> Dict[str, Tuple[float, float]]

   Crée un layout personnalisé pour la visualisation.

   :param automaton: L'automate à disposer
   :param layout_function: Fonction de disposition personnalisée
   :return: Positions des nœuds

   **Exemple d'utilisation** :

   .. code-block:: python

      from baobab_automata.visualization import create_custom_layout

      def circular_layout(automaton):
          """Disposition circulaire des états."""
          states = list(automaton.states)
          positions = {}
          radius = 2.0
          
          for i, state in enumerate(states):
              angle = 2 * math.pi * i / len(states)
              x = radius * math.cos(angle)
              y = radius * math.sin(angle)
              positions[state] = (x, y)
          
          return positions

      # Appliquer le layout personnalisé
      positions = create_custom_layout(dfa, circular_layout)
      dfa.visualize('circular_layout.png', custom_positions=positions)

Exemples d'utilisation complète
--------------------------------

Visualisation complète d'un projet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from baobab_automata import DFA, NFA
   from baobab_automata.algorithms import nfa_to_dfa, minimize_dfa
   from baobab_automata.visualization import (
       visualize, compare_automata, create_gif_animation,
       apply_theme, visualize_performance
   )

   # Créer un NFA
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

   # Conversion et optimisation
   dfa = nfa_to_dfa(nfa)
   minimal_dfa = minimize_dfa(dfa)

   # Appliquer un thème
   theme_options = apply_theme('academic')

   # Visualisations individuelles
   nfa.visualize('nfa.png', **theme_options)
   dfa.visualize('dfa.png', **theme_options)
   minimal_dfa.visualize('minimal_dfa.png', **theme_options)

   # Comparaison
   compare_automata(
       [nfa, dfa, minimal_dfa],
       labels=['NFA Original', 'DFA Converti', 'DFA Minimal'],
       filename='comparison.png',
       **theme_options
   )

   # Animation
   test_strings = ['a', 'ab', 'abb', 'abbb', 'abbbb']
   create_gif_animation(
       minimal_dfa,
       test_strings,
       filename='automaton_demo.gif',
       **theme_options
   )

   # Analyse de performance
   performance_tests = ['a' * i for i in range(1, 50)]
   visualize_performance(
       minimal_dfa,
       performance_tests,
       filename='performance_analysis.png',
       **theme_options
   )

Conseils d'utilisation
-----------------------

* **Formats** : Utilisez SVG pour la qualité, PNG pour la compatibilité
* **Résolution** : Augmentez le DPI pour les publications académiques
* **Layouts** : Testez différents algorithmes de disposition selon la taille
* **Thèmes** : Choisissez le thème selon le contexte d'utilisation
* **Performance** : Pour de gros automates, utilisez des layouts optimisés
* **Accessibilité** : Utilisez des couleurs contrastées et des étiquettes claires
