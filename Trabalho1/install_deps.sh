#!/bin/bash
echo "=========================================================="
echo "Instalando dependencias do projeto (Trabalho 1 - IA)..."
echo "=========================================================="

# Verifica se o Python 3 está disponível
if ! command -v python3 &> /dev/null
then
    echo "Erro: python3 não encontrado. Por favor, instale o Python 3.10 ou superior."
    exit 1
fi

# Verifica se o pip3 está disponível
if ! command -v pip3 &> /dev/null
then
    echo "Aviso: 'pip3' não encontrado, tentando usar 'pip'..."
    PIP_COMMAND=pip
else
    PIP_COMMAND=pip3
fi

# Tenta instalar usando o pip encontrado
$PIP_COMMAND install -r requirements.txt

# Verifica se a instalação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo ""
    echo ">>> Dependencias instaladas com sucesso!"
else
    echo ""
    echo ">>> Erro durante a instalação. Verifique sua instalação do Python/pip."
fi

echo "=========================================================="
# Mantém o terminal aberto por alguns segundos (opcional)
sleep 3