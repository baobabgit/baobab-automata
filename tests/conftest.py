"""
Configuration globale pour les tests pytest.

Ce module contient les fixtures et configurations communes
à tous les tests du projet Baobab Automata.
"""

from typing import Any, Dict, List

import pytest


@pytest.fixture
def sample_states() -> List[str]:
    """Fixture fournissant des états d'exemple pour les tests."""
    return ["q0", "q1", "q2", "q3"]


@pytest.fixture
def sample_alphabet() -> List[str]:
    """Fixture fournissant un alphabet d'exemple pour les tests."""
    return ["a", "b", "c"]


@pytest.fixture
def sample_transitions() -> Dict[tuple, str]:
    """Fixture fournissant des transitions d'exemple pour les tests."""
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
