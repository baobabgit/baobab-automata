# Spécifications Détaillées - Phase 003.004 - Implémentation du Parser de Grammaires Hors-Contexte

## Vue d'ensemble

Cette spécification détaille l'implémentation du parser de grammaires hors-contexte (Context-Free Grammar - CFG) pour la conversion bidirectionnelle entre grammaires et automates à pile. Le parser permet de créer des automates à partir de grammaires et vice versa.

## Objectifs

- Implémenter un parser complet de grammaires hors-contexte
- Fournir des conversions bidirectionnelles grammaire ↔ PDA
- Valider et optimiser les grammaires
- Détecter et éliminer les productions vides
- Normaliser les grammaires (forme normale de Chomsky, forme normale de Greibach)

## Architecture

### Classe principale : GrammarParser

```python
class GrammarParser:
    """Parser de grammaires hors-contexte avec conversions vers/depuis les automates à pile."""
```

### Structure des grammaires

- **Variables** : Symboles non-terminaux
- **Terminaux** : Symboles terminaux
- **Productions** : Règles de réécriture
- **Symbole de départ** : Variable de départ

## Spécifications détaillées

### 1. Classes de support

#### 1.1 Représentation des grammaires

```python
@dataclass(frozen=True)
class Production:
    """Représente une production d'une grammaire."""
    left_side: str  # Variable de gauche
    right_side: List[str]  # Séquence de symboles de droite
    
@dataclass(frozen=True)
class ContextFreeGrammar:
    """Représente une grammaire hors-contexte."""
    variables: Set[str]  # Symboles non-terminaux
    terminals: Set[str]  # Symboles terminaux
    productions: Set[Production]  # Règles de production
    start_symbol: str  # Symbole de départ
    name: Optional[str] = None  # Nom optionnel
```

#### 1.2 Types de grammaires

```python
class GrammarType(Enum):
    """Types de grammaires supportés."""
    GENERAL = "general"
    CHOMSKY_NORMAL_FORM = "chomsky_normal_form"
    GREIBACH_NORMAL_FORM = "greibach_normal_form"
    LEFT_RECURSIVE = "left_recursive"
    RIGHT_RECURSIVE = "right_recursive"
    AMBIGUOUS = "ambiguous"
```

### 2. Constructeur et initialisation

#### 2.1 Constructeur principal

```python
def __init__(
    self,
    grammar: Optional[ContextFreeGrammar] = None,
    strict_validation: bool = True
) -> None:
    """Initialise le parser de grammaires.
    
    :param grammar: Grammaire optionnelle à parser
    :param strict_validation: Validation stricte des grammaires
    :raises GrammarError: Si la grammaire n'est pas valide
    """
```

#### 2.2 Chargement de grammaires

```python
def load_grammar(self, grammar: ContextFreeGrammar) -> None:
    """Charge une grammaire dans le parser.
    
    :param grammar: Grammaire à charger
    :raises GrammarError: Si la grammaire n'est pas valide
    """

def load_from_string(self, grammar_string: str) -> None:
    """Charge une grammaire depuis une chaîne de caractères.
    
    :param grammar_string: Représentation textuelle de la grammaire
    :raises GrammarError: Si la grammaire n'est pas valide
    """

def load_from_file(self, file_path: str) -> None:
    """Charge une grammaire depuis un fichier.
    
    :param file_path: Chemin vers le fichier
    :raises GrammarError: Si la grammaire n'est pas valide
    """
```

### 3. Parsing et validation

#### 3.1 Parsing de grammaires

```python
def parse_grammar(self, grammar_string: str) -> ContextFreeGrammar:
    """Parse une grammaire depuis une chaîne de caractères.
    
    :param grammar_string: Représentation textuelle de la grammaire
    :return: Grammaire parsée
    :raises GrammarParseError: Si le parsing échoue
    """
```

**Format supporté :**
```
S -> aSb | ε
A -> aA | b
B -> bB | a
```

#### 3.2 Validation des grammaires

```python
def validate_grammar(self, grammar: ContextFreeGrammar) -> bool:
    """Valide une grammaire.
    
    :param grammar: Grammaire à valider
    :return: True si la grammaire est valide, False sinon
    :raises GrammarError: Si la grammaire n'est pas valide
    """
```

**Critères de validation :**
- Toutes les variables référencées existent
- Tous les terminaux sont définis
- Le symbole de départ existe
- Les productions sont cohérentes
- Aucune production vide sauf pour le symbole de départ

#### 3.3 Analyse des propriétés

```python
def analyze_grammar(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
    """Analyse les propriétés d'une grammaire.
    
    :param grammar: Grammaire à analyser
    :return: Dictionnaire avec les propriétés de la grammaire
    """
```

**Propriétés analysées :**
- Type de grammaire
- Récursivité gauche/droite
- Ambiguïté
- Productions vides
- Symboles inaccessibles
- Symboles non-générateurs

### 4. Conversions grammaire ↔ PDA

#### 4.1 Conversion grammaire → PDA

```python
def grammar_to_pda(self, grammar: ContextFreeGrammar) -> PDA:
    """Convertit une grammaire en PDA.
    
    :param grammar: Grammaire à convertir
    :return: PDA équivalent
    :raises GrammarConversionError: Si la conversion échoue
    """
```

**Algorithme de conversion :**
1. Création des états du PDA
2. Ajout des transitions pour chaque production
3. Gestion des productions vides
4. Configuration de l'état initial et final

#### 4.2 Conversion PDA → grammaire

```python
def pda_to_grammar(self, pda: PDA) -> ContextFreeGrammar:
    """Convertit un PDA en grammaire.
    
    :param pda: PDA à convertir
    :return: Grammaire équivalente
    :raises GrammarConversionError: Si la conversion échoue
    """
```

**Algorithme de conversion :**
1. Création des variables pour chaque paire d'états
2. Ajout des productions pour chaque transition
3. Gestion des transitions epsilon
4. Configuration du symbole de départ

#### 4.3 Conversion avec DPDA et NPDA

```python
def grammar_to_dpda(self, grammar: ContextFreeGrammar) -> DPDA:
    """Convertit une grammaire en DPDA si possible.
    
    :param grammar: Grammaire à convertir
    :return: DPDA équivalent
    :raises GrammarConversionError: Si la conversion n'est pas possible
    """

def grammar_to_npda(self, grammar: ContextFreeGrammar) -> NPDA:
    """Convertit une grammaire en NPDA.
    
    :param grammar: Grammaire à convertir
    :return: NPDA équivalent
    :raises GrammarConversionError: Si la conversion échoue
    """
```

### 5. Normalisation des grammaires

#### 5.1 Forme normale de Chomsky

```python
def to_chomsky_normal_form(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Convertit une grammaire en forme normale de Chomsky.
    
    :param grammar: Grammaire à convertir
    :return: Grammaire en forme normale de Chomsky
    :raises GrammarError: Si la conversion échoue
    """
```

**Étapes de conversion :**
1. Élimination des productions vides
2. Élimination des productions unitaires
3. Élimination des symboles inaccessibles
4. Élimination des symboles non-générateurs
5. Conversion en productions binaires

#### 5.2 Forme normale de Greibach

```python
def to_greibach_normal_form(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Convertit une grammaire en forme normale de Greibach.
    
    :param grammar: Grammaire à convertir
    :return: Grammaire en forme normale de Greibach
    :raises GrammarError: Si la conversion échoue
    """
```

**Étapes de conversion :**
1. Conversion en forme normale de Chomsky
2. Élimination de la récursivité gauche
3. Conversion en productions de la forme A → aα

#### 5.3 Élimination des productions vides

```python
def eliminate_empty_productions(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Élimine les productions vides d'une grammaire.
    
    :param grammar: Grammaire à traiter
    :return: Grammaire sans productions vides
    :raises GrammarError: Si l'élimination échoue
    """
```

#### 5.4 Élimination de la récursivité gauche

```python
def eliminate_left_recursion(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Élimine la récursivité gauche d'une grammaire.
    
    :param grammar: Grammaire à traiter
    :return: Grammaire sans récursivité gauche
    :raises GrammarError: Si l'élimination échoue
    """
```

### 6. Optimisations

#### 6.1 Optimisation des grammaires

```python
def optimize_grammar(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Optimise une grammaire.
    
    :param grammar: Grammaire à optimiser
    :return: Grammaire optimisée
    :raises GrammarError: Si l'optimisation échoue
    """
```

**Optimisations implémentées :**
- Élimination des symboles inaccessibles
- Élimination des symboles non-générateurs
- Fusion des productions équivalentes
- Réduction du nombre de productions

#### 6.2 Détection d'ambiguïté

```python
def detect_ambiguity(self, grammar: ContextFreeGrammar) -> bool:
    """Détecte si une grammaire est ambiguë.
    
    :param grammar: Grammaire à analyser
    :return: True si la grammaire est ambiguë, False sinon
    """
```

#### 6.3 Analyse de la récursivité

```python
def analyze_recursion(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
    """Analyse la récursivité d'une grammaire.
    
    :param grammar: Grammaire à analyser
    :return: Dictionnaire avec l'analyse de récursivité
    """
```

### 7. Méthodes utilitaires

#### 7.1 Sérialisation

```python
def to_dict(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
    """Convertit une grammaire en dictionnaire.
    
    :param grammar: Grammaire à sérialiser
    :return: Représentation dictionnaire de la grammaire
    """

def from_dict(self, data: Dict[str, Any]) -> ContextFreeGrammar:
    """Crée une grammaire à partir d'un dictionnaire.
    
    :param data: Données de la grammaire
    :return: Grammaire créée
    :raises GrammarError: Si les données sont invalides
    """
```

#### 7.2 Export/Import

```python
def export_grammar(self, grammar: ContextFreeGrammar, format: str = "text") -> str:
    """Exporte une grammaire dans un format donné.
    
    :param grammar: Grammaire à exporter
    :param format: Format d'export (text, json, xml)
    :return: Représentation de la grammaire
    """

def import_grammar(self, data: str, format: str = "text") -> ContextFreeGrammar:
    """Importe une grammaire depuis un format donné.
    
    :param data: Données de la grammaire
    :param format: Format d'import (text, json, xml)
    :return: Grammaire importée
    :raises GrammarError: Si l'import échoue
    """
```

#### 7.3 Représentation

```python
def to_string(self, grammar: ContextFreeGrammar) -> str:
    """Convertit une grammaire en chaîne de caractères.
    
    :param grammar: Grammaire à convertir
    :return: Représentation textuelle de la grammaire
    """

def __str__(self) -> str:
    """Représentation textuelle du parser."""
```

### 8. Gestion d'erreurs

#### 8.1 Exceptions personnalisées

```python
class GrammarError(Exception):
    """Exception de base pour les grammaires."""

class GrammarParseError(GrammarError):
    """Exception pour erreur de parsing."""

class GrammarValidationError(GrammarError):
    """Exception pour erreur de validation."""

class GrammarConversionError(GrammarError):
    """Exception pour erreur de conversion."""

class GrammarNormalizationError(GrammarError):
    """Exception pour erreur de normalisation."""

class GrammarOptimizationError(GrammarError):
    """Exception pour erreur d'optimisation."""
```

### 9. Tests unitaires

#### 9.1 Couverture de tests

- Tests de parsing et validation
- Tests de conversion grammaire ↔ PDA
- Tests de normalisation (Chomsky, Greibach)
- Tests d'optimisation
- Tests de sérialisation/désérialisation
- Tests de performance
- Tests d'erreurs et cas limites

#### 9.2 Exemples de tests

```python
def test_grammar_parsing():
    """Test de parsing de grammaires."""
    
def test_grammar_validation():
    """Test de validation de grammaires."""
    
def test_grammar_to_pda():
    """Test de conversion grammaire → PDA."""
    
def test_pda_to_grammar():
    """Test de conversion PDA → grammaire."""
    
def test_chomsky_normal_form():
    """Test de conversion en forme normale de Chomsky."""
    
def test_greibach_normal_form():
    """Test de conversion en forme normale de Greibach."""
    
def test_eliminate_empty_productions():
    """Test d'élimination des productions vides."""
    
def test_eliminate_left_recursion():
    """Test d'élimination de la récursivité gauche."""
    
def test_grammar_optimization():
    """Test d'optimisation des grammaires."""
    
def test_ambiguity_detection():
    """Test de détection d'ambiguïté."""
    
def test_grammar_serialization():
    """Test de sérialisation/désérialisation."""
```

### 10. Exemples d'utilisation

#### 10.1 Parsing d'une grammaire simple

```python
# Parsing d'une grammaire pour a^n b^n
grammar_string = """
S -> aSb | ε
"""

parser = GrammarParser()
grammar = parser.parse_grammar(grammar_string)

# Validation
assert parser.validate_grammar(grammar)

# Conversion en PDA
pda = parser.grammar_to_pda(grammar)
assert pda.accepts('aabb')  # True
assert pda.accepts('aaabbb')  # True
assert not pda.accepts('abab')  # False
```

#### 10.2 Normalisation en forme de Chomsky

```python
# Grammaire originale
grammar = ContextFreeGrammar(
    variables={'S', 'A', 'B'},
    terminals={'a', 'b'},
    productions={
        Production('S', ['a', 'S', 'b']),
        Production('S', []),  # Production vide
        Production('A', ['a', 'A']),
        Production('A', ['b'])
    },
    start_symbol='S'
)

# Conversion en forme normale de Chomsky
cnf_grammar = parser.to_chomsky_normal_form(grammar)

# Vérification que toutes les productions sont binaires
for production in cnf_grammar.productions:
    assert len(production.right_side) <= 2
```

#### 10.3 Conversion PDA → grammaire

```python
# Création d'un PDA
pda = PDA(...)

# Conversion en grammaire
grammar = parser.pda_to_grammar(pda)

# Vérification de l'équivalence
assert parser.validate_grammar(grammar)
```

### 11. Métriques de performance

#### 11.1 Objectifs de performance

- Parsing : < 10ms pour des grammaires de 100 productions
- Conversion grammaire → PDA : < 50ms pour des grammaires de 100 productions
- Conversion PDA → grammaire : < 100ms pour des PDA de 100 états
- Normalisation : < 200ms pour des grammaires de 100 productions

#### 11.2 Optimisations implémentées

- Parsing optimisé avec cache
- Conversion efficace avec structures de données optimisées
- Normalisation incrémentale
- Mise en cache des résultats de conversion

### 12. Documentation

#### 12.1 Docstrings

- Documentation complète de toutes les méthodes
- Exemples d'utilisation dans les docstrings
- Spécification des paramètres et valeurs de retour
- Documentation des exceptions possibles

#### 12.2 Exemples

- Exemples d'utilisation dans la documentation
- Cas d'usage typiques
- Guide de migration depuis les grammaires existantes

### 13. Intégration

#### 13.1 Interface commune

- Compatibilité avec les automates à pile
- Interface unifiée pour les conversions
- Support des différents formats de grammaires

#### 13.2 Extensibilité

- Architecture modulaire pour les extensions
- Support des formats de grammaires personnalisés
- Interface pour les algorithmes spécialisés

## Critères de validation

- [ ] Classe GrammarParser implémentée selon les spécifications
- [ ] Parsing de grammaires fonctionnel
- [ ] Validation des grammaires opérationnelle
- [ ] Conversions bidirectionnelles grammaire ↔ PDA opérationnelles
- [ ] Normalisation des grammaires implémentée
- [ ] Optimisations des grammaires fonctionnelles
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Performance conforme aux spécifications
- [ ] Documentation complète avec docstrings
- [ ] Gestion d'erreurs robuste
- [ ] Support de la sérialisation/désérialisation

## Dépendances

- Phase 001 : Interfaces abstraites et infrastructure
- Phase 002 : Automates finis (pour les conversions et optimisations)
- Phase 003.001 : PDA (pour les conversions)
- Phase 003.002 : DPDA (pour les conversions)
- Phase 003.003 : NPDA (pour les conversions)

## Notes d'implémentation

1. **Parsing** : Parser récursif descent pour les grammaires
2. **Validation** : Vérification complète de la cohérence des grammaires
3. **Conversions** : Algorithmes efficaces pour les conversions bidirectionnelles
4. **Normalisation** : Implémentation des formes normales de Chomsky et Greibach
5. **Optimisation** : Réduction du nombre de productions et symboles