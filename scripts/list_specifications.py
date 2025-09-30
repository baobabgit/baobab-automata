#!/usr/bin/env python3
"""
Script pour lister les spécifications détaillées par priorité.

Usage:
    python scripts/list_specifications.py [--phase PHASE] [--priority PRIORITY] [--sort-by SORT]
"""

import sys
import os
import argparse
from pathlib import Path
import re

def parse_filename(filename):
    """Parse un nom de fichier de spécification et retourne les informations."""
    pattern = r'^(\d{3})_(\d{3})_PHASE_(\d{3})_(.+)\.md$'
    match = re.match(pattern, filename)
    
    if match:
        priority, phase_num, phase_id, description = match.groups()
        return {
            'filename': filename,
            'priority': int(priority),
            'phase_num': int(phase_num),
            'phase_id': phase_id,
            'description': description.replace('_', ' ').title()
        }
    return None

def list_specifications(phase_filter=None, priority_filter=None, sort_by='priority'):
    """Liste les spécifications selon les critères donnés."""
    
    specs_dir = Path("docs/detailed_specifications")
    
    if not specs_dir.exists():
        print("Erreur: Le répertoire des spécifications détaillées n'existe pas")
        return
    
    specifications = []
    
    # Lecture des fichiers
    for filepath in specs_dir.glob("*.md"):
        spec_info = parse_filename(filepath.name)
        if spec_info:
            # Filtrage
            if phase_filter and spec_info['phase_num'] != phase_filter:
                continue
            if priority_filter and spec_info['priority'] != priority_filter:
                continue
            
            specifications.append(spec_info)
    
    # Tri
    if sort_by == 'priority':
        specifications.sort(key=lambda x: x['priority'])
    elif sort_by == 'phase':
        specifications.sort(key=lambda x: (x['phase_num'], x['priority']))
    elif sort_by == 'name':
        specifications.sort(key=lambda x: x['description'])
    
    # Affichage
    if not specifications:
        print("Aucune spécification trouvée avec les critères donnés")
        return
    
    print(f"📋 Spécifications détaillées ({len(specifications)} trouvée(s))")
    print("=" * 80)
    
    current_phase = None
    for spec in specifications:
        # Affichage de l'en-tête de phase si changement
        if current_phase != spec['phase_num']:
            current_phase = spec['phase_num']
            phase_names = {
                1: "Architecture de Base et Infrastructure",
                2: "Automates Finis",
                3: "Automates à Pile",
                4: "Machines de Turing",
                5: "Visualisation",
                6: "Optimisations et Performance",
                7: "Tests, Documentation et Déploiement"
            }
            print(f"\n🔹 Phase {spec['phase_num']:03d} - {phase_names.get(spec['phase_num'], 'Phase Inconnue')}")
            print("-" * 60)
        
        # Affichage de la spécification
        priority_color = get_priority_color(spec['priority'])
        print(f"  {priority_color}Priorité {spec['priority']:03d}{' ' * 2}│ {spec['description']}")
        print(f"  {' ' * 8}│ 📄 {spec['filename']}")
        print()

def get_priority_color(priority):
    """Retourne un emoji de couleur basé sur la priorité."""
    if priority < 100:
        return "🔴"  # Rouge pour Phase 001
    elif priority < 200:
        return "🟠"  # Orange pour Phase 002
    elif priority < 300:
        return "🟡"  # Jaune pour Phase 003
    elif priority < 400:
        return "🟢"  # Vert pour Phase 004
    elif priority < 500:
        return "🔵"  # Bleu pour Phase 005
    elif priority < 600:
        return "🟣"  # Violet pour Phase 006
    else:
        return "⚫"  # Noir pour Phase 007

def show_statistics():
    """Affiche les statistiques des spécifications."""
    specs_dir = Path("docs/detailed_specifications")
    
    if not specs_dir.exists():
        print("Erreur: Le répertoire des spécifications détaillées n'existe pas")
        return
    
    phase_counts = {}
    total_specs = 0
    
    for filepath in specs_dir.glob("*.md"):
        spec_info = parse_filename(filepath.name)
        if spec_info:
            phase = spec_info['phase_num']
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
            total_specs += 1
    
    print("📊 Statistiques des Spécifications Détaillées")
    print("=" * 50)
    print(f"Total des spécifications: {total_specs}")
    print()
    
    phase_names = {
        1: "Architecture de Base",
        2: "Automates Finis",
        3: "Automates à Pile",
        4: "Machines de Turing",
        5: "Visualisation",
        6: "Optimisations",
        7: "Tests et Déploiement"
    }
    
    for phase in sorted(phase_counts.keys()):
        count = phase_counts[phase]
        name = phase_names.get(phase, f"Phase {phase}")
        print(f"Phase {phase:03d} - {name}: {count} spécification(s)")

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Liste les spécifications détaillées par priorité")
    parser.add_argument("--phase", type=int, help="Filtrer par numéro de phase (001-007)")
    parser.add_argument("--priority", type=int, help="Filtrer par priorité")
    parser.add_argument("--sort-by", choices=['priority', 'phase', 'name'], default='priority',
                       help="Critère de tri (default: priority)")
    parser.add_argument("--stats", action='store_true', help="Afficher les statistiques")
    
    args = parser.parse_args()
    
    if args.stats:
        show_statistics()
    else:
        list_specifications(args.phase, args.priority, args.sort_by)

if __name__ == "__main__":
    main()