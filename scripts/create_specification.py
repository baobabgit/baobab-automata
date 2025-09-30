#!/usr/bin/env python3
"""
Script pour créer de nouvelles spécifications détaillées avec la notation de priorité.

Usage:
    python scripts/create_specification.py <phase> <priority> <description>

Exemples:
    python scripts/create_specification.py 003 201 "PDA Implementation"
    python scripts/create_specification.py 004 301 "TM Implementation"
"""

import sys
import os
from pathlib import Path

def create_specification(phase, priority, description):
    """Crée un nouveau fichier de spécification détaillée."""
    
    # Validation des paramètres
    if not phase.isdigit() or len(phase) != 3:
        print("Erreur: La phase doit être un nombre sur 3 chiffres (ex: 001, 002, etc.)")
        return False
    
    if not priority.isdigit() or len(priority) != 3:
        print("Erreur: La priorité doit être un nombre sur 3 chiffres (ex: 001, 101, etc.)")
        return False
    
    # Génération du nom de fichier
    phase_num = int(phase)
    priority_num = int(priority)
    
    # Validation de la cohérence phase/priorité
    expected_min_priority = (phase_num - 1) * 100 + 1
    expected_max_priority = phase_num * 100 - 1
    
    if not (expected_min_priority <= priority_num <= expected_max_priority):
        print(f"Attention: La priorité {priority} ne correspond pas à la phase {phase}")
        print(f"Priorités attendues pour la phase {phase}: {expected_min_priority}-{expected_max_priority}")
        response = input("Continuer quand même? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # Création du nom de fichier
    description_clean = description.upper().replace(' ', '_').replace('-', '_')
    filename = f"{priority}_{phase}_PHASE_{phase:0>3}_{description_clean}.md"
    
    # Chemin du fichier
    filepath = Path("docs/detailed_specifications") / filename
    
    # Vérification si le fichier existe déjà
    if filepath.exists():
        print(f"Erreur: Le fichier {filename} existe déjà")
        return False
    
    # Création du contenu du fichier
    content = f"""# {description} - Phase {phase}

## Objectif

[Description de l'objectif de cette spécification détaillée]

## Priorité de Développement

**Priorité : {priority}** (Phase {phase})

## Spécifications Techniques

### 1. [Première spécification]

[Description détaillée]

### 2. [Deuxième spécification]

[Description détaillée]

## Implémentation

### Classes Principales

- `[NomClasse]` : [Description]

### Méthodes Principales

- `[nom_methode]` : [Description]

## Tests

### Tests Unitaires

- [ ] Test de [fonctionnalité 1]
- [ ] Test de [fonctionnalité 2]

### Tests d'Intégration

- [ ] Test d'intégration avec [composant 1]
- [ ] Test d'intégration avec [composant 2]

## Dépendances

- [Liste des dépendances]

## Critères de Validation

- [ ] [Critère 1]
- [ ] [Critère 2]

## Notes de Développement

[Notes spécifiques pour le développement]
"""
    
    # Création du fichier
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fichier créé avec succès: {filepath}")
        print(f"📝 Nom du fichier: {filename}")
        print(f"🔢 Priorité: {priority}")
        print(f"📋 Phase: {phase}")
        print(f"📄 Description: {description}")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de la création du fichier: {e}")
        return False

def show_help():
    """Affiche l'aide du script."""
    print("""
Script pour créer de nouvelles spécifications détaillées avec la notation de priorité.

Usage:
    python scripts/create_specification.py <phase> <priority> <description>

Paramètres:
    phase       : Numéro de phase sur 3 chiffres (001-007)
    priority    : Numéro de priorité sur 3 chiffres (001-999)
    description : Description de la spécification (sans guillemets)

Exemples:
    python scripts/create_specification.py 003 201 "PDA Implementation"
    python scripts/create_specification.py 004 301 "TM Implementation"
    python scripts/create_specification.py 005 401 "Graphviz Rendering"

Plages de priorités par phase:
    Phase 001: 001-099 (Architecture de Base)
    Phase 002: 100-199 (Automates Finis)
    Phase 003: 200-299 (Automates à Pile)
    Phase 004: 300-399 (Machines de Turing)
    Phase 005: 400-499 (Visualisation)
    Phase 006: 500-599 (Optimisations)
    Phase 007: 600-699 (Tests et Déploiement)
""")

def main():
    """Fonction principale."""
    if len(sys.argv) != 4:
        show_help()
        sys.exit(1)
    
    phase = sys.argv[1]
    priority = sys.argv[2]
    description = sys.argv[3]
    
    success = create_specification(phase, priority, description)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()