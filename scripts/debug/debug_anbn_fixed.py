import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Script de débogage avec un DPDA corrigé pour a^n b^n."""

from src.baobab_automata.pushdown.dpda import DPDA

def test_anbn_fixed():
    """Test avec un DPDA corrigé pour a^n b^n."""
    # DPDA pour reconnaître a^n b^n avec états séparés
    dpda = DPDA(
        states={'q0', 'q1', 'q2', 'q3'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): ('q0', 'AZ'),  # Empiler A pour chaque a
            ('q0', 'a', 'A'): ('q0', 'AA'),  # Empiler A pour chaque a
            ('q0', 'b', 'A'): ('q1', ''),    # Dépiler A pour chaque b
            ('q1', 'b', 'A'): ('q1', ''),    # Dépiler A pour chaque b
            ('q1', 'b', 'Z'): ('q2', 'Z'),   # Transition vers état de vérification
            ('q2', '', 'Z'): ('q3', 'Z')     # Transition epsilon vers état final
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q3'}
    )
    
    print("=== Test du DPDA corrigé pour a^n b^n ===")
    test_words = ['ab', 'aabb', 'aaabbb', 'a', 'b', 'abab', '']
    
    for word in test_words:
        result = dpda.accepts(word)
        print(f"Mot '{word}': {'Accepté' if result else 'Rejeté'}")

if __name__ == "__main__":
    test_anbn_fixed()