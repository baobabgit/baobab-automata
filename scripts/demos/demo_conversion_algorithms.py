#!/usr/bin/env python3
"""
Script de démonstration des algorithmes de conversion.

Ce script démontre l'utilisation de la classe ConversionAlgorithms
pour convertir entre différents types d'automates finis.
"""

from baobab_automata.finite import (
    ConversionAlgorithms,
    DFA,
    EpsilonNFA,
    NFA
)


def main():
    """Fonction principale de démonstration."""
    print("=== Démonstration des Algorithmes de Conversion ===\n")
    
    # Créer le convertisseur
    converter = ConversionAlgorithms(optimization_enabled=True, max_states=1000)
    print("✅ Convertisseur créé avec optimisations activées")
    
    # ========================================================================
    # Démonstration NFA → DFA
    # ========================================================================
    print("\n--- Conversion NFA → DFA ---")
    
    # Créer un NFA simple
    nfa = NFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): {'q1', 'q2'},
            ('q1', 'b'): {'q2'}
        },
        initial_state='q0',
        final_states={'q2'}
    )
    
    print(f"NFA original: {nfa}")
    print(f"  États: {nfa.states}")
    print(f"  Alphabet: {nfa.alphabet}")
    print(f"  État initial: {nfa.initial_state}")
    print(f"  États finaux: {nfa.final_states}")
    
    # Convertir en DFA
    dfa = converter.nfa_to_dfa_optimized(nfa)
    print(f"\nDFA converti: {dfa}")
    print(f"  États: {dfa.states}")
    print(f"  Alphabet: {dfa.alphabet}")
    print(f"  État initial: {dfa.initial_state}")
    print(f"  États finaux: {dfa.final_states}")
    
    # ========================================================================
    # Démonstration ε-NFA → NFA
    # ========================================================================
    print("\n--- Conversion ε-NFA → NFA ---")
    
    # Créer un ε-NFA simple
    epsilon_nfa = EpsilonNFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'ε'): {'q1'},
            ('q0', 'a'): {'q2'},
            ('q1', 'b'): {'q2'}
        },
        initial_state='q0',
        final_states={'q2'}
    )
    
    print(f"ε-NFA original: {epsilon_nfa}")
    print(f"  États: {epsilon_nfa.states}")
    print(f"  Alphabet: {epsilon_nfa.alphabet}")
    print(f"  Symbole epsilon: {epsilon_nfa.epsilon_symbol}")
    
    # Convertir en NFA
    nfa_from_epsilon = converter.epsilon_nfa_to_nfa_optimized(epsilon_nfa)
    print(f"\nNFA converti: {nfa_from_epsilon}")
    print(f"  États: {nfa_from_epsilon.states}")
    print(f"  Alphabet: {nfa_from_epsilon.alphabet}")
    
    # ========================================================================
    # Démonstration ε-NFA → DFA
    # ========================================================================
    print("\n--- Conversion ε-NFA → DFA ---")
    
    # Convertir ε-NFA en DFA
    dfa_from_epsilon = converter.epsilon_nfa_to_dfa_optimized(epsilon_nfa)
    print(f"DFA converti: {dfa_from_epsilon}")
    print(f"  États: {dfa_from_epsilon.states}")
    print(f"  Alphabet: {dfa_from_epsilon.alphabet}")
    
    # ========================================================================
    # Démonstration Expression Régulière → Automate
    # ========================================================================
    print("\n--- Conversion Expression Régulière → Automate ---")
    
    # Convertir des expressions régulières en automates
    expressions = ['a', 'a*', 'a+']
    
    for expr in expressions:
        print(f"\nExpression: '{expr}'")
        
        # Conversion vers ε-NFA
        epsilon_nfa_from_regex = converter.regex_to_automaton_optimized(expr, 'epsilon_nfa')
        print(f"  ε-NFA: {epsilon_nfa_from_regex}")
        
        # Conversion vers DFA
        dfa_from_regex = converter.regex_to_automaton_optimized(expr, 'dfa')
        print(f"  DFA: {dfa_from_regex}")
    
    # ========================================================================
    # Démonstration Automate → Expression Régulière
    # ========================================================================
    print("\n--- Conversion Automate → Expression Régulière ---")
    
    # Créer un DFA simple
    simple_dfa = DFA(
        states={'q0', 'q1'},
        alphabet={'a'},
        transitions={('q0', 'a'): 'q1'},
        initial_state='q0',
        final_states={'q1'}
    )
    
    print(f"DFA original: {simple_dfa}")
    
    # Convertir en expression régulière
    regex = converter.automaton_to_regex_optimized(simple_dfa)
    print(f"Expression régulière: '{regex}'")
    
    # ========================================================================
    # Démonstration des fonctionnalités avancées
    # ========================================================================
    print("\n--- Fonctionnalités Avancées ---")
    
    # Statistiques du cache
    cache_stats = converter.get_cache_stats()
    print(f"Statistiques du cache:")
    print(f"  Taille: {cache_stats['cache_size']}")
    print(f"  Hits: {cache_stats['cache_hits']}")
    print(f"  Misses: {cache_stats['cache_misses']}")
    print(f"  Taux de hit: {cache_stats['hit_rate']:.2%}")
    
    # Statistiques de conversion
    conversion_stats = converter.get_conversion_stats()
    print(f"\nStatistiques de conversion:")
    print(f"  Total conversions: {conversion_stats['total_conversions']}")
    print(f"  Temps total: {conversion_stats['total_time']:.4f}s")
    print(f"  Temps moyen: {conversion_stats['average_time']:.4f}s")
    
    # Validation d'une conversion
    print(f"\nValidation de conversion:")
    is_valid = converter.validate_conversion(nfa, dfa)
    print(f"  NFA → DFA équivalent: {is_valid}")
    
    # ========================================================================
    # Démonstration des optimisations
    # ========================================================================
    print("\n--- Optimisations ---")
    
    # Créer un DFA avec des états inaccessibles
    dfa_with_unreachable = DFA(
        states={'q0', 'q1', 'q2', 'q3'},
        alphabet={'a'},
        transitions={('q0', 'a'): 'q1'},
        initial_state='q0',
        final_states={'q1', 'q3'}  # q3 est inaccessible
    )
    
    print(f"DFA avec états inaccessibles: {dfa_with_unreachable}")
    print(f"  États: {dfa_with_unreachable.states}")
    print(f"  États accessibles: {dfa_with_unreachable.get_reachable_states()}")
    
    # Optimiser
    optimized_dfa = converter.optimize_automaton(dfa_with_unreachable)
    print(f"DFA optimisé: {optimized_dfa}")
    print(f"  États: {optimized_dfa.states}")
    
    print("\n=== Démonstration terminée ===")


if __name__ == "__main__":
    main()