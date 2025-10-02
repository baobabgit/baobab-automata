Installation et Configuration
==============================

Ce guide vous accompagne dans l'installation et la configuration de Baobab Automata.

Prérequis
---------

Baobab Automata nécessite :

* **Python** >= 3.11
* **pip** (gestionnaire de paquets Python)
* **Git** (pour l'installation depuis les sources)

Dépendances système
-------------------

Certaines fonctionnalités de visualisation nécessitent des dépendances système :

* **Graphviz** : Pour la génération de graphiques d'automates
* **LaTeX** (optionnel) : Pour la génération de documents PDF avec formules mathématiques

Installation de Graphviz
~~~~~~~~~~~~~~~~~~~~~~~~~

Ubuntu/Debian
^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install graphviz graphviz-dev

CentOS/RHEL/Fedora
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo yum install graphviz graphviz-devel
   # ou pour Fedora
   sudo dnf install graphviz graphviz-devel

macOS
^^^^^

.. code-block:: bash

   brew install graphviz

Windows
^^^^^^^

Téléchargez et installez Graphviz depuis `https://graphviz.org/download/`

Installation de Baobab Automata
-------------------------------

Installation depuis PyPI (recommandée)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install baobab-automata

Installation avec dépendances de développement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install baobab-automata[dev]

Installation depuis les sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour installer la version de développement :

.. code-block:: bash

   # Cloner le repository
   git clone https://github.com/baobab-automata/baobab-automata.git
   cd baobab-automata

   # Créer un environnement virtuel
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows

   # Installer en mode développement
   pip install -e .[dev]

Configuration de l'environnement
--------------------------------

Variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez configurer les variables d'environnement suivantes :

.. code-block:: bash

   # Chemin vers l'exécutable Graphviz
   export GRAPHVIZ_BIN=/usr/bin/dot

   # Niveau de logging (DEBUG, INFO, WARNING, ERROR)
   export BAOBAB_LOG_LEVEL=INFO

   # Dossier de cache pour les visualisations
   export BAOBAB_CACHE_DIR=~/.cache/baobab-automata

Configuration Python
~~~~~~~~~~~~~~~~~~~~

Pour une configuration personnalisée, créez un fichier ``baobab_config.py`` :

.. code-block:: python

   # baobab_config.py
   import os

   # Configuration des chemins
   GRAPHVIZ_BIN = os.getenv('GRAPHVIZ_BIN', '/usr/bin/dot')
   CACHE_DIR = os.getenv('BAOBAB_CACHE_DIR', '~/.cache/baobab-automata')
   
   # Configuration des visualisations
   DEFAULT_FORMAT = 'png'
   DEFAULT_DPI = 300
   
   # Configuration des algorithmes
   MAX_STATES_FOR_EXHAUSTIVE = 1000
   TIMEOUT_SECONDS = 30

Vérification de l'installation
------------------------------

Testez votre installation avec le script suivant :

.. code-block:: python

   # test_installation.py
   import baobab_automata
   from baobab_automata import DFA

   print(f"Version de Baobab Automata : {baobab_automata.__version__}")

   # Test basique
   dfa = DFA(
       states={'q0', 'q1'},
       alphabet={'a'},
       transitions={('q0', 'a'): 'q1'},
       initial_state='q0',
       final_states={'q1'}
   )

   assert dfa.accepts('a')
   print("✓ Installation réussie !")

Exécutez le test :

.. code-block:: bash

   python test_installation.py

Dépannage
---------

Problèmes courants
~~~~~~~~~~~~~~~~~~

**Erreur "dot not found"**
   Assurez-vous que Graphviz est installé et que l'exécutable ``dot`` est dans votre PATH.

**Erreur d'importation**
   Vérifiez que vous utilisez Python >= 3.11 et que toutes les dépendances sont installées.

**Problèmes de performance**
   Pour de gros automates, ajustez les paramètres de configuration ou utilisez les algorithmes optimisés.

Support
-------

Si vous rencontrez des problèmes :

* Consultez la `section FAQ <faq.html>`_
* Ouvrez une issue sur `GitHub <https://github.com/baobab-automata/baobab-automata/issues>`_
* Consultez la documentation API complète

Prochaines étapes
-----------------

Une fois l'installation terminée, consultez :

* :doc:`quickstart` - Guide de démarrage rapide
* :doc:`../examples/index` - Exemples d'utilisation
* :doc:`index` - Documentation API complète
