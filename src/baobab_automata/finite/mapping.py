"""
Mapping pour les homomorphismes sur les langages.

Ce module implémente la classe Mapping pour gérer les transformations
d'alphabet dans les opérations d'homomorphisme sur les langages réguliers.
"""

from typing import Dict, Set
from .language.language_operations_exceptions import InvalidMappingError


class Mapping:
    """
    Classe pour gérer les mappings d'alphabet dans les homomorphismes.

    Cette classe permet de définir et valider les transformations
    d'alphabet pour les opérations d'homomorphisme et d'homomorphisme inverse.
    """

    def __init__(self, mapping: Dict[str, str]) -> None:
        """
        Initialise le mapping avec un dictionnaire de correspondances.

        :param mapping: Dictionnaire des correspondances symbole -> symbole
        :type mapping: Dict[str, str]
        :raises InvalidMappingError: Si le mapping n'est pas valide
        """
        self._mapping = mapping.copy()
        self._inverse_mapping: Dict[str, Set[str]] = {}

        if not self.validate():
            raise InvalidMappingError("Invalid mapping provided")

        self._build_inverse_mapping()

    def apply(self, symbol: str) -> str:
        """
        Applique le mapping à un symbole.

        :param symbol: Symbole à transformer
        :type symbol: str
        :return: Symbole transformé
        :rtype: str
        :raises KeyError: Si le symbole n'est pas dans le mapping
        """
        if symbol not in self._mapping:
            raise KeyError(f"Symbol '{symbol}' not found in mapping")
        return self._mapping[symbol]

    def apply_to_set(self, symbols: Set[str]) -> Set[str]:
        """
        Applique le mapping à un ensemble de symboles.

        :param symbols: Ensemble de symboles à transformer
        :type symbols: Set[str]
        :return: Ensemble des symboles transformés
        :rtype: Set[str]
        """
        result = set()
        for symbol in symbols:
            if symbol in self._mapping:
                result.add(self._mapping[symbol])
            else:
                result.add(symbol)  # Garder le symbole original s'il n'est pas mappé
        return result

    def inverse(self) -> "Mapping":
        """
        Crée le mapping inverse.

        :return: Nouveau mapping inverse
        :rtype: Mapping
        :raises InvalidMappingError: Si le mapping inverse n'est pas valide
        """
        inverse_dict = {}

        # Construire le mapping inverse
        for original, mapped in self._mapping.items():
            if mapped in inverse_dict:
                # Si plusieurs symboles mappent vers le même, on ne peut pas inverser
                raise InvalidMappingError(
                    f"Multiple symbols map to '{mapped}', cannot create inverse mapping"
                )
            inverse_dict[mapped] = original

        return Mapping(inverse_dict)

    def get_inverse_symbols(self, symbol: str) -> Set[str]:
        """
        Récupère tous les symboles qui mappent vers le symbole donné.

        :param symbol: Symbole cible
        :type symbol: str
        :return: Ensemble des symboles qui mappent vers le symbole cible
        :rtype: Set[str]
        """
        return self._inverse_mapping.get(symbol, set())

    def validate(self) -> bool:
        """
        Valide la cohérence du mapping.

        :return: True si le mapping est valide, False sinon
        :rtype: bool
        """
        if not self._mapping:
            return False

        # Vérifier que tous les symboles sont des chaînes non vides
        for original, mapped in self._mapping.items():
            if not isinstance(original, str) or not isinstance(mapped, str):
                return False
            if not original or not mapped:
                return False

        return True

    def get_domain(self) -> Set[str]:
        """
        Récupère le domaine du mapping (symboles d'origine).

        :return: Ensemble des symboles du domaine
        :rtype: Set[str]
        """
        return set(self._mapping.keys())

    def get_codomain(self) -> Set[str]:
        """
        Récupère le codomaine du mapping (symboles de destination).

        :return: Ensemble des symboles du codomaine
        :rtype: Set[str]
        """
        return set(self._mapping.values())

    def is_injective(self) -> bool:
        """
        Vérifie si le mapping est injectif (injectif = chaque symbole de destination
        a au plus un symbole source).

        :return: True si le mapping est injectif, False sinon
        :rtype: bool
        """
        return len(self._mapping) == len(set(self._mapping.values()))

    def is_surjective(self, target_alphabet: Set[str]) -> bool:
        """
        Vérifie si le mapping est surjectif sur l'alphabet cible.

        :param target_alphabet: Alphabet cible
        :type target_alphabet: Set[str]
        :return: True si le mapping est surjectif, False sinon
        :rtype: bool
        """
        codomain = self.get_codomain()
        return target_alphabet.issubset(codomain)

    def is_bijective(self, target_alphabet: Set[str]) -> bool:
        """
        Vérifie si le mapping est bijectif.

        :param target_alphabet: Alphabet cible
        :type target_alphabet: Set[str]
        :return: True si le mapping est bijectif, False sinon
        :rtype: bool
        """
        return self.is_injective() and self.is_surjective(target_alphabet)

    def to_dict(self) -> Dict[str, str]:
        """
        Convertit le mapping en dictionnaire.

        :return: Dictionnaire représentant le mapping
        :rtype: Dict[str, str]
        """
        return self._mapping.copy()

    def __len__(self) -> int:
        """
        Retourne le nombre de correspondances dans le mapping.

        :return: Nombre de correspondances
        :rtype: int
        """
        return len(self._mapping)

    def __contains__(self, symbol: str) -> bool:
        """
        Vérifie si un symbole est dans le domaine du mapping.

        :param symbol: Symbole à vérifier
        :type symbol: str
        :return: True si le symbole est dans le domaine, False sinon
        :rtype: bool
        """
        return symbol in self._mapping

    def __str__(self) -> str:
        """
        Représentation string du mapping.

        :return: Représentation string
        :rtype: str
        """
        return f"Mapping({self._mapping})"

    def __repr__(self) -> str:
        """
        Représentation détaillée du mapping.

        :return: Représentation détaillée
        :rtype: str
        """
        return f"Mapping({self._mapping!r})"

    def _build_inverse_mapping(self) -> None:
        """
        Construit le mapping inverse pour les recherches rapides.

        Cette méthode est appelée lors de l'initialisation pour construire
        un index inverse permettant de retrouver rapidement tous les symboles
        qui mappent vers un symbole donné.
        """
        for original, mapped in self._mapping.items():
            if mapped not in self._inverse_mapping:
                self._inverse_mapping[mapped] = set()
            self._inverse_mapping[mapped].add(original)
