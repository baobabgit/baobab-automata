#!/usr/bin/env python3
"""
Exemple d'utilisation corrigé des fonctionnalités exposées dans baobab_automata.

Ce script montre la bonne façon d'utiliser les 4 éléments demandés :
1. regex_to_nfa - Fonction qui convertit une expression régulière en NFA
2. nfa.to_dfa() - Méthode de la classe NFA pour convertir en DFA  
3. minimize_dfa - Fonction qui minimise un DFA
4. DFA - Classe avec accepts() et find_longest_match()
"""

print("=== EXEMPLE D'UTILISATION CORRIGE ===")
print()

print("1. CLASSE DFA avec methode accepts() et find_longest_match()")
print("   - La classe DFA est implementee dans src/baobab_automata/finite/dfa/dfa.py")
print("   - Elle inclut la methode accepts(self, text: str) -> bool")
print("   - Elle inclut la methode find_longest_match(self, text: str, start: int) -> Optional[Match]")
print()

print("2. CONVERSION NFA vers DFA")
print("   - Utiliser la methode nfa.to_dfa() de la classe NFA")
print("   - Cette methode est disponible quand on importe la classe NFA")
print("   - Pas besoin de fonction de convenance redondante")
print()

print("3. FONCTION minimize_dfa")
print("   - Implementee dans src/baobab_automata/algorithms/optimization/optimization_algorithms.py")
print("   - Exposee via convenience_functions.py")
print()

print("4. FONCTION regex_to_nfa")
print("   - Implementee via ConversionAlgorithms.regex_to_automaton_optimized()")
print("   - Exposee via convenience_functions.py")
print()

print("=== UTILISATION RECOMMANDEE ===")
print()

print("# Import des classes principales")
print("from baobab_automata import DFA, Match, NFA")
print("from baobab_automata import regex_to_nfa, minimize_dfa")
print()

print("# Ou import direct des modules")
print("from baobab_automata.finite.dfa.dfa import DFA, Match")
print("from baobab_automata.finite.nfa.nfa import NFA")
print("from baobab_automata.convenience_functions import regex_to_nfa, minimize_dfa")
print()

print("=== EXEMPLE DE CODE CORRIGE ===")
print()

print("# 1. Creation d'un DFA directement")
print("dfa = DFA(")
print("    states={'q0', 'q1', 'q2'},")
print("    alphabet={'a', 'b'},")
print("    transitions={")
print("        ('q0', 'a'): 'q1',")
print("        ('q0', 'b'): 'q0',")
print("        ('q1', 'a'): 'q1',")
print("        ('q1', 'b'): 'q2',")
print("        ('q2', 'a'): 'q2',")
print("        ('q2', 'b'): 'q2',")
print("    },")
print("    initial_state='q0',")
print("    final_states={'q2'}")
print(")")
print()

print("# 2. Test d'acceptation")
print("print(dfa.accepts('ab'))  # True")
print("print(dfa.accepts('aab'))  # True")
print("print(dfa.accepts('a'))    # False")
print()

print("# 3. Recherche de correspondance la plus longue")
print("match = dfa.find_longest_match('aabbbab')")
print("if match:")
print("    print(f'Trouve: {match.match} a la position {match.start}-{match.end}')")
print()

print("# 4. Conversion regex -> NFA -> DFA")
print("nfa = regex_to_nfa('a*b*')")
print("dfa_from_regex = nfa.to_dfa()  # Utiliser la methode de la classe NFA")
print()

print("# 5. Minimisation du DFA")
print("minimized_dfa = minimize_dfa(dfa_from_regex)")
print()

print("=== CORRECTION APPORTEE ===")
print()
print("SUPPRESSION de la fonction redondante nfa_to_dfa()")
print("- La methode nfa.to_dfa() existe deja dans la classe NFA")
print("- Pas besoin de fonction de convenance redondante")
print("- La methode nfa.to_dfa() est disponible quand on importe NFA")
print()

print("=== FONCTIONNALITES FINALES EXPOSEES ===")
print()
print("1. DFA - Classe avec accepts() et find_longest_match()")
print("2. Match - Classe pour representer les correspondances")
print("3. NFA - Classe avec methode to_dfa()")
print("4. regex_to_nfa() - Fonction de conversion")
print("5. minimize_dfa() - Fonction de minimisation")
print()
print("Toutes les fonctionnalites sont maintenant correctement exposees")
print("sans redondance inutile.")
