#!/usr/bin/env python3
"""
Script pour corriger automatiquement tous les imports dans les tests
après la réorganisation de la structure du projet.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Corrige les imports dans un fichier de test."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Corrections des imports
        replacements = [
            # Core -> interfaces/implementations
            (r'from baobab_automata\.core\.interfaces\.', 'from baobab_automata.interfaces.'),
            (r'from baobab_automata\.core\.implementations\.', 'from baobab_automata.implementations.'),
            
            # Automata -> modules directs
            (r'from baobab_automata\.automata\.finite\.', 'from baobab_automata.finite.'),
            (r'from baobab_automata\.automata\.pushdown\.', 'from baobab_automata.pushdown.'),
            (r'from baobab_automata\.automata\.turing\.', 'from baobab_automata.turing.'),
            
            # Algorithms
            (r'from baobab_automata\.algorithms\.conversion\.', 'from baobab_automata.algorithms.finite.'),
            (r'from baobab_automata\.algorithms\.optimization\.', 'from baobab_automata.algorithms.finite.'),
            (r'from baobab_automata\.algorithms\.pushdown\.', 'from baobab_automata.algorithms.pushdown.'),
            (r'from baobab_automata\.algorithms\.turing\.', 'from baobab_automata.algorithms.turing.'),
            
            # Turing conversion
            (r'from baobab_automata\.turing\.conversion\.', 'from baobab_automata.algorithms.turing.'),
            (r'from baobab_automata\.turing\.complexity\.', 'from baobab_automata.algorithms.turing.'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Si le contenu a changé, sauvegarder
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Corrige: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"[ERREUR] {file_path}: {e}")
        return False

def main():
    """Corrige tous les imports dans les tests."""
    tests_dir = Path("tests")
    
    if not tests_dir.exists():
        print("Dossier tests/ non trouvé!")
        return
    
    corrected_files = 0
    total_files = 0
    
    # Parcourir tous les fichiers Python dans tests/
    for py_file in tests_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        total_files += 1
        if fix_imports_in_file(py_file):
            corrected_files += 1
    
    print(f"\nRésumé:")
    print(f"- Fichiers traités: {total_files}")
    print(f"- Fichiers corrigés: {corrected_files}")

if __name__ == "__main__":
    main()
