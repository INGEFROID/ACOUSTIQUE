#!/bin/bash
echo "🚀 Calculateur Acoustique Interactif - Hôtel L'Uciole"
echo "📍 Activation de l'environnement virtuel acoustique_env"
echo "="*60

# Navigation vers le dossier du script
cd "$(dirname "$0")"

# Vérification de l'existence de l'environnement virtuel
if [ ! -d "acoustique_env" ]; then
    echo "❌ Environnement virtuel 'acoustique_env' non trouvé"
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv acoustique_env
    
    if [ $? -eq 0 ]; then
        echo "✅ Environnement virtuel créé avec succès"
    else
        echo "❌ Erreur lors de la création de l'environnement virtuel"
        read -p "Appuyez sur Entrée pour fermer..."
        exit 1
    fi
fi

# Activation de l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel acoustique_env..."
source acoustique_env/bin/activate

# Vérification de l'activation
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "✅ Environnement virtuel activé : $(basename $VIRTUAL_ENV)"
else
    echo "⚠️ Problème d'activation de l'environnement virtuel"
fi

# Vérification et installation de ReportLab
echo "📦 Vérification des dépendances..."
python3 -c "import reportlab" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "📥 Installation de ReportLab dans acoustique_env..."
    pip install reportlab
    
    if [ $? -eq 0 ]; then
        echo "✅ ReportLab installé avec succès"
    else
        echo "❌ Erreur lors de l'installation de ReportLab"
        read -p "Appuyez sur Entrée pour fermer..."
        exit 1
    fi
else
    echo "✅ ReportLab déjà installé et fonctionnel"
fi

# Affichage des informations de l'environnement
echo ""
echo "📋 Informations de l'environnement :"
echo "   • Python : $(python3 --version)"
echo "   • Environnement : $(basename $VIRTUAL_ENV)"
echo "   • Dossier de travail : $(pwd)"
echo ""

# Lancement du calculateur acoustique
echo "🎯 Lancement du calculateur acoustique interactif..."
echo "="*60
echo ""

# Vérification de l'existence du fichier Python
if [ -f "Calculateur Acoustique Interactif.py" ]; then
    python3 "Calculateur Acoustique Interactif.py"
else
    echo "❌ Le fichier 'Calculateur Acoustique Interactif.py' n'a pas été trouvé."
    echo "💡 Assurez-vous que le fichier Python est dans le même dossier et que le nom est correct."
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

# Fin du script
echo ""
echo "="*60
echo "🏁 Calculateur acoustique terminé"
echo "🌐 Environnement virtuel : $(basename $VIRTUAL_ENV)"
echo "="*60

# Maintien de la fenêtre ouverte
read -p "Appuyez sur Entrée pour fermer..."
