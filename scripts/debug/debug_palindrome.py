import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Debug du PDA pour les palindromes."""

from src.baobab_automata.pushdown import PDA

def debug_palindrome():
    """Debug du PDA pour les palindromes."""
    print("=== DEBUG PDA POUR PALINDROMES ===")
    
    # PDA pour palindromes de longueur impaire
    pda_palindrome = PDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A', 'B'},
        transitions={
            ('q0', 'a', 'Z'): {('q0', 'AZ')},
            ('q0', 'b', 'Z'): {('q0', 'BZ')},
            ('q0', 'a', 'A'): {('q0', 'AA'), ('q1', '')},  # Deux transitions possibles
            ('q0', 'b', 'A'): {('q0', 'BA')},
            ('q0', 'a', 'B'): {('q0', 'AB')},
            ('q0', 'b', 'B'): {('q0', 'BB'), ('q1', '')},  # Deux transitions possibles
            ('q1', 'a', 'A'): {('q1', '')},
            ('q1', 'b', 'B'): {('q1', '')},
            ('q1', '', 'Z'): {('q2', 'Z')}
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print(f"PDA: {pda_palindrome}")
    print(f"Transitions: {pda_palindrome._transitions}")
    
    # Test avec différents mots
    test_words = ['a', 'b', 'aba', 'bab', 'ababa']
    
    for word in test_words:
        print(f"\n=== TEST AVEC LE MOT '{word}' ===")
        result = pda_palindrome.accepts(word)
        print(f"Résultat: {'✓ ACCEPTÉ' if result else '✗ REJETÉ'}")
        
        # Simulation manuelle pour 'a'
        if word == 'a':
            print("\nSimulation manuelle pour 'a':")
            print("Étape 1: (q0, a, Z) --a,Z--> (q0, , AZ)")
            print("  Pile après empilage de 'AZ' sur 'Z': 'AZ'")
            print("  Sommet de pile: 'A'")
            print("  Mot entièrement lu: oui")
            print("  État final: q0 (non final)")
            print("  Résultat: REJETÉ")
            
            print("\nAlternative: (q0, a, Z) --a,Z--> (q1, , Z)")
            print("  Transition alternative vers q1")
            print("  Pile après dépilage de 'A': 'Z'")
            print("  Sommet de pile: 'Z'")
            print("  Mot entièrement lu: oui")
            print("  État final: q1 (non final)")
            print("  Résultat: REJETÉ")

if __name__ == "__main__":
    debug_palindrome()