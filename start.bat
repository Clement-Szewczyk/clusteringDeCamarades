@echo off
echo Démarrage de l'application ClusteringDeCamarades...

echo Lancement du frontend...
cd frontend
start npm install
start npm run dev
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des dépendances du frontend.
    exit /b %errorlevel%
)
cd ..

echo Lancement du backend...
cd backend
call back.bat

echo Application démarrée avec succès!
