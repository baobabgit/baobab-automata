# Spécification Détaillée - Système de Validation

## Agent IA Cible
Agent de développement spécialisé dans la validation de données et la gestion d'erreurs en Python.

## Objectif
Implémenter un système de validation robuste pour tous les composants du projet Baobab Automata.

## Spécifications Techniques

### 1. Interface IValidator

#### 1.1 Définition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum

class ValidationLevel(Enum):
    """Niveaux de validation."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class ValidationResult:
    """Résultat d'une validation."""
    
    def __init__(self, is_valid: bool, errors: List[str], warnings: List[str], info: List[str]):
        self.is_valid = is_valid
        self.errors = errors
        self.warnings = warnings
        self.info = info
    
    def add_error(self, message: str) -> None:
        """Ajoute une erreur."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """Ajoute un avertissement."""
        self.warnings.append(message)
    
    def add_info(self, message: str) -> None:
        """Ajoute une information."""
        self.info.append(message)
    
    def get_messages(self, level: ValidationLevel) -> List[str]:
        """Récupère les messages d'un niveau donné."""
        if level == ValidationLevel.ERROR:
            return self.errors
        elif level == ValidationLevel.WARNING:
            return self.warnings
        else:
            return self.info
    
    def __str__(self) -> str:
        """Représentation string du résultat."""
        messages = []
        if self.errors:
            messages.append(f"Errors: {', '.join(self.errors)}")
        if self.warnings:
            messages.append(f"Warnings: {', '.join(self.warnings)}")
        if self.info:
            messages.append(f"Info: {', '.join(self.info)}")
        return "; ".join(messages)

class IValidator(ABC):
    """Interface abstraite pour les validateurs."""
    
    @abstractmethod
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Valide des données."""
        pass
    
    @abstractmethod
    def can_validate(self, data: Any) -> bool:
        """Vérifie si le validateur peut valider les données."""
        pass
    
    @abstractmethod
    def get_validation_rules(self) -> Dict[str, Any]:
        """Retourne les règles de validation."""
        pass
```

### 2. Validateur d'États

#### 2.1 Implémentation
```python
from typing import Any, Dict, List, Optional
import re

class StateValidator(IValidator):
    """Validateur pour les états d'automates."""
    
    def __init__(self):
        self.identifier_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
        self.max_identifier_length = 100
    
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Valide un état."""
        result = ValidationResult(True, [], [], [])
        
        if not isinstance(data, IState):
            result.add_error("Data must be an IState instance")
            return result
        
        # Validation de l'identifiant
        self._validate_identifier(data.identifier, result)
        
        # Validation du type d'état
        self._validate_state_type(data.state_type, result)
        
        # Validation des métadonnées
        self._validate_metadata(data.metadata, result)
        
        return result
    
    def can_validate(self, data: Any) -> bool:
        """Vérifie si le validateur peut valider les données."""
        return isinstance(data, IState)
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Retourne les règles de validation."""
        return {
            "identifier_pattern": self.identifier_pattern.pattern,
            "max_identifier_length": self.max_identifier_length,
            "required_state_type": "StateType enum value",
            "metadata_type": "Dict[str, Any]"
        }
    
    def _validate_identifier(self, identifier: str, result: ValidationResult) -> None:
        """Valide l'identifiant de l'état."""
        if not identifier:
            result.add_error("State identifier cannot be empty")
            return
        
        if len(identifier) > self.max_identifier_length:
            result.add_error(f"State identifier too long (max {self.max_identifier_length} characters)")
        
        if not self.identifier_pattern.match(identifier):
            result.add_error("State identifier must match pattern: ^[a-zA-Z_][a-zA-Z0-9_]*$")
    
    def _validate_state_type(self, state_type: StateType, result: ValidationResult) -> None:
        """Valide le type d'état."""
        if not isinstance(state_type, StateType):
            result.add_error("State type must be a StateType enum value")
    
    def _validate_metadata(self, metadata: Dict[str, Any], result: ValidationResult) -> None:
        """Valide les métadonnées de l'état."""
        if not isinstance(metadata, dict):
            result.add_error("State metadata must be a dictionary")
            return
        
        for key, value in metadata.items():
            if not isinstance(key, str):
                result.add_error("Metadata keys must be strings")
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                result.add_warning(f"Metadata value for key '{key}' has unexpected type: {type(value)}")
```

### 3. Validateur de Transitions

#### 3.1 Implémentation
```python
class TransitionValidator(IValidator):
    """Validateur pour les transitions d'automates."""
    
    def __init__(self):
        self.max_symbol_length = 10
        self.allowed_symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Valide une transition."""
        result = ValidationResult(True, [], [], [])
        
        if not isinstance(data, ITransition):
            result.add_error("Data must be an ITransition instance")
            return result
        
        # Validation des états
        self._validate_states(data.source_state, data.target_state, result)
        
        # Validation du symbole
        self._validate_symbol(data.symbol, result)
        
        # Validation du type de transition
        self._validate_transition_type(data.transition_type, result)
        
        # Validation des conditions et actions
        self._validate_conditions(data.conditions, result)
        self._validate_actions(data.actions, result)
        
        return result
    
    def can_validate(self, data: Any) -> bool:
        """Vérifie si le validateur peut valider les données."""
        return isinstance(data, ITransition)
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Retourne les règles de validation."""
        return {
            "max_symbol_length": self.max_symbol_length,
            "allowed_symbols": list(self.allowed_symbols),
            "required_transition_type": "TransitionType enum value",
            "conditions_type": "Dict[str, Any]",
            "actions_type": "Dict[str, Any]"
        }
    
    def _validate_states(self, source: IState, target: IState, result: ValidationResult) -> None:
        """Valide les états source et cible."""
        if not isinstance(source, IState):
            result.add_error("Source state must be an IState instance")
        
        if not isinstance(target, IState):
            result.add_error("Target state must be an IState instance")
        
        if source == target:
            result.add_warning("Self-transitions are allowed but may indicate design issues")
    
    def _validate_symbol(self, symbol: Optional[str], result: ValidationResult) -> None:
        """Valide le symbole de la transition."""
        if symbol is None:
            result.add_info("Epsilon transition detected")
            return
        
        if not isinstance(symbol, str):
            result.add_error("Symbol must be a string or None")
            return
        
        if len(symbol) > self.max_symbol_length:
            result.add_error(f"Symbol too long (max {self.max_symbol_length} characters)")
        
        if not all(c in self.allowed_symbols for c in symbol):
            result.add_warning(f"Symbol contains non-standard characters: {symbol}")
    
    def _validate_transition_type(self, transition_type: TransitionType, result: ValidationResult) -> None:
        """Valide le type de transition."""
        if not isinstance(transition_type, TransitionType):
            result.add_error("Transition type must be a TransitionType enum value")
    
    def _validate_conditions(self, conditions: Dict[str, Any], result: ValidationResult) -> None:
        """Valide les conditions de la transition."""
        if not isinstance(conditions, dict):
            result.add_error("Transition conditions must be a dictionary")
            return
        
        for key, value in conditions.items():
            if not isinstance(key, str):
                result.add_error("Condition keys must be strings")
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                result.add_warning(f"Condition value for key '{key}' has unexpected type: {type(value)}")
    
    def _validate_actions(self, actions: Dict[str, Any], result: ValidationResult) -> None:
        """Valide les actions de la transition."""
        if not isinstance(actions, dict):
            result.add_error("Transition actions must be a dictionary")
            return
        
        for key, value in actions.items():
            if not isinstance(key, str):
                result.add_error("Action keys must be strings")
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                result.add_warning(f"Action value for key '{key}' has unexpected type: {type(value)}")
```

### 4. Validateur d'Automates

#### 4.1 Implémentation
```python
class AutomatonValidator(IValidator):
    """Validateur pour les automates."""
    
    def __init__(self):
        self.state_validator = StateValidator()
        self.transition_validator = TransitionValidator()
    
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Valide un automate."""
        result = ValidationResult(True, [], [], [])
        
        if not isinstance(data, IAutomaton):
            result.add_error("Data must be an IAutomaton instance")
            return result
        
        # Validation des états
        self._validate_states(data, result)
        
        # Validation des transitions
        self._validate_transitions(data, result)
        
        # Validation de la cohérence
        self._validate_consistency(data, result)
        
        # Validation des propriétés spécifiques
        self._validate_specific_properties(data, result)
        
        return result
    
    def can_validate(self, data: Any) -> bool:
        """Vérifie si le validateur peut valider les données."""
        return isinstance(data, IAutomaton)
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Retourne les règles de validation."""
        return {
            "min_states": 1,
            "max_states": 100000,
            "min_transitions": 0,
            "max_transitions": 1000000,
            "required_initial_states": "At least one initial state",
            "required_final_states": "At least one final state for recognition",
            "alphabet_consistency": "All transition symbols must be in alphabet"
        }
    
    def _validate_states(self, automaton: IAutomaton, result: ValidationResult) -> None:
        """Valide les états de l'automate."""
        if not automaton.states:
            result.add_error("Automaton must have at least one state")
            return
        
        if len(automaton.states) > 100000:
            result.add_error("Automaton has too many states (max 100000)")
        
        # Validation de chaque état
        for state in automaton.states:
            state_result = self.state_validator.validate(state)
            if not state_result.is_valid:
                result.add_error(f"Invalid state {state.identifier}: {state_result}")
        
        # Validation des états initiaux
        if not automaton.initial_states:
            result.add_error("Automaton must have at least one initial state")
        
        # Validation des états finaux
        if not automaton.final_states:
            result.add_warning("Automaton has no final states - may not recognize any words")
        
        # Vérification que les états initiaux et finaux sont dans l'ensemble des états
        for state in automaton.initial_states:
            if state not in automaton.states:
                result.add_error(f"Initial state {state.identifier} not in states set")
        
        for state in automaton.final_states:
            if state not in automaton.states:
                result.add_error(f"Final state {state.identifier} not in states set")
    
    def _validate_transitions(self, automaton: IAutomaton, result: ValidationResult) -> None:
        """Valide les transitions de l'automate."""
        if len(automaton.transitions) > 1000000:
            result.add_error("Automaton has too many transitions (max 1000000)")
        
        # Validation de chaque transition
        for transition in automaton.transitions:
            transition_result = self.transition_validator.validate(transition)
            if not transition_result.is_valid:
                result.add_error(f"Invalid transition: {transition_result}")
        
        # Vérification que les états des transitions sont dans l'ensemble des états
        for transition in automaton.transitions:
            if transition.source_state not in automaton.states:
                result.add_error(f"Transition source state {transition.source_state.identifier} not in states set")
            if transition.target_state not in automaton.states:
                result.add_error(f"Transition target state {transition.target_state.identifier} not in states set")
    
    def _validate_consistency(self, automaton: IAutomaton, result: ValidationResult) -> None:
        """Valide la cohérence de l'automate."""
        # Vérification de la cohérence de l'alphabet
        transition_symbols = set()
        for transition in automaton.transitions:
            if transition.symbol is not None:
                transition_symbols.add(transition.symbol)
        
        alphabet_symbols = automaton.alphabet
        if not transition_symbols.issubset(alphabet_symbols):
            extra_symbols = transition_symbols - alphabet_symbols
            result.add_error(f"Transition symbols not in alphabet: {extra_symbols}")
        
        if not alphabet_symbols.issubset(transition_symbols):
            unused_symbols = alphabet_symbols - transition_symbols
            result.add_warning(f"Unused alphabet symbols: {unused_symbols}")
    
    def _validate_specific_properties(self, automaton: IAutomaton, result: ValidationResult) -> None:
        """Valide les propriétés spécifiques au type d'automate."""
        # Validation spécifique selon le type d'automate
        if automaton.automaton_type == AutomatonType.DFA:
            self._validate_dfa_properties(automaton, result)
        elif automaton.automaton_type == AutomatonType.NFA:
            self._validate_nfa_properties(automaton, result)
        # Ajouter d'autres types d'automates selon les besoins
    
    def _validate_dfa_properties(self, automaton: IAutomaton, result: ValidationResult) -> None:
        """Valide les propriétés spécifiques aux DFA."""
        # Vérification du déterminisme
        for state in automaton.states:
            for symbol in automaton.alphabet:
                transitions = automaton.get_transitions(state, symbol)
                if len(transitions) > 1:
                    result.add_error(f"DFA violation: multiple transitions from {state.identifier} on symbol '{symbol}'")
                elif len(transitions) == 0:
                    result.add_warning(f"DFA has no transition from {state.identifier} on symbol '{symbol}'")
    
    def _validate_nfa_properties(self, automaton: IAutomaton, result: ValidationResult) -> None:
        """Valide les propriétés spécifiques aux NFA."""
        # Vérification des transitions epsilon
        epsilon_transitions = [t for t in automaton.transitions if t.symbol is None]
        if epsilon_transitions:
            result.add_info(f"NFA has {len(epsilon_transitions)} epsilon transitions")
```

### 5. Gestionnaire de Validation

#### 5.1 Implémentation
```python
from typing import Any, Dict, List, Optional, Type

class ValidationManager:
    """Gestionnaire centralisé de validation."""
    
    def __init__(self):
        self.validators: Dict[Type, IValidator] = {}
        self._register_default_validators()
    
    def _register_default_validators(self) -> None:
        """Enregistre les validateurs par défaut."""
        self.validators[IState] = StateValidator()
        self.validators[ITransition] = TransitionValidator()
        self.validators[IAutomaton] = AutomatonValidator()
    
    def register_validator(self, data_type: Type, validator: IValidator) -> None:
        """Enregistre un validateur pour un type de données."""
        self.validators[data_type] = validator
    
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Valide des données en utilisant le validateur approprié."""
        data_type = type(data)
        
        # Recherche du validateur approprié
        validator = self.validators.get(data_type)
        if validator is None:
            # Recherche dans les classes parentes
            for parent_type in data_type.__mro__:
                if parent_type in self.validators:
                    validator = self.validators[parent_type]
                    break
        
        if validator is None:
            return ValidationResult(False, [f"No validator found for type {data_type}"], [], [])
        
        return validator.validate(data, context)
    
    def validate_all(self, data_list: List[Any], context: Optional[Dict[str, Any]] = None) -> List[ValidationResult]:
        """Valide une liste de données."""
        return [self.validate(data, context) for data in data_list]
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, int]:
        """Retourne un résumé des résultats de validation."""
        total = len(results)
        valid = sum(1 for r in results if r.is_valid)
        errors = sum(len(r.errors) for r in results)
        warnings = sum(len(r.warnings) for r in results)
        info = sum(len(r.info) for r in results)
        
        return {
            "total": total,
            "valid": valid,
            "invalid": total - valid,
            "errors": errors,
            "warnings": warnings,
            "info": info
        }
```

## Critères de Validation

### 1. Fonctionnalité
- [ ] Tous les validateurs implémentent l'interface IValidator
- [ ] Validation des états, transitions et automates
- [ ] Gestion des erreurs, avertissements et informations
- [ ] Validation contextuelle

### 2. Performance
- [ ] Validation rapide pour les petits automates
- [ ] Validation efficace pour les gros automates
- [ ] Gestion de la mémoire optimisée
- [ ] Cache des résultats de validation

### 3. Qualité
- [ ] Code formaté avec Black
- [ ] Score Pylint >= 8.5/10
- [ ] Pas d'erreurs Flake8
- [ ] Pas de vulnérabilités Bandit
- [ ] Types validés avec MyPy

### 4. Tests
- [ ] Tests unitaires pour tous les validateurs
- [ ] Tests de performance
- [ ] Tests de cas limites
- [ ] Couverture de code >= 95%

## Exemples d'Utilisation

### Validation d'un État
```python
# Création d'un état
state = State("q0", StateType.INITIAL)

# Validation
validator = StateValidator()
result = validator.validate(state)

if result.is_valid:
    print("État valide")
else:
    print(f"Erreurs: {result.errors}")
```

### Validation d'un Automate
```python
# Création d'un automate
automaton = DFA(...)

# Validation
validator = AutomatonValidator()
result = validator.validate(automaton)

if result.is_valid:
    print("Automate valide")
else:
    print(f"Erreurs: {result.errors}")
    print(f"Avertissements: {result.warnings}")
```

### Utilisation du Gestionnaire
```python
# Création du gestionnaire
manager = ValidationManager()

# Validation
result = manager.validate(automaton)

# Validation multiple
results = manager.validate_all([state1, state2, transition1])

# Résumé
summary = manager.get_validation_summary(results)
print(f"Total: {summary['total']}, Valides: {summary['valid']}")
```

## Notes d'Implémentation

1. **Performance** : Validation optimisée pour les gros volumes
2. **Extensibilité** : Facile d'ajouter de nouveaux validateurs
3. **Flexibilité** : Validation contextuelle et configurable
4. **Robustesse** : Gestion d'erreurs complète
5. **Documentation** : Messages d'erreur clairs et informatifs
