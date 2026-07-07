# Baixa modelos Ollama no stack local (profile init).
# Executar na raiz do repositório:
#   .\deploy\scripts\pull_models.ps1

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$EnvFile = Join-Path $RepoRoot "deploy\.env"
$EnvExample = Join-Path $RepoRoot "deploy\.env.example"

if (-not (Test-Path $EnvFile)) {
    Write-Host "Criando deploy/.env a partir de .env.example..."
    Copy-Item $EnvExample $EnvFile
}

docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile init run --rm ollama-pull

Write-Host "Modelos instalados. Suba o stack com:"
Write-Host "  docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d"