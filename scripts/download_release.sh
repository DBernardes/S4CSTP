#!/bin/bash

# Nome do repositório
REPO="DBernardes/S4ACS"

# API do GitHub para a última release
API_URL="https://api.github.com/repos/$REPO/releases/latest"

# Diretório da área de trabalho (compatível com Linux/macOS/WSL/Git Bash)
DESKTOP_DIR="$HOME/Desktop"

# Pegar a URL do arquivo .zip
ZIP_URL=$(curl -s "$API_URL" | grep "browser_download_url" | grep ".zip" | cut -d '"' -f 4)

# Verifica se encontrou o arquivo
if [[ -z "$ZIP_URL" ]]; then
    echo "Nenhum arquivo .zip encontrado na última release."
    exit 1
fi

# Nome do arquivo (sem o caminho)
FILENAME=$(basename "$ZIP_URL")

# Caminho completo para salvar o arquivo
OUTPUT_PATH="$DESKTOP_DIR/$FILENAME"

# Baixar o arquivo
echo "Baixando: $ZIP_URL"
echo "Salvando em: $OUTPUT_PATH"
curl -L "$ZIP_URL" -o "$OUTPUT_PATH"

echo "Download concluído!"
