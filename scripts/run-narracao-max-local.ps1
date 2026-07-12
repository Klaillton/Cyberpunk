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

# Offload: ~35 camadas na RTX 4070, resto na RAM. Omita para auto do Ollama.
if (-not $env:OLLAMA_NUM_GPU) {
    $env:OLLAMA_NUM_GPU = "35"
}

function Test-OllamaModelInstalled {
    param([string]$ModelName)
    $baseUrl = if ($env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL } else { "http://127.0.0.1:11434" }
    try {
        $tags = curl -s "$baseUrl/api/tags" | ConvertFrom-Json
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
    $baseUrl = if ($env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL } else { "http://127.0.0.1:11434" }
    Write-Host "CLI ausente — baixando $ModelName via API $baseUrl ..."
    curl -s -N -X POST "$baseUrl/api/pull" -d "{`"name`":`"$ModelName`"}" | Out-Null
}

function Wait-OllamaReady {
    param([int]$MaxSeconds = 90)
    $baseUrl = if ($env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL } else { "http://127.0.0.1:11434" }
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
    $baseUrl = if ($env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL } else { "http://127.0.0.1:11434" }
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

Invoke-OllamaPull $env:OLLAMA_MODEL_NARRATION
Invoke-OllamaPull "phi3:mini"
Wait-OllamaReady
Warm-OllamaModel $env:OLLAMA_MODEL_NARRATION

Write-Host "Iniciando API com narracao local maxima ($($env:OLLAMA_MODEL_NARRATION))..."
Write-Host "Rescue Grok: desligado (100% Ollama). Turnos 14B: aguarde alguns minutos no chat."
python c:/workspace/Cyberpunk/scripts/narracao_api.py