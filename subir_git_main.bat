@echo off
cd /d "%~dp0"
echo ================================
echo  Subiendo cambios a GitHub...
echo ================================

:: Agregar todos los archivos modificados
git add .

:: Crear commit con fecha y hora actual
set FECHA=%date:~6,4%-%date:~3,2%-%date:~0,2%
set HORA=%time:~0,2%%time:~3,2%
git commit -m "Subida automatica %FECHA% %HORA%"

:: Subir a la rama main
git push origin main

echo ================================
echo  Subida completada.
pause