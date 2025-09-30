# Spécification Détaillée - Interfaces Abstraites

## Agent IA Cible
Agent de développement spécialisé dans la conception d'interfaces et d'architectures orientées objet en Python.

## Objectif
Définir et implémenter les interfaces abstraites communes pour tous les types d'automates dans le projet Baobab Automata.

## Spécifications Techniques

### 1. Interface IState

#### 1.1 Définition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Set, Optional
from enum import Enum

class StateType(Enum):
    """Types d'états possibles dans un automate."""
    INITIAL = "initial"
    FINAL = "final"
    INTERMEDIATE = "intermediate"
    ACCEPTING = "accepting"
    REJECTING = "rejecting"

class IState(ABC):
    """Interface abstraite pour les états d'un automate."""
    
    @property
    @abstractmethod
    def identifier(self) -> str:
        """Identifiant unique de l'état."""
        pass
    
    @property
    @abstractmethod
    def state_type(self) -> StateType:
        """Type de l'état."""
        pass
    
    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """Métadonnées associées à l'état."""
        pass
    
    @abstractmethod
    def is_initial(self) -> bool:
        """Vérifie si l'état est initial."""
        pass
    
    @abstractmethod
    def is_final(self) -> bool:
        """Vérifie si l'état est final."""
        pass
    
    @abstractmethod
    def is_accepting(self) -> bool:
        """Vérifie si l'état est acceptant."""
        pass
    
    @abstractmethod
    def add_metadata(self, key: str, value: Any) -> None:
        """Ajoute une métadonnée à l'état."""
        pass
    
    @abstractmethod
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Récupère une métadonnée de l'état."""
        pass
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité entre états."""
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """Hash de l'état pour utilisation dans des sets."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Représentation string de l'état."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """Représentation détaillée de l'état."""
        pass
```

#### 1.2 Implémentation Concrète
```python
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

@dataclass(frozen=True)
class State(IState):
    """Implémentation concrète d'un état d'automate."""
    
    identifier: str
    state_type: StateType
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_initial(self) -> bool:
        """Vérifie si l'état est initial."""
        return self.state_type == StateType.INITIAL
    
    def is_final(self) -> bool:
        """Vérifie si l'état est final."""
        return self.state_type == StateType.FINAL
    
    def is_accepting(self) -> bool:
        """Vérifie si l'état est acceptant."""
        return self.state_type in {StateType.FINAL, StateType.ACCEPTING}
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Ajoute une métadonnée à l'état."""
        # Note: Cette méthode ne peut pas être implémentée avec @dataclass(frozen=True)
        # Une implémentation alternative sera nécessaire
        raise NotImplementedError("Cannot modify frozen dataclass")
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Récupère une métadonnée de l'état."""
        return self.metadata.get(key, default)
    
    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité entre états."""
        if not isinstance(other, State):
            return False
        return self.identifier == other.identifier
    
    def __hash__(self) -> int:
        """Hash de l'état pour utilisation dans des sets."""
        return hash(self.identifier)
    
    def __str__(self) -> str:
        """Représentation string de l'état."""
        return f"State({self.identifier})"
    
    def __repr__(self) -> str:
        """Représentation détaillée de l'état."""
        return f"State(identifier='{self.identifier}', type={self.state_type})"
```

### 2. Interface ITransition

#### 2.1 Définition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from enum import Enum

class TransitionType(Enum):
    """Types de transitions possibles."""
    SYMBOL = "symbol"
    EPSILON = "epsilon"
    STACK_PUSH = "stack_push"
    STACK_POP = "stack_pop"
    STACK_READ = "stack_read"
    TAPE_READ = "tape_read"
    TAPE_WRITE = "tape_write"
    TAPE_MOVE = "tape_move"

class ITransition(ABC):
    """Interface abstraite pour les transitions d'un automate."""
    
    @property
    @abstractmethod
    def source_state(self) -> IState:
        """État source de la transition."""
        pass
    
    @property
    @abstractmethod
    def target_state(self) -> IState:
        """État cible de la transition."""
        pass
    
    @property
    @abstractmethod
    def symbol(self) -> Optional[str]:
        """Symbole de la transition (None pour epsilon)."""
        pass
    
    @property
    @abstractmethod
    def transition_type(self) -> TransitionType:
        """Type de la transition."""
        pass
    
    @property
    @abstractmethod
    def conditions(self) -> Dict[str, Any]:
        """Conditions de la transition."""
        pass
    
    @property
    @abstractmethod
    def actions(self) -> Dict[str, Any]:
        """Actions de la transition."""
        pass
    
    @abstractmethod
    def is_applicable(self, symbol: Optional[str], context: Dict[str, Any]) -> bool:
        """Vérifie si la transition est applicable."""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la transition et retourne le nouveau contexte."""
        pass
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité entre transitions."""
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """Hash de la transition."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Représentation string de la transition."""
        pass
```

#### 2.2 Implémentation Concrète
```python
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class Transition(ITransition):
    """Implémentation concrète d'une transition d'automate."""
    
    source_state: IState
    target_state: IState
    symbol: Optional[str]
    transition_type: TransitionType
    conditions: Dict[str, Any] = field(default_factory=dict)
    actions: Dict[str, Any] = field(default_factory=dict)
    
    def is_applicable(self, symbol: Optional[str], context: Dict[str, Any]) -> bool:
        """Vérifie si la transition est applicable."""
        # Vérification du symbole
        if self.symbol is not None and self.symbol != symbol:
            return False
        
        # Vérification des conditions
        for condition_key, condition_value in self.conditions.items():
            if context.get(condition_key) != condition_value:
                return False
        
        return True
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la transition et retourne le nouveau contexte."""
        new_context = context.copy()
        
        # Exécution des actions
        for action_key, action_value in self.actions.items():
            new_context[action_key] = action_value
        
        return new_context
    
    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité entre transitions."""
        if not isinstance(other, Transition):
            return False
        return (self.source_state == other.source_state and
                self.target_state == other.target_state and
                self.symbol == other.symbol and
                self.transition_type == other.transition_type)
    
    def __hash__(self) -> int:
        """Hash de la transition."""
        return hash((self.source_state, self.target_state, self.symbol, self.transition_type))
    
    def __str__(self) -> str:
        """Représentation string de la transition."""
        symbol_str = self.symbol if self.symbol is not None else "ε"
        return f"{self.source_state} --{symbol_str}--> {self.target_state}"
```

### 3. Interface IAutomaton

#### 3.1 Définition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum

class AutomatonType(Enum):
    """Types d'automates supportés."""
    DFA = "dfa"
    NFA = "nfa"
    EPSILON_NFA = "epsilon_nfa"
    PDA = "pda"
    DPDA = "dpda"
    NPDA = "npda"
    TM = "tm"
    DTM = "dtm"
    NTM = "ntm"
    MULTI_TAPE_TM = "multi_tape_tm"

class IAutomaton(ABC):
    """Interface abstraite pour tous les types d'automates."""
    
    @property
    @abstractmethod
    def automaton_type(self) -> AutomatonType:
        """Type de l'automate."""
        pass
    
    @property
    @abstractmethod
    def states(self) -> Set[IState]:
        """Ensemble des états de l'automate."""
        pass
    
    @property
    @abstractmethod
    def initial_states(self) -> Set[IState]:
        """Ensemble des états initiaux."""
        pass
    
    @property
    @abstractmethod
    def final_states(self) -> Set[IState]:
        """Ensemble des états finaux."""
        pass
    
    @property
    @abstractmethod
    def alphabet(self) -> Set[str]:
        """Alphabet de l'automate."""
        pass
    
    @property
    @abstractmethod
    def transitions(self) -> Set[ITransition]:
        """Ensemble des transitions de l'automate."""
        pass
    
    @abstractmethod
    def add_state(self, state: IState) -> None:
        """Ajoute un état à l'automate."""
        pass
    
    @abstractmethod
    def remove_state(self, state: IState) -> None:
        """Supprime un état de l'automate."""
        pass
    
    @abstractmethod
    def add_transition(self, transition: ITransition) -> None:
        """Ajoute une transition à l'automate."""
        pass
    
    @abstractmethod
    def remove_transition(self, transition: ITransition) -> None:
        """Supprime une transition de l'automate."""
        pass
    
    @abstractmethod
    def get_transitions_from(self, state: IState) -> Set[ITransition]:
        """Récupère les transitions partant d'un état."""
        pass
    
    @abstractmethod
    def get_transitions_to(self, state: IState) -> Set[ITransition]:
        """Récupère les transitions arrivant à un état."""
        pass
    
    @abstractmethod
    def get_transitions(self, source: IState, symbol: Optional[str]) -> Set[ITransition]:
        """Récupère les transitions pour un état et un symbole donnés."""
        pass
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Vérifie si l'automate est valide."""
        pass
    
    @abstractmethod
    def validate(self) -> List[str]:
        """Valide l'automate et retourne la liste des erreurs."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise l'automate en dictionnaire."""
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Désérialise l'automate depuis un dictionnaire."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Représentation string de l'automate."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """Représentation détaillée de l'automate."""
        pass
```

### 4. Interface IRecognizer

#### 4.1 Définition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class IRecognizer(ABC):
    """Interface abstraite pour la reconnaissance de mots."""
    
    @abstractmethod
    def recognize(self, word: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Reconnaît si un mot appartient au langage de l'automate."""
        pass
    
    @abstractmethod
    def recognize_with_trace(self, word: str, context: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """Reconnaît un mot et retourne la trace d'exécution."""
        pass
    
    @abstractmethod
    def get_accepting_paths(self, word: str, context: Optional[Dict[str, Any]] = None) -> List[List[IState]]:
        """Retourne tous les chemins acceptants pour un mot."""
        pass
    
    @abstractmethod
    def is_deterministic(self) -> bool:
        """Vérifie si l'automate est déterministe."""
        pass
    
    @abstractmethod
    def get_language_properties(self) -> Dict[str, Any]:
        """Retourne les propriétés du langage reconnu."""
        pass
```

### 5. Interface IConverter

#### 5.1 Définition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

class IConverter(ABC):
    """Interface abstraite pour les conversions d'automates."""
    
    @abstractmethod
    def can_convert(self, source_type: AutomatonType, target_type: AutomatonType) -> bool:
        """Vérifie si la conversion est possible."""
        pass
    
    @abstractmethod
    def convert(self, automaton: IAutomaton, target_type: AutomatonType) -> IAutomaton:
        """Convertit un automate vers un autre type."""
        pass
    
    @abstractmethod
    def get_conversion_options(self, source_type: AutomatonType) -> List[AutomatonType]:
        """Retourne les types d'automates vers lesquels on peut convertir."""
        pass
    
    @abstractmethod
    def get_conversion_info(self, source_type: AutomatonType, target_type: AutomatonType) -> Dict[str, Any]:
        """Retourne des informations sur la conversion."""
        pass
```

### 6. Exceptions Personnalisées

#### 6.1 Définition
```python
class BaobabAutomataError(Exception):
    """Exception de base pour Baobab Automata."""
    pass

class InvalidAutomatonError(BaobabAutomataError):
    """Exception levée quand un automate est invalide."""
    pass

class InvalidStateError(BaobabAutomataError):
    """Exception levée quand un état est invalide."""
    pass

class InvalidTransitionError(BaobabAutomataError):
    """Exception levée quand une transition est invalide."""
    pass

class ConversionError(BaobabAutomataError):
    """Exception levée quand une conversion échoue."""
    pass

class RecognitionError(BaobabAutomataError):
    """Exception levée quand la reconnaissance échoue."""
    pass
```

## Critères de Validation

### 1. Interfaces
- [ ] Toutes les interfaces sont définies avec des méthodes abstraites
- [ ] Les interfaces respectent les principes SOLID
- [ ] Les interfaces sont documentées avec des docstrings
- [ ] Les interfaces sont typées strictement

### 2. Implémentations
- [ ] Implémentations concrètes des interfaces
- [ ] Implémentations testées unitairement
- [ ] Implémentations documentées
- [ ] Implémentations respectent les contraintes de performance

### 3. Qualité
- [ ] Code formaté avec Black
- [ ] Score Pylint >= 8.5/10
- [ ] Pas d'erreurs Flake8
- [ ] Pas de vulnérabilités Bandit
- [ ] Types validés avec MyPy

### 4. Tests
- [ ] Tests unitaires pour toutes les interfaces
- [ ] Tests unitaires pour toutes les implémentations
- [ ] Couverture de code >= 95%
- [ ] Tests de performance

## Exemples d'Utilisation

### Création d'un État
```python
# Création d'un état initial
initial_state = State(
    identifier="q0",
    state_type=StateType.INITIAL,
    metadata={"description": "État initial"}
)

# Création d'un état final
final_state = State(
    identifier="q1",
    state_type=StateType.FINAL,
    metadata={"description": "État final"}
)
```

### Création d'une Transition
```python
# Création d'une transition symbolique
transition = Transition(
    source_state=initial_state,
    target_state=final_state,
    symbol="a",
    transition_type=TransitionType.SYMBOL
)
```

### Utilisation d'une Interface
```python
# Vérification du type d'état
if state.is_initial():
    print("État initial")

# Vérification de l'applicabilité d'une transition
if transition.is_applicable("a", {}):
    print("Transition applicable")
```

## Notes d'Implémentation

1. **Immutabilité** : Les états et transitions sont immutables pour éviter les effets de bord
2. **Typage** : Utilisation stricte des types pour la sécurité
3. **Performance** : Optimisation des structures de données pour les gros volumes
4. **Extensibilité** : Interfaces conçues pour être facilement étendues
5. **Documentation** : Docstrings complètes pour toutes les méthodes