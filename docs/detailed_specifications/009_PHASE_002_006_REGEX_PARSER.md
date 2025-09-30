# Spécifications Détaillées - Regex Parser Implementation

## Vue d'ensemble

Cette spécification détaille l'implémentation du parser d'expressions régulières pour la phase 2 du projet Baobab Automata. Le parser permet de construire des automates à partir d'expressions régulières et de convertir des automates en expressions régulières.

## Objectifs

- Implémenter un parser d'expressions régulières complet et performant
- Fournir la construction d'automates à partir d'expressions
- Implémenter la conversion automate → expression régulière
- Assurer la compatibilité avec l'architecture du projet

## Spécifications Techniques

### 1. Classe RegexParser

#### 1.1 Structure de Base

**Fichier** : `src/baobab_automata/finite/regex_parser.py`

**Attributs** :
- `alphabet: Set[str]` - Alphabet supporté
- `operators: Set[str]` - Opérateurs supportés
- `precedence: Dict[str, int]` - Priorité des opérateurs
- `cache: Dict[str, AbstractFiniteAutomaton]` - Cache des expressions parsées

#### 1.2 Constructeur

```python
def __init__(self, alphabet: Optional[Set[str]] = None) -> None
```

**Configuration par défaut** :
- Alphabet : `{'a', 'b', 'c', ..., 'z', '0', '1', ..., '9'}`
- Opérateurs : `{'.', '|', '*', '+', '?', '(', ')'}`
- Priorité : `{'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}`

### 2. Parser d'Expressions Régulières

#### 2.1 Analyse Syntaxique

```python
def parse(self, regex: str) -> AbstractFiniteAutomaton
```

**Algorithme** :
1. Tokenisation de l'expression
2. Analyse syntaxique (shunting yard ou récursive descent)
3. Construction de l'arbre syntaxique
4. Construction de l'automate à partir de l'arbre

**Complexité** : O(n) où n est la longueur de l'expression

#### 2.2 Tokenisation

```python
def _tokenize(self, regex: str) -> List[Token]
```

**Types de tokens** :
- `LITERAL` : Caractères littéraux
- `OPERATOR` : Opérateurs (|, *, +, ?, .)
- `PARENTHESIS` : Parenthèses
- `ESCAPE` : Caractères échappés

**Gestion des caractères spéciaux** :
- `\d` : Chiffres
- `\w` : Caractères alphanumériques
- `\s` : Espaces
- `\.` : Point littéral
- `\*` : Astérisque littéral

#### 2.3 Analyse Syntaxique

```python
def _parse_expression(self, tokens: List[Token]) -> ASTNode
```

**Grammaire** :
```
Expression → Term | Expression '|' Term
Term → Factor | Term Factor
Factor → Primary | Primary '*' | Primary '+' | Primary '?'
Primary → Literal | '(' Expression ')'
```

**Algorithme** : Récursive descent avec gestion de la priorité

### 3. Construction d'Automates

#### 3.1 Construction à partir d'AST

```python
def _build_automaton(self, node: ASTNode) -> AbstractFiniteAutomaton
```

**Règles de construction** :
- **Littéral** : Automate simple avec une transition
- **Union (|)** : Union des automates
- **Concaténation** : Concaténation des automates
- **Kleene (*)** : Étoile de Kleene
- **Plus (+)** : Concaténation + étoile
- **Optionnel (?)** : Union avec mot vide

#### 3.2 Optimisations

```python
def _optimize_automaton(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton
```

**Stratégies** :
- Minimisation des DFA
- Élimination des états inaccessibles
- Fusion des transitions identiques
- Cache des automates fréquemment utilisés

### 4. Conversion Automate → Expression Régulière

#### 4.1 Algorithme de Kleene

```python
def automaton_to_regex(self, automaton: AbstractFiniteAutomaton) -> str
```

**Algorithme** :
1. Convertir l'automate en DFA si nécessaire
2. Appliquer l'algorithme de Kleene
3. Simplifier l'expression résultante

**Complexité** : O(n³) où n est le nombre d'états

#### 4.2 Simplification d'Expressions

```python
def _simplify_regex(self, regex: str) -> str
```

**Règles de simplification** :
- `a**` → `a*`
- `a*?` → `a*`
- `a|a` → `a`
- `a|ε` → `a?`
- `ε|a` → `a?`

### 5. Méthodes Utilitaires

#### 5.1 Validation d'Expressions

```python
def validate(self, regex: str) -> bool
```

**Vérifications** :
- Syntaxe correcte
- Parenthèses équilibrées
- Opérateurs valides
- Caractères supportés

#### 5.2 Normalisation

```python
def normalize(self, regex: str) -> str
```

**Transformations** :
- Ajout de concaténations implicites
- Normalisation des parenthèses
- Simplification des expressions

#### 5.3 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]
def from_dict(data: Dict[str, Any]) -> 'RegexParser'
```

**Format** :
```json
{
    "alphabet": ["a", "b", "c"],
    "operators": [".", "|", "*", "+", "?"],
    "precedence": {
        "*": 3,
        "+": 3,
        "?": 3,
        ".": 2,
        "|": 1
    }
}
```

### 6. Classes de Support

#### 6.1 Token

```python
class Token:
    def __init__(self, type: str, value: str, position: int)
    def __repr__(self) -> str
    def __eq__(self, other) -> bool
```

#### 6.2 ASTNode

```python
class ASTNode:
    def __init__(self, type: str, value: str = None, children: List['ASTNode'] = None)
    def __repr__(self) -> str
    def __eq__(self, other) -> bool
```

#### 6.3 RegexError

```python
class RegexError(Exception):
    """Exception de base pour les erreurs de regex"""

class RegexSyntaxError(RegexError):
    """Erreur de syntaxe dans l'expression régulière"""

class RegexParseError(RegexError):
    """Erreur lors du parsing"""

class RegexConversionError(RegexError):
    """Erreur lors de la conversion"""
```

### 7. Tests Unitaires

#### 7.1 Structure des Tests

**Fichier** : `tests/finite/test_regex_parser.py`

**Classe** : `TestRegexParser`

#### 7.2 Cas de Test

1. **Parsing** :
   - Expressions simples
   - Expressions complexes
   - Expressions avec parenthèses
   - Expressions avec opérateurs multiples

2. **Construction d'automates** :
   - Automates pour littéraux
   - Automates pour unions
   - Automates pour concaténations
   - Automates pour étoile de Kleene

3. **Conversion** :
   - DFA vers expression régulière
   - NFA vers expression régulière
   - ε-NFA vers expression régulière

4. **Validation** :
   - Expressions valides
   - Expressions invalides
   - Gestion d'erreurs

5. **Performance** :
   - Expressions longues
   - Automates complexes
   - Cache des résultats

### 8. Contraintes de Performance

- **Temps de parsing** : < 10ms pour expressions < 1000 caractères
- **Temps de construction** : < 100ms pour automates < 100 états
- **Temps de conversion** : < 500ms pour automates < 50 états
- **Mémoire** : < 1MB pour expressions < 10000 caractères
- **Scalabilité** : Support jusqu'à 1000 caractères par expression

### 9. Gestion d'Erreurs

#### 9.1 Exceptions Personnalisées

```python
class RegexError(Exception):
    """Exception de base pour les erreurs de regex"""

class RegexSyntaxError(RegexError):
    """Erreur de syntaxe dans l'expression régulière"""

class RegexParseError(RegexError):
    """Erreur lors du parsing"""

class RegexConversionError(RegexError):
    """Erreur lors de la conversion"""
```

#### 9.2 Validation des Entrées

- Vérification de la syntaxe
- Validation des caractères
- Messages d'erreur explicites
- Position des erreurs

### 10. Documentation

#### 10.1 Docstrings

- Format reStructuredText
- Exemples d'utilisation
- Documentation des paramètres
- Documentation des exceptions

#### 10.2 Exemples d'Utilisation

```python
# Création du parser
parser = RegexParser()

# Parsing d'une expression
automaton = parser.parse("a*b+")

# Validation
assert parser.validate("a*b+") == True

# Conversion
regex = parser.automaton_to_regex(automaton)

# Cache
cached_automaton = parser.parse("a*b+")  # Utilise le cache
```

### 11. Intégration

#### 11.1 Interfaces

- Compatibilité avec DFA, NFA, ε-NFA
- Support des conversions bidirectionnelles
- Intégration avec les opérations sur les langages

#### 11.2 Dépendances

- Dépend de DFA, NFA, ε-NFA (pour les conversions)
- Utilisation des interfaces de la phase 1
- Préparation pour les algorithmes de conversion

### 12. Critères de Validation

- [ ] Classe RegexParser implémentée
- [ ] Parser d'expressions régulières fonctionnel
- [ ] Construction d'automates opérationnelle
- [ ] Conversion automate → expression régulière fonctionnelle
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Performance conforme aux spécifications
- [ ] Documentation complète
- [ ] Gestion d'erreurs robuste
- [ ] Score Pylint >= 8.5/10
- [ ] Aucune vulnérabilité de sécurité

## Notes de Développement

1. **Priorité** : Cette classe peut être développée en parallèle avec les algorithmes de conversion
2. **Performance** : Optimiser le parsing et la construction d'automates
3. **Robustesse** : Gestion d'erreurs complète
4. **Extensibilité** : Préparer pour les extensions futures
5. **Cache** : Implémenter un système de cache efficace
