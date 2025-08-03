#!/bin/bash

echo "=== XML Unifier ==="
echo "Iniciando unificação de arquivos XML..."

# Verifica se a pasta files existe
if [ ! -d "files" ]; then
    echo "Criando pasta files..."
    mkdir -p files
fi

# Verifica se a pasta output existe
if [ ! -d "output" ]; then
    echo "Criando pasta output..."
    mkdir -p output
fi

# Conta arquivos XML
xml_count=$(find files -name "*.xml" | wc -l)
echo "Encontrados $xml_count arquivos XML na pasta files/"

if [ $xml_count -eq 0 ]; then
    echo "⚠️  Nenhum arquivo XML encontrado!"
    echo "Por favor, adicione os arquivos XML na pasta 'files/' e execute novamente."
    exit 1
fi

echo "🚀 Executando Docker Compose..."
docker-compose up --build

# Verifica se o arquivo foi criado
if [ -f "output/final_list.xml" ]; then
    echo "✅ Unificação concluída!"
    echo "📄 Arquivo final: output/final_list.xml"
    
    # Mostra estatísticas do arquivo final
    lines=$(wc -l < "output/final_list.xml")
    size=$(du -h "output/final_list.xml" | cut -f1)
    echo "📊 Estatísticas: $lines linhas, $size"
else
    echo "❌ Erro: Arquivo final não foi criado"
    exit 1
fi
