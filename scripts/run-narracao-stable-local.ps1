# Perfil estavel local: llama3.1 8B — sessao diaria (turno alvo ~30-90s).
# Uso: pwsh -File scripts/run-narracao-stable-local.ps1

$ErrorActionPreference = "Stop"
$script:RepoRoot = $PSScriptRoot.Parent.FullName
Set-Location $script:RepoRoot

$env:NARRACAO_PROVIDER = "ollama"
$env:OLLAMA_MODEL_NARRATION = "llama3.1:8b"
$env:OLLAMA_MODEL_AUX = "phi3:mini"
$env:LLM_ROUTING_POLICY = "local_only"
$env:CLOUD_FALLBACK_ENABLED = "false"
$env:QUALITY_RESCUE_CLOUD_ENABLED = "false"
$env:NARRACAO_MIN_TIER = "standard"

# Contexto e geracao — 8B cabe inteiro na GPU; priorizar resposta rapida
$env:OLLAMA_NUM_CTX_NARRATION = "4096"
$env:OLLAMA_NUM_PREDICT_NARRATION = "350"
$env:OLLAMA_MAX_PROMPT_CHARS = "6000"
$env:OLLAMA_MAX_CONTEXT_FILES = "8"
$env:OLLAMA_KEEP_ALIVE = "15m"
$env:OLLAMA_REQUEST_TIMEOUT = "180"

. (Join-Path $PSScriptRoot "lib/OllamaBootstrap.ps1")

Ensure-OllamaDocker
Wait-OllamaReady
Invoke-OllamaPull $env:OLLAMA_MODEL_NARRATION
Invoke-OllamaPull $env:OLLAMA_MODEL_AUX
Warm-OllamaModel $env:OLLAMA_MODEL_NARRATION -TimeoutSec 90

Write-Host "Rescue Grok: desligado (100% Ollama 8B). Turnos estaveis: ~30-90s."
Start-NarracaoApi -ProfileLabel "estavel"