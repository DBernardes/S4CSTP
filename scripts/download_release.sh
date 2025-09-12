#!/bin/bash

# Nome do repositório
REPO="dev-LNA/S4ACS"

# API do GitHub para a última release
API_URL="https://api.github.com/repos/$REPO/releases/latest"

# Diretório da área de trabalho
DESKTOP_DIR="$HOME/Desktop"

# Obter URL do .zip na última release
ZIP_URL=$(curl -s "$API_URL" | grep "browser_download_url" | grep ".zip" | cut -d '"' -f 4)

# Verificar se encontrou o zip
if [[ -z "$ZIP_URL" ]]; then
    echo "Nenhum arquivo .zip encontrado na última release."
    exit 1
fi

# Nome do arquivo zip
ZIP_FILENAME=$(basename "$ZIP_URL")

# Caminho completo para salvar o zip
ZIP_PATH="$DESKTOP_DIR/$ZIP_FILENAME"

# Nome da pasta de extração (mesmo nome do zip, sem extensão)
EXTRACT_DIR="$DESKTOP_DIR/${ZIP_FILENAME%.zip}"

# Baixar o zip
echo "Baixando: $ZIP_URL"
echo "Salvando em: $ZIP_PATH"
curl -L "$ZIP_URL" -o "$ZIP_PATH"

# Verificar se o download foi bem-sucedido
if [[ $? -ne 0 ]]; then
    echo "Erro ao baixar o arquivo."
    exit 1
fi

# Extrair o conteúdo do zip
echo "Extraindo para: $EXTRACT_DIR"
mkdir -p "$EXTRACT_DIR"
unzip -q "$ZIP_PATH" -d "$EXTRACT_DIR"
rm "$ZIP_PATH"

echo "Extração concluída!"
