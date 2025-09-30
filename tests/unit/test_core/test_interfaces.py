"""
Tests unitaires pour les interfaces de base.

Ce module contient les tests pour les interfaces et classes de base
du module core.
"""

import pytest
from typing import List, Dict, Any


class TestInterfaces:
    """Tests pour les interfaces de base."""

    def test_placeholder(self) -> None:
        """Test placeholder pour valider le fonctionnement de pytest."""
        assert True

    def test_sample_states_fixture(self, sample_states) -> None:
        """Test de la fixture sample_states."""
        assert isinstance(sample_states, dict)
        assert len(sample_states) > 0
        assert "initial" in sample_states
        assert "intermediate" in sample_states
        assert "final" in sample_states
        assert "accepting" in sample_states

    def test_sample_alphabet_fixture(self, sample_alphabet) -> None:
        """Test de la fixture sample_alphabet."""
        assert isinstance(sample_alphabet, set)
        assert len(sample_alphabet) > 0
        assert all(isinstance(symbol, str) for symbol in sample_alphabet)

    def test_sample_transitions_fixture(
        self, sample_transitions
    ) -> None:
        """Test de la fixture sample_transitions."""
        assert isinstance(sample_transitions, dict)
        assert len(sample_transitions) > 0
        assert "symbol" in sample_transitions
        assert "epsilon" in sample_transitions

    def test_sample_initial_state_fixture(
        self, sample_initial_state: str
    ) -> None:
        """Test de la fixture sample_initial_state."""
        assert isinstance(sample_initial_state, str)
        assert len(sample_initial_state) > 0

    def test_sample_final_states_fixture(
        self, sample_final_states: List[str]
    ) -> None:
        """Test de la fixture sample_final_states."""
        assert isinstance(sample_final_states, list)
        assert len(sample_final_states) > 0
        assert all(isinstance(state, str) for state in sample_final_states)

    def test_sample_strings_fixture(self, sample_strings: List[str]) -> None:
        """Test de la fixture sample_strings."""
        assert isinstance(sample_strings, list)
        assert len(sample_strings) > 0
        assert all(isinstance(string, str) for string in sample_strings)