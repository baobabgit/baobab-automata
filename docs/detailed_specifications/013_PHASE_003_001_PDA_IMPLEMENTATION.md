# Spécifications Détaillées - Phase 003.001 - Implémentation des Automates à Pile Non-Déterministes (PDA)

## Vue d'ensemble

Cette spécification détaille l'implémentation des automates à pile non-déterministes (Pushdown Automaton - PDA) pour la reconnaissance des langages hors-contexte. Les PDA étendent les automates finis en ajoutant une pile (stack) qui permet de reconnaître des langages plus complexes.

## Objectifs

- Implémenter une classe PDA complète et performante
- Gérer les transitions conditionnelles (lecture, écriture, pile)
- Fournir des algorithmes de reconnaissance de mots efficaces
- Assurer la validation et la cohérence des automates
- Optimiser les performances pour les gros automates

## Architecture

### Classe principale : PDA

```python
class PDA(AbstractPushdownAutomaton):
    """Automate à pile non-déterministe pour la reconnaissance de langages hors-contexte."""
```

### Structure de données

- **États** : Ensemble d'états finis
- **Alphabet d'entrée** : Symboles d'entrée
- **Alphabet de pile** : Symboles de pile (incluant le symbole de fond de pile)
- **Transitions** : Fonction de transition δ : Q × (Σ ∪ {ε}) × Γ → P(Q × Γ*)
- **État initial** : État de départ
- **Symbole de fond de pile** : Symbole initial de la pile
- **États finaux** : États d'acceptation

## Spécifications détaillées

### 1. Constructeur et initialisation

#### 1.1 Constructeur principal

```python
def __init__(
    self,
    states: Set[str],
    input_alphabet: Set[str],
    stack_alphabet: Set[str],
    transitions: Dict[Tuple[str, str, str], Set[Tuple[str, str]]],
    initial_state: str,
    initial_stack_symbol: str,
    final_states: Set[str],
    name: Optional[str] = None
) -> None:
    """Initialise un automate à pile non-déterministe.
    
    :param states: Ensemble des états
    :param input_alphabet: Alphabet d'entrée
    :param stack_alphabet: Alphabet de pile
    :param transitions: Fonction de transition
    :param initial_state: État initial
    :param initial_stack_symbol: Symbole initial de pile
    :param final_states: États finaux
    :param name: Nom optionnel de l'automate
    :raises InvalidPDAError: Si l'automate n'est pas valide
    """
```

#### 1.2 Validation automatique

- Vérification de la cohérence des états
- Validation des alphabets
- Vérification des transitions
- Contrôle de l'état initial et des états finaux
- Validation du symbole de fond de pile

### 2. Méthodes de base

#### 2.1 Reconnaissance de mots

```python
def accepts(self, word: str) -> bool:
    """Vérifie si un mot est accepté par l'automate.
    
    :param word: Mot à tester
    :return: True si le mot est accepté, False sinon
    :raises PDAError: En cas d'erreur de traitement
    """
```

**Algorithme de reconnaissance :**
1. Initialisation avec l'état initial et le symbole de fond de pile
2. Simulation non-déterministe avec toutes les branches possibles
3. Utilisation d'une pile pour gérer les symboles
4. Arrêt quand le mot est entièrement lu ou qu'aucune transition n'est possible
5. Acceptation si un état final est atteint

#### 2.2 Gestion des transitions

```python
def get_transitions(
    self, 
    state: str, 
    input_symbol: str, 
    stack_symbol: str
) -> Set[Tuple[str, str]]:
    """Récupère les transitions possibles depuis un état donné.
    
    :param state: État source
    :param input_symbol: Symbole d'entrée (peut être ε)
    :param stack_symbol: Symbole de pile
    :return: Ensemble des transitions possibles
    :raises InvalidStateError: Si l'état n'existe pas
    """
```

#### 2.3 États et validation

```python
def is_final_state(self, state: str) -> bool:
    """Vérifie si un état est final.
    
    :param state: État à vérifier
    :return: True si l'état est final, False sinon
    :raises InvalidStateError: Si l'état n'existe pas
    """

def get_reachable_states(self, from_state: str) -> Set[str]:
    """Récupère tous les états accessibles depuis un état donné.
    
    :param from_state: État de départ
    :return: Ensemble des états accessibles
    :raises InvalidStateError: Si l'état n'existe pas
    """
```

### 3. Algorithmes spécialisés

#### 3.1 Simulation non-déterministe

```python
def _simulate_word(self, word: str) -> bool:
    """Simule la reconnaissance d'un mot de manière non-déterministe.
    
    :param word: Mot à simuler
    :return: True si le mot est accepté, False sinon
    """
```

**Caractéristiques :**
- Utilisation d'une file de priorité pour gérer les configurations
- Gestion des transitions epsilon
- Optimisation avec mise en cache des configurations visitées
- Limitation de la profondeur de pile pour éviter les boucles infinies

#### 3.2 Gestion des configurations

```python
@dataclass(frozen=True)
class PDAConfiguration:
    """Configuration d'un PDA (état, mot restant, pile)."""
    state: str
    remaining_input: str
    stack: str  # Représentation de la pile comme une chaîne
```

#### 3.3 Fermeture epsilon

```python
def _epsilon_closure(self, state: str, stack_symbol: str) -> Set[Tuple[str, str]]:
    """Calcule la fermeture epsilon pour un état et un symbole de pile.
    
    :param state: État de départ
    :param stack_symbol: Symbole de pile
    :return: Ensemble des configurations accessibles par transitions epsilon
    """
```

### 4. Opérations sur les langages

#### 4.1 Union de PDA

```python
def union(self, other: 'PDA') -> 'PDA':
    """Crée l'union de deux PDA.
    
    :param other: Autre PDA
    :return: PDA reconnaissant l'union des langages
    :raises PDAError: Si les PDA ne sont pas compatibles
    """
```

#### 4.2 Concaténation de PDA

```python
def concatenation(self, other: 'PDA') -> 'PDA':
    """Crée la concaténation de deux PDA.
    
    :param other: Autre PDA
    :return: PDA reconnaissant la concaténation des langages
    :raises PDAError: Si les PDA ne sont pas compatibles
    """
```

#### 4.3 Étoile de Kleene

```python
def kleene_star(self) -> 'PDA':
    """Crée l'étoile de Kleene d'un PDA.
    
    :return: PDA reconnaissant l'étoile de Kleene du langage
    :raises PDAError: Si l'opération échoue
    """
```

### 5. Méthodes utilitaires

#### 5.1 Validation

```python
def validate(self) -> bool:
    """Valide la cohérence de l'automate.
    
    :return: True si l'automate est valide, False sinon
    :raises InvalidPDAError: Si l'automate n'est pas valide
    """
```

**Critères de validation :**
- Tous les états référencés existent
- Tous les symboles d'entrée sont dans l'alphabet d'entrée
- Tous les symboles de pile sont dans l'alphabet de pile
- L'état initial existe
- Les états finaux sont des sous-ensembles des états
- Le symbole de fond de pile est dans l'alphabet de pile

#### 5.2 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]:
    """Convertit l'automate en dictionnaire.
    
    :return: Représentation dictionnaire de l'automate
    """

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'PDA':
    """Crée un automate à partir d'un dictionnaire.
    
    :param data: Données de l'automate
    :return: Instance de PDA
    :raises InvalidPDAError: Si les données sont invalides
    """
```

#### 5.3 Représentation

```python
def __str__(self) -> str:
    """Représentation textuelle de l'automate."""

def __repr__(self) -> str:
    """Représentation technique de l'automate."""
```

### 6. Optimisations

#### 6.1 Mise en cache

- Cache des configurations visitées pendant la simulation
- Cache des fermetures epsilon
- Cache des états accessibles

#### 6.2 Optimisations de performance

- Utilisation de structures de données optimisées (set, frozenset)
- Algorithme de simulation optimisé
- Gestion mémoire efficace pour les gros automates

### 7. Gestion d'erreurs

#### 7.1 Exceptions personnalisées

```python
class PDAError(Exception):
    """Exception de base pour les PDA."""

class InvalidPDAError(PDAError):
    """Exception pour PDA invalide."""

class InvalidStateError(PDAError):
    """Exception pour état invalide."""

class InvalidTransitionError(PDAError):
    """Exception pour transition invalide."""

class PDASimulationError(PDAError):
    """Exception pour erreur de simulation."""
```

### 8. Tests unitaires

#### 8.1 Couverture de tests

- Tests de construction et validation
- Tests de reconnaissance de mots (cas simples et complexes)
- Tests des opérations sur les langages
- Tests de sérialisation/désérialisation
- Tests de performance
- Tests d'erreurs et cas limites

#### 8.2 Exemples de tests

```python
def test_pda_construction():
    """Test de construction d'un PDA simple."""
    
def test_pda_word_recognition():
    """Test de reconnaissance de mots."""
    
def test_pda_union():
    """Test de l'union de deux PDA."""
    
def test_pda_concatenation():
    """Test de la concaténation de deux PDA."""
    
def test_pda_kleene_star():
    """Test de l'étoile de Kleene."""
    
def test_pda_validation():
    """Test de validation d'un PDA."""
    
def test_pda_serialization():
    """Test de sérialisation/désérialisation."""
```

### 9. Exemples d'utilisation

#### 9.1 PDA pour le langage a^n b^n

```python
# Construction d'un PDA reconnaissant a^n b^n
pda = PDA(
    states={'q0', 'q1', 'q2'},
    input_alphabet={'a', 'b'},
    stack_alphabet={'Z', 'A'},
    transitions={
        ('q0', 'a', 'Z'): {('q0', 'AZ')},
        ('q0', 'a', 'A'): {('q0', 'AA')},
        ('q0', 'b', 'A'): {('q1', '')},
        ('q1', 'b', 'A'): {('q1', '')},
        ('q1', '', 'Z'): {('q2', 'Z')}
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'}
)

# Test de reconnaissance
assert pda.accepts('aabb')  # True
assert pda.accepts('aaabbb')  # True
assert not pda.accepts('abab')  # False
```

#### 9.2 PDA pour les palindromes

```python
# Construction d'un PDA reconnaissant les palindromes
pda_palindrome = PDA(
    states={'q0', 'q1', 'q2'},
    input_alphabet={'a', 'b'},
    stack_alphabet={'Z', 'A', 'B'},
    transitions={
        ('q0', 'a', 'Z'): {('q0', 'AZ')},
        ('q0', 'b', 'Z'): {('q0', 'BZ')},
        ('q0', 'a', 'A'): {('q0', 'AA')},
        ('q0', 'b', 'A'): {('q0', 'BA')},
        ('q0', 'a', 'B'): {('q0', 'AB')},
        ('q0', 'b', 'B'): {('q0', 'BB')},
        ('q0', 'a', 'A'): {('q1', '')},
        ('q0', 'b', 'B'): {('q1', '')},
        ('q1', 'a', 'A'): {('q1', '')},
        ('q1', 'b', 'B'): {('q1', '')},
        ('q1', '', 'Z'): {('q2', 'Z')}
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'}
)
```

### 10. Métriques de performance

#### 10.1 Objectifs de performance

- Reconnaissance de mots : < 100ms pour des mots de 1000 caractères
- Construction : < 50ms pour des automates de 100 états
- Mémoire : < 10MB pour des automates de 1000 états

#### 10.2 Optimisations implémentées

- Structures de données optimisées
- Algorithmes de simulation efficaces
- Mise en cache intelligente
- Gestion mémoire optimisée

### 11. Documentation

#### 11.1 Docstrings

- Documentation complète de toutes les méthodes
- Exemples d'utilisation dans les docstrings
- Spécification des paramètres et valeurs de retour
- Documentation des exceptions possibles

#### 11.2 Exemples

- Exemples d'utilisation dans la documentation
- Cas d'usage typiques
- Guide de migration depuis les automates finis

### 12. Intégration

#### 12.1 Interface commune

- Implémentation de `AbstractPushdownAutomaton`
- Compatibilité avec les autres types d'automates
- Interface unifiée pour les opérations communes

#### 12.2 Extensibilité

- Architecture modulaire pour les extensions
- Support des sous-classes personnalisées
- Interface pour les algorithmes spécialisés

## Critères de validation

- [ ] Classe PDA implémentée selon les spécifications
- [ ] Algorithme de reconnaissance non-déterministe fonctionnel
- [ ] Gestion des transitions conditionnelles opérationnelle
- [ ] Opérations sur les langages implémentées
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Performance conforme aux spécifications
- [ ] Documentation complète avec docstrings
- [ ] Gestion d'erreurs robuste
- [ ] Validation automatique de la cohérence
- [ ] Support de la sérialisation/désérialisation

## Dépendances

- Phase 001 : Interfaces abstraites et infrastructure
- Phase 002 : Automates finis (pour les conversions et optimisations)

## Notes d'implémentation

1. **Gestion de la pile** : La pile est représentée comme une chaîne de caractères avec le sommet à droite
2. **Transitions epsilon** : Support complet des transitions vides pour l'entrée et la pile
3. **Non-déterminisme** : Simulation de toutes les branches possibles
4. **Optimisations** : Mise en cache et structures de données optimisées
5. **Validation** : Vérification automatique de la cohérence des automates