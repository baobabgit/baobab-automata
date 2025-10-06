#!/usr/bin/env python3
"""
Script pour corriger automatiquement les imports après réorganisation.
"""

import os
import re

def fix_imports_in_file(file_path):
    """Corrige les imports dans un fichier."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Corrections pour les automates finis
    content = re.sub(
        r'from \.abstract_finite_automaton import',
        'from ..abstract_finite_automaton import',
        content
    )
    
    # Corrections pour les automates à pile
    content = re.sub(
        r'from \.abstract_pushdown_automaton import',
        'from ..abstract_pushdown_automaton import',
        content
    )
    
    # Corrections pour les machines de Turing
    content = re.sub(
        r'from \.tm import',
        'from ..tm import',
        content
    )
    
    # Corrections pour les algorithmes
    content = re.sub(
        r'from \.\.\.automata\.finite\.',
        'from ...finite.',
        content
    )
    content = re.sub(
        r'from \.\.\.automata\.pushdown\.',
        'from ...pushdown.',
        content
    )
    content = re.sub(
        r'from \.\.\.automata\.turing\.',
        'from ...turing.',
        content
    )
    
    # Corrections pour les imports relatifs dans les sous-dossiers
    content = re.sub(
        r'from \.dfa import',
        'from ..dfa import',
        content
    )
    content = re.sub(
        r'from \.nfa import',
        'from ..nfa import',
        content
    )
    content = re.sub(
        r'from \.regex import',
        'from ..regex import',
        content
    )
    content = re.sub(
        r'from \.language import',
        'from ..language import',
        content
    )
    content = re.sub(
        r'from \.optimization import',
        'from ..optimization import',
        content
    )
    
    # Corrections pour les automates à pile
    content = re.sub(
        r'from \.pda import',
        'from ..pda import',
        content
    )
    content = re.sub(
        r'from \.dpda import',
        'from ..dpda import',
        content
    )
    content = re.sub(
        r'from \.npda import',
        'from ..npda import',
        content
    )
    content = re.sub(
        r'from \.grammar import',
        'from ..grammar import',
        content
    )
    
    # Corrections pour les machines de Turing
    content = re.sub(
        r'from \.dtm import',
        'from ..dtm import',
        content
    )
    content = re.sub(
        r'from \.ntm import',
        'from ..ntm import',
        content
    )
    content = re.sub(
        r'from \.multitape import',
        'from ..multitape import',
        content
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Corrigé: {file_path}")
        return True
    return False

def main():
    """Fonction principale."""
    src_dir = "src/baobab_automata"
    fixed_count = 0
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_imports_in_file(file_path):
                    fixed_count += 1
    
    print(f"Total de fichiers corrigés: {fixed_count}")

if __name__ == "__main__":
    main()
