#!/usr/bin/env python3
"""Test des opérations sur la pile."""

from src.baobab_automata.pushdown.pda_configuration import PDAConfiguration

def test_stack_operations():
    """Test des opérations sur la pile."""
    print("=== TEST DES OPÉRATIONS SUR LA PILE ===")
    
    # Configuration initiale
    config = PDAConfiguration('q0', 'ab', 'Z')
    print(f"Configuration initiale: {config}")
    print(f"Pile: '{config.stack}'")
    print(f"Sommet de pile: '{config.stack_top}'")
    
    # Empiler 'AZ'
    config = config.push_symbols('AZ')
    print(f"\nAprès empilage de 'AZ':")
    print(f"Pile: '{config.stack}'")
    print(f"Sommet de pile: '{config.stack_top}'")
    
    # Consommer 'a'
    config = config.consume_input('a')
    print(f"\nAprès consommation de 'a':")
    print(f"Mot restant: '{config.remaining_input}'")
    print(f"Pile: '{config.stack}'")
    print(f"Sommet de pile: '{config.stack_top}'")
    
    # Changer d'état
    config = config.change_state('q0')
    print(f"\nAprès changement d'état vers 'q0':")
    print(f"État: '{config.state}'")
    print(f"Pile: '{config.stack}'")
    print(f"Sommet de pile: '{config.stack_top}'")

if __name__ == "__main__":
    test_stack_operations()