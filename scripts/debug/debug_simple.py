#!/usr/bin/env python3
"""Script de débogage simple."""

from src.baobab_automata.pushdown.dpda import DPDA

def test_simple():
    """Test simple d'un DPDA."""
    # DPDA très simple pour tester
    dpda = DPDA(
        states={'q0', 'q1'},
        input_alphabet={'a'},
        stack_alphabet={'Z'},
        transitions={
            ('q0', 'a', 'Z'): ('q1', 'Z')
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q1'}
    )
    
    print("DPDA simple créé")
    print(f"Accepte 'a': {dpda.accepts('a')}")
    print(f"Accepte '': {dpda.accepts('')}")

if __name__ == "__main__":
    test_simple()