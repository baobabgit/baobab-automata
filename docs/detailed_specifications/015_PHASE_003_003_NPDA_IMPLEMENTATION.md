# Spécifications Détaillées - Phase 003.003 - Implémentation des Automates à Pile Non-Déterministes (NPDA)

## Vue d'ensemble

Cette spécification détaille l'implémentation des automates à pile non-déterministes (Non-deterministic Pushdown Automaton - NPDA) pour la reconnaissance des langages hors-contexte. Les NPDA sont des PDA avec des capacités non-déterministes avancées et des optimisations spécialisées pour la simulation parallèle.

## Objectifs

- Implémenter une classe NPDA avec capacités non-déterministes avancées
- Fournir des algorithmes de simulation parallèle optimisés
- Gérer les calculs acceptants de manière efficace
- Optimiser les calculs parallèles
- Analyser la complexité des algorithmes

## Architecture

### Classe principale : NPDA

```python
class NPDA(AbstractPushdownAutomaton):
    """Automate à pile non-déterministe avec capacités avancées pour la simulation parallèle."""
```

### Caractéristiques des NPDA

Les NPDA étendent les PDA avec :
1. **Simulation parallèle** : Exécution simultanée de toutes les branches de calcul
2. **Gestion des calculs acceptants** : Détection efficace des chemins acceptants
3. **Optimisations parallèles** : Algorithmes optimisés pour le non-déterminisme
4. **Analyse de complexité** : Métriques de performance et d'efficacité

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
    name: Optional[str] = None,
    max_parallel_branches: int = 1000
) -> None:
    """Initialise un automate à pile non-déterministe.
    
    :param states: Ensemble des états
    :param input_alphabet: Alphabet d'entrée
    :param stack_alphabet: Alphabet de pile
    :param transitions: Fonction de transition non-déterministe
    :param initial_state: État initial
    :param initial_stack_symbol: Symbole initial de pile
    :param final_states: États finaux
    :param name: Nom optionnel de l'automate
    :param max_parallel_branches: Nombre maximum de branches parallèles
    :raises InvalidNPDAError: Si l'automate n'est pas valide
    """
```

#### 1.2 Configuration des capacités parallèles

```python
def configure_parallel_execution(
    self,
    max_branches: int = 1000,
    timeout: float = 10.0,
    memory_limit: int = 100 * 1024 * 1024  # 100MB
) -> None:
    """Configure les paramètres d'exécution parallèle.
    
    :param max_branches: Nombre maximum de branches parallèles
    :param timeout: Timeout en secondes
    :param memory_limit: Limite de mémoire en octets
    :raises NPDAError: Si la configuration est invalide
    """
```

### 2. Méthodes de base

#### 2.1 Reconnaissance de mots parallèle

```python
def accepts(self, word: str) -> bool:
    """Vérifie si un mot est accepté par l'automate.
    
    :param word: Mot à tester
    :return: True si le mot est accepté, False sinon
    :raises NPDAError: En cas d'erreur de traitement
    :raises NPDATimeoutError: Si le calcul dépasse le timeout
    :raises NPDAMemoryError: Si le calcul dépasse la limite mémoire
    """
```

**Algorithme de reconnaissance parallèle :**
1. Initialisation avec l'état initial et le symbole de fond de pile
2. Simulation parallèle de toutes les branches possibles
3. Utilisation d'une file de priorité pour gérer les configurations
4. Arrêt quand le mot est entièrement lu ou qu'aucune transition n'est possible
5. Acceptation si un état final est atteint dans une branche

#### 2.2 Gestion des transitions non-déterministes

```python
def get_transitions(
    self, 
    state: str, 
    input_symbol: str, 
    stack_symbol: str
) -> Set[Tuple[str, str]]:
    """Récupère toutes les transitions possibles depuis un état donné.
    
    :param state: État source
    :param input_symbol: Symbole d'entrée (peut être ε)
    :param stack_symbol: Symbole de pile
    :return: Ensemble des transitions possibles
    :raises InvalidStateError: Si l'état n'existe pas
    """
```

#### 2.3 Simulation parallèle

```python
def _simulate_word_parallel(self, word: str) -> bool:
    """Simule la reconnaissance d'un mot de manière parallèle.
    
    :param word: Mot à simuler
    :return: True si le mot est accepté, False sinon
    """
```

**Caractéristiques :**
- Simulation parallèle de toutes les branches
- Gestion des transitions epsilon
- Optimisation avec mise en cache des configurations
- Limitation du nombre de branches parallèles
- Détection précoce des chemins acceptants

### 3. Algorithmes spécialisés

#### 3.1 Gestion des configurations parallèles

```python
@dataclass(frozen=True)
class NPDAConfiguration:
    """Configuration d'un NPDA (état, mot restant, pile, priorité)."""
    state: str
    remaining_input: str
    stack: str  # Représentation de la pile comme une chaîne
    priority: int = 0  # Priorité pour l'ordre de traitement
    branch_id: int = 0  # Identifiant de la branche
```

#### 3.2 Fermeture epsilon parallèle

```python
def _epsilon_closure_parallel(self, state: str, stack_symbol: str) -> Set[NPDAConfiguration]:
    """Calcule la fermeture epsilon parallèle pour un état et un symbole de pile.
    
    :param state: État de départ
    :param stack_symbol: Symbole de pile
    :return: Ensemble des configurations accessibles par transitions epsilon
    """
```

#### 3.3 Gestion des branches parallèles

```python
def _manage_parallel_branches(self, configurations: List[NPDAConfiguration]) -> List[NPDAConfiguration]:
    """Gère les branches parallèles en respectant les limites.
    
    :param configurations: Liste des configurations à traiter
    :return: Liste des configurations sélectionnées pour le traitement
    """
```

#### 3.4 Détection des calculs acceptants

```python
def _detect_accepting_computations(self, configurations: List[NPDAConfiguration]) -> bool:
    """Détecte si une configuration acceptante existe.
    
    :param configurations: Liste des configurations à vérifier
    :return: True si une configuration acceptante existe, False sinon
    """
```

### 4. Opérations sur les langages

#### 4.1 Union de NPDA

```python
def union(self, other: 'NPDA') -> 'NPDA':
    """Crée l'union de deux NPDA.
    
    :param other: Autre NPDA
    :return: NPDA reconnaissant l'union des langages
    :raises NPDAError: Si les NPDA ne sont pas compatibles
    """
```

#### 4.2 Concaténation de NPDA

```python
def concatenation(self, other: 'NPDA') -> 'NPDA':
    """Crée la concaténation de deux NPDA.
    
    :param other: Autre NPDA
    :return: NPDA reconnaissant la concaténation des langages
    :raises NPDAError: Si les NPDA ne sont pas compatibles
    """
```

#### 4.3 Étoile de Kleene

```python
def kleene_star(self) -> 'NPDA':
    """Crée l'étoile de Kleene d'un NPDA.
    
    :return: NPDA reconnaissant l'étoile de Kleene du langage
    :raises NPDAError: Si l'opération échoue
    """
```

### 5. Conversions

#### 5.1 Conversion PDA → NPDA

```python
@classmethod
def from_pda(cls, pda: 'PDA') -> 'NPDA':
    """Convertit un PDA en NPDA.
    
    :param pda: PDA à convertir
    :return: NPDA équivalent
    :raises NPDAError: Si la conversion échoue
    """
```

#### 5.2 Conversion NPDA → PDA

```python
def to_pda(self) -> 'PDA':
    """Convertit le NPDA en PDA.
    
    :return: PDA équivalent
    """
```

#### 5.3 Conversion DPDA → NPDA

```python
@classmethod
def from_dpda(cls, dpda: 'DPDA') -> 'NPDA':
    """Convertit un DPDA en NPDA.
    
    :param dpda: DPDA à convertir
    :return: NPDA équivalent
    :raises NPDAError: Si la conversion échoue
    """
```

### 6. Méthodes utilitaires

#### 6.1 Validation étendue

```python
def validate(self) -> bool:
    """Valide la cohérence de l'automate.
    
    :return: True si l'automate est valide, False sinon
    :raises InvalidNPDAError: Si l'automate n'est pas valide
    """
```

#### 6.2 Analyse de complexité

```python
def analyze_complexity(self) -> Dict[str, Any]:
    """Analyse la complexité de l'automate.
    
    :return: Dictionnaire avec les métriques de complexité
    """
```

**Métriques incluses :**
- Nombre maximum de branches parallèles
- Complexité temporelle moyenne
- Complexité spatiale
- Nombre de transitions epsilon
- Profondeur maximale de pile

#### 6.3 Statistiques de performance

```python
def get_performance_stats(self) -> Dict[str, Any]:
    """Récupère les statistiques de performance.
    
    :return: Dictionnaire avec les statistiques de performance
    """
```

#### 6.4 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]:
    """Convertit l'automate en dictionnaire.
    
    :return: Représentation dictionnaire de l'automate
    """

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'NPDA':
    """Crée un automate à partir d'un dictionnaire.
    
    :param data: Données de l'automate
    :return: Instance de NPDA
    :raises InvalidNPDAError: Si les données sont invalides
    """
```

### 7. Optimisations

#### 7.1 Optimisations parallèles

```python
def optimize_parallel_execution(self) -> 'NPDA':
    """Optimise l'exécution parallèle de l'automate.
    
    :return: NPDA optimisé
    :raises NPDAError: Si l'optimisation échoue
    """
```

**Optimisations implémentées :**
- Réduction du nombre de branches parallèles
- Optimisation des transitions epsilon
- Mise en cache des configurations fréquentes
- Élimination des branches redondantes

#### 7.2 Mise en cache avancée

- Cache des configurations visitées
- Cache des fermetures epsilon
- Cache des transitions calculées
- Cache des résultats de reconnaissance

#### 7.3 Optimisations de performance

- Simulation parallèle optimisée
- Structures de données spécialisées
- Gestion mémoire efficace
- Détection précoce des échecs

### 8. Gestion d'erreurs

#### 8.1 Exceptions personnalisées

```python
class NPDAError(Exception):
    """Exception de base pour les NPDA."""

class InvalidNPDAError(NPDAError):
    """Exception pour NPDA invalide."""

class NPDATimeoutError(NPDAError):
    """Exception pour timeout de calcul."""

class NPDAMemoryError(NPDAError):
    """Exception pour dépassement de mémoire."""

class NPDAConfigurationError(NPDAError):
    """Exception pour erreur de configuration."""

class NPDAConversionError(NPDAError):
    """Exception pour erreur de conversion."""
```

### 9. Tests unitaires

#### 9.1 Couverture de tests

- Tests de construction et validation
- Tests de reconnaissance de mots parallèle
- Tests des opérations sur les langages
- Tests de conversion avec autres types d'automates
- Tests de sérialisation/désérialisation
- Tests de performance et complexité
- Tests d'erreurs et cas limites

#### 9.2 Exemples de tests

```python
def test_npda_construction():
    """Test de construction d'un NPDA simple."""
    
def test_npda_parallel_recognition():
    """Test de reconnaissance de mots parallèle."""
    
def test_npda_branch_management():
    """Test de gestion des branches parallèles."""
    
def test_npda_epsilon_closure():
    """Test de fermeture epsilon parallèle."""
    
def test_npda_union():
    """Test de l'union de deux NPDA."""
    
def test_npda_concatenation():
    """Test de la concaténation de deux NPDA."""
    
def test_npda_kleene_star():
    """Test de l'étoile de Kleene."""
    
def test_npda_conversion():
    """Test de conversion avec PDA et DPDA."""
    
def test_npda_validation():
    """Test de validation d'un NPDA."""
    
def test_npda_serialization():
    """Test de sérialisation/désérialisation."""
    
def test_npda_performance():
    """Test de performance et complexité."""
    
def test_npda_optimization():
    """Test d'optimisation parallèle."""
```

### 10. Exemples d'utilisation

#### 10.1 NPDA pour le langage a^n b^n c^n

```python
# Construction d'un NPDA reconnaissant a^n b^n c^n
npda = NPDA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_alphabet={'a', 'b', 'c'},
    stack_alphabet={'Z', 'A', 'B'},
    transitions={
        ('q0', 'a', 'Z'): {('q0', 'AZ')},
        ('q0', 'a', 'A'): {('q0', 'AA')},
        ('q0', 'b', 'A'): {('q1', 'BA')},
        ('q1', 'b', 'A'): {('q1', 'BA')},
        ('q1', 'b', 'B'): {('q1', 'BB')},
        ('q1', 'c', 'B'): {('q2', '')},
        ('q2', 'c', 'B'): {('q2', '')},
        ('q2', '', 'Z'): {('q3', 'Z')}
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q3'},
    max_parallel_branches=100
)

# Test de reconnaissance
assert npda.accepts('aabbcc')  # True
assert npda.accepts('aaabbbccc')  # True
assert not npda.accepts('aabbc')  # False
```

#### 10.2 NPDA pour les palindromes avec centre

```python
# Construction d'un NPDA reconnaissant les palindromes avec centre
npda_palindrome = NPDA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_alphabet={'a', 'b', 'c'},
    stack_alphabet={'Z', 'A', 'B'},
    transitions={
        ('q0', 'a', 'Z'): {('q0', 'AZ')},
        ('q0', 'b', 'Z'): {('q0', 'BZ')},
        ('q0', 'a', 'A'): {('q0', 'AA')},
        ('q0', 'b', 'A'): {('q0', 'BA')},
        ('q0', 'a', 'B'): {('q0', 'AB')},
        ('q0', 'b', 'B'): {('q0', 'BB')},
        ('q0', 'c', 'A'): {('q1', '')},
        ('q0', 'c', 'B'): {('q1', '')},
        ('q1', 'a', 'A'): {('q1', '')},
        ('q1', 'b', 'B'): {('q1', '')},
        ('q1', '', 'Z'): {('q2', 'Z')}
    },
    initial_state='q0',
    initial_stack_symbol='Z',
    final_states={'q2'},
    max_parallel_branches=50
)
```

#### 10.3 Configuration des capacités parallèles

```python
# Configuration des paramètres d'exécution parallèle
npda.configure_parallel_execution(
    max_branches=500,
    timeout=5.0,
    memory_limit=50 * 1024 * 1024  # 50MB
)

# Analyse de la complexité
complexity = npda.analyze_complexity()
print(f"Complexité temporelle: {complexity['time_complexity']}")
print(f"Branches parallèles max: {complexity['max_parallel_branches']}")
```

### 11. Métriques de performance

#### 11.1 Objectifs de performance

- Reconnaissance de mots : < 200ms pour des mots de 1000 caractères
- Construction : < 100ms pour des automates de 100 états
- Mémoire : < 20MB pour des automates de 1000 états
- Branches parallèles : Gestion efficace jusqu'à 1000 branches

#### 11.2 Optimisations implémentées

- Simulation parallèle optimisée
- Structures de données spécialisées
- Mise en cache intelligente
- Gestion mémoire optimisée
- Détection précoce des échecs

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

- [ ] Classe NPDA implémentée selon les spécifications
- [ ] Simulation parallèle fonctionnelle
- [ ] Gestion des branches parallèles opérationnelle
- [ ] Détection des calculs acceptants implémentée
- [ ] Conversions avec PDA et DPDA opérationnelles
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
- Phase 003.002 : DPDA (pour les conversions)

## Notes d'implémentation

1. **Simulation parallèle** : Gestion efficace des branches parallèles
2. **Gestion des calculs acceptants** : Détection précoce des chemins acceptants
3. **Optimisations parallèles** : Algorithmes optimisés pour le non-déterminisme
4. **Analyse de complexité** : Métriques de performance et d'efficacité
5. **Performance** : Simulation parallèle plus rapide que les PDA séquentiels