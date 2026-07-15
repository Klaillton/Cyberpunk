# Perfil maximo local: qwen2.5 14B com offload GPU+RAM (4070 8GB + 64GB RAM).
# Uso: pwsh -File scripts/run-narracao-max-local.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot.Parent.FullName

$env:NARRACAO_PROVIDER = "ollama"
$env:OLLAMA_MODEL_NARRATION = "qwen2.5:14b-instruct"
$env:OLLAMA_MODEL_AUX = "phi3:mini"
$env:LLM_ROUTING_POLICY = "local_only"
$env:CLOUD_FALLBACK_ENABLED = "false"
$env:QUALITY_RESCUE_CLOUD_ENABLED = "false"
$env:NARRACAO_MIN_TIER = "standard"

# Contexto e geracao — 14B com offload: priorizar latencia (turno alvo ~3-6 min)
$env:OLLAMA_NUM_CTX_NARRATION = "6144"
$env:OLLAMA_NUM_PREDICT_NARRATION = "400"
$env:OLLAMA_MAX_PROMPT_CHARS = "7500"
$env:OLLAMA_MAX_CONTEXT_FILES = "6"
$env:OLLAMA_KEEP_ALIVE = "30m"
$env:OLLAMA_REQUEST_TIMEOUT = "480"

# Offload: 28 camadas na RTX 4070 (8GB) — 35 costuma gerar CUDA error em dialogos longos.
if (-not $env:OLLAMA_NUM_GPU) {
    $env:OLLAMA_NUM_GPU = "28"
}

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
    $composeFile = Join-Path $PSScriptRoot.Parent.FullName "deploy/docker-compose.yml"
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
    param([string]$ModelName)
    $baseUrl = Get-OllamaBaseUrl
    Write-Host "Aquecendo modelo $ModelName (primeira carga pode levar 1-3 min)..."
    $payload = @{
        model      = $ModelName
        prompt     = "Responda apenas: pronto."
        stream     = $false
        keep_alive = "30m"
        options    = @{ num_predict = 8; num_ctx = 2048 }
    }
    if ($env:OLLAMA_NUM_GPU) {
        $payload.options.num_gpu = [int]$env:OLLAMA_NUM_GPU
    }
    try {
        Invoke-RestMethod -Uri "$baseUrl/api/generate" -Method Post -Body ($payload | ConvertTo-Json -Depth 5) -ContentType "application/json" -TimeoutSec 240 | Out-Null
        Write-Host "Modelo $ModelName carregado."
    } catch {
        Write-Warning "Warm-up falhou (a primeira narracao ainda pode demorar): $_"
    }
}

Ensure-OllamaDocker
Wait-OllamaReady
Invoke-OllamaPull $env:OLLAMA_MODEL_NARRATION
Invoke-OllamaPull "phi3:mini"
Warm-OllamaModel $env:OLLAMA_MODEL_NARRATION

Write-Host "Iniciando API com narracao local maxima ($($env:OLLAMA_MODEL_NARRATION))..."
Write-Host "Rescue Grok: desligado (100% Ollama). Turnos 14B: aguarde alguns minutos no chat."
python c:/workspace/Cyberpunk/scripts/narracao_api.py