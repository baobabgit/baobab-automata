"""Configuration globale des tests pour Baobab Automata."""
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock

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
