# Spécifications Détaillées - Phase 003.002 - Implémentation des Automates à Pile Déterministes (DPDA)

## Vue d'ensemble

Cette spécification détaille l'implémentation des automates à pile déterministes (Deterministic Pushdown Automaton - DPDA) pour la reconnaissance des langages hors-contexte déterministes. Les DPDA sont des PDA avec des contraintes de déterminisme qui permettent des algorithmes de reconnaissance plus efficaces.

## Objectifs

- Implémenter une classe DPDA avec contraintes de déterminisme
- Fournir des algorithmes de reconnaissance optimisés
- Gérer les conflits de déterminisme
- Assurer la validation du déterminisme
- Optimiser les performances pour les gros automates

## Architecture

### Classe principale : DPDA

```python
class DPDA(AbstractPushdownAutomaton):
    """Automate à pile déterministe pour la reconnaissance de langages hors-contexte déterministes."""
```

### Contraintes de déterminisme

Un DPDA doit satisfaire les contraintes suivantes :
1. **Déterminisme des transitions** : Pour tout état q, symbole d'entrée a, et symbole de pile Z, il existe au plus une transition
2. **Gestion des transitions epsilon** : Si une transition epsilon existe depuis un état, aucune transition avec symbole d'entrée n'est possible depuis cet état
3. **Unicité des transitions** : Chaque configuration (état, symbole d'entrée, symbole de pile) a au plus une transition possible

## Spécifications détaillées

### 1. Constructeur et initialisation

#### 1.1 Constructeur principal

```python
def __init__(
    self,
    states: Set[str],
    input_alphabet: Set[str],
    stack_alphabet: Set[str],
    transitions: Dict[Tuple[str, str, str], Tuple[str, str]],
    initial_state: str,
    initial_stack_symbol: str,
    final_states: Set[str],
    name: Optional[str] = None
) -> None:
    """Initialise un automate à pile déterministe.
    
    :param states: Ensemble des états
    :param input_alphabet: Alphabet d'entrée
    :param stack_alphabet: Alphabet de pile
    :param transitions: Fonction de transition déterministe
    :param initial_state: État initial
    :param initial_stack_symbol: Symbole initial de pile
    :param final_states: États finaux
    :param name: Nom optionnel de l'automate
    :raises InvalidDPDAError: Si l'automate n'est pas valide ou non-déterministe
    """
```

#### 1.2 Validation du déterminisme

```python
def _validate_determinism(self) -> bool:
    """Valide que l'automate respecte les contraintes de déterminisme.
    
    :return: True si l'automate est déterministe, False sinon
    :raises InvalidDPDAError: Si l'automate n'est pas déterministe
    """
```

**Critères de validation :**
- Vérification de l'unicité des transitions
- Contrôle des conflits epsilon/symbole
- Validation de la cohérence des transitions

### 2. Méthodes de base

#### 2.1 Reconnaissance de mots optimisée

```python
def accepts(self, word: str) -> bool:
    """Vérifie si un mot est accepté par l'automate.
    
    :param word: Mot à tester
    :return: True si le mot est accepté, False sinon
    :raises DPDAError: En cas d'erreur de traitement
    """
```

**Algorithme de reconnaissance optimisé :**
1. Initialisation avec l'état initial et le symbole de fond de pile
2. Simulation déterministe (une seule branche)
3. Utilisation d'une pile pour gérer les symboles
4. Arrêt quand le mot est entièrement lu ou qu'aucune transition n'est possible
5. Acceptation si un état final est atteint

#### 2.2 Gestion des transitions déterministes

```python
def get_transition(
    self, 
    state: str, 
    input_symbol: str, 
    stack_symbol: str
) -> Optional[Tuple[str, str]]:
    """Récupère la transition unique depuis un état donné.
    
    :param state: État source
    :param input_symbol: Symbole d'entrée (peut être ε)
    :param stack_symbol: Symbole de pile
    :return: Transition unique ou None si aucune transition
    :raises InvalidStateError: Si l'état n'existe pas
    :raises DPDAError: Si plusieurs transitions sont possibles
    """
```

#### 2.3 Simulation déterministe

```python
def _simulate_word_deterministic(self, word: str) -> bool:
    """Simule la reconnaissance d'un mot de manière déterministe.
    
    :param word: Mot à simuler
    :return: True si le mot est accepté, False sinon
    """
```

**Caractéristiques :**
- Simulation linéaire (une seule branche)
- Gestion des transitions epsilon
- Optimisation avec mise en cache des configurations
- Détection précoce des échecs

### 3. Algorithmes spécialisés

#### 3.1 Gestion des configurations déterministes

```python
@dataclass(frozen=True)
class DPDAConfiguration:
    """Configuration d'un DPDA (état, mot restant, pile)."""
    state: str
    remaining_input: str
    stack: str  # Représentation de la pile comme une chaîne
```

#### 3.2 Fermeture epsilon déterministe

```python
def _epsilon_closure_deterministic(self, state: str, stack_symbol: str) -> Optional[Tuple[str, str]]:
    """Calcule la fermeture epsilon déterministe pour un état et un symbole de pile.
    
    :param state: État de départ
    :param stack_symbol: Symbole de pile
    :return: Configuration unique accessible par transitions epsilon ou None
    """
```

#### 3.3 Détection des conflits

```python
def _detect_conflicts(self) -> List[str]:
    """Détecte les conflits de déterminisme dans l'automate.
    
    :return: Liste des descriptions des conflits détectés
    """
```

### 4. Opérations sur les langages

#### 4.1 Union de DPDA

```python
def union(self, other: 'DPDA') -> 'DPDA':
    """Crée l'union de deux DPDA.
    
    :param other: Autre DPDA
    :return: DPDA reconnaissant l'union des langages
    :raises DPDAError: Si les DPDA ne sont pas compatibles
    :raises InvalidDPDAError: Si le résultat n'est pas déterministe
    """
```

**Note :** L'union de deux DPDA peut ne pas être déterministe. Dans ce cas, une exception est levée.

#### 4.2 Concaténation de DPDA

```python
def concatenation(self, other: 'DPDA') -> 'DPDA':
    """Crée la concaténation de deux DPDA.
    
    :param other: Autre DPDA
    :return: DPDA reconnaissant la concaténation des langages
    :raises DPDAError: Si les DPDA ne sont pas compatibles
    :raises InvalidDPDAError: Si le résultat n'est pas déterministe
    """
```

#### 4.3 Étoile de Kleene

```python
def kleene_star(self) -> 'DPDA':
    """Crée l'étoile de Kleene d'un DPDA.
    
    :return: DPDA reconnaissant l'étoile de Kleene du langage
    :raises DPDAError: Si l'opération échoue
    :raises InvalidDPDAError: Si le résultat n'est pas déterministe
    """
```

### 5. Conversions

#### 5.1 Conversion PDA → DPDA

```python
@classmethod
def from_pda(cls, pda: 'PDA') -> 'DPDA':
    """Convertit un PDA en DPDA si possible.
    
    :param pda: PDA à convertir
    :return: DPDA équivalent
    :raises InvalidDPDAError: Si la conversion n'est pas possible
    """
```

**Algorithme de conversion :**
1. Analyse du PDA pour détecter les conflits
2. Résolution des conflits par ajout d'états
3. Validation du déterminisme du résultat
4. Optimisation des transitions

#### 5.2 Conversion DPDA → PDA

```python
def to_pda(self) -> 'PDA':
    """Convertit le DPDA en PDA.
    
    :return: PDA équivalent
    """
```

### 6. Méthodes utilitaires

#### 6.1 Validation étendue

```python
def validate(self) -> bool:
    """Valide la cohérence et le déterminisme de l'automate.
    
    :return: True si l'automate est valide, False sinon
    :raises InvalidDPDAError: Si l'automate n'est pas valide
    """
```

**Critères de validation :**
- Validation de base (états, transitions, etc.)
- Validation du déterminisme
- Détection des conflits
- Vérification de la cohérence des transitions

#### 6.2 Analyse de déterminisme

```python
def analyze_determinism(self) -> Dict[str, Any]:
    """Analyse le niveau de déterminisme de l'automate.
    
    :return: Dictionnaire avec les métriques de déterminisme
    """
```

**Métriques incluses :**
- Nombre de conflits détectés
- Pourcentage de transitions déterministes
- Complexité de résolution des conflits
- Recommandations d'optimisation

#### 6.3 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]:
    """Convertit l'automate en dictionnaire.
    
    :return: Représentation dictionnaire de l'automate
    """

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'DPDA':
    """Crée un automate à partir d'un dictionnaire.
    
    :param data: Données de l'automate
    :return: Instance de DPDA
    :raises InvalidDPDAError: Si les données sont invalides
    """
```

### 7. Optimisations

#### 7.1 Optimisations spécifiques aux DPDA

```python
def optimize_transitions(self) -> 'DPDA':
    """Optimise les transitions de l'automate.
    
    :return: DPDA optimisé
    :raises DPDAError: Si l'optimisation échoue
    """
```

**Optimisations implémentées :**
- Fusion des transitions équivalentes
- Élimination des états inaccessibles
- Réduction des symboles de pile
- Optimisation des transitions epsilon

#### 7.2 Mise en cache

- Cache des configurations visitées
- Cache des fermetures epsilon
- Cache des transitions calculées

#### 7.3 Optimisations de performance

- Simulation déterministe optimisée
- Structures de données spécialisées
- Gestion mémoire efficace

### 8. Gestion d'erreurs

#### 8.1 Exceptions personnalisées

```python
class DPDAError(Exception):
    """Exception de base pour les DPDA."""

class InvalidDPDAError(DPDAError):
    """Exception pour DPDA invalide."""

class DeterminismError(DPDAError):
    """Exception pour violation du déterminisme."""

class ConflictError(DPDAError):
    """Exception pour conflit de déterminisme."""

class ConversionError(DPDAError):
    """Exception pour erreur de conversion."""
```

### 9. Tests unitaires

#### 9.1 Couverture de tests

- Tests de construction et validation
- Tests de déterminisme
- Tests de reconnaissance de mots
- Tests des opérations sur les langages
- Tests de conversion PDA ↔ DPDA
- Tests de sérialisation/désérialisation
- Tests de performance
- Tests d'erreurs et cas limites

#### 9.2 Exemples de tests

```python
def test_dpda_construction():
    """Test de construction d'un DPDA simple."""
    
def test_dpda_determinism_validation():
    """Test de validation du déterminisme."""
    
def test_dpda_word_recognition():
    """Test de reconnaissance de mots."""
    
def test_dpda_conflict_detection():
    """Test de détection des conflits."""
    
def test_dpda_pda_conversion():
    """Test de conversion PDA ↔ DPDA."""
    
def test_dpda_union():
    """Test de l'union de deux DPDA."""
    
def test_dpda_concatenation():
    """Test de la concaténation de deux DPDA."""
    
def test_dpda_kleene_star():
    """Test de l'étoile de Kleene."""
    
def test_dpda_validation():
    """Test de validation d'un DPDA."""
    
def test_dpda_serialization():
    """Test de sérialisation/désérialisation."""
    
def test_dpda_optimization():
    """Test d'optimisation des transitions."""
```

### 10. Exemples d'utilisation

#### 10.1 DPDA pour le langage a^n b^n

```python
# Construction d'un DPDA reconnaissant a^n b^n
dpda = DPDA(
    states={'q0', 'q1', 'q2'},
    input_alphabet={'a', 'b'},
    stack_alphabet={'Z', 'A'},
    transitions={
        ('q0', 'a', 'Z'): ('q0', 'AZ'),
        ('q0', 'a', 'A'): ('q0', 'AA'),
        ('q0', 'b', 'A'): ('q1', ''),
        ('q1', 'b', 'A'): ('q1', ''),
        ('q1', '', 'Z'): ('q2', 'Z')
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'}
)

# Test de reconnaissance
assert dpda.accepts('aabb')  # True
assert dpda.accepts('aaabbb')  # True
assert not dpda.accepts('abab')  # False
```

#### 10.2 DPDA pour les palindromes

```python
# Construction d'un DPDA reconnaissant les palindromes
dpda_palindrome = DPDA(
    states={'q0', 'q1', 'q2'},
    input_alphabet={'a', 'b'},
    stack_alphabet={'Z', 'A', 'B'},
    transitions={
        ('q0', 'a', 'Z'): ('q0', 'AZ'),
        ('q0', 'b', 'Z'): ('q0', 'BZ'),
        ('q0', 'a', 'A'): ('q0', 'AA'),
        ('q0', 'b', 'A'): ('q0', 'BA'),
        ('q0', 'a', 'B'): ('q0', 'AB'),
        ('q0', 'b', 'B'): ('q0', 'BB'),
        ('q0', 'a', 'A'): ('q1', ''),
        ('q0', 'b', 'B'): ('q1', ''),
        ('q1', 'a', 'A'): ('q1', ''),
        ('q1', 'b', 'B'): ('q1', ''),
        ('q1', '', 'Z'): ('q2', 'Z')
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'}
)
```

#### 10.3 Conversion PDA → DPDA

```python
# Conversion d'un PDA en DPDA
pda = PDA(...)  # PDA non-déterministe
try:
    dpda = DPDA.from_pda(pda)
    print("Conversion réussie")
except InvalidDPDAError as e:
    print(f"Conversion impossible: {e}")
```

### 11. Métriques de performance

#### 11.1 Objectifs de performance

- Reconnaissance de mots : < 50ms pour des mots de 1000 caractères
- Construction : < 30ms pour des automates de 100 états
- Mémoire : < 5MB pour des automates de 1000 états
- Conversion PDA → DPDA : < 100ms pour des automates de 100 états

#### 11.2 Optimisations implémentées

- Simulation déterministe optimisée
- Structures de données spécialisées
- Mise en cache intelligente
- Gestion mémoire optimisée

### 12. Documentation

#### 12.1 Docstrings

- Documentation complète de toutes les méthodes
- Exemples d'utilisation dans les docstrings
- Spécification des paramètres et valeurs de retour
- Documentation des exceptions possibles

#### 12.2 Exemples

- Exemples d'utilisation dans la documentation
- Cas d'usage typiques
- Guide de migration depuis les PDA

### 13. Intégration

#### 13.1 Interface commune

- Implémentation de `AbstractPushdownAutomaton`
- Compatibilité avec les autres types d'automates
- Interface unifiée pour les opérations communes

#### 13.2 Extensibilité

- Architecture modulaire pour les extensions
- Support des sous-classes personnalisées
- Interface pour les algorithmes spécialisés

## Critères de validation

- [ ] Classe DPDA implémentée selon les spécifications
- [ ] Validation du déterminisme opérationnelle
- [ ] Algorithme de reconnaissance déterministe fonctionnel
- [ ] Détection des conflits implémentée
- [ ] Conversions PDA ↔ DPDA opérationnelles
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
- Phase 003.001 : PDA (pour les conversions)

## Notes d'implémentation

1. **Déterminisme** : Validation stricte des contraintes de déterminisme
2. **Gestion des conflits** : Détection et résolution des conflits de déterminisme
3. **Optimisations** : Algorithmes optimisés pour les DPDA
4. **Conversions** : Support des conversions bidirectionnelles avec PDA
5. **Performance** : Simulation déterministe plus rapide que les PDA