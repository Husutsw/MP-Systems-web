@echo off
cd /d "%~dp0"
echo ================================
echo  SUBIENDO CAMBIOS A GITHUB
echo ================================
git add .
git commit -m "Subida automatica desde batch"
git push origin master
echo ================================
echo  SUBIDA COMPLETADA
echo ================================
pause
