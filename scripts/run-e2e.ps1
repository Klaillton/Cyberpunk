# Executa e2e com porta limpa e exit code confiavel para CI/monitores.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$port = if ($env:E2E_PORT) { $env:E2E_PORT } else { "8791" }
$listeners = netstat -ano | findstr ":$port" | findstr LISTENING
if ($listeners) {
  $listeners | ForEach-Object {
    $pid = ($_ -split '\s+')[-1]
    if ($pid -match '^\d+$') {
      Stop-Process -Id ([int]$pid) -Force -ErrorAction SilentlyContinue
    }
  }
  Start-Sleep -Milliseconds 300
}

npm run test:e2e
exit $LASTEXITCODE