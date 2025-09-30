# Spécifications Détaillées - NFA Implementation

## Vue d'ensemble

Cette spécification détaille l'implémentation des Automates Finis Non-Déterministes (NFA) pour la phase 2 du projet Baobab Automata. Le NFA étend les capacités du DFA en permettant des transitions multiples pour un même symbole.

## Objectifs

- Implémenter une classe NFA complète et performante
- Fournir l'algorithme de reconnaissance non-déterministe
- Implémenter la conversion NFA → DFA (algorithme des sous-ensembles)
- Assurer la compatibilité avec l'architecture du projet

## Spécifications Techniques

### 1. Classe NFA

#### 1.1 Structure de Base

**Fichier** : `src/baobab_automata/finite/nfa.py`

**Héritage** : `AbstractFiniteAutomaton`

**Attributs** :
- `states: Set[str]` - Ensemble des états
- `alphabet: Set[str]` - Alphabet de l'automate
- `transitions: Dict[Tuple[str, str], Set[str]]` - Fonction de transition (peut retourner plusieurs états)
- `initial_state: str` - État initial
- `final_states: Set[str]` - Ensemble des états finaux

#### 1.2 Constructeur

```python
def __init__(self, states: Set[str], alphabet: Set[str], 
             transitions: Dict[Tuple[str, str], Set[str]], 
             initial_state: str, final_states: Set[str]) -> None
```

**Validation** :
- Vérifier que `initial_state` est dans `states`
- Vérifier que `final_states` est un sous-ensemble de `states`
- Vérifier que toutes les transitions sont valides
- Vérifier que l'alphabet est cohérent avec les transitions

#### 1.3 Méthodes de Base

##### `accepts(word: str) -> bool`
- Algorithme de reconnaissance non-déterministe
- Simulation de toutes les branches possibles
- Retourne `True` si au moins une branche accepte le mot

##### `get_transitions(state: str, symbol: str) -> Set[str]`
- Retourne l'ensemble des états de destination pour une transition donnée
- Retourne un ensemble vide si aucune transition n'existe

##### `is_final_state(state: str) -> bool`
- Vérifie si un état est final

##### `get_reachable_states() -> Set[str]`
- Retourne tous les états accessibles depuis l'état initial

### 2. Algorithme de Reconnaissance

#### 2.1 Simulation Non-Déterministe

```python
def _simulate_nfa(self, word: str) -> bool
```

**Algorithme** :
1. Initialiser avec l'état initial
2. Pour chaque symbole du mot :
   - Calculer tous les états possibles
   - Mettre à jour l'ensemble des états courants
3. Vérifier si au moins un état final est atteint

**Complexité** : O(n × m) où n est la longueur du mot et m le nombre d'états

#### 2.2 Optimisation avec Cache

```python
def _cached_simulation(self, word: str) -> bool
```

**Stratégie** :
- Mise en cache des résultats de simulation
- Réutilisation pour les sous-mots identiques
- Amélioration des performances pour les mots répétitifs

### 3. Conversion NFA → DFA

#### 3.1 Algorithme des Sous-ensembles

```python
def to_dfa(self) -> 'DFA'
```

**Algorithme** :
1. Créer l'état initial du DFA (sous-ensemble contenant l'état initial du NFA)
2. Pour chaque état du DFA et chaque symbole :
   - Calculer l'union des transitions du NFA
   - Créer un nouvel état du DFA si nécessaire
3. Marquer comme finaux les états contenant au moins un état final du NFA

**Complexité** : O(2^n × |Σ|) où n est le nombre d'états du NFA

#### 3.2 Optimisation des États

```python
def _optimize_dfa_states(self, dfa_states: Set[FrozenSet[str]]) -> Set[FrozenSet[str]]
```

**Stratégies** :
- Élimination des états inaccessibles
- Fusion des états équivalents
- Réduction de la taille de l'automate résultant

### 4. Méthodes Spécialisées

#### 4.1 États Accessibles

```python
def get_accessible_states(self) -> Set[str]
```

**Algorithme** :
1. Parcours en largeur depuis l'état initial
2. Collecte de tous les états atteignables
3. Retour de l'ensemble des états accessibles

#### 4.2 États Cœurs

```python
def get_coaccessible_states(self) -> Set[str]
```

**Algorithme** :
1. Parcours en largeur depuis les états finaux (sens inverse)
2. Collecte de tous les états pouvant atteindre un état final
3. Retour de l'ensemble des états cœurs

#### 4.3 États Utiles

```python
def get_useful_states(self) -> Set[str]
```

**Algorithme** :
- Intersection des états accessibles et cœurs
- Élimination des états inutiles

### 5. Opérations sur les Langages

#### 5.1 Union

```python
def union(self, other: 'NFA') -> 'NFA'
```

**Algorithme** :
1. Créer un nouvel état initial
2. Connecter aux états initiaux des deux NFA
3. Préserver tous les états et transitions

#### 5.2 Concaténation

```python
def concatenation(self, other: 'NFA') -> 'NFA'
```

**Algorithme** :
1. Connecter les états finaux du premier NFA à l'état initial du second
2. Ajuster les états finaux

#### 5.3 Étoile de Kleene

```python
def kleene_star(self) -> 'NFA'
```

**Algorithme** :
1. Ajouter un nouvel état initial
2. Connecter l'ancien état initial aux états finaux
3. Marquer le nouvel état initial comme final

### 6. Méthodes Utilitaires

#### 6.1 Validation

```python
def validate(self) -> bool
```

**Vérifications** :
- Cohérence des transitions
- Existence de l'état initial
- Validité de l'alphabet
- Vérification des ensembles de transitions

#### 6.2 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]
def from_dict(data: Dict[str, Any]) -> 'NFA'
```

**Format** :
```json
{
    "states": ["q0", "q1", "q2"],
    "alphabet": ["a", "b"],
    "transitions": {
        "q0,a": ["q1", "q2"],
        "q1,b": ["q2"]
    },
    "initial_state": "q0",
    "final_states": ["q2"]
}
```

#### 6.3 Conversion vers DFA

```python
def to_dfa(self) -> 'DFA'
```

**Implémentation** :
- Utilisation de l'algorithme des sous-ensembles
- Optimisation des états résultants
- Validation du DFA généré

### 7. Tests Unitaires

#### 7.1 Structure des Tests

**Fichier** : `tests/finite/test_nfa.py`

**Classe** : `TestNFA`

#### 7.2 Cas de Test

1. **Construction** :
   - Construction valide
   - Construction avec paramètres invalides
   - Validation des attributs

2. **Reconnaissance** :
   - Mots acceptés (cas déterministes)
   - Mots acceptés (cas non-déterministes)
   - Mots rejetés
   - Mots vides
   - Mots avec symboles invalides

3. **Conversion DFA** :
   - Conversion de NFA simple
   - Conversion de NFA complexe
   - Validation de l'équivalence
   - Performance de la conversion

4. **Opérations** :
   - Union de NFA
   - Concaténation de NFA
   - Étoile de Kleene

5. **Performance** :
   - NFA avec beaucoup d'états
   - Mots longs
   - Conversions complexes

### 8. Contraintes de Performance

- **Temps de reconnaissance** : < 50ms pour mots < 1000 symboles
- **Temps de conversion** : < 500ms pour NFA < 20 états
- **Mémoire** : < 2MB pour NFA < 1000 états
- **Scalabilité** : Support jusqu'à 50 états (conversion DFA)

### 9. Gestion d'Erreurs

#### 9.1 Exceptions Personnalisées

```python
class NFAError(Exception):
    """Exception de base pour les erreurs NFA"""

class InvalidNFAError(NFAError):
    """NFA invalide"""

class InvalidTransitionError(NFAError):
    """Transition invalide"""

class ConversionError(NFAError):
    """Erreur lors de la conversion"""
```

#### 9.2 Validation des Entrées

- Vérification des types
- Validation des ensembles de transitions
- Messages d'erreur explicites

### 10. Documentation

#### 10.1 Docstrings

- Format reStructuredText
- Exemples d'utilisation
- Documentation des paramètres
- Documentation des exceptions

#### 10.2 Exemples d'Utilisation

```python
# Création d'un NFA simple
nfa = NFA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'a'): {'q1', 'q2'},
        ('q1', 'b'): {'q2'}
    },
    initial_state='q0',
    final_states={'q2'}
)

# Reconnaissance de mots
assert nfa.accepts('ab') == True
assert nfa.accepts('a') == False

# Conversion vers DFA
dfa = nfa.to_dfa()

# Opérations
union_nfa = nfa1.union(nfa2)
```

### 11. Intégration

#### 11.1 Interfaces

- Implémentation de `AbstractFiniteAutomaton`
- Compatibilité avec DFA
- Support des conversions

#### 11.2 Dépendances

- Dépend de DFA (pour la conversion)
- Utilisation des interfaces de la phase 1
- Préparation pour les conversions vers ε-NFA

### 12. Critères de Validation

- [ ] Classe NFA implémentée
- [ ] Algorithme de reconnaissance fonctionnel
- [ ] Conversion NFA → DFA opérationnelle
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Performance conforme aux spécifications
- [ ] Documentation complète
- [ ] Gestion d'erreurs robuste
- [ ] Score Pylint >= 8.5/10
- [ ] Aucune vulnérabilité de sécurité

## Notes de Développement

1. **Priorité** : Cette classe doit être implémentée après DFA
2. **Performance** : Optimiser l'algorithme de reconnaissance
3. **Conversion** : Implémenter l'algorithme des sous-ensembles efficacement
4. **Robustesse** : Gestion d'erreurs complète
5. **Extensibilité** : Préparer pour les ε-NFA
