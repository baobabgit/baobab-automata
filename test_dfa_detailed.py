#!/usr/bin/env python3
"""
Test détaillé pour analyser le problème avec l'automate DFA.
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
        
        # Afficher les détails du DFA
        print(f"  États: {minimized_dfa.states}")
        print(f"  Alphabet: {minimized_dfa.alphabet}")
        print(f"  État initial: {minimized_dfa.initial_state}")
        print(f"  États finaux: {minimized_dfa.final_states}")
        
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
            print(f"  ✓ Trouvé: '{match.match}' à la position {match.start}-{match.end}")
        else:
            print("  ✗ Aucune correspondance trouvée")
            
        # Test manuel de simulation
        print(f"\nTest manuel de simulation:")
        word = "hello"
        current_state = minimized_dfa.initial_state
        print(f"  État initial: {current_state}")
        
        for i, symbol in enumerate(word):
            print(f"  Symbole '{symbol}' à la position {i}")
            if symbol not in minimized_dfa.alphabet:
                print(f"    ✗ Symbole '{symbol}' pas dans l'alphabet")
                break
            
            # Simuler la transition
            transition_key = (current_state, symbol)
            print(f"    Clé de transition: {transition_key}")
            
            # Accéder aux transitions privées
            if hasattr(minimized_dfa, '_transitions'):
                transitions = minimized_dfa._transitions
                print(f"    Transitions disponibles: {transitions}")
                if transition_key in transitions:
                    current_state = transitions[transition_key]
                    print(f"    → Nouvel état: {current_state}")
                else:
                    print(f"    ✗ Transition non trouvée")
                    break
            else:
                print(f"    ✗ Attribut _transitions non trouvé")
                break
        
        print(f"  État final: {current_state}")
        print(f"  Est final: {current_state in minimized_dfa.final_states}")
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== DIAGNOSTIC DU PROBLÈME DFA (DÉTAILLÉ) ===")
    test_simple_regex()
    print("\n=== FIN DU DIAGNOSTIC ===")
