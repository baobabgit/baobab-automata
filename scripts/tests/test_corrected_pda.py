#!/usr/bin/env python3
"""Test du PDA avec la définition corrigée."""

from src.baobab_automata.pushdown import PDA

def test_corrected_pda():
    """Test du PDA avec la définition corrigée."""
    print("=== TEST PDA AVEC DÉFINITION CORRIGÉE ===")
    
    # PDA pour a^n b^n - définition corrigée
    # La pile est représentée avec le sommet à droite
    # Quand on empile 'AZ' sur 'Z', on obtient 'ZAZ' avec 'Z' au sommet
    pda = PDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): {('q0', 'AZ')},  # Lire 'a', empiler 'AZ' sur 'Z'
            ('q0', 'a', 'A'): {('q0', 'AA')},  # Lire 'a', empiler 'AA' sur 'A'
            ('q0', 'b', 'A'): {('q1', '')},    # Lire 'b', dépiler 'A'
            ('q1', 'b', 'A'): {('q1', '')},    # Lire 'b', dépiler 'A'
            ('q1', '', 'Z'): {('q2', 'Z')}     # Transition epsilon, dépiler 'Z'
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print(f"PDA: {pda}")
    print(f"Transitions: {pda._transitions}")
    
    # Test avec le mot 'ab' - simulation manuelle
    print(f"\n=== SIMULATION MANUELLE POUR 'ab' ===")
    
    # Étape 1: (q0, ab, Z) --a,Z--> (q0, b, ZAZ)
    # On lit 'a', on empile 'AZ' sur 'Z' -> 'ZAZ'
    print("Étape 1: (q0, ab, Z) --a,Z--> (q0, b, ZAZ)")
    print("  Pile après empilage de 'AZ' sur 'Z': 'ZAZ'")
    print("  Sommet de pile: 'Z'")
    
    # Étape 2: (q0, b, ZAZ) --b,A--> (q1, , ZA)
    # On lit 'b', on dépile 'A' -> 'ZA'
    print("Étape 2: (q0, b, ZAZ) --b,A--> (q1, , ZA)")
    print("  Pile après dépilage de 'A': 'ZA'")
    print("  Sommet de pile: 'Z'")
    
    # Étape 3: (q1, , ZA) --ε,Z--> (q2, , ZA)
    # Transition epsilon, on dépile 'Z' -> 'A'
    print("Étape 3: (q1, , ZA) --ε,Z--> (q2, , A)")
    print("  Pile après dépilage de 'Z': 'A'")
    print("  État final atteint: q2")
    
    # Test avec l'implémentation
    test_words = ['ab', 'aabb', 'aaabbb', 'a', 'b', 'abab', '']
    
    for word in test_words:
        result = pda.accepts(word)
        print(f"Mot '{word}': {'✓ ACCEPTÉ' if result else '✗ REJETÉ'}")

if __name__ == "__main__":
    test_corrected_pda()