# Spécifications Détaillées - Phase 003.006 - Implémentation des Algorithmes Spécialisés

## Vue d'ensemble

Cette spécification détaille l'implémentation des algorithmes spécialisés pour les grammaires hors-contexte et les automates à pile. Ces algorithmes incluent CYK (Cocke-Younger-Kasami), Earley, et d'autres algorithmes avancés pour l'analyse syntaxique et la manipulation des grammaires.

## Objectifs

- Implémenter l'algorithme CYK pour l'analyse syntaxique
- Implémenter l'algorithme Earley pour le parsing
- Détecter et éliminer la récursivité gauche
- Éliminer les productions vides
- Normaliser les grammaires
- Fournir des algorithmes d'analyse avancés

## Architecture

### Classe principale : SpecializedAlgorithms

```python
class SpecializedAlgorithms:
    """Algorithmes spécialisés pour les grammaires hors-contexte et les automates à pile."""
```

### Types d'algorithmes supportés

- **CYK** : Algorithme de parsing pour les grammaires en forme normale de Chomsky
- **Earley** : Algorithme de parsing général pour les grammaires hors-contexte
- **Élimination de récursivité gauche** : Algorithmes pour éliminer la récursivité gauche
- **Élimination de productions vides** : Algorithmes pour éliminer les productions vides
- **Normalisation** : Algorithmes de normalisation des grammaires

## Spécifications détaillées

### 1. Constructeur et initialisation

#### 1.1 Constructeur principal

```python
def __init__(
    self,
    enable_caching: bool = True,
    max_cache_size: int = 1000,
    timeout: float = 60.0
) -> None:
    """Initialise les algorithmes spécialisés.
    
    :param enable_caching: Active la mise en cache des résultats
    :param max_cache_size: Taille maximale du cache
    :param timeout: Timeout en secondes pour les algorithmes
    :raises AlgorithmError: Si l'initialisation échoue
    """
```

#### 1.2 Configuration des algorithmes

```python
def configure_algorithm(
    self,
    algorithm_type: str,
    parameters: Dict[str, Any]
) -> None:
    """Configure un algorithme spécifique.
    
    :param algorithm_type: Type d'algorithme à configurer
    :param parameters: Paramètres de configuration
    :raises AlgorithmError: Si la configuration échoue
    """
```

### 2. Algorithme CYK

#### 2.1 Implémentation de base

```python
def cyk_parse(
    self, 
    grammar: ContextFreeGrammar, 
    word: str
) -> bool:
    """Parse un mot avec l'algorithme CYK.
    
    :param grammar: Grammaire en forme normale de Chomsky
    :param word: Mot à parser
    :return: True si le mot est généré par la grammaire, False sinon
    :raises AlgorithmError: Si le parsing échoue
    :raises AlgorithmTimeoutError: Si le parsing dépasse le timeout
    """
```

**Algorithme CYK :**
1. Vérification que la grammaire est en forme normale de Chomsky
2. Construction de la table de parsing CYK
3. Remplissage de la table avec les productions
4. Vérification de l'appartenance du mot au langage

#### 2.2 CYK avec arbre de dérivation

```python
def cyk_parse_with_tree(
    self, 
    grammar: ContextFreeGrammar, 
    word: str
) -> Optional[ParseTree]:
    """Parse un mot avec l'algorithme CYK et retourne l'arbre de dérivation.
    
    :param grammar: Grammaire en forme normale de Chomsky
    :param word: Mot à parser
    :return: Arbre de dérivation ou None si le mot n'est pas généré
    :raises AlgorithmError: Si le parsing échoue
    """
```

#### 2.3 CYK optimisé

```python
def cyk_parse_optimized(
    self, 
    grammar: ContextFreeGrammar, 
    word: str
) -> bool:
    """Parse un mot avec l'algorithme CYK optimisé.
    
    :param grammar: Grammaire en forme normale de Chomsky
    :param word: Mot à parser
    :return: True si le mot est généré par la grammaire, False sinon
    :raises AlgorithmError: Si le parsing échoue
    """
```

**Optimisations implémentées :**
- Mise en cache des résultats intermédiaires
- Optimisation de la structure de données
- Détection précoce des échecs
- Gestion mémoire efficace

### 3. Algorithme Earley

#### 3.1 Implémentation de base

```python
def earley_parse(
    self, 
    grammar: ContextFreeGrammar, 
    word: str
) -> bool:
    """Parse un mot avec l'algorithme Earley.
    
    :param grammar: Grammaire hors-contexte
    :param word: Mot à parser
    :return: True si le mot est généré par la grammaire, False sinon
    :raises AlgorithmError: Si le parsing échoue
    :raises AlgorithmTimeoutError: Si le parsing dépasse le timeout
    """
```

**Algorithme Earley :**
1. Initialisation avec l'état de départ
2. Construction des états pour chaque position
3. Application des règles de prédiction, scan et complétion
4. Vérification de l'acceptation

#### 3.2 Earley avec arbre de dérivation

```python
def earley_parse_with_tree(
    self, 
    grammar: ContextFreeGrammar, 
    word: str
) -> Optional[ParseTree]:
    """Parse un mot avec l'algorithme Earley et retourne l'arbre de dérivation.
    
    :param grammar: Grammaire hors-contexte
    :param word: Mot à parser
    :return: Arbre de dérivation ou None si le mot n'est pas généré
    :raises AlgorithmError: Si le parsing échoue
    """
```

#### 3.3 Earley optimisé

```python
def earley_parse_optimized(
    self, 
    grammar: ContextFreeGrammar, 
    word: str
) -> bool:
    """Parse un mot avec l'algorithme Earley optimisé.
    
    :param grammar: Grammaire hors-contexte
    :param word: Mot à parser
    :return: True si le mot est généré par la grammaire, False sinon
    :raises AlgorithmError: Si le parsing échoue
    """
```

**Optimisations implémentées :**
- Mise en cache des états
- Optimisation des règles de prédiction
- Détection précoce des échecs
- Gestion mémoire efficace

### 4. Élimination de la récursivité gauche

#### 4.1 Détection de récursivité gauche

```python
def detect_left_recursion(self, grammar: ContextFreeGrammar) -> Dict[str, List[str]]:
    """Détecte la récursivité gauche dans une grammaire.
    
    :param grammar: Grammaire à analyser
    :return: Dictionnaire des variables avec récursivité gauche
    :raises AlgorithmError: Si l'analyse échoue
    """
```

#### 4.2 Élimination de récursivité gauche

```python
def eliminate_left_recursion(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Élimine la récursivité gauche d'une grammaire.
    
    :param grammar: Grammaire à traiter
    :return: Grammaire sans récursivité gauche
    :raises AlgorithmError: Si l'élimination échoue
    """
```

**Algorithme d'élimination :**
1. Détection des variables avec récursivité gauche
2. Application de la transformation A → Aα | β → A → βA', A' → αA' | ε
3. Validation de la grammaire résultante

#### 4.3 Élimination de récursivité gauche indirecte

```python
def eliminate_indirect_left_recursion(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Élimine la récursivité gauche indirecte d'une grammaire.
    
    :param grammar: Grammaire à traiter
    :return: Grammaire sans récursivité gauche indirecte
    :raises AlgorithmError: Si l'élimination échoue
    """
```

### 5. Élimination des productions vides

#### 5.1 Détection des productions vides

```python
def detect_empty_productions(self, grammar: ContextFreeGrammar) -> Set[str]:
    """Détecte les variables qui peuvent générer le mot vide.
    
    :param grammar: Grammaire à analyser
    :return: Ensemble des variables générant le mot vide
    :raises AlgorithmError: Si l'analyse échoue
    """
```

#### 5.2 Élimination des productions vides

```python
def eliminate_empty_productions(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Élimine les productions vides d'une grammaire.
    
    :param grammar: Grammaire à traiter
    :return: Grammaire sans productions vides
    :raises AlgorithmError: Si l'élimination échoue
    """
```

**Algorithme d'élimination :**
1. Détection des variables générant le mot vide
2. Ajout des productions sans ces variables
3. Suppression des productions vides
4. Validation de la grammaire résultante

### 6. Normalisation des grammaires

#### 6.1 Forme normale de Chomsky

```python
def to_chomsky_normal_form(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Convertit une grammaire en forme normale de Chomsky.
    
    :param grammar: Grammaire à convertir
    :return: Grammaire en forme normale de Chomsky
    :raises AlgorithmError: Si la conversion échoue
    """
```

**Étapes de conversion :**
1. Élimination des productions vides
2. Élimination des productions unitaires
3. Élimination des symboles inaccessibles
4. Élimination des symboles non-générateurs
5. Conversion en productions binaires

#### 6.2 Forme normale de Greibach

```python
def to_greibach_normal_form(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
    """Convertit une grammaire en forme normale de Greibach.
    
    :param grammar: Grammaire à convertir
    :return: Grammaire en forme normale de Greibach
    :raises AlgorithmError: Si la conversion échoue
    """
```

**Étapes de conversion :**
1. Conversion en forme normale de Chomsky
2. Élimination de la récursivité gauche
3. Conversion en productions de la forme A → aα

### 7. Analyse avancée des grammaires

#### 7.1 Détection d'ambiguïté

```python
def detect_ambiguity(self, grammar: ContextFreeGrammar) -> bool:
    """Détecte si une grammaire est ambiguë.
    
    :param grammar: Grammaire à analyser
    :return: True si la grammaire est ambiguë, False sinon
    :raises AlgorithmError: Si l'analyse échoue
    """
```

#### 7.2 Analyse de la récursivité

```python
def analyze_recursion(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
    """Analyse la récursivité d'une grammaire.
    
    :param grammar: Grammaire à analyser
    :return: Dictionnaire avec l'analyse de récursivité
    :raises AlgorithmError: Si l'analyse échoue
    """
```

#### 7.3 Analyse des symboles

```python
def analyze_symbols(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
    """Analyse les symboles d'une grammaire.
    
    :param grammar: Grammaire à analyser
    :return: Dictionnaire avec l'analyse des symboles
    :raises AlgorithmError: Si l'analyse échoue
    """
```

### 8. Méthodes utilitaires

#### 8.1 Gestion du cache

```python
def clear_cache(self) -> None:
    """Vide le cache des algorithmes."""

def get_cache_stats(self) -> Dict[str, Any]:
    """Récupère les statistiques du cache.
    
    :return: Dictionnaire avec les statistiques du cache
    """
```

#### 8.2 Métriques de performance

```python
def get_performance_stats(self) -> Dict[str, Any]:
    """Récupère les statistiques de performance.
    
    :return: Dictionnaire avec les statistiques de performance
    """
```

#### 8.3 Sérialisation

```python
def to_dict(self) -> Dict[str, Any]:
    """Convertit les algorithmes en dictionnaire.
    
    :return: Représentation dictionnaire des algorithmes
    """

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'SpecializedAlgorithms':
    """Crée les algorithmes à partir d'un dictionnaire.
    
    :param data: Données des algorithmes
    :return: Instance des algorithmes
    :raises AlgorithmError: Si les données sont invalides
    """
```

### 9. Gestion d'erreurs

#### 9.1 Exceptions personnalisées

```python
class AlgorithmError(Exception):
    """Exception de base pour les algorithmes."""

class AlgorithmTimeoutError(AlgorithmError):
    """Exception pour timeout d'algorithme."""

class AlgorithmMemoryError(AlgorithmError):
    """Exception pour dépassement de mémoire."""

class AlgorithmValidationError(AlgorithmError):
    """Exception pour erreur de validation."""

class AlgorithmOptimizationError(AlgorithmError):
    """Exception pour erreur d'optimisation."""
```

### 10. Tests unitaires

#### 10.1 Couverture de tests

- Tests de l'algorithme CYK
- Tests de l'algorithme Earley
- Tests d'élimination de récursivité gauche
- Tests d'élimination de productions vides
- Tests de normalisation des grammaires
- Tests d'analyse avancée
- Tests de sérialisation/désérialisation
- Tests de performance
- Tests d'erreurs et cas limites

#### 10.2 Exemples de tests

```python
def test_cyk_parse():
    """Test de l'algorithme CYK."""
    
def test_cyk_parse_with_tree():
    """Test de CYK avec arbre de dérivation."""
    
def test_cyk_parse_optimized():
    """Test de CYK optimisé."""
    
def test_earley_parse():
    """Test de l'algorithme Earley."""
    
def test_earley_parse_with_tree():
    """Test d'Earley avec arbre de dérivation."""
    
def test_earley_parse_optimized():
    """Test d'Earley optimisé."""
    
def test_detect_left_recursion():
    """Test de détection de récursivité gauche."""
    
def test_eliminate_left_recursion():
    """Test d'élimination de récursivité gauche."""
    
def test_eliminate_indirect_left_recursion():
    """Test d'élimination de récursivité gauche indirecte."""
    
def test_detect_empty_productions():
    """Test de détection de productions vides."""
    
def test_eliminate_empty_productions():
    """Test d'élimination de productions vides."""
    
def test_to_chomsky_normal_form():
    """Test de conversion en forme normale de Chomsky."""
    
def test_to_greibach_normal_form():
    """Test de conversion en forme normale de Greibach."""
    
def test_detect_ambiguity():
    """Test de détection d'ambiguïté."""
    
def test_analyze_recursion():
    """Test d'analyse de récursivité."""
    
def test_analyze_symbols():
    """Test d'analyse des symboles."""
    
def test_algorithm_serialization():
    """Test de sérialisation/désérialisation."""
```

### 11. Exemples d'utilisation

#### 11.1 Parsing avec CYK

```python
# Grammaire en forme normale de Chomsky
grammar = ContextFreeGrammar(
    variables={'S', 'A', 'B'},
    terminals={'a', 'b'},
    productions={
        Production('S', ['A', 'B']),
        Production('A', ['a']),
        Production('B', ['b'])
    },
    start_symbol='S'
)

# Parsing avec CYK
algorithms = SpecializedAlgorithms()
result = algorithms.cyk_parse(grammar, 'ab')
assert result  # True

# Parsing avec arbre de dérivation
tree = algorithms.cyk_parse_with_tree(grammar, 'ab')
assert tree is not None
```

#### 11.2 Parsing avec Earley

```python
# Grammaire générale
grammar = ContextFreeGrammar(
    variables={'S', 'A'},
    terminals={'a', 'b'},
    productions={
        Production('S', ['a', 'A']),
        Production('A', ['b']),
        Production('A', ['A', 'b'])
    },
    start_symbol='S'
)

# Parsing avec Earley
algorithms = SpecializedAlgorithms()
result = algorithms.earley_parse(grammar, 'abb')
assert result  # True
```

#### 11.3 Élimination de récursivité gauche

```python
# Grammaire avec récursivité gauche
grammar = ContextFreeGrammar(
    variables={'S', 'A'},
    terminals={'a', 'b'},
    productions={
        Production('S', ['S', 'a']),
        Production('S', ['b'])
    },
    start_symbol='S'
)

# Élimination de récursivité gauche
algorithms = SpecializedAlgorithms()
new_grammar = algorithms.eliminate_left_recursion(grammar)

# Vérification que la récursivité gauche est éliminée
left_recursion = algorithms.detect_left_recursion(new_grammar)
assert not left_recursion  # Aucune récursivité gauche
```

### 12. Métriques de performance

#### 12.1 Objectifs de performance

- CYK : < 100ms pour des mots de 1000 caractères
- Earley : < 200ms pour des mots de 1000 caractères
- Élimination de récursivité gauche : < 50ms pour des grammaires de 100 productions
- Élimination de productions vides : < 30ms pour des grammaires de 100 productions
- Normalisation : < 150ms pour des grammaires de 100 productions

#### 12.2 Optimisations implémentées

- Mise en cache des résultats
- Algorithmes optimisés
- Gestion mémoire efficace
- Détection précoce des échecs

### 13. Documentation

#### 13.1 Docstrings

- Documentation complète de toutes les méthodes
- Exemples d'utilisation dans les docstrings
- Spécification des paramètres et valeurs de retour
- Documentation des exceptions possibles

#### 13.2 Exemples

- Exemples d'utilisation dans la documentation
- Cas d'usage typiques
- Guide de migration depuis les algorithmes existants

### 14. Intégration

#### 14.1 Interface commune

- Compatibilité avec les grammaires hors-contexte
- Interface unifiée pour les algorithmes
- Support des différents types de grammaires

#### 14.2 Extensibilité

- Architecture modulaire pour les extensions
- Support des algorithmes personnalisés
- Interface pour les optimisations spécialisées

## Critères de validation

- [ ] Classe SpecializedAlgorithms implémentée selon les spécifications
- [ ] Algorithme CYK fonctionnel
- [ ] Algorithme Earley fonctionnel
- [ ] Élimination de récursivité gauche opérationnelle
- [ ] Élimination de productions vides opérationnelle
- [ ] Normalisation des grammaires fonctionnelle
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
- Phase 003.004 : GrammarParser (pour les conversions)

## Notes d'implémentation

1. **CYK** : Algorithme de parsing pour les grammaires en forme normale de Chomsky
2. **Earley** : Algorithme de parsing général pour les grammaires hors-contexte
3. **Élimination de récursivité** : Algorithmes pour éliminer la récursivité gauche
4. **Élimination de productions vides** : Algorithmes pour éliminer les productions vides
5. **Normalisation** : Algorithmes de normalisation des grammaires