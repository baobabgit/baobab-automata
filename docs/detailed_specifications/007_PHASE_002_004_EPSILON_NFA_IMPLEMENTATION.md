# Spécifications Détaillées - ε-NFA Implementation

## Vue d'ensemble

Cette spécification détaille l'implémentation des Automates Finis Non-Déterministes avec transitions epsilon (ε-NFA) pour la phase 2 du projet Baobab Automata. Les ε-NFA étendent les NFA en permettant des transitions vides (epsilon).

## Objectifs

- Implémenter une classe ε-NFA complète et performante
- Fournir l'algorithme de reconnaissance avec fermeture epsilon
- Implémenter les conversions ε-NFA → NFA et ε-NFA → DFA
- Assurer la compatibilité avec l'architecture du projet

## Spécifications Techniques

### 1. Classe ε-NFA

#### 1.1 Structure de Base

**Fichier** : `src/baobab_automata/finite/epsilon_nfa.py`

**Héritage** : `AbstractFiniteAutomaton`

**Attributs** :
- `states: Set[str]` - Ensemble des états
- `alphabet: Set[str]` - Alphabet de l'automate (sans epsilon)
- `transitions: Dict[Tuple[str, str], Set[str]]` - Fonction de transition (peut inclure epsilon)
- `initial_state: str` - État initial
- `final_states: Set[str]` - Ensemble des états finaux
- `epsilon_symbol: str` - Symbole epsilon (par défaut 'ε')

#### 1.2 Constructeur

```python
def __init__(self, states: Set[str], alphabet: Set[str], 
             transitions: Dict[Tuple[str, str], Set[str]], 
             initial_state: str, final_states: Set[str],
             epsilon_symbol: str = 'ε') -> None
```

**Validation** :
- Vérifier que `initial_state` est dans `states`
- Vérifier que `final_states` est un sous-ensemble de `states`
- Vérifier que toutes les transitions sont valides
- Vérifier que l'alphabet est cohérent avec les transitions
- Vérifier que l'epsilon_symbol n'est pas dans l'alphabet

#### 1.3 Méthodes de Base

##### `accepts(word: str) -> bool`
- Algorithme de reconnaissance avec fermeture epsilon
- Simulation de toutes les branches possibles incluant les transitions epsilon
- Retourne `True` si au moins une branche accepte le mot

##### `get_transitions(state: str, symbol: str) -> Set[str]`
- Retourne l'ensemble des états de destination pour une transition donnée
- Retourne un ensemble vide si aucune transition n'existe

##### `is_final_state(state: str) -> bool`
- Vérifie si un état est final

##### `get_reachable_states() -> Set[str]`
- Retourne tous les états accessibles depuis l'état initial

### 2. Algorithme de Reconnaissance

#### 2.1 Fermeture Epsilon

```python
def epsilon_closure(self, states: Set[str]) -> Set[str]
```

**Algorithme** :
1. Initialiser avec l'ensemble d'états donné
2. Répéter jusqu'à convergence :
   - Ajouter tous les états accessibles par des transitions epsilon
   - Mettre à jour l'ensemble des états
3. Retourner l'ensemble final

**Complexité** : O(n²) où n est le nombre d'états

#### 2.2 Simulation avec Epsilon

```python
def _simulate_epsilon_nfa(self, word: str) -> bool
```

**Algorithme** :
1. Calculer la fermeture epsilon de l'état initial
2. Pour chaque symbole du mot :
   - Calculer les transitions pour le symbole
   - Calculer la fermeture epsilon du résultat
   - Mettre à jour l'ensemble des états courants
3. Vérifier si au moins un état final est atteint

**Complexité** : O(n × m × k) où n est la longueur du mot, m le nombre d'états et k le nombre de transitions epsilon

#### 2.3 Optimisation avec Cache

```python
def _cached_epsilon_closure(self, states: Set[str]) -> Set[str]
```

**Stratégie** :
- Mise en cache des fermetures epsilon
- Réutilisation pour les mêmes ensembles d'états
- Amélioration des performances pour les calculs répétitifs

### 3. Conversions

#### 3.1 ε-NFA → NFA

```python
def to_nfa(self) -> 'NFA'
```

**Algorithme** :
1. Calculer la fermeture epsilon de chaque état
2. Pour chaque état et chaque symbole :
   - Calculer les transitions directes
   - Ajouter les transitions via epsilon
3. Ajuster les états finaux si nécessaire

**Complexité** : O(n² × |Σ|) où n est le nombre d'états

#### 3.2 ε-NFA → DFA

```python
def to_dfa(self) -> 'DFA'
```

**Algorithme** :
1. Convertir vers NFA
2. Convertir le NFA vers DFA
3. Optimiser le DFA résultant

**Complexité** : O(2^n × |Σ|) où n est le nombre d'états

#### 3.3 Conversion Directe ε-NFA → DFA

```python
def to_dfa_direct(self) -> 'DFA'
```

**Algorithme** :
1. Utiliser l'algorithme des sous-ensembles avec fermeture epsilon
2. Calculer les fermetures epsilon à chaque étape
3. Construire directement le DFA

**Avantage** : Évite la conversion intermédiaire vers NFA

### 4. Méthodes Spécialisées

#### 4.1 États Accessibles

```python
def get_accessible_states(self) -> Set[str]
```

**Algorithme** :
1. Parcours en largeur depuis l'état initial
2. Inclure les transitions epsilon
3. Collecte de tous les états atteignables

#### 4.2 États Cœurs

```python
def get_coaccessible_states(self) -> Set[str]
```

**Algorithme** :
1. Parcours en largeur depuis les états finaux (sens inverse)
2. Inclure les transitions epsilon inverses
3. Collecte de tous les états pouvant atteindre un état final

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
def union(self, other: 'εNFA') -> 'εNFA'
```

**Algorithme** :
1. Créer un nouvel état initial
2. Connecter via epsilon aux états initiaux des deux ε-NFA
3. Préserver tous les états et transitions

#### 5.2 Concaténation

```python
def concatenation(self, other: 'εNFA') -> 'εNFA'
```

**Algorithme** :
1. Connecter les états finaux du premier ε-NFA à l'état initial du second via epsilon
2. Ajuster les états finaux

#### 5.3 Étoile de Kleene

```python
def kleene_star(self) -> 'εNFA'
```

**Algorithme** :
1. Ajouter un nouvel état initial
2. Connecter l'ancien état initial aux états finaux via epsilon
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
- Validation des transitions epsilon

#### 6.2 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]
def from_dict(data: Dict[str, Any]) -> 'εNFA'
```

**Format** :
```json
{
    "states": ["q0", "q1", "q2"],
    "alphabet": ["a", "b"],
    "transitions": {
        "q0,ε": ["q1"],
        "q0,a": ["q2"],
        "q1,b": ["q2"]
    },
    "initial_state": "q0",
    "final_states": ["q2"],
    "epsilon_symbol": "ε"
}
```

#### 6.3 Conversion vers NFA

```python
def to_nfa(self) -> 'NFA'
```

**Implémentation** :
- Utilisation de l'algorithme d'élimination des transitions epsilon
- Optimisation des états résultants
- Validation du NFA généré

#### 6.4 Conversion vers DFA

```python
def to_dfa(self) -> 'DFA'
```

**Implémentation** :
- Conversion directe ou via NFA
- Optimisation des états résultants
- Validation du DFA généré

### 7. Tests Unitaires

#### 7.1 Structure des Tests

**Fichier** : `tests/finite/test_epsilon_nfa.py`

**Classe** : `TestEpsilonNFA`

#### 7.2 Cas de Test

1. **Construction** :
   - Construction valide
   - Construction avec paramètres invalides
   - Validation des attributs

2. **Reconnaissance** :
   - Mots acceptés (cas déterministes)
   - Mots acceptés (cas non-déterministes)
   - Mots acceptés (cas avec epsilon)
   - Mots rejetés
   - Mots vides
   - Mots avec symboles invalides

3. **Fermeture Epsilon** :
   - Fermeture simple
   - Fermeture complexe
   - Fermeture avec cycles
   - Performance de la fermeture

4. **Conversions** :
   - Conversion vers NFA
   - Conversion vers DFA
   - Validation de l'équivalence
   - Performance des conversions

5. **Opérations** :
   - Union de ε-NFA
   - Concaténation de ε-NFA
   - Étoile de Kleene

6. **Performance** :
   - ε-NFA avec beaucoup d'états
   - Mots longs
   - Conversions complexes

### 8. Contraintes de Performance

- **Temps de reconnaissance** : < 100ms pour mots < 1000 symboles
- **Temps de fermeture epsilon** : < 10ms pour ε-NFA < 100 états
- **Temps de conversion** : < 1000ms pour ε-NFA < 20 états
- **Mémoire** : < 3MB pour ε-NFA < 1000 états
- **Scalabilité** : Support jusqu'à 50 états (conversion DFA)

### 9. Gestion d'Erreurs

#### 9.1 Exceptions Personnalisées

```python
class EpsilonNFAError(Exception):
    """Exception de base pour les erreurs ε-NFA"""

class InvalidEpsilonNFAError(EpsilonNFAError):
    """ε-NFA invalide"""

class InvalidEpsilonTransitionError(EpsilonNFAError):
    """Transition epsilon invalide"""

class ConversionError(EpsilonNFAError):
    """Erreur lors de la conversion"""
```

#### 9.2 Validation des Entrées

- Vérification des types
- Validation des ensembles de transitions
- Validation des transitions epsilon
- Messages d'erreur explicites

### 10. Documentation

#### 10.1 Docstrings

- Format reStructuredText
- Exemples d'utilisation
- Documentation des paramètres
- Documentation des exceptions

#### 10.2 Exemples d'Utilisation

```python
# Création d'un ε-NFA simple
epsilon_nfa = εNFA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'ε'): {'q1'},
        ('q0', 'a'): {'q2'},
        ('q1', 'b'): {'q2'}
    },
    initial_state='q0',
    final_states={'q2'}
)

# Reconnaissance de mots
assert epsilon_nfa.accepts('ab') == True
assert epsilon_nfa.accepts('a') == True  # Via epsilon

# Fermeture epsilon
closure = epsilon_nfa.epsilon_closure({'q0'})
assert closure == {'q0', 'q1'}

# Conversions
nfa = epsilon_nfa.to_nfa()
dfa = epsilon_nfa.to_dfa()

# Opérations
union_epsilon_nfa = epsilon_nfa1.union(epsilon_nfa2)
```

### 11. Intégration

#### 11.1 Interfaces

- Implémentation de `AbstractFiniteAutomaton`
- Compatibilité avec NFA et DFA
- Support des conversions

#### 11.2 Dépendances

- Dépend de NFA et DFA (pour les conversions)
- Utilisation des interfaces de la phase 1
- Préparation pour les expressions régulières

### 12. Critères de Validation

- [ ] Classe ε-NFA implémentée
- [ ] Algorithme de reconnaissance avec fermeture epsilon fonctionnel
- [ ] Conversions ε-NFA → NFA et ε-NFA → DFA opérationnelles
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Performance conforme aux spécifications
- [ ] Documentation complète
- [ ] Gestion d'erreurs robuste
- [ ] Score Pylint >= 8.5/10
- [ ] Aucune vulnérabilité de sécurité

## Notes de Développement

1. **Priorité** : Cette classe doit être implémentée après NFA
2. **Performance** : Optimiser l'algorithme de fermeture epsilon
3. **Conversion** : Implémenter les conversions efficacement
4. **Robustesse** : Gestion d'erreurs complète
5. **Extensibilité** : Préparer pour les expressions régulières
