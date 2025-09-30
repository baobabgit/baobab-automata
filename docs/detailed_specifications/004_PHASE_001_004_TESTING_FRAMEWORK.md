# Spécification Détaillée - Framework de Tests

## Agent IA Cible
Agent de développement spécialisé dans la création de frameworks de tests et l'implémentation de tests unitaires en Python.

## Objectif
Implémenter un framework de tests complet et robuste pour le projet Baobab Automata.

## Spécifications Techniques

### 1. Configuration de Base

#### 1.1 conftest.py
```python
"""Configuration globale des tests pour Baobab Automata."""
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock

from baobab_automata.core.interfaces import IState, ITransition, IAutomaton
from baobab_automata.core.base import State, Transition
from baobab_automata.core.exceptions import BaobabAutomataError

@pytest.fixture(scope="session")
def temp_dir() -> Generator[Path, None, None]:
    """Crée un répertoire temporaire pour les tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_states() -> Dict[str, IState]:
    """Crée des états d'exemple pour les tests."""
    return {
        "initial": State("q0", StateType.INITIAL),
        "intermediate": State("q1", StateType.INTERMEDIATE),
        "final": State("q2", StateType.FINAL),
        "accepting": State("q3", StateType.ACCEPTING),
    }

@pytest.fixture
def sample_transitions(sample_states: Dict[str, IState]) -> Dict[str, ITransition]:
    """Crée des transitions d'exemple pour les tests."""
    return {
        "symbol": Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["intermediate"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        ),
        "epsilon": Transition(
            source_state=sample_states["intermediate"],
            target_state=sample_states["final"],
            symbol=None,
            transition_type=TransitionType.EPSILON
        ),
    }

@pytest.fixture
def sample_alphabet() -> set:
    """Crée un alphabet d'exemple pour les tests."""
    return {"a", "b", "c"}

@pytest.fixture
def mock_automaton() -> Mock:
    """Crée un mock d'automate pour les tests."""
    mock = Mock(spec=IAutomaton)
    mock.automaton_type = AutomatonType.DFA
    mock.states = set()
    mock.initial_states = set()
    mock.final_states = set()
    mock.alphabet = set()
    mock.transitions = set()
    return mock
```

### 2. Tests des Interfaces

#### 2.1 Tests des États
```python
"""Tests unitaires pour les états d'automates."""
import pytest
from baobab_automata.core.interfaces import StateType
from baobab_automata.core.base import State

class TestState:
    """Tests pour la classe State."""
    
    def test_state_creation(self):
        """Test la création d'un état."""
        state = State("q0", StateType.INITIAL)
        assert state.identifier == "q0"
        assert state.state_type == StateType.INITIAL
        assert state.metadata == {}
    
    def test_state_creation_with_metadata(self):
        """Test la création d'un état avec métadonnées."""
        metadata = {"description": "Test state", "priority": 1}
        state = State("q0", StateType.INITIAL, metadata)
        assert state.metadata == metadata
    
    def test_is_initial(self):
        """Test la méthode is_initial."""
        initial_state = State("q0", StateType.INITIAL)
        non_initial_state = State("q1", StateType.INTERMEDIATE)
        
        assert initial_state.is_initial() is True
        assert non_initial_state.is_initial() is False
    
    def test_is_final(self):
        """Test la méthode is_final."""
        final_state = State("q0", StateType.FINAL)
        non_final_state = State("q1", StateType.INTERMEDIATE)
        
        assert final_state.is_final() is True
        assert non_final_state.is_final() is False
    
    def test_is_accepting(self):
        """Test la méthode is_accepting."""
        accepting_state = State("q0", StateType.ACCEPTING)
        final_state = State("q1", StateType.FINAL)
        non_accepting_state = State("q2", StateType.INTERMEDIATE)
        
        assert accepting_state.is_accepting() is True
        assert final_state.is_accepting() is True
        assert non_accepting_state.is_accepting() is False
    
    def test_equality(self):
        """Test l'égalité entre états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)
        
        assert state1 == state2
        assert state1 != state3
        assert state1 != "not_a_state"
    
    def test_hash(self):
        """Test le hash des états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)
        
        assert hash(state1) == hash(state2)
        assert hash(state1) != hash(state3)
        
        # Test dans un set
        states_set = {state1, state2, state3}
        assert len(states_set) == 2  # state1 et state2 sont identiques
    
    def test_string_representation(self):
        """Test la représentation string des états."""
        state = State("q0", StateType.INITIAL)
        assert str(state) == "State(q0)"
        assert "q0" in repr(state)
        assert "INITIAL" in repr(state)
    
    def test_metadata_operations(self):
        """Test les opérations sur les métadonnées."""
        state = State("q0", StateType.INITIAL, {"key1": "value1"})
        
        assert state.get_metadata("key1") == "value1"
        assert state.get_metadata("key2") is None
        assert state.get_metadata("key2", "default") == "default"
    
    @pytest.mark.parametrize("identifier,state_type,expected_valid", [
        ("q0", StateType.INITIAL, True),
        ("", StateType.INITIAL, False),
        ("q0", "invalid_type", False),
    ])
    def test_validation(self, identifier, state_type, expected_valid):
        """Test la validation des états."""
        if expected_valid:
            state = State(identifier, state_type)
            assert state.identifier == identifier
        else:
            with pytest.raises((ValueError, TypeError)):
                State(identifier, state_type)
```

#### 2.2 Tests des Transitions
```python
"""Tests unitaires pour les transitions d'automates."""
import pytest
from baobab_automata.core.interfaces import TransitionType
from baobab_automata.core.base import State, Transition

class TestTransition:
    """Tests pour la classe Transition."""
    
    def test_transition_creation(self, sample_states):
        """Test la création d'une transition."""
        transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        assert transition.source_state == sample_states["initial"]
        assert transition.target_state == sample_states["final"]
        assert transition.symbol == "a"
        assert transition.transition_type == TransitionType.SYMBOL
    
    def test_epsilon_transition(self, sample_states):
        """Test la création d'une transition epsilon."""
        transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol=None,
            transition_type=TransitionType.EPSILON
        )
        
        assert transition.symbol is None
        assert transition.transition_type == TransitionType.EPSILON
    
    def test_transition_with_conditions_and_actions(self, sample_states):
        """Test la création d'une transition avec conditions et actions."""
        conditions = {"stack_top": "A"}
        actions = {"stack_push": "B"}
        
        transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL,
            conditions=conditions,
            actions=actions
        )
        
        assert transition.conditions == conditions
        assert transition.actions == actions
    
    def test_is_applicable(self, sample_states):
        """Test la méthode is_applicable."""
        transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        # Test avec symbole correct
        assert transition.is_applicable("a", {}) is True
        
        # Test avec symbole incorrect
        assert transition.is_applicable("b", {}) is False
        
        # Test avec conditions
        transition_with_conditions = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL,
            conditions={"stack_top": "A"}
        )
        
        assert transition_with_conditions.is_applicable("a", {"stack_top": "A"}) is True
        assert transition_with_conditions.is_applicable("a", {"stack_top": "B"}) is False
    
    def test_execute(self, sample_states):
        """Test la méthode execute."""
        actions = {"stack_push": "B", "counter": 1}
        transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL,
            actions=actions
        )
        
        context = {"stack": ["A"]}
        new_context = transition.execute(context)
        
        assert new_context["stack_push"] == "B"
        assert new_context["counter"] == 1
        assert "stack" in new_context  # Contexte original préservé
    
    def test_equality(self, sample_states):
        """Test l'égalité entre transitions."""
        transition1 = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        transition3 = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="b",
            transition_type=TransitionType.SYMBOL
        )
        
        assert transition1 == transition2
        assert transition1 != transition3
        assert transition1 != "not_a_transition"
    
    def test_hash(self, sample_states):
        """Test le hash des transitions."""
        transition1 = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        transition3 = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="b",
            transition_type=TransitionType.SYMBOL
        )
        
        assert hash(transition1) == hash(transition2)
        assert hash(transition1) != hash(transition3)
        
        # Test dans un set
        transitions_set = {transition1, transition2, transition3}
        assert len(transitions_set) == 2  # transition1 et transition2 sont identiques
    
    def test_string_representation(self, sample_states):
        """Test la représentation string des transitions."""
        transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol="a",
            transition_type=TransitionType.SYMBOL
        )
        
        assert "q0" in str(transition)
        assert "q2" in str(transition)
        assert "a" in str(transition)
        
        # Test transition epsilon
        epsilon_transition = Transition(
            source_state=sample_states["initial"],
            target_state=sample_states["final"],
            symbol=None,
            transition_type=TransitionType.EPSILON
        )
        
        assert "ε" in str(epsilon_transition)
```

### 3. Tests des Automates

#### 3.1 Tests des DFA
```python
"""Tests unitaires pour les automates finis déterministes."""
import pytest
from baobab_automata.finite.dfa import DFA
from baobab_automata.core.interfaces import StateType, TransitionType

class TestDFA:
    """Tests pour la classe DFA."""
    
    def test_dfa_creation(self, sample_states, sample_alphabet):
        """Test la création d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        assert dfa.automaton_type == AutomatonType.DFA
        assert len(dfa.states) == 2
        assert len(dfa.initial_states) == 1
        assert len(dfa.final_states) == 1
        assert dfa.alphabet == sample_alphabet
    
    def test_add_state(self, sample_states, sample_alphabet):
        """Test l'ajout d'un état."""
        dfa = DFA(
            states=set(),
            initial_states=set(),
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        dfa.add_state(sample_states["initial"])
        assert sample_states["initial"] in dfa.states
    
    def test_remove_state(self, sample_states, sample_alphabet):
        """Test la suppression d'un état."""
        dfa = DFA(
            states={sample_states["initial"]},
            initial_states={sample_states["initial"]},
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        dfa.remove_state(sample_states["initial"])
        assert sample_states["initial"] not in dfa.states
    
    def test_add_transition(self, sample_states, sample_alphabet, sample_transitions):
        """Test l'ajout d'une transition."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        dfa.add_transition(sample_transitions["symbol"])
        assert sample_transitions["symbol"] in dfa.transitions
    
    def test_get_transitions_from(self, sample_states, sample_alphabet, sample_transitions):
        """Test la récupération des transitions partant d'un état."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]}
        )
        
        transitions = dfa.get_transitions_from(sample_states["initial"])
        assert sample_transitions["symbol"] in transitions
    
    def test_get_transitions_to(self, sample_states, sample_alphabet, sample_transitions):
        """Test la récupération des transitions arrivant à un état."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]}
        )
        
        transitions = dfa.get_transitions_to(sample_states["final"])
        assert sample_transitions["symbol"] in transitions
    
    def test_get_transitions(self, sample_states, sample_alphabet, sample_transitions):
        """Test la récupération des transitions pour un état et un symbole."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]}
        )
        
        transitions = dfa.get_transitions(sample_states["initial"], "a")
        assert sample_transitions["symbol"] in transitions
        
        transitions = dfa.get_transitions(sample_states["initial"], "b")
        assert len(transitions) == 0
    
    def test_is_valid(self, sample_states, sample_alphabet):
        """Test la validation d'un DFA."""
        # DFA valide
        valid_dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        assert valid_dfa.is_valid() is True
        
        # DFA invalide (pas d'état initial)
        invalid_dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states=set(),
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        assert invalid_dfa.is_valid() is False
    
    def test_validate(self, sample_states, sample_alphabet):
        """Test la validation détaillée d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        errors = dfa.validate()
        assert isinstance(errors, list)
    
    def test_to_dict(self, sample_states, sample_alphabet):
        """Test la sérialisation d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        data = dfa.to_dict()
        assert isinstance(data, dict)
        assert "states" in data
        assert "transitions" in data
        assert "alphabet" in data
    
    def test_from_dict(self, sample_states, sample_alphabet):
        """Test la désérialisation d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        data = dfa.to_dict()
        new_dfa = DFA.from_dict(data)
        
        assert new_dfa.states == dfa.states
        assert new_dfa.initial_states == dfa.initial_states
        assert new_dfa.final_states == dfa.final_states
        assert new_dfa.alphabet == dfa.alphabet
```

### 4. Tests de Performance

#### 4.1 Tests de Benchmark
```python
"""Tests de performance pour Baobab Automata."""
import pytest
import time
from baobab_automata.finite.dfa import DFA
from baobab_automata.core.interfaces import StateType, TransitionType

class TestPerformance:
    """Tests de performance."""
    
    @pytest.mark.performance
    def test_dfa_creation_performance(self):
        """Test la performance de création d'un DFA."""
        start_time = time.time()
        
        # Création d'un DFA avec 1000 états
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q999", StateType.FINAL)}
        alphabet = {"a", "b"}
        transitions = set()
        
        dfa = DFA(states, initial_states, final_states, alphabet, transitions)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        # Vérification que la création prend moins de 1 seconde
        assert creation_time < 1.0
        assert len(dfa.states) == 1000
    
    @pytest.mark.performance
    def test_transition_lookup_performance(self):
        """Test la performance de recherche de transitions."""
        # Création d'un DFA avec beaucoup de transitions
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q99", StateType.FINAL)}
        alphabet = {"a", "b", "c"}
        
        transitions = set()
        for i in range(99):
            for symbol in alphabet:
                transitions.add(Transition(
                    source_state=State(f"q{i}", StateType.INTERMEDIATE),
                    target_state=State(f"q{i+1}", StateType.INTERMEDIATE),
                    symbol=symbol,
                    transition_type=TransitionType.SYMBOL
                ))
        
        dfa = DFA(states, initial_states, final_states, alphabet, transitions)
        
        # Test de performance de recherche
        start_time = time.time()
        
        for _ in range(1000):
            dfa.get_transitions(State("q0", StateType.INTERMEDIATE), "a")
        
        end_time = time.time()
        lookup_time = end_time - start_time
        
        # Vérification que la recherche prend moins de 0.1 seconde
        assert lookup_time < 0.1
    
    @pytest.mark.slow
    def test_large_automaton_performance(self):
        """Test la performance avec un très gros automate."""
        # Création d'un automate avec 10000 états
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(10000)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q9999", StateType.FINAL)}
        alphabet = {"a", "b"}
        transitions = set()
        
        start_time = time.time()
        
        dfa = DFA(states, initial_states, final_states, alphabet, transitions)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        # Vérification que la création prend moins de 5 secondes
        assert creation_time < 5.0
        assert len(dfa.states) == 10000
```

### 5. Tests d'Intégration

#### 5.1 Tests de Workflow
```python
"""Tests d'intégration pour les workflows complets."""
import pytest
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.nfa import NFA
from baobab_automata.algorithms.conversion import NFAToDFAConverter
from baobab_automata.algorithms.recognition import DFARecognizer

class TestIntegration:
    """Tests d'intégration."""
    
    def test_nfa_to_dfa_conversion_workflow(self):
        """Test le workflow complet de conversion NFA vers DFA."""
        # Création d'un NFA
        nfa = NFA(...)
        
        # Conversion vers DFA
        converter = NFAToDFAConverter()
        dfa = converter.convert(nfa)
        
        # Vérification que le DFA est valide
        assert dfa.is_valid()
        
        # Test de reconnaissance
        recognizer = DFARecognizer(dfa)
        assert recognizer.recognize("test_word")
    
    def test_automaton_serialization_workflow(self):
        """Test le workflow de sérialisation/désérialisation."""
        # Création d'un automate
        dfa = DFA(...)
        
        # Sérialisation
        data = dfa.to_dict()
        
        # Désérialisation
        new_dfa = DFA.from_dict(data)
        
        # Vérification de l'égalité
        assert new_dfa.states == dfa.states
        assert new_dfa.transitions == dfa.transitions
    
    def test_validation_workflow(self):
        """Test le workflow de validation."""
        # Création d'un automate
        dfa = DFA(...)
        
        # Validation
        errors = dfa.validate()
        
        # Vérification qu'il n'y a pas d'erreurs
        assert len(errors) == 0
```

### 6. Configuration des Tests

#### 6.1 pytest.ini
```ini
[tool:pytest]
minversion = 7.0
addopts = 
    --strict-markers
    --strict-config
    --cov=baobab_automata
    --cov-report=term-missing
    --cov-report=html:docs/coverage
    --cov-report=xml:docs/coverage/coverage.xml
    --cov-fail-under=95
    --durations=10
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    slow: Slow tests
    regression: Regression tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

#### 6.2 Makefile pour les Tests
```makefile
.PHONY: test test-unit test-integration test-performance test-coverage test-all

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-performance:
	pytest -m performance

test-slow:
	pytest -m slow

test-coverage:
	pytest --cov=baobab_automata --cov-report=html:docs/coverage

test-all:
	pytest -m "unit or integration or performance"

test-watch:
	pytest-watch --runner "pytest -xvs"
```

## Critères de Validation

### 1. Couverture de Code
- [ ] Couverture >= 95% pour tous les modules
- [ ] Couverture >= 90% pour les lignes critiques
- [ ] Couverture >= 80% pour les branches
- [ ] Couverture >= 90% pour les fonctions

### 2. Types de Tests
- [ ] Tests unitaires pour toutes les classes
- [ ] Tests d'intégration pour les workflows
- [ ] Tests de performance pour les algorithmes
- [ ] Tests de régression pour les bugs

### 3. Qualité des Tests
- [ ] Tests rapides (< 1 seconde pour les tests unitaires)
- [ ] Tests déterministes (pas de dépendances externes)
- [ ] Tests isolés (pas de dépendances entre tests)
- [ ] Tests maintenables (faciles à comprendre et modifier)

### 4. Documentation
- [ ] Docstrings pour tous les tests
- [ ] Exemples d'utilisation dans les tests
- [ ] Documentation des cas de test complexes
- [ ] Guide de contribution aux tests

## Exemples d'Utilisation

### Exécution des Tests
```bash
# Tous les tests
make test

# Tests unitaires seulement
make test-unit

# Tests de performance
make test-performance

# Tests avec couverture
make test-coverage
```

### Ajout de Nouveaux Tests
```python
def test_new_feature():
    """Test d'une nouvelle fonctionnalité."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = new_feature(input_data)
    
    # Assert
    assert result is not None
    assert result.expected_property == expected_value
```

## Notes d'Implémentation

1. **Performance** : Tests optimisés pour la vitesse d'exécution
2. **Maintenabilité** : Structure claire et modulaire des tests
3. **Fiabilité** : Tests déterministes et reproductibles
4. **Documentation** : Tests auto-documentés avec des noms clairs
5. **Couverture** : Couverture complète de tous les cas de code
