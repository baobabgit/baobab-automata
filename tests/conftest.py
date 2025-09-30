"""
Configuration globale pour les tests pytest.

Ce module contient les fixtures et configurations communes
à tous les tests du projet Baobab Automata.
"""

import tempfile
import shutil
from pathlib import Path
from typing import Any, Dict, Generator, List
from unittest.mock import Mock

import pytest

from baobab_automata.interfaces.state import IState, StateType
from baobab_automata.interfaces.transition import ITransition, TransitionType
from baobab_automata.interfaces.automaton import IAutomaton, AutomatonType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition


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
            _source_state=sample_states["initial"],
            _target_state=sample_states["intermediate"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        ),
        "epsilon": Transition(
            _source_state=sample_states["intermediate"],
            _target_state=sample_states["final"],
            _symbol=None,
            _transition_type=TransitionType.EPSILON
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


# Fixtures de compatibilité pour les tests existants
@pytest.fixture
def sample_states_legacy() -> List[str]:
    """Fixture fournissant des états d'exemple pour les tests (legacy)."""
    return ["q0", "q1", "q2", "q3"]


@pytest.fixture
def sample_alphabet_legacy() -> List[str]:
    """Fixture fournissant un alphabet d'exemple pour les tests (legacy)."""
    return ["a", "b", "c"]


@pytest.fixture
def sample_transitions_legacy() -> Dict[tuple, str]:
    """Fixture fournissant des transitions d'exemple pour les tests (legacy)."""
    return {
        ("q0", "a"): "q1",
        ("q1", "b"): "q2",
        ("q2", "c"): "q3",
    }


@pytest.fixture
def sample_initial_state() -> str:
    """Fixture fournissant un état initial d'exemple pour les tests."""
    return "q0"


@pytest.fixture
def sample_final_states() -> List[str]:
    """Fixture fournissant des états finaux d'exemple pour les tests."""
    return ["q3"]


@pytest.fixture
def sample_strings() -> List[str]:
    """Fixture fournissant des chaînes d'exemple pour les tests."""
    return ["", "a", "ab", "abc", "abab", "invalid"]


# Configuration des marqueurs pytest
def pytest_configure(config: Any) -> None:
    """Configuration des marqueurs pytest."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "regression: Regression tests")
