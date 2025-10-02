"""Tests unitaires pour la classe Mapping."""

import pytest
from baobab_automata.finite.mapping import Mapping
from baobab_automata.finite.language_operations_exceptions import InvalidMappingError


@pytest.mark.unit
class TestMapping:
    """Tests pour la classe Mapping."""

    def test_mapping_creation(self):
        """Test la création d'un mapping valide."""
        mapping_dict = {"a": "x", "b": "y", "c": "z"}
        mapping = Mapping(mapping_dict)
        
        assert mapping.get_domain() == {"a", "b", "c"}
        assert mapping.get_codomain() == {"x", "y", "z"}
        assert len(mapping) == 3

    def test_mapping_creation_empty(self):
        """Test la création d'un mapping vide (invalide)."""
        with pytest.raises(InvalidMappingError):
            Mapping({})

    def test_mapping_creation_invalid_types(self):
        """Test la création d'un mapping avec des types invalides."""
        with pytest.raises(InvalidMappingError):
            Mapping({1: "x"})  # Clé non-string
        
        with pytest.raises(InvalidMappingError):
            Mapping({"a": 1})  # Valeur non-string

    def test_mapping_creation_empty_strings(self):
        """Test la création d'un mapping avec des chaînes vides."""
        with pytest.raises(InvalidMappingError):
            Mapping({"": "x"})  # Clé vide
        
        with pytest.raises(InvalidMappingError):
            Mapping({"a": ""})  # Valeur vide

    def test_apply(self):
        """Test l'application du mapping à un symbole."""
        mapping = Mapping({"a": "x", "b": "y"})
        
        assert mapping.apply("a") == "x"
        assert mapping.apply("b") == "y"
        
        with pytest.raises(KeyError):
            mapping.apply("c")

    def test_apply_to_set(self):
        """Test l'application du mapping à un ensemble de symboles."""
        mapping = Mapping({"a": "x", "b": "y"})
        
        result = mapping.apply_to_set({"a", "b", "c"})
        assert result == {"x", "y", "c"}  # 'c' reste inchangé

    def test_apply_to_set_empty(self):
        """Test l'application du mapping à un ensemble vide."""
        mapping = Mapping({"a": "x"})
        result = mapping.apply_to_set(set())
        assert result == set()

    def test_inverse_mapping(self):
        """Test la création du mapping inverse."""
        mapping = Mapping({"a": "x", "b": "y"})
        inverse = mapping.inverse()
        
        assert inverse.get_domain() == {"x", "y"}
        assert inverse.get_codomain() == {"a", "b"}
        assert inverse.apply("x") == "a"
        assert inverse.apply("y") == "b"

    def test_inverse_mapping_not_injective(self):
        """Test la création du mapping inverse avec un mapping non-injectif."""
        mapping = Mapping({"a": "x", "b": "x"})  # Deux symboles mappent vers 'x'
        
        with pytest.raises(InvalidMappingError):
            mapping.inverse()

    def test_get_inverse_symbols(self):
        """Test la récupération des symboles inverses."""
        mapping = Mapping({"a": "x", "b": "x", "c": "y"})
        
        assert mapping.get_inverse_symbols("x") == {"a", "b"}
        assert mapping.get_inverse_symbols("y") == {"c"}
        assert mapping.get_inverse_symbols("z") == set()

    def test_validate(self):
        """Test la validation d'un mapping."""
        # Mapping valide
        mapping = Mapping({"a": "x"})
        assert mapping.validate() is True
        
        # Mapping invalide (vide)
        mapping._mapping = {}
        assert mapping.validate() is False

    def test_get_domain(self):
        """Test la récupération du domaine."""
        mapping = Mapping({"a": "x", "b": "y", "c": "z"})
        assert mapping.get_domain() == {"a", "b", "c"}

    def test_get_codomain(self):
        """Test la récupération du codomaine."""
        mapping = Mapping({"a": "x", "b": "y", "c": "z"})
        assert mapping.get_codomain() == {"x", "y", "z"}

    def test_is_injective(self):
        """Test si le mapping est injectif."""
        # Mapping injectif
        mapping1 = Mapping({"a": "x", "b": "y"})
        assert mapping1.is_injective() is True
        
        # Mapping non-injectif
        mapping2 = Mapping({"a": "x", "b": "x"})
        assert mapping2.is_injective() is False

    def test_is_surjective(self):
        """Test si le mapping est surjectif."""
        mapping = Mapping({"a": "x", "b": "y"})
        
        # Surjectif
        assert mapping.is_surjective({"x", "y"}) is True
        assert mapping.is_surjective({"x"}) is True
        
        # Non-surjectif
        assert mapping.is_surjective({"x", "y", "z"}) is False

    def test_is_bijective(self):
        """Test si le mapping est bijectif."""
        # Mapping bijectif
        mapping1 = Mapping({"a": "x", "b": "y"})
        assert mapping1.is_bijective({"x", "y"}) is True
        
        # Mapping non-bijectif (non-injectif)
        mapping2 = Mapping({"a": "x", "b": "x"})
        assert mapping2.is_bijective({"x"}) is False
        
        # Mapping non-bijectif (non-surjectif)
        mapping3 = Mapping({"a": "x"})
        assert mapping3.is_bijective({"x", "y"}) is False

    def test_to_dict(self):
        """Test la conversion en dictionnaire."""
        original_dict = {"a": "x", "b": "y"}
        mapping = Mapping(original_dict)
        result_dict = mapping.to_dict()
        
        assert result_dict == original_dict
        assert result_dict is not original_dict  # Copie, pas référence

    def test_len(self):
        """Test la longueur du mapping."""
        mapping = Mapping({"a": "x", "b": "y", "c": "z"})
        assert len(mapping) == 3

    def test_contains(self):
        """Test l'opérateur in."""
        mapping = Mapping({"a": "x", "b": "y"})
        
        assert "a" in mapping
        assert "b" in mapping
        assert "c" not in mapping

    def test_str(self):
        """Test la représentation string."""
        mapping = Mapping({"a": "x"})
        expected = "Mapping({'a': 'x'})"
        assert str(mapping) == expected

    def test_repr(self):
        """Test la représentation détaillée."""
        mapping = Mapping({"a": "x"})
        expected = "Mapping({'a': 'x'})"
        assert repr(mapping) == expected

    def test_mapping_immutability(self):
        """Test que le mapping interne est protégé."""
        original_dict = {"a": "x"}
        mapping = Mapping(original_dict)
        
        # Modifier le dictionnaire original ne doit pas affecter le mapping
        original_dict["b"] = "y"
        assert "b" not in mapping
        assert len(mapping) == 1

    def test_mapping_copy(self):
        """Test que le mapping fait une copie du dictionnaire."""
        original_dict = {"a": "x"}
        mapping = Mapping(original_dict)
        
        # Le dictionnaire retourné par to_dict() doit être une copie
        result_dict = mapping.to_dict()
        result_dict["b"] = "y"
        
        assert "b" not in mapping
        assert len(mapping) == 1

    def test_edge_cases(self):
        """Test des cas limites."""
        # Mapping avec un seul élément
        mapping = Mapping({"a": "x"})
        assert mapping.apply("a") == "x"
        assert mapping.is_injective() is True
        assert mapping.is_surjective({"x"}) is True
        assert mapping.is_bijective({"x"}) is True

        # Mapping avec des symboles identiques
        mapping = Mapping({"a": "a"})
        assert mapping.apply("a") == "a"
        assert mapping.is_injective() is True

    def test_complex_mapping(self):
        """Test avec un mapping complexe."""
        mapping_dict = {
            "a": "alpha",
            "b": "beta", 
            "c": "gamma",
            "d": "delta"
        }
        mapping = Mapping(mapping_dict)
        
        assert len(mapping) == 4
        assert mapping.get_domain() == {"a", "b", "c", "d"}
        assert mapping.get_codomain() == {"alpha", "beta", "gamma", "delta"}
        assert mapping.is_injective() is True
        assert mapping.is_surjective({"alpha", "beta", "gamma", "delta"}) is True
        assert mapping.is_bijective({"alpha", "beta", "gamma", "delta"}) is True

    def test_apply_to_set_with_mixed_symbols(self):
        """Test l'application à un ensemble avec des symboles mappés et non-mappés."""
        mapping = Mapping({"a": "x", "b": "y"})
        symbols = {"a", "b", "c", "d"}
        result = mapping.apply_to_set(symbols)
        
        assert result == {"x", "y", "c", "d"}