#!/bin/bash
echo "🚀 Lancement du calculateur acoustique..."
echo "📍 Projet: Hôtel L'Uciole, Crans-Montana"
echo ""

cd "$(dirname "$0")"

if command -v python3 &> /dev/null; then
    python3 calculateur_acoustique.py
elif command -v python &> /dev/null; then
    python calculateur_acoustique.py
else
    echo "❌ Python n'est pas installé sur ce système"
    echo "Veuillez installer Python depuis https://www.python.org/"
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi
