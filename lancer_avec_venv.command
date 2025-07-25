#!/bin/bash
echo "🚀 Configuration de l'environnement virtuel..."
cd "$(dirname "$0")"

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "acoustique_env" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv acoustique_env
fi

# Activer l'environnement virtuel
source acoustique_env/bin/activate

# Installer ReportLab si nécessaire
python3 -c "import reportlab" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installation de ReportLab..."
    pip install reportlab
fi

echo "✅ Environnement prêt!"
echo "🔄 Lancement du calculateur..."
python3 calculateur_acoustique.py

read -p "Appuyez sur Entrée pour fermer..."
