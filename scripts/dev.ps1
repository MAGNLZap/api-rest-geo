param(
    [ValidateSet("api", "web")]
    [string]$Service = "web",
    [int]$ApiPort = 8001
)

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Push-Location $Root
$Names = @("ENVIRONMENT", "DATABASE_URL", "HOST", "PORT", "ROOT_PATH", "API_PROXY_TARGET", "VITE_PUBLIC_BASE", "VITE_API_BASE")
$Previous = @{}
foreach ($Name in $Names) { $Previous[$Name] = [Environment]::GetEnvironmentVariable($Name, "Process") }

try {
    if ($Service -eq "api") {
        $Python = Join-Path $Root ".venv\Scripts\python.exe"
        if (-not (Test-Path $Python)) { throw "Crea .venv e instala requirements-dev.txt primero." }
        $env:ENVIRONMENT = "development"
        $env:HOST = "127.0.0.1"
        $env:PORT = "$ApiPort"
        $env:ROOT_PATH = ""
        & $Python -m uvicorn scripts.dev_api:create_app --factory --host 127.0.0.1 --port $ApiPort --reload --reload-dir app
    } else {
        Set-Location (Join-Path $Root "frontend")
        $env:API_PROXY_TARGET = "http://127.0.0.1:$ApiPort"
        $env:VITE_PUBLIC_BASE = "/"
        $env:VITE_API_BASE = ""
        & npm run dev
    }
    if ($LASTEXITCODE -ne 0) { throw "El proceso terminó con código $LASTEXITCODE." }
} finally {
    foreach ($Name in $Names) {
        [Environment]::SetEnvironmentVariable($Name, $Previous[$Name], "Process")
    }
    Pop-Location
}
