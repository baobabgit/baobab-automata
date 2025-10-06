# Makefile PowerShell pour Baobab Automata
# Équivalent du Makefile pour les postes Windows

# Configuration
$VENV_DIR = ".venv"
$PYTHON = "$VENV_DIR\Scripts\python.exe"
$PIP = "$VENV_DIR\Scripts\pip.exe"

# Couleurs pour l'affichage
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Fonction pour vérifier si l'environnement virtuel existe
function Test-VirtualEnv {
    if (-not (Test-Path $VENV_DIR)) {
        Write-ColorOutput "❌ Environnement virtuel non trouvé. Exécutez d'abord 'make setup' ou 'python -m venv .venv'" $Red
        exit 1
    }
}

# Fonction pour activer l'environnement virtuel
function Invoke-ActivateVenv {
    if (Test-Path "$VENV_DIR\Scripts\Activate.ps1") {
        & "$VENV_DIR\Scripts\Activate.ps1"
    } else {
        Write-ColorOutput "❌ Script d'activation non trouvé" $Red
        exit 1
    }
}

# Fonction pour exécuter les tests
function Invoke-Tests {
    param(
        [string]$TestType = "all",
        [string]$ExtraArgs = ""
    )
    
    Test-VirtualEnv
    
    $testCommand = switch ($TestType) {
        "unit" { "python -m pytest tests/baobab_automata/ -m unit $ExtraArgs" }
        "integration" { "python -m pytest tests/integration/ -m integration $ExtraArgs" }
        "performance" { "python -m pytest tests/performance/ -m performance $ExtraArgs" }
        "slow" { "python -m pytest tests/ -m slow $ExtraArgs" }
        "coverage" { "python -m pytest tests/ --cov=baobab_automata --cov-report=html --cov-report=term-missing $ExtraArgs" }
        "all" { "python -m pytest tests/ $ExtraArgs" }
        default { "python -m pytest tests/ $ExtraArgs" }
    }
    
    Write-ColorOutput "🚀 Exécution des tests: $testCommand" $Blue
    Invoke-Expression $testCommand
}

# Fonction pour exécuter les tests en mode watch
function Invoke-TestWatch {
    Test-VirtualEnv
    
    Write-ColorOutput "👀 Mode watch activé - Les tests se relanceront automatiquement" $Yellow
    Write-ColorOutput "Appuyez sur Ctrl+C pour arrêter" $Yellow
    
    python -m pytest_watch --runner "python -m pytest tests/ --tb=short"
}

# Fonction pour installer les dépendances
function Install-Dependencies {
    Test-VirtualEnv
    
    Write-ColorOutput "📦 Installation des dépendances de développement..." $Blue
    & $PIP install -e ".[dev]"
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Dépendances installées avec succès" $Green
    } else {
        Write-ColorOutput "❌ Erreur lors de l'installation des dépendances" $Red
        exit 1
    }
}

# Fonction pour exécuter l'analyse de sécurité avec Bandit
function Invoke-SecurityCheck {
    Test-VirtualEnv
    
    Write-ColorOutput "🔒 Exécution de l'analyse de sécurité avec Bandit..." $Blue
    
    # Créer le dossier docs/bandit s'il n'existe pas
    if (-not (Test-Path "docs/bandit")) {
        New-Item -ItemType Directory -Path "docs/bandit" -Force | Out-Null
        Write-ColorOutput "  Créé le dossier docs/bandit/" $Yellow
    }
    
    # Exécuter Bandit avec sortie JSON
    python -m bandit -r src/ -f json -o docs/bandit/bandit_report.json
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Analyse de sécurité terminée - Rapport: docs/bandit/bandit_report.json" $Green
    } else {
        Write-ColorOutput "⚠️  Analyse de sécurité terminée avec des avertissements - Rapport: docs/bandit/bandit_report.json" $Yellow
    }
}

# Fonction pour nettoyer les fichiers temporaires
function Clear-TempFiles {
    Write-ColorOutput "🧹 Nettoyage des fichiers temporaires..." $Blue
    
    $tempDirs = @(
        "htmlcov",
        ".coverage",
        ".pytest_cache",
        "docs/bandit",
        "__pycache__",
        "*.pyc",
        "*.pyo"
    )
    
    foreach ($pattern in $tempDirs) {
        if (Test-Path $pattern) {
            Remove-Item -Recurse -Force $pattern -ErrorAction SilentlyContinue
            Write-ColorOutput "  Supprimé: $pattern" $Yellow
        }
    }
    
    Write-ColorOutput "✅ Nettoyage terminé" $Green
}

# Fonction pour afficher l'aide
function Show-Help {
    Write-ColorOutput "🔧 Makefile PowerShell pour Baobab Automata" $Blue
    Write-ColorOutput ""
    Write-ColorOutput "Commandes disponibles:" $Yellow
    Write-ColorOutput "  .\Makefile.ps1 test                    - Exécuter tous les tests" $White
    Write-ColorOutput "  .\Makefile.ps1 test-unit              - Exécuter les tests unitaires" $White
    Write-ColorOutput "  .\Makefile.ps1 test-integration       - Exécuter les tests d'intégration" $White
    Write-ColorOutput "  .\Makefile.ps1 test-performance       - Exécuter les tests de performance" $White
    Write-ColorOutput "  .\Makefile.ps1 test-slow              - Exécuter les tests lents" $White
    Write-ColorOutput "  .\Makefile.ps1 test-coverage          - Exécuter avec couverture de code" $White
    Write-ColorOutput "  .\Makefile.ps1 test-all               - Exécuter tous les tests avec couverture" $White
    Write-ColorOutput "  .\Makefile.ps1 test-watch             - Mode watch (relance automatique)" $White
    Write-ColorOutput "  .\Makefile.ps1 install                - Installer les dépendances" $White
    Write-ColorOutput "  .\Makefile.ps1 security               - Analyse de sécurité avec Bandit" $White
    Write-ColorOutput "  .\Makefile.ps1 clean                  - Nettoyer les fichiers temporaires" $White
    Write-ColorOutput "  .\Makefile.ps1 help                   - Afficher cette aide" $White
    Write-ColorOutput ""
    Write-ColorOutput "Exemples:" $Yellow
    Write-ColorOutput "  .\Makefile.ps1 test -v                - Tests avec affichage détaillé" $White
    Write-ColorOutput "  .\Makefile.ps1 test-unit -k test_state - Tests unitaires filtrés" $White
    Write-ColorOutput "  .\Makefile.ps1 test-coverage --html   - Couverture avec rapport HTML" $White
}

# Fonction principale
function Main {
    param(
        [string]$Command = "help",
        [string[]]$Args = @()
    )
    
    $ExtraArgs = $Args -join " "
    
    switch ($Command) {
        "test" { Invoke-Tests "all" $ExtraArgs }
        "test-unit" { Invoke-Tests "unit" $ExtraArgs }
        "test-integration" { Invoke-Tests "integration" $ExtraArgs }
        "test-performance" { Invoke-Tests "performance" $ExtraArgs }
        "test-slow" { Invoke-Tests "slow" $ExtraArgs }
        "test-coverage" { Invoke-Tests "coverage" $ExtraArgs }
        "test-all" { Invoke-Tests "coverage" $ExtraArgs }
        "test-watch" { Invoke-TestWatch }
        "install" { Install-Dependencies }
        "security" { Invoke-SecurityCheck }
        "clean" { Clear-TempFiles }
        "help" { Show-Help }
        default { 
            Write-ColorOutput "❌ Commande inconnue: $Command" $Red
            Show-Help
        }
    }
}

# Exécution de la commande
if ($args.Count -eq 0) {
    Show-Help
} else {
    Main $args[0] $args[1..($args.Count-1)]
}