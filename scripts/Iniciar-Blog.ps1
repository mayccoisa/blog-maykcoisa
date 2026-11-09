param([switch]$SemAbrir)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$config = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'blog-local.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$logRoot = Join-Path $env:LOCALAPPDATA ('AppsPessoais\logs\' + $config.id)
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
$mutex = New-Object Threading.Mutex($false, ('Local\Iniciar-' + $config.id))
$locked = $false

function Http-Pronto([string]$url, [string]$marca = '') {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
        return $response.StatusCode -eq 200 -and (-not $marca -or $response.Content.Contains($marca))
    } catch { return $false }
}

function Aguardar-Http([string]$url, [string]$marca = '') {
    $deadline = (Get-Date).AddSeconds(150)
    while ((Get-Date) -lt $deadline) {
        if (Http-Pronto $url $marca) { return }
        Start-Sleep -Milliseconds 750
    }
    throw "A pagina nao respondeu em $url. Consulte os logs em $logRoot."
}

function Executar-Docker([string]$argumentos, [string]$logName) {
    $process = Start-Process -FilePath $docker -ArgumentList $argumentos -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput (Join-Path $logRoot ($logName + '.log')) -RedirectStandardError (Join-Path $logRoot ($logName + '.err.log'))
    return $process.ExitCode
}

try {
    $locked = $mutex.WaitOne(240000)
    if (-not $locked) { throw 'Outra inicializacao ainda esta em andamento. Tente novamente em alguns instantes.' }
    $docker = (Get-Command docker.exe -ErrorAction Stop).Source
    $dockerExit = Executar-Docker 'info --format {{.ServerVersion}}' 'docker'
    if ($dockerExit -ne 0) {
        $desktopExe = Join-Path $env:ProgramFiles 'Docker\Docker\Docker Desktop.exe'
        if (-not (Test-Path -LiteralPath $desktopExe)) { throw 'Docker Desktop nao encontrado.' }
        Start-Process -FilePath $desktopExe -WindowStyle Hidden
        $deadline = (Get-Date).AddSeconds(150)
        do {
            Start-Sleep -Seconds 2
            $dockerExit = Executar-Docker 'info --format {{.ServerVersion}}' 'docker'
            if ($dockerExit -eq 0) { break }
        } while ((Get-Date) -lt $deadline)
        if ($dockerExit -ne 0) { throw 'O Docker nao iniciou. Abra o Docker Desktop e conclua eventuais avisos de inicializacao.' }
    }
    $composePath = Join-Path $projectRoot 'ghost\compose.yaml'
    if ((Executar-Docker ('compose -f "' + $composePath + '" up -d') 'compose') -ne 0) { throw "Falha ao iniciar o Ghost. Consulte os logs compose em $logRoot." }
    Aguardar-Http $config.ghostUrl
    Aguardar-Http ($config.ghostUrl + '/ghost/')

    if ($config.preview) {
        if (-not (Http-Pronto $config.openUrl 'Mayccoisa')) {
            $node = (Get-Command node.exe -ErrorAction Stop).Source
            Start-Process -FilePath $node -ArgumentList 'visual/server.mjs' -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logRoot 'visual.out.log') -RedirectStandardError (Join-Path $logRoot 'visual.err.log')
        }
        Aguardar-Http $config.openUrl 'Mayccoisa'
    }
    if (-not $SemAbrir) { Start-Process $config.openUrl }
    Write-Output ($config.nome + ' pronto em ' + $config.openUrl + '. Painel: ' + $config.ghostUrl + '/ghost/')
} catch {
    $_.Exception.Message | Set-Content -LiteralPath (Join-Path $logRoot 'erro.log') -Encoding UTF8
    if ($SemAbrir) { Write-Error $_.Exception.Message } else {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, $config.nome, 'OK', 'Error') | Out-Null
    }
    exit 1
} finally {
    if ($locked) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}
