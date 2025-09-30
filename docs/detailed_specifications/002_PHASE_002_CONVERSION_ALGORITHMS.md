# Spécifications Détaillées - Conversion Algorithms Implementation

## Vue d'ensemble

Cette spécification détaille l'implémentation des algorithmes de conversion entre différents types d'automates finis pour la phase 2 du projet Baobab Automata. Ces algorithmes permettent de convertir entre DFA, NFA, ε-NFA et expressions régulières.

## Objectifs

- Implémenter tous les algorithmes de conversion entre types d'automates
- Fournir des conversions bidirectionnelles
- Assurer l'équivalence des automates avant et après conversion
- Optimiser les performances des conversions

## Spécifications Techniques

### 1. Classe ConversionAlgorithms

#### 1.1 Structure de Base

**Fichier** : `src/baobab_automata/finite/conversion_algorithms.py`

**Attributs** :
- `cache: Dict[str, AbstractFiniteAutomaton]` - Cache des conversions
- `optimization_enabled: bool` - Activation des optimisations
- `max_states: int` - Limite du nombre d'états pour les conversions

#### 1.2 Constructeur

```python
def __init__(self, optimization_enabled: bool = True, max_states: int = 1000) -> None
```

**Configuration** :
- Optimisation activée par défaut
- Limite de 1000 états pour les conversions
- Cache vide initialement

### 2. Conversions NFA → DFA

#### 2.1 Algorithme des Sous-ensembles

```python
@staticmethod
def nfa_to_dfa(nfa: NFA) -> DFA
```

**Algorithme** :
1. Créer l'état initial du DFA (sous-ensemble contenant l'état initial du NFA)
2. Pour chaque état du DFA et chaque symbole :
   - Calculer l'union des transitions du NFA
   - Créer un nouvel état du DFA si nécessaire
3. Marquer comme finaux les états contenant au moins un état final du NFA

**Complexité** : O(2^n × |Σ|) où n est le nombre d'états du NFA

**Optimisations** :
- Élimination des états inaccessibles
- Fusion des états équivalents
- Cache des sous-ensembles fréquents

#### 2.2 Conversion Optimisée

```python
def nfa_to_dfa_optimized(self, nfa: NFA) -> DFA
```

**Stratégies d'optimisation** :
- Vérification du cache
- Construction incrémentale
- Élimination précoce des états inaccessibles
- Minimisation intégrée

### 3. Conversions ε-NFA → NFA

#### 3.1 Élimination des Transitions Epsilon

```python
@staticmethod
def epsilon_nfa_to_nfa(epsilon_nfa: εNFA) -> NFA
```

**Algorithme** :
1. Calculer la fermeture epsilon de chaque état
2. Pour chaque état et chaque symbole :
   - Calculer les transitions directes
   - Ajouter les transitions via epsilon
3. Ajuster les états finaux si nécessaire

**Complexité** : O(n² × |Σ|) où n est le nombre d'états

**Optimisations** :
- Cache des fermetures epsilon
- Construction incrémentale
- Élimination des états inaccessibles

#### 3.2 Conversion Optimisée

```python
def epsilon_nfa_to_nfa_optimized(self, epsilon_nfa: εNFA) -> NFA
```

**Stratégies** :
- Vérification du cache
- Calcul optimisé des fermetures epsilon
- Construction directe du NFA

### 4. Conversions ε-NFA → DFA

#### 4.1 Conversion Directe

```python
@staticmethod
def epsilon_nfa_to_dfa(epsilon_nfa: εNFA) -> DFA
```

**Algorithme** :
1. Utiliser l'algorithme des sous-ensembles avec fermeture epsilon
2. Calculer les fermetures epsilon à chaque étape
3. Construire directement le DFA

**Complexité** : O(2^n × |Σ|) où n est le nombre d'états

**Avantages** :
- Évite la conversion intermédiaire vers NFA
- Meilleure performance
- Moins de mémoire utilisée

#### 4.2 Conversion via NFA

```python
def epsilon_nfa_to_dfa_via_nfa(self, epsilon_nfa: εNFA) -> DFA
```

**Algorithme** :
1. Convertir ε-NFA → NFA
2. Convertir NFA → DFA
3. Optimiser le DFA résultant

**Utilisation** : Quand la conversion directe n'est pas possible

### 5. Conversions Expression Régulière → Automate

#### 5.1 Construction à partir d'AST

```python
@staticmethod
def regex_to_automaton(regex: str) -> AbstractFiniteAutomaton
```

**Algorithme** :
1. Parser l'expression régulière
2. Construire l'AST
3. Construire l'automate à partir de l'AST
4. Optimiser l'automate

**Complexité** : O(n) où n est la longueur de l'expression

**Types d'automates** :
- Préférer ε-NFA pour la construction
- Convertir vers DFA si nécessaire
- Optimiser selon le cas d'usage

#### 5.2 Construction Optimisée

```python
def regex_to_automaton_optimized(self, regex: str, target_type: str = 'epsilon_nfa') -> AbstractFiniteAutomaton
```

**Paramètres** :
- `target_type` : Type d'automate cible ('dfa', 'nfa', 'epsilon_nfa')
- Optimisation selon le type cible
- Cache des expressions fréquentes

### 6. Conversions Automate → Expression Régulière

#### 6.1 Algorithme de Kleene

```python
@staticmethod
def automaton_to_regex(automaton: AbstractFiniteAutomaton) -> str
```

**Algorithme** :
1. Convertir l'automate en DFA si nécessaire
2. Appliquer l'algorithme de Kleene
3. Simplifier l'expression résultante

**Complexité** : O(n³) où n est le nombre d'états

**Optimisations** :
- Simplification des expressions
- Élimination des redondances
- Formatage lisible

#### 6.2 Conversion Optimisée

```python
def automaton_to_regex_optimized(self, automaton: AbstractFiniteAutomaton) -> str
```

**Stratégies** :
- Vérification du cache
- Optimisation de l'algorithme de Kleene
- Simplification avancée

### 7. Méthodes Utilitaires

#### 7.1 Validation des Conversions

```python
def validate_conversion(self, original: AbstractFiniteAutomaton, 
                       converted: AbstractFiniteAutomaton) -> bool
```

**Vérifications** :
- Équivalence des langages
- Test sur un échantillon de mots
- Validation des propriétés

#### 7.2 Optimisation des Automates

```python
def optimize_automaton(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton
```

**Stratégies** :
- Minimisation des DFA
- Élimination des états inaccessibles
- Fusion des transitions identiques

#### 7.3 Cache Management

```python
def clear_cache(self) -> None
def get_cache_stats(self) -> Dict[str, Any]
def set_cache_size(self, size: int) -> None
```

**Fonctionnalités** :
- Gestion du cache
- Statistiques d'utilisation
- Configuration de la taille

### 8. Classes de Support

#### 8.1 ConversionError

```python
class ConversionError(Exception):
    """Exception de base pour les erreurs de conversion"""

class ConversionTimeoutError(ConversionError):
    """Timeout lors de la conversion"""

class ConversionMemoryError(ConversionError):
    """Erreur de mémoire lors de la conversion"""

class ConversionValidationError(ConversionError):
    """Erreur de validation de la conversion"""
```

#### 8.2 ConversionStats

```python
class ConversionStats:
    def __init__(self)
    def add_conversion(self, source_type: str, target_type: str, time: float)
    def get_stats(self) -> Dict[str, Any]
    def reset(self) -> None
```

### 9. Tests Unitaires

#### 9.1 Structure des Tests

**Fichier** : `tests/finite/test_conversion_algorithms.py`

**Classe** : `TestConversionAlgorithms`

#### 9.2 Cas de Test

1. **Conversions NFA → DFA** :
   - NFA simples
   - NFA complexes
   - Validation de l'équivalence
   - Performance des conversions

2. **Conversions ε-NFA → NFA** :
   - ε-NFA simples
   - ε-NFA complexes
   - Validation de l'équivalence
   - Performance des conversions

3. **Conversions ε-NFA → DFA** :
   - Conversion directe
   - Conversion via NFA
   - Validation de l'équivalence
   - Performance des conversions

4. **Conversions Expression → Automate** :
   - Expressions simples
   - Expressions complexes
   - Validation de l'équivalence
   - Performance des conversions

5. **Conversions Automate → Expression** :
   - DFA vers expression
   - NFA vers expression
   - ε-NFA vers expression
   - Validation de l'équivalence

6. **Performance** :
   - Automates avec beaucoup d'états
   - Conversions complexes
   - Cache des résultats

### 10. Contraintes de Performance

- **Temps de conversion NFA → DFA** : < 500ms pour NFA < 20 états
- **Temps de conversion ε-NFA → NFA** : < 100ms pour ε-NFA < 50 états
- **Temps de conversion ε-NFA → DFA** : < 1000ms pour ε-NFA < 20 états
- **Temps de conversion Expression → Automate** : < 50ms pour expressions < 1000 caractères
- **Temps de conversion Automate → Expression** : < 500ms pour automates < 50 états
- **Mémoire** : < 10MB pour conversions < 1000 états

### 11. Gestion d'Erreurs

#### 11.1 Exceptions Personnalisées

```python
class ConversionError(Exception):
    """Exception de base pour les erreurs de conversion"""

class ConversionTimeoutError(ConversionError):
    """Timeout lors de la conversion"""

class ConversionMemoryError(ConversionError):
    """Erreur de mémoire lors de la conversion"""

class ConversionValidationError(ConversionError):
    """Erreur de validation de la conversion"""
```

#### 11.2 Validation des Entrées

- Vérification des types d'automates
- Validation des paramètres
- Messages d'erreur explicites
- Gestion des timeouts

### 12. Documentation

#### 12.1 Docstrings

- Format reStructuredText
- Exemples d'utilisation
- Documentation des paramètres
- Documentation des exceptions

#### 12.2 Exemples d'Utilisation

```python
# Création du convertisseur
converter = ConversionAlgorithms()

# Conversion NFA → DFA
dfa = converter.nfa_to_dfa(nfa)

# Conversion ε-NFA → NFA
nfa = converter.epsilon_nfa_to_nfa(epsilon_nfa)

# Conversion ε-NFA → DFA
dfa = converter.epsilon_nfa_to_dfa(epsilon_nfa)

# Conversion Expression → Automate
automaton = converter.regex_to_automaton("a*b+")

# Conversion Automate → Expression
regex = converter.automaton_to_regex(automaton)

# Validation
assert converter.validate_conversion(original, converted)
```

### 13. Intégration

#### 13.1 Interfaces

- Compatibilité avec DFA, NFA, ε-NFA
- Support des conversions bidirectionnelles
- Intégration avec le parser d'expressions régulières

#### 13.2 Dépendances

- Dépend de DFA, NFA, ε-NFA
- Utilisation du parser d'expressions régulières
- Préparation pour les algorithmes d'optimisation

### 14. Critères de Validation

- [ ] Classe ConversionAlgorithms implémentée
- [ ] Toutes les conversions fonctionnelles
- [ ] Validation des conversions opérationnelle
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Performance conforme aux spécifications
- [ ] Documentation complète
- [ ] Gestion d'erreurs robuste
- [ ] Score Pylint >= 8.5/10
- [ ] Aucune vulnérabilité de sécurité

## Notes de Développement

1. **Priorité** : Cette classe peut être développée en parallèle avec le parser d'expressions régulières
2. **Performance** : Optimiser les algorithmes de conversion
3. **Robustesse** : Gestion d'erreurs complète
4. **Extensibilité** : Préparer pour les extensions futures
5. **Cache** : Implémenter un système de cache efficace