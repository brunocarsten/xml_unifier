# Estrutura do Projeto XML Unifier

## Arquivos Principais

### `xml_unifier.py`
- **Função**: Programa principal em Python
- **Responsabilidades**:
  - Escaneamento da pasta `files/` para arquivos `.xml`
  - Parse individual de cada arquivo XML
  - Unificação dos elementos XML mantendo a estrutura
  - Formatação e exportação do arquivo final
  - Logs detalhados do processo
  - Tratamento de erros

### `Dockerfile`
- **Função**: Definição da imagem Docker
- **Base**: Python 3.11-slim
- **Inclui**: Instalação do lxml para processamento XML robusto

### `docker-compose.yml`
- **Função**: Orquestração simplificada
- **Volumes**: 
  - `./files:/app/files` - Mapeia arquivos de entrada
  - `./output:/app/output` - Mapeia arquivo de saída

### `requirements.txt`
- **Dependências**: `lxml>=4.9.0` para processamento XML avançado

## Pastas

### `files/`
- **Propósito**: Armazenar arquivos XML baixados do navegador
- **Formato aceito**: Qualquer arquivo `.xml`
- **Comportamento**: O programa processa todos os XMLs dinamicamente

### `output/`
- **Propósito**: Destino do arquivo unificado `final_list.xml`
- **Acesso**: Mapeado do container para facilitar acesso

## Scripts de Conveniência

### `run.ps1` (Windows PowerShell)
- Script automatizado para execução no Windows
- Verificações de pré-requisitos
- Estatísticas do resultado

### `run.sh` (Bash/Linux)
- Equivalente do `run.ps1` para sistemas Unix-like

## Características Técnicas

### Processamento XML
- **Parser**: `xml.etree.ElementTree` (biblioteca padrão)
- **Formatação**: `xml.dom.minidom` para saída legível
- **Estrutura**: Mantém hierarquia do primeiro arquivo como base
- **Compatibilidade**: Lida com XMLs de estruturas similares

### Tratamento de Erros
- XMLs malformados são reportados e ignorados
- Estruturas diferentes geram warnings mas são incluídas
- Logs informativos em tempo real

### Docker
- **Ambiente isolado**: Não requer instalação local do Python
- **Portabilidade**: Funciona em qualquer sistema com Docker
- **Volumes**: Acesso dinâmico aos arquivos locais

## Fluxo de Execução

1. **Inicialização**: Container inicia e verifica pasta `files/`
2. **Descoberta**: Lista todos os arquivos `.xml` disponíveis
3. **Processamento**: 
   - Parse do primeiro arquivo (estabelece estrutura base)
   - Parse dos demais arquivos
   - Merge dos elementos
4. **Saída**: Geração do `final_list.xml` formatado
5. **Cópia**: Arquivo movido para pasta `output/` no host

## Exemplo de Uso Típico

```bash
# 1. Baixar XMLs do navegador (Ctrl+S) para pasta files/
# 2. Executar unificação
docker-compose up --build

# 3. Arquivo final disponível em output/final_list.xml
```

## Logs de Exemplo

```
INFO - Iniciando XML Unifier...
INFO - Encontrados 2 arquivos XML em files
INFO - Arquivo processado com sucesso: example1.xml
INFO - Arquivo processado com sucesso: example2.xml
INFO - Arquivo unificado salvo como: final_list.xml
INFO - Unificação concluída com sucesso!
```
