param(
    [switch]$SemReiniciar
)

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
$origem = Join-Path $raiz 'theme\mayccoisa'
$destino = Join-Path $raiz 'ghost\content\themes\mayccoisa'
$compose = Join-Path $raiz 'ghost\compose.yaml'

if (-not (Test-Path -LiteralPath $origem)) {
    throw "Tema nao encontrado em $origem."
}

New-Item -ItemType Directory -Path $destino -Force | Out-Null

$robocopy = Start-Process -FilePath 'robocopy.exe' `
    -ArgumentList @($origem, $destino, '/MIR', '/NFL', '/NDL', '/NJH', '/NJS') `
    -Wait -PassThru -WindowStyle Hidden

if ($robocopy.ExitCode -ge 8) {
    throw "Falha ao copiar o tema (robocopy codigo $($robocopy.ExitCode))."
}

Write-Output "Tema copiado para $destino."

if ($SemReiniciar) {
    Write-Output 'Reinicio do Ghost ignorado (-SemReiniciar).'
    exit 0
}

& docker compose -f $compose restart
if ($LASTEXITCODE -ne 0) {
    throw 'Falha ao reiniciar o Ghost.'
}

$limite = (Get-Date).AddSeconds(120)
do {
    Start-Sleep -Milliseconds 800
    try {
        $resposta = Invoke-WebRequest -Uri 'http://localhost:2368' -UseBasicParsing -TimeoutSec 3
        if ($resposta.StatusCode -eq 200) { break }
    } catch {
        # ainda subindo
    }
} while ((Get-Date) -lt $limite)

Write-Output 'Ghost pronto em http://localhost:2368'
