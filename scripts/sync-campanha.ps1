# Sync campanha: Grok shares -> resumo de sessao -> GitHub
# Uso:
#   .\scripts\sync-campanha.ps1              # sync se houver novidades
#   .\scripts\sync-campanha.ps1 -Bootstrap   # primeira vez
#   .\scripts\sync-campanha.ps1 -DryRun
#   .\scripts\sync-campanha.ps1 -Tail 5 -Apply -Yes   # teste

param(
    [switch]$Bootstrap,
    [switch]$DryRun,
    [switch]$Apply,
    [int]$Tail = 0,
    [switch]$Yes,
    [switch]$SkipPull,
    [switch]$SkipAi,
    [switch]$SkipCommit
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $RepoRoot

$pyArgs = @("$PSScriptRoot\sync_campanha.py")
if ($Bootstrap) { $pyArgs += "--bootstrap" }
if ($DryRun) { $pyArgs += "--dry-run" }
if ($Apply) { $pyArgs += "--apply" }
if ($Tail -gt 0) { $pyArgs += "--tail", "$Tail" }
if ($Yes) { $pyArgs += "-y" }
if ($SkipPull) { $pyArgs += "--skip-pull" }
if ($SkipAi) { $pyArgs += "--skip-ai" }
if ($SkipCommit) { $pyArgs += "--skip-commit" }

python @pyArgs
exit $LASTEXITCODE