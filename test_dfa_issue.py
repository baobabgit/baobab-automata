#!/usr/bin/env python3
"""
Test pour reproduire le problème avec l'automate DFA.
Le problème semble être que même une regex simple ne fonctionne pas correctement.
"""

import sys
import os

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from baobab_automata import regex_to_nfa, minimize_dfa, DFA, Match
    print("✓ Import réussi des fonctions baobab-automata")
except ImportError as e:
    print(f"✗ Erreur d'import: {e}")
    sys.exit(1)

def test_simple_regex():
    """Test avec une regex simple pour identifier le problème."""
    print("\n=== TEST AVEC REGEX SIMPLE ===")
    
    # Test 1: Regex simple "hello"
    print("\n1. Test avec regex 'hello':")
    try:
        nfa = regex_to_nfa('hello')
        print(f"✓ NFA créé: {nfa}")
        
        dfa = nfa.to_dfa()
        print(f"✓ DFA créé: {dfa}")
        
        minimized_dfa = minimize_dfa(dfa)
        print(f"✓ DFA minimisé: {minimized_dfa}")
        
        # Test d'acceptation
        test_text = "hello world"
        print(f"\nTest d'acceptation avec '{test_text}':")
        print(f"  accepts('hello'): {minimized_dfa.accepts('hello')}")
        print(f"  accepts('hello world'): {minimized_dfa.accepts('hello world')}")
        print(f"  accepts('world'): {minimized_dfa.accepts('world')}")
        
        # Test de recherche de correspondance
        print(f"\nTest de recherche dans '{test_text}':")
        match = minimized_dfa.find_longest_match(test_text, 0)
        if match:
            print(f"  ✓ Trouvé: '{match.value}' à la position {match.start}-{match.end}")
        else:
            print("  ✗ Aucune correspondance trouvée")
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()

def test_string_regex():
    """Test avec une regex pour les chaînes entre guillemets."""
    print("\n=== TEST AVEC REGEX POUR CHAÎNES ===")
    
    # Test 2: Regex pour chaînes entre guillemets
    print("\n2. Test avec regex '\"hello\"':")
    try:
        nfa = regex_to_nfa('"hello"')
        print(f"✓ NFA créé: {nfa}")
        
        dfa = nfa.to_dfa()
        print(f"✓ DFA créé: {dfa}")
        
        minimized_dfa = minimize_dfa(dfa)
        print(f"✓ DFA minimisé: {minimized_dfa}")
        
        # Test d'acceptation
        test_text = '"hello" world'
        print(f"\nTest d'acceptation avec '{test_text}':")
        print(f"  accepts('\"hello\"'): {minimized_dfa.accepts('\"hello\"')}")
        print(f"  accepts('\"hello\" world'): {minimized_dfa.accepts('\"hello\" world')}")
        print(f"  accepts('world'): {minimized_dfa.accepts('world')}")
        
        # Test de recherche de correspondance
        print(f"\nTest de recherche dans '{test_text}':")
        match = minimized_dfa.find_longest_match(test_text, 0)
        if match:
            print(f"  ✓ Trouvé: '{match.value}' à la position {match.start}-{match.end}")
        else:
            print("  ✗ Aucune correspondance trouvée")
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()

def test_character_regex():
    """Test avec une regex pour un seul caractère."""
    print("\n=== TEST AVEC REGEX POUR UN CARACTÈRE ===")
    
    # Test 3: Regex pour un seul caractère 'o'
    print("\n3. Test avec regex 'o':")
    try:
        nfa = regex_to_nfa('o')
        print(f"✓ NFA créé: {nfa}")
        
        dfa = nfa.to_dfa()
        print(f"✓ DFA créé: {dfa}")
        
        minimized_dfa = minimize_dfa(dfa)
        print(f"✓ DFA minimisé: {minimized_dfa}")
        
        # Test d'acceptation
        test_text = "hello world"
        print(f"\nTest d'acceptation avec '{test_text}':")
        print(f"  accepts('o'): {minimized_dfa.accepts('o')}")
        print(f"  accepts('hello'): {minimized_dfa.accepts('hello')}")
        
        # Test de recherche de correspondance
        print(f"\nTest de recherche dans '{test_text}':")
        match = minimized_dfa.find_longest_match(test_text, 0)
        if match:
            print(f"  ✓ Trouvé: '{match.value}' à la position {match.start}-{match.end}")
        else:
            print("  ✗ Aucune correspondance trouvée")
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== DIAGNOSTIC DU PROBLÈME DFA ===")
    
    # Test des regex simples
    test_simple_regex()
    test_string_regex()
    test_character_regex()
    
    print("\n=== FIN DU DIAGNOSTIC ===")
