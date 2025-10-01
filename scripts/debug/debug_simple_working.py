#!/usr/bin/env python3
"""Script de débogage avec un DPDA simple qui fonctionne."""

from src.baobab_automata.pushdown.dpda import DPDA

def test_simple_working():
    """Test avec un DPDA simple qui fonctionne."""
    # DPDA très simple qui accepte le mot 'ab'
    dpda = DPDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z'},
        transitions={
            ('q0', 'a', 'Z'): ('q1', 'Z'),
            ('q1', 'b', 'Z'): ('q2', 'Z')
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print("=== Test du DPDA simple ===")
    test_words = ['ab', 'a', 'b', 'ba', '']
    
    for word in test_words:
        result = dpda.accepts(word)
        print(f"Mot '{word}': {'Accepté' if result else 'Rejeté'}")

if __name__ == "__main__":
    test_simple_working()