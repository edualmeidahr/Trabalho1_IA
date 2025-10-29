@echo off
title Instalador de Dependencias - Trabalho 2 IA

echo ==========================================================
echo Instalando dependencias do projeto (Trabalho 2 - IA)...
echo ==========================================================

REM Tenta usar o 'py' launcher (preferido no Windows)
py -m pip install -r requirements.txt

REM Se falhar (errorlevel nao for 0), tenta usar 'pip' direto
IF %ERRORLEVEL% NEQ 0 (
    echo "Falha ao usar 'py -m pip', tentando 'pip' diretamente..."
    pip install -r requirements.txt
)

REM Verifica o resultado final
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo >>> Erro: Nao foi possivel instalar as dependencias.
    echo >>> Verifique se o Python 3.10+ esta instalado e adicionado ao PATH.
    echo ==========================================================
    pause
    exit /b 1
)

echo.
echo >>> Dependencias instaladas com sucesso!
echo ==========================================================
pause