from src.baobab_automata.pushdown.pda import PDA
from src.baobab_automata.pushdown.conversion_algorithms import PushdownConversionAlgorithms

# Créer un PDA simple
pda = PDA(
    states={'q0', 'q1', 'q2'},
    input_alphabet={'a', 'b'},
    stack_alphabet={'A', 'Z'},
    transitions={
        ('q0', 'a', 'Z'): {('q0', 'AZ')},
        ('q0', 'a', 'A'): {('q0', 'AA')},
        ('q0', 'b', 'A'): {('q1', '')},
        ('q1', 'b', 'A'): {('q1', '')},
        ('q1', 'b', 'Z'): {('q2', 'Z')},
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'},
    name='simple_pda',
)

# Tester la minimisation avec debug
converter = PushdownConversionAlgorithms()
used_stack_symbols = converter._get_used_stack_symbols(pda)
symbol_mapping = {symbol: chr(ord('A') + i) for i, symbol in enumerate(used_stack_symbols)}

# Créer les transitions converties
converted_transitions = {}
for (state, symbol, stack_symbol), transitions in pda._transitions.items():
    if stack_symbol in used_stack_symbols:
        new_key = (state, symbol, symbol_mapping[stack_symbol])
        new_transitions = set()
        for next_state, stack_ops in transitions:
            new_stack_ops = ''.join(symbol_mapping.get(s, s) for s in stack_ops)
            new_transitions.add((next_state, new_stack_ops))
        converted_transitions[new_key] = new_transitions

# Créer le PDA minimisé
new_stack_alphabet = set(symbol_mapping.values())

# Créer le PDA minimisé sans validation pour voir les erreurs
try:
    minimized = PDA.__new__(PDA)
    minimized._states = frozenset(pda.states)
    minimized._input_alphabet = frozenset(pda.input_alphabet)
    minimized._stack_alphabet = frozenset(new_stack_alphabet)
    minimized._transitions = converted_transitions
    minimized._initial_state = pda.initial_state
    minimized._initial_stack_symbol = symbol_mapping[pda.initial_stack_symbol]
    minimized._final_states = frozenset(pda.final_states)
    minimized._name = 'simple_pda_minimized'
    minimized._epsilon_closure_cache = {}
    minimized._reachable_states_cache = {}
    
    print('PDA minimisé créé sans validation')
    print('Validation:', minimized.validate())
    
    # Vérifier les erreurs de validation des transitions
    errors = []
    for (state, _, stack_symbol), transitions in minimized._transitions.items():
        if state not in minimized._states:
            errors.append('Transition depuis un état invalide: ' + state)
        
        if stack_symbol not in minimized._stack_alphabet:
            errors.append('Symbole de pile invalide dans la transition: ' + stack_symbol)
        
        for next_state, stack_operation in transitions:
            if next_state not in minimized._states:
                errors.append('Transition vers un état invalide: ' + next_state)
            
            # Validation de l'opération de pile
            for symbol in stack_operation:
                if symbol not in minimized._stack_alphabet:
                    errors.append('Symbole de pile invalide dans l operation: ' + symbol)
    
    print('Erreurs de validation des transitions:', errors)
    
except Exception as e:
    print('Erreur lors de la création du PDA minimisé:', e)