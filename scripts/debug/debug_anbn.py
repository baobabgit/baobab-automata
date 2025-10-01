import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Script de débogage pour a^n b^n."""

from src.baobab_automata.pushdown.dpda import DPDA

def test_anbn():
    """Test avec un DPDA pour a^n b^n qui fonctionne."""
    # DPDA pour reconnaître a^n b^n avec approche différente
    dpda = DPDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): ('q0', 'AZ'),  # Empiler A pour chaque a
            ('q0', 'a', 'A'): ('q0', 'AA'),  # Empiler A pour chaque a
            ('q0', 'b', 'A'): ('q1', ''),    # Dépiler A pour chaque b
            ('q1', 'b', 'A'): ('q1', ''),    # Dépiler A pour chaque b
            ('q1', 'b', 'Z'): ('q2', 'Z')    # Transition directe vers état final
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print("=== Test du DPDA pour a^n b^n ===")
    
    # Test détaillé du mot 'ab'
    print("\n--- Test du mot 'ab' ---")
    word = 'ab'
    print(f"Mot: '{word}'")
    print(f"Résultat: {dpda.accepts(word)}")
    
    # Test détaillé du mot 'aabb'
    print("\n--- Test du mot 'aabb' ---")
    word = 'aabb'
    print(f"Mot: '{word}'")
    print(f"Résultat: {dpda.accepts(word)}")
    
    # Test détaillé du mot 'a'
    print("\n--- Test du mot 'a' ---")
    word = 'a'
    print(f"Mot: '{word}'")
    print(f"Résultat: {dpda.accepts(word)}")

if __name__ == "__main__":
    test_anbn()