@echo off
echo ====================================
echo  LotoEngine Desktop - Build .EXE
echo ====================================
echo.

echo 1. Verificando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo 2. Instalando PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo.
echo 3. Criando diretorio de saida...
if not exist "dist" mkdir dist

echo.
echo 4. Gerando executavel...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "LotoEngine-Desktop" ^
    --add-data "data;data" ^
    --hidden-import src.core.generator ^
    --hidden-import src.core.validator ^
    --hidden-import src.core.analyzer ^
    --hidden-import src.core.auditor ^
    --hidden-import src.core.charts ^
    --hidden-import src.data.loader ^
    --hidden-import src.gui.main_window ^
    --hidden-import src.gui.weight_panel ^
    --hidden-import src.gui.results_view ^
    --hidden-import src.gui.charts_view ^
    --hidden-import src.database.connection ^
    --hidden-import src.database.models ^
    --hidden-import src.database.migrations ^
    --collect-all customtkinter ^
    --collect-all matplotlib ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo ERRO: Falha ao gerar executavel
    pause
    exit /b 1
)

echo.
echo ====================================
echo  BUILD CONCLUIDO!
echo  Executavel: dist\LotoEngine-Desktop.exe
echo ====================================
pause
