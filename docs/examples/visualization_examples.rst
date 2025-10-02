Exemples de Visualisation
===========================

Cette section présente des exemples pratiques d'utilisation des outils de visualisation de Baobab Automata.

Exemple 1 : Visualisation basique d'un DFA
--------------------------------------------

**Problème** : Créer et visualiser un automate fini déterministe simple.

**Solution** :

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

   # Visualisation basique
   dfa.visualize('dfa_basic.png')
   print("Visualisation basique générée: dfa_basic.png")

   # Visualisation avec options
   dfa.visualize(
       'dfa_detailed.png',
       format='svg',
       dpi=300,
       show_labels=True,
       layout='neato',
       node_size='large',
       edge_color='blue',
       final_node_color='gold'
   )
   print("Visualisation détaillée générée: dfa_detailed.png")

Exemple 2 : Génération de code Mermaid
---------------------------------------

**Problème** : Générer du code Mermaid pour intégrer dans la documentation.

**Solution** :

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

   # Génération du code Mermaid
   mermaid_code = nfa.to_mermaid()
   print("Code Mermaid généré:")
   print(mermaid_code)

   # Sauvegarder dans un fichier Markdown
   with open('nfa_mermaid.md', 'w') as f:
       f.write("# Automate NFA\n\n")
       f.write("```mermaid\n")
       f.write(mermaid_code)
       f.write("\n```\n")

   print("Code Mermaid sauvegardé dans nfa_mermaid.md")

Exemple 3 : Visualisation d'un automate à pile
-----------------------------------------------

**Problème** : Visualiser un automate à pile déterministe.

**Solution** :

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

   # Visualisation avec options spéciales pour PDA
   dpda.visualize(
       'dpda_example.png',
       format='png',
       dpi=300,
       show_labels=True,
       show_stack_operations=True,
       layout='dot',
       node_color='lightblue',
       final_node_color='lightgreen',
       edge_color='darkblue'
   )

   print("Visualisation DPDA générée: dpda_example.png")

Exemple 4 : Comparaison visuelle d'automates
----------------------------------------------

**Problème** : Comparer visuellement un NFA et son DFA équivalent.

**Solution** :

.. code-block:: python

   from baobab_automata import NFA
   from baobab_automata.algorithms import nfa_to_dfa
   from baobab_automata.visualization import compare_automata

   # NFA original
   nfa = NFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): {'q0', 'q1'},
           ('q1', 'b'): {'q2'},
       },
       initial_state='q0',
       final_states={'q2'}
   )

   # Conversion en DFA
   dfa = nfa_to_dfa(nfa)

   # Visualisations individuelles
   nfa.visualize('nfa_original.png', title='NFA Original')
   dfa.visualize('dfa_converted.png', title='DFA Converti')

   # Comparaison côte à côte
   compare_automata(
       [nfa, dfa],
       labels=['NFA Original', 'DFA Converti'],
       filename='comparison.png',
       layout='horizontal',
       show_differences=True,
       title='Comparaison NFA vs DFA'
   )

   print("Comparaison générée: comparison.png")

Exemple 5 : Visualisation interactive
---------------------------------------

**Problème** : Créer une visualisation interactive avec Plotly.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.visualization import create_interactive_plot

   # DFA complexe pour la démonstration
   complex_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4'},
       alphabet={'a', 'b', 'c'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q2',
           ('q0', 'c'): 'q3',
           ('q1', 'a'): 'q1',
           ('q1', 'b'): 'q4',
           ('q1', 'c'): 'q0',
           ('q2', 'a'): 'q4',
           ('q2', 'b'): 'q2',
           ('q2', 'c'): 'q0',
           ('q3', 'a'): 'q0',
           ('q3', 'b'): 'q0',
           ('q3', 'c'): 'q3',
           ('q4', 'a'): 'q4',
           ('q4', 'b'): 'q4',
           ('q4', 'c'): 'q4'),
       },
       initial_state='q0',
       final_states={'q4'}
   )

   # Créer une visualisation interactive
   create_interactive_plot(
       complex_dfa,
       title="DFA Interactif",
       show_tooltips=True,
       enable_zoom=True,
       animation_speed=1000,
       node_colors={
           'default': '#E3F2FD',
           'initial': '#FFCDD2',
           'final': '#C8E6C9',
           'initial_final': '#FFF3E0'
       },
       edge_colors={
           'default': '#1976D2',
           'highlight': '#FF5722'
       }
   )

   print("Visualisation interactive créée")

Exemple 6 : Animation d'exécution
----------------------------------

**Problème** : Créer une animation montrant l'exécution d'un automate.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.visualization import create_gif_animation

   # DFA pour l'animation
   animation_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q0',
           ('q1', 'a'): 'q2',
           ('q1', 'b'): 'q0',
           ('q2', 'a'): 'q2',
           ('q2', 'b'): 'q3',
           ('q3', 'a'): 'q1',
           ('q3', 'b'): 'q0'),
       },
       initial_state='q0',
       final_states={'q3'}
   )

   # Créer une animation GIF
   test_strings = ['a', 'ab', 'abb', 'abbb', 'abbbb']
   create_gif_animation(
       animation_dfa,
       test_strings,
       filename='dfa_animation.gif',
       duration=1000,
       loop=True,
       show_labels=True,
       highlight_path=True,
       title="Exécution DFA"
   )

   print("Animation GIF générée: dfa_animation.gif")

Exemple 7 : Thèmes de visualisation
------------------------------------

**Problème** : Appliquer différents thèmes de visualisation.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.visualization import apply_theme

   # DFA pour les thèmes
   theme_dfa = DFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q1', 'b'): 'q2'),
       },
       initial_state='q0',
       final_states={'q2'}
   )

   # Thème par défaut
   theme_dfa.visualize('theme_default.png', title='Thème par défaut')

   # Thème sombre
   dark_theme = apply_theme('dark')
   theme_dfa.visualize('theme_dark.png', **dark_theme, title='Thème sombre')

   # Thème coloré
   colorful_theme = apply_theme('colorful')
   theme_dfa.visualize('theme_colorful.png', **colorful_theme, title='Thème coloré')

   # Thème minimaliste
   minimal_theme = apply_theme('minimal')
   theme_dfa.visualize('theme_minimal.png', **minimal_theme, title='Thème minimal')

   # Thème académique
   academic_theme = apply_theme('academic')
   theme_dfa.visualize('theme_academic.png', **academic_theme, title='Thème académique')

   print("Thèmes de visualisation générés")

Exemple 8 : Visualisation de métriques
---------------------------------------

**Problème** : Visualiser les métriques d'un automate.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.visualization import visualize_metrics

   # DFA pour l'analyse de métriques
   metrics_dfa = DFA(
       states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
       alphabet={'a', 'b', 'c'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q0', 'b'): 'q2',
           ('q0', 'c'): 'q3',
           ('q1', 'a'): 'q4',
           ('q1', 'b'): 'q0',
           ('q1', 'c'): 'q5',
           ('q2', 'a'): 'q0',
           ('q2', 'b'): 'q4',
           ('q2', 'c'): 'q5',
           ('q3', 'a'): 'q5',
           ('q3', 'b'): 'q5',
           ('q3', 'c'): 'q4',
           ('q4', 'a'): 'q4',
           ('q4', 'b'): 'q4',
           ('q4', 'c'): 'q4',
           ('q5', 'a'): 'q5',
           ('q5', 'b'): 'q5',
           ('q5', 'c'): 'q5'),
       },
       initial_state='q0',
       final_states={'q4', 'q5'}
   )

   # Visualisation des métriques
   visualize_metrics(
       metrics_dfa,
       show_statistics=True,
       create_charts=True,
       export_data=True,
       filename='metrics_analysis.png',
       title='Analyse des Métriques DFA'
   )

   print("Analyse des métriques générée: metrics_analysis.png")

Exemple 9 : Export vers différents formats
-------------------------------------------

**Problème** : Exporter un automate vers différents formats.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.visualization import export_visualization

   # DFA pour l'export
   export_dfa = DFA(
       states={'q0', 'q1', 'q2'},
       alphabet={'a', 'b'},
       transitions={
           ('q0', 'a'): 'q1',
           ('q1', 'b'): 'q2'),
       },
       initial_state='q0',
       final_states={'q2'}
   )

   # Export vers différents formats
   formats = ['png', 'svg', 'pdf', 'jpg']
   
   for format_type in formats:
       try:
           export_visualization(
               export_dfa,
               format_type,
               filename=f'export_dfa.{format_type}',
               dpi=300 if format_type in ['png', 'jpg'] else None
           )
           print(f"Export {format_type.upper()} réussi: export_dfa.{format_type}")
       except Exception as e:
           print(f"Erreur export {format_type.upper()}: {e}")

   # Export JSON
   json_data = export_dfa.to_json()
   with open('export_dfa.json', 'w') as f:
       f.write(json_data)
   print("Export JSON réussi: export_dfa.json")

   # Export Graphviz
   graphviz_code = export_dfa.to_graphviz()
   with open('export_dfa.dot', 'w') as f:
       f.write(graphviz_code)
   print("Export Graphviz réussi: export_dfa.dot")

Exemple 10 : Visualisation personnalisée
------------------------------------------

**Problème** : Créer une visualisation avec des styles personnalisés.

**Solution** :

.. code-block:: python

   from baobab_automata import DFA
   from baobab_automata.visualization import create_custom_style

   # DFA pour la personnalisation
   custom_dfa = DFA(
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
           ('q3', 'b'): 'q2'),
       },
       initial_state='q0',
       final_states={'q3'}
   )

   # Style personnalisé
   custom_style = create_custom_style({
       'node_color': '#FF6B6B',
       'edge_color': '#4ECDC4',
       'final_node_color': '#45B7D1',
       'initial_node_color': '#96CEB4',
       'font_family': 'Arial',
       'font_size': 14,
       'edge_width': 2,
       'node_size': 0.8,
       'background_color': '#F8F9FA',
       'grid_color': '#E9ECEF'
   })

   # Appliquer le style personnalisé
   custom_dfa.visualize(
       'custom_style.png',
       **custom_style,
       title='Style Personnalisé',
       show_labels=True,
       layout='neato'
   )

   print("Visualisation personnalisée générée: custom_style.png")

Conseils d'utilisation
-----------------------

* **Formats** : Utilisez SVG pour la qualité, PNG pour la compatibilité
* **Résolution** : Augmentez le DPI pour les publications académiques
* **Layouts** : Testez différents algorithmes selon la taille de l'automate
* **Thèmes** : Choisissez le thème selon le contexte d'utilisation
* **Performance** : Pour de gros automates, utilisez des layouts optimisés
* **Accessibilité** : Utilisez des couleurs contrastées et des étiquettes claires
