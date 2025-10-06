#!/usr/bin/env python3
"""
Script pour corriger automatiquement tous les imports restants dans les tests
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
        
        # Corrections des imports - version étendue
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
            
            # Corrections spécifiques pour les modules manquants
            # Finite
            (r'from baobab_automata\.finite\.dfa_exceptions', 'from baobab_automata.finite.dfa.dfa_exceptions'),
            (r'from baobab_automata\.finite\.nfa_exceptions', 'from baobab_automata.finite.nfa.nfa_exceptions'),
            (r'from baobab_automata\.finite\.epsilon_nfa_exceptions', 'from baobab_automata.finite.nfa.epsilon_nfa_exceptions'),
            (r'from baobab_automata\.finite\.language_operations_exceptions', 'from baobab_automata.finite.language.language_operations_exceptions'),
            (r'from baobab_automata\.finite\.optimization_exceptions', 'from baobab_automata.finite.optimization.optimization_exceptions'),
            (r'from baobab_automata\.finite\.regex_exceptions', 'from baobab_automata.finite.regex.regex_exceptions'),
            (r'from baobab_automata\.finite\.regex_ast', 'from baobab_automata.finite.regex.regex_ast'),
            (r'from baobab_automata\.finite\.regex_parser', 'from baobab_automata.finite.regex.regex_parser'),
            (r'from baobab_automata\.finite\.regex_token', 'from baobab_automata.finite.regex.regex_token'),
            (r'from baobab_automata\.finite\.transition_change', 'from baobab_automata.finite.optimization.transition_change'),
            (r'from baobab_automata\.finite\.conversion_algorithms', 'from baobab_automata.algorithms.finite.conversion_algorithms'),
            (r'from baobab_automata\.finite\.optimization_algorithms', 'from baobab_automata.algorithms.finite.optimization_algorithms'),
            (r'from baobab_automata\.finite\.language_operations', 'from baobab_automata.finite.language.language_operations'),
            
            # Pushdown
            (r'from baobab_automata\.pushdown\.dpda_exceptions', 'from baobab_automata.pushdown.dpda.dpda_exceptions'),
            (r'from baobab_automata\.pushdown\.dpda_configuration', 'from baobab_automata.pushdown.dpda.dpda_configuration'),
            (r'from baobab_automata\.pushdown\.npda_exceptions', 'from baobab_automata.pushdown.npda.npda_exceptions'),
            (r'from baobab_automata\.pushdown\.npda_configuration', 'from baobab_automata.pushdown.npda.npda_configuration'),
            (r'from baobab_automata\.pushdown\.grammar_parser', 'from baobab_automata.pushdown.grammar.grammar_parser'),
            (r'from baobab_automata\.pushdown\.grammar_types', 'from baobab_automata.pushdown.grammar.grammar_types'),
            (r'from baobab_automata\.pushdown\.pda_operations', 'from baobab_automata.pushdown.pda.pda_operations'),
            (r'from baobab_automata\.pushdown\.conversion_algorithms', 'from baobab_automata.algorithms.pushdown.pushdown_conversion_algorithms'),
            (r'from baobab_automata\.pushdown\.optimization_algorithms', 'from baobab_automata.algorithms.pushdown.pushdown_optimization_algorithms'),
            (r'from baobab_automata\.pushdown\.specialized_algorithms', 'from baobab_automata.pushdown.specialized.specialized_algorithms'),
            
            # Turing
            (r'from baobab_automata\.turing\.multitape_tm', 'from baobab_automata.turing.multitape.multitape_tm'),
            (r'from baobab_automata\.turing\.multitape_configuration', 'from baobab_automata.turing.multitape.multitape_configuration'),
            
            # Algorithms spécifiques
            (r'from baobab_automata\.algorithms\.dependency_analysis', 'from baobab_automata.algorithms.finite.dependency_analysis'),
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


