# XML Unifier - Script PowerShell

Write-Host "=== XML Unifier ===" -ForegroundColor Cyan
Write-Host "Iniciando unificação de arquivos XML..." -ForegroundColor Green

# Verifica se a pasta files existe
if (!(Test-Path "files")) {
    Write-Host "Criando pasta files..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "files" -Force | Out-Null
}

# Verifica se a pasta output existe
if (!(Test-Path "output")) {
    Write-Host "Criando pasta output..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "output" -Force | Out-Null
}

# Conta arquivos XML
$xmlFiles = Get-ChildItem -Path "files" -Filter "*.xml"
$xmlCount = $xmlFiles.Count

Write-Host "Encontrados $xmlCount arquivos XML na pasta files/" -ForegroundColor White

if ($xmlCount -eq 0) {
    Write-Host "⚠️  Nenhum arquivo XML encontrado!" -ForegroundColor Red
    Write-Host "Por favor, adicione os arquivos XML na pasta 'files/' e execute novamente." -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 Executando Docker Compose..." -ForegroundColor Cyan
docker-compose up --build

# Verifica se o arquivo foi criado
if (Test-Path "output/final_list.xml") {
    Write-Host "✅ Unificação concluída!" -ForegroundColor Green
    Write-Host "📄 Arquivo final: output/final_list.xml" -ForegroundColor White
    
    # Mostra estatísticas do arquivo final
    $file = Get-Item "output/final_list.xml"
    $lines = (Get-Content "output/final_list.xml" | Measure-Object).Count
    $sizeKB = [math]::Round($file.Length / 1KB, 2)
    
    Write-Host "📊 Estatísticas: $lines linhas, $sizeKB KB" -ForegroundColor White
} else {
    Write-Host "❌ Erro: Arquivo final não foi criado" -ForegroundColor Red
    exit 1
}

Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
