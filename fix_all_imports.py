#!/usr/bin/env python3
"""
Script pour corriger tous les imports restants dans les tests
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Corrige les imports dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Corrections spécifiques pour les modules manquants
        corrections = [
            # Dependency analysis
            (r'from baobab_automata\.algorithms\.finite\.dependency_analysis import', 
             'from baobab_automata.algorithms.finite.specialized_algorithms import'),
            
            # ASTNode
            (r'from baobab_automata\.finite import.*ASTNode', 
             'from baobab_automata.finite.regex.regex_parser import ASTNode'),
            
            # Grammar exceptions
            (r'from baobab_automata\.pushdown\.grammar_exceptions import', 
             'from baobab_automata.pushdown.grammar.grammar_exceptions import'),
            
            # Optimization exceptions
            (r'from baobab_automata\.pushdown\.optimization_exceptions import', 
             'from baobab_automata.pushdown.optimization.optimization_exceptions import'),
            
            # PDAConfiguration
            (r'from baobab_automata\.pushdown import.*PDAConfiguration', 
             'from baobab_automata.pushdown.pda.pda_configuration import PDAConfiguration'),
            
            # Specialized algorithms
            (r'from baobab_automata\.pushdown\.specialized\.specialized_algorithms import', 
             'from baobab_automata.algorithms.pushdown.specialized_algorithms import'),
            
            # NTM configuration
            (r'from baobab_automata\.turing\.ntm_configuration import', 
             'from baobab_automata.turing.ntm.ntm_configuration import'),
            
            # TM configuration
            (r'from baobab_automata\.turing\.tm_configuration import', 
             'from baobab_automata.turing.tm.tm_configuration import'),
            
            # Turing conversion modules
            (r'from src\.baobab_automata\.turing\.conversion\.', 
             'from baobab_automata.turing.conversion.'),
            
            # PDA configuration
            (r'from baobab_automata\.pushdown\.pda_configuration import', 
             'from baobab_automata.pushdown.pda.pda_configuration import'),
            
            # PDA exceptions
            (r'from baobab_automata\.pushdown\.pda_exceptions import', 
             'from baobab_automata.pushdown.pda.pda_exceptions import'),
        ]
        
        for pattern, replacement in corrections:
            content = re.sub(pattern, replacement, content)
        
        # Si le contenu a changé, sauvegarder
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"[ERREUR] {file_path}: {e}")
        return False

def main():
    """Fonction principale"""
    print("Correction des imports restants dans les tests...")
    
    # Trouver tous les fichiers de test
    test_dir = Path("tests")
    test_files = []
    
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith('.py') and file.startswith('test_'):
                test_files.append(os.path.join(root, file))
    
    print(f"Trouvé {len(test_files)} fichiers de test")
    
    fixed_count = 0
    for file_path in test_files:
        if fix_imports_in_file(file_path):
            print(f"[OK] Corrigé: {file_path}")
            fixed_count += 1
    
    print(f"\nCorrection terminée: {fixed_count} fichiers modifiés")

if __name__ == "__main__":
    main()
