import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Test du PDA corrigé pour a^n b^n."""

from src.baobab_automata.pushdown import PDA

def test_correct_pda():
    """Test du PDA corrigé pour a^n b^n."""
    print("=== TEST PDA CORRIGÉ POUR a^n b^n ===")
    
    # PDA pour a^n b^n - version corrigée
    pda = PDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): {('q0', 'AZ')},  # Empiler A sur Z
            ('q0', 'a', 'A'): {('q0', 'AA')},  # Empiler A sur A
            ('q0', 'b', 'A'): {('q1', '')},    # Dépiler A
            ('q1', 'b', 'A'): {('q1', '')},    # Dépiler A
            ('q1', '', 'Z'): {('q2', 'Z')}     # Transition epsilon vers état final
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print(f"PDA: {pda}")
    print(f"Transitions: {pda._transitions}")
    
    # Test avec différents mots
    test_words = ['ab', 'aabb', 'aaabbb', 'a', 'b', 'abab', '']
    
    for word in test_words:
        result = pda.accepts(word)
        print(f"Mot '{word}': {'✓ ACCEPTÉ' if result else '✗ REJETÉ'}")

if __name__ == "__main__":
    test_correct_pda()