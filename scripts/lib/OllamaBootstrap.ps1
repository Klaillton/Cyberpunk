# Helpers compartilhados para scripts run-narracao-*-local.ps1

function Get-OllamaBaseUrl {
    if ($env:OLLAMA_BASE_URL) { return $env:OLLAMA_BASE_URL }
    return "http://127.0.0.1:11434"
}

function Test-OllamaApiReachable {
    param([int]$TimeoutSec = 3)
    try {
        $null = Invoke-RestMethod -Uri "$(Get-OllamaBaseUrl)/api/tags" -Method Get -TimeoutSec $TimeoutSec
        return $true
    } catch {
        return $false
    }
}

function Ensure-OllamaDocker {
    if (Test-OllamaApiReachable) { return }
    $docker = Get-Command docker -ErrorAction SilentlyContinue
    if (-not $docker) {
        throw "Ollama nao responde em $(Get-OllamaBaseUrl) e Docker CLI nao encontrado."
    }
    $repoRoot = if ($script:RepoRoot) { $script:RepoRoot } else { (Get-Item $PSScriptRoot).Parent.Parent.FullName }
    $composeFile = Join-Path $repoRoot "deploy/docker-compose.yml"
    Write-Host "Ollama offline — iniciando container cyberpunk-ollama ..."
    docker compose -f $composeFile up -d ollama
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao subir Ollama. Rode: docker compose -f deploy/docker-compose.yml up -d ollama"
    }
}

function Test-OllamaModelInstalled {
    param([string]$ModelName)
    if (-not (Test-OllamaApiReachable)) { return $false }
    try {
        $tags = Invoke-RestMethod -Uri "$(Get-OllamaBaseUrl)/api/tags" -Method Get -TimeoutSec 8
        foreach ($entry in $tags.models) {
            if ($entry.name -eq $ModelName) { return $true }
        }
    } catch {
        return $false
    }
    return $false
}

function Invoke-OllamaPull {
    param([string]$ModelName)
    if (Test-OllamaModelInstalled $ModelName) {
        Write-Host "Modelo $ModelName ja instalado — pulando pull."
        return
    }
    $ollama = Get-Command ollama -ErrorAction SilentlyContinue
    if ($ollama) {
        & ollama pull $ModelName
        return
    }
    $baseUrl = Get-OllamaBaseUrl
    Write-Host "CLI ausente — baixando $ModelName via API $baseUrl ..."
    curl -s -N -X POST "$baseUrl/api/pull" -d "{`"name`":`"$ModelName`"}" | Out-Null
}

function Wait-OllamaReady {
    param([int]$MaxSeconds = 120)
    $baseUrl = Get-OllamaBaseUrl
    $deadline = (Get-Date).AddSeconds($MaxSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $tags = Invoke-RestMethod -Uri "$baseUrl/api/tags" -Method Get -TimeoutSec 8
            if ($tags.models -and $tags.models.Count -gt 0) {
                Write-Host "Ollama pronto em $baseUrl ($($tags.models.Count) modelos)."
                return
            }
        } catch {
            Start-Sleep -Seconds 2
        }
    }
    throw "Ollama nao respondeu em $baseUrl apos ${MaxSeconds}s. Verifique: docker compose -f deploy/docker-compose.yml up -d ollama"
}

function Warm-OllamaModel {
    param(
        [string]$ModelName,
        [int]$TimeoutSec = 120
    )
    $baseUrl = Get-OllamaBaseUrl
    Write-Host "Aquecendo modelo $ModelName (primeira carga pode levar 1-2 min)..."
    $payload = @{
        model      = $ModelName
        prompt     = "Responda apenas: pronto."
        stream     = $false
        keep_alive = $(if ($env:OLLAMA_KEEP_ALIVE) { $env:OLLAMA_KEEP_ALIVE } else { "15m" })
        options    = @{ num_predict = 8; num_ctx = 2048 }
    }
    if ($env:OLLAMA_NUM_GPU) {
        $payload.options.num_gpu = [int]$env:OLLAMA_NUM_GPU
    }
    try {
        Invoke-RestMethod -Uri "$baseUrl/api/generate" -Method Post -Body ($payload | ConvertTo-Json -Depth 5) -ContentType "application/json" -TimeoutSec $TimeoutSec | Out-Null
        Write-Host "Modelo $ModelName carregado."
    } catch {
        Write-Warning "Warm-up falhou (a primeira narracao ainda pode demorar): $_"
    }
}

function Start-NarracaoApi {
    param([string]$ProfileLabel)
    $repoRoot = if ($script:RepoRoot) { $script:RepoRoot } else { (Get-Item $PSScriptRoot).Parent.Parent.FullName }
    $apiScript = Join-Path $repoRoot "scripts/narracao_api.py"
    Write-Host "Iniciando API — perfil $ProfileLabel ($($env:OLLAMA_MODEL_NARRATION))..."
    python $apiScript
}