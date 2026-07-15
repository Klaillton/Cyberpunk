# Perfil maximo local: qwen2.5 14B com offload GPU+RAM (4070 8GB + 64GB RAM).
# Uso: pwsh -File scripts/run-narracao-max-local.ps1

$ErrorActionPreference = "Stop"
$script:RepoRoot = $PSScriptRoot.Parent.FullName
Set-Location $script:RepoRoot

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

. (Join-Path $PSScriptRoot "lib/OllamaBootstrap.ps1")

Ensure-OllamaDocker
Wait-OllamaReady
Invoke-OllamaPull $env:OLLAMA_MODEL_NARRATION
Invoke-OllamaPull "phi3:mini"
Warm-OllamaModel $env:OLLAMA_MODEL_NARRATION -TimeoutSec 240

Write-Host "Rescue Grok: desligado (100% Ollama). Turnos 14B: aguarde alguns minutos no chat."
Start-NarracaoApi -ProfileLabel "maximo"