# XML Unifier

Este projeto unifica múltiplos arquivos XML em um único arquivo, mantendo a estrutura original.

## Características

- **Linguagem**: Python 3.11
- **Execução**: Docker
- **Entrada**: Arquivos XML na pasta `files/`
- **Saída**: Arquivo `final_list.xml` na pasta `output/`

## Como usar

### 1. Preparação dos arquivos

1. Coloque todos os arquivos XML que você baixou do navegador (Ctrl+S) na pasta `files/`
2. Os arquivos devem ter extensão `.xml`

### 2. Execução com Docker Compose (Recomendado)

```bash
# Construir e executar o container
docker-compose up --build

# Ou apenas executar se já foi construído
docker-compose up
```

### 3. Execução com Docker diretamente

**Windows PowerShell:**
```powershell
# Construir a imagem
docker build -t xml-unifier .

# Executar o container
docker run --rm -v "${PWD}/files:/app/files" -v "${PWD}/output:/app/output" xml-unifier
```

**Windows Command Prompt:**
```cmd
# Construir a imagem
docker build -t xml-unifier .

# Executar o container
docker run --rm -v "%cd%/files:/app/files" -v "%cd%/output:/app/output" xml-unifier
```

**Linux/macOS:**
```bash
# Construir a imagem
docker build -t xml-unifier .

# Executar o container
docker run --rm -v "$(pwd)/files:/app/files" -v "$(pwd)/output:/app/output" xml-unifier

#Executar numa paulada so
docker build -t xml-unifier . ; docker run --rm -v "${PWD}/files:/app/files" -v "${PWD}/output:/app/output" xml-unifier
```


### 4. Execução local (sem Docker)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o programa
python xml_unifier.py
```

## Estrutura do projeto

```
xml_unifier/
├── xml_unifier.py      # Programa principal
├── Dockerfile          # Configuração do Docker
├── docker-compose.yml  # Orquestração simplificada
├── requirements.txt    # Dependências Python
├── files/              # Pasta para arquivos XML de entrada
├── output/             # Pasta para o arquivo final
└── README.md          # Este arquivo
```

## Como funciona

1. O programa escaneia a pasta `files/` procurando por arquivos `.xml`
2. **Detecção automática**: Analisa os arquivos para determinar se deve criar um `sitemapindex` ou `urlset`
   - **sitemapindex**: Para unificar índices de sitemap (contém referências para outros sitemaps)
   - **urlset**: Para unificar sitemaps de URLs (contém URLs individuais)
3. Faz o parse de cada arquivo XML compatível
4. Adiciona os elementos ao XML unificado mantendo o formato correto
5. Salva o resultado como `final_list.xml` na pasta `output/`

### Tipos de Sitemap Suportados

- **Sitemapindex** (`<sitemapindex>`): Índice que referencia outros arquivos de sitemap
- **Urlset** (`<urlset>`): Sitemap contendo URLs individuais do site
- **Detecção automática**: O programa prioriza sitemapindex se encontrar pelo menos um arquivo deste tipo

## Logs

O programa gera logs detalhados mostrando:
- Quantos arquivos foram encontrados
- Quais arquivos foram processados com sucesso
- Eventuais erros de parsing
- Status da unificação

## Tratamento de erros

- Arquivos XML malformados são reportados mas não interrompem o processamento
- XMLs com estruturas diferentes são incluídos mas geram warnings
- Se nenhum arquivo XML for encontrado, o programa cria a pasta `files/` e solicita que adicione os arquivos

## Exemplo de uso

1. Baixe vários XMLs do navegador (Ctrl+S)
2. Coloque na pasta `files/`
3. Execute: `docker-compose up --build`
4. O arquivo unificado estará em `output/final_list.xml`
