"""
Tests unitaires pour la classe Mapping.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
de la classe Mapping selon les spécifications détaillées.
"""

import unittest

from baobab_automata.finite.language_operations_exceptions import InvalidMappingError
from baobab_automata.finite.mapping import Mapping


class TestMapping(unittest.TestCase):
    """Tests unitaires pour la classe Mapping."""

    def setUp(self):
        """Configuration des tests."""
        self.valid_mapping = {"a": "x", "b": "y", "c": "z"}
        self.mapping = Mapping(self.valid_mapping)

    def test_mapping_construction_valid(self):
        """Test de construction d'un mapping valide."""
        mapping = Mapping({"a": "x", "b": "y"})
        self.assertEqual(mapping._mapping, {"a": "x", "b": "y"})
        self.assertTrue(mapping.validate())

    def test_mapping_construction_invalid_empty(self):
        """Test de construction d'un mapping vide (invalide)."""
        with self.assertRaises(InvalidMappingError):
            Mapping({})

    def test_mapping_construction_invalid_non_string(self):
        """Test de construction d'un mapping avec des clés/valeurs non-string."""
        with self.assertRaises(InvalidMappingError):
            Mapping({"a": 1, "b": "y"})

        with self.assertRaises(InvalidMappingError):
            Mapping({1: "x", "b": "y"})

    def test_mapping_construction_invalid_empty_strings(self):
        """Test de construction d'un mapping avec des chaînes vides."""
        with self.assertRaises(InvalidMappingError):
            Mapping({"": "x", "b": "y"})

        with self.assertRaises(InvalidMappingError):
            Mapping({"a": "", "b": "y"})

    def test_apply_valid_symbol(self):
        """Test d'application du mapping à un symbole valide."""
        result = self.mapping.apply("a")
        self.assertEqual(result, "x")

        result = self.mapping.apply("b")
        self.assertEqual(result, "y")

    def test_apply_invalid_symbol(self):
        """Test d'application du mapping à un symbole invalide."""
        with self.assertRaises(KeyError):
            self.mapping.apply("d")

    def test_apply_to_set(self):
        """Test d'application du mapping à un ensemble de symboles."""
        symbols = {"a", "b", "d"}  # 'd' n'est pas dans le mapping
        result = self.mapping.apply_to_set(symbols)
        expected = {"x", "y", "d"}  # 'd' reste inchangé
        self.assertEqual(result, expected)

    def test_inverse_valid(self):
        """Test de création du mapping inverse valide."""
        inverse = self.mapping.inverse()
        expected = {"x": "a", "y": "b", "z": "c"}
        self.assertEqual(inverse._mapping, expected)

    def test_inverse_invalid_multiple_mappings(self):
        """Test de création du mapping inverse avec mappings multiples."""
        mapping = Mapping({"a": "x", "b": "x"})  # Deux symboles mappent vers 'x'
        with self.assertRaises(InvalidMappingError):
            mapping.inverse()

    def test_get_inverse_symbols(self):
        """Test de récupération des symboles inverses."""
        # Construire le mapping inverse manuellement pour le test
        inverse_symbols = self.mapping.get_inverse_symbols("x")
        self.assertEqual(inverse_symbols, {"a"})

        inverse_symbols = self.mapping.get_inverse_symbols("w")  # Symbole non mappé
        self.assertEqual(inverse_symbols, set())

    def test_validate(self):
        """Test de validation du mapping."""
        self.assertTrue(self.mapping.validate())

        # Test avec un mapping invalide
        invalid_mapping = Mapping({"a": "x"})
        invalid_mapping._mapping = {}  # Rendre vide
        self.assertFalse(invalid_mapping.validate())

    def test_get_domain(self):
        """Test de récupération du domaine."""
        domain = self.mapping.get_domain()
        expected = {"a", "b", "c"}
        self.assertEqual(domain, expected)

    def test_get_codomain(self):
        """Test de récupération du codomaine."""
        codomain = self.mapping.get_codomain()
        expected = {"x", "y", "z"}
        self.assertEqual(codomain, expected)

    def test_is_injective(self):
        """Test de vérification d'injectivité."""
        # Le mapping de test est injectif
        self.assertTrue(self.mapping.is_injective())

        # Test avec un mapping non injectif
        non_injective = Mapping({"a": "x", "b": "x"})
        self.assertFalse(non_injective.is_injective())

    def test_is_surjective(self):
        """Test de vérification de surjectivité."""
        target_alphabet = {"x", "y", "z"}
        self.assertTrue(self.mapping.is_surjective(target_alphabet))

        target_alphabet = {"x", "y", "z", "w"}
        self.assertFalse(self.mapping.is_surjective(target_alphabet))

    def test_is_bijective(self):
        """Test de vérification de bijectivité."""
        target_alphabet = {"x", "y", "z"}
        self.assertTrue(self.mapping.is_bijective(target_alphabet))

        target_alphabet = {"x", "y", "z", "w"}
        self.assertFalse(self.mapping.is_bijective(target_alphabet))

    def test_to_dict(self):
        """Test de conversion en dictionnaire."""
        result = self.mapping.to_dict()
        self.assertEqual(result, self.valid_mapping)
        # Vérifier que c'est une copie
        self.assertIsNot(result, self.valid_mapping)

    def test_len(self):
        """Test de la longueur du mapping."""
        self.assertEqual(len(self.mapping), 3)

    def test_contains(self):
        """Test de l'opérateur in."""
        self.assertIn("a", self.mapping)
        self.assertNotIn("d", self.mapping)

    def test_str(self):
        """Test de la représentation string."""
        str_repr = str(self.mapping)
        self.assertIn("Mapping", str_repr)
        self.assertIn("a", str_repr)

    def test_repr(self):
        """Test de la représentation détaillée."""
        repr_str = repr(self.mapping)
        self.assertIn("Mapping", repr_str)
        self.assertIn("a", repr_str)

    def test_build_inverse_mapping(self):
        """Test de construction du mapping inverse interne."""
        # Vérifier que le mapping inverse interne est construit correctement
        self.assertIn("x", self.mapping._inverse_mapping)
        self.assertIn("y", self.mapping._inverse_mapping)
        self.assertIn("z", self.mapping._inverse_mapping)

        self.assertEqual(self.mapping._inverse_mapping["x"], {"a"})
        self.assertEqual(self.mapping._inverse_mapping["y"], {"b"})
        self.assertEqual(self.mapping._inverse_mapping["z"], {"c"})


if __name__ == "__main__":
    unittest.main()
