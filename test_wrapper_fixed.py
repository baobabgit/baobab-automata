#!/usr/bin/env python3
"""
Test du wrapper BaobabAutomataWrapper avec la correction.
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

class BaobabAutomataWrapper:
    """Wrapper pour baobab-automata avec cache."""
    
    def __init__(self):
        self._dfa_cache = {}
        self._regex_cache = {}
    
    def create_dfa_from_regex(self, regex: str) -> DFA:
        """Crée un DFA à partir d'une expression régulière."""
        if regex in self._regex_cache:
            return self._regex_cache[regex]
        
        try:
            nfa = regex_to_nfa(regex)
            dfa = nfa.to_dfa()
            dfa = minimize_dfa(dfa)
            self._regex_cache[regex] = dfa
            return dfa
        except Exception as e:
            print(f"Erreur lors de la création du DFA: {e}")
            return None
    
    def find_match(self, dfa: DFA, text: str, start: int) -> dict:
        """Trouve la correspondance la plus longue."""
        if not dfa:
            return None
        
        try:
            match = dfa.find_longest_match(text, start)
            if match:
                return {
                    'start': match.start,
                    'end': match.end,
                    'value': match.match  # Utiliser match.match au lieu de match.value
                }
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
        
        return None

def test_wrapper():
    """Test du wrapper avec la regex 'hello'."""
    print("\n=== TEST DU WRAPPER ===")
    
    wrapper = BaobabAutomataWrapper()
    
    # Test avec regex 'hello'
    print("\n1. Test avec regex 'hello':")
    dfa = wrapper.create_dfa_from_regex('hello')
    
    if dfa:
        print(f"✓ DFA créé: {dfa}")
        print(f"  États: {dfa.states}")
        print(f"  Alphabet: {dfa.alphabet}")
        print(f"  État initial: {dfa.initial_state}")
        print(f"  États finaux: {dfa.final_states}")
        
        # Test d'acceptation
        test_text = "hello world"
        print(f"\nTest d'acceptation avec '{test_text}':")
        print(f"  accepts('hello'): {dfa.accepts('hello')}")
        print(f"  accepts('hello world'): {dfa.accepts('hello world')}")
        
        # Test de recherche
        print(f"\nTest de recherche dans '{test_text}':")
        match = wrapper.find_match(dfa, test_text, 0)
        if match:
            print(f"  ✓ Trouvé: '{match['value']}' à la position {match['start']}-{match['end']}")
        else:
            print("  ✗ Aucune correspondance trouvée")
    else:
        print("✗ Échec de la création du DFA")

if __name__ == "__main__":
    print("=== TEST DU WRAPPER CORRIGÉ ===")
    test_wrapper()
    print("\n=== FIN DU TEST ===")
