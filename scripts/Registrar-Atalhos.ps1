$ErrorActionPreference = 'Stop'
$productsRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$catalogRoot = 'C:\proj\apps-pessoais'
$catalogPath = Join-Path $catalogRoot 'apps.json'
$catalog = Get-Content -LiteralPath $catalogPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ids = @('blog-mayccoisa', 'blog-jogos')
$names = @('Blog Mayccoisa', 'Blog de jogos')
$existingApps = @($catalog.apps | Where-Object { $_.id -notin $ids })
$newApps = @()
for ($i = 0; $i -lt $ids.Count; $i++) {
    $entryScript = Join-Path $productsRoot ($ids[$i] + '\scripts\Abrir-Blog.vbs')
    if (-not (Test-Path -LiteralPath $entryScript)) { throw "Inicializador nao encontrado: $entryScript" }
    $newApps += [pscustomobject]@{id=$ids[$i];nome=$names[$i];tipo='exe';exe=@($entryScript);icone=($env:SystemRoot + '\System32\imageres.dll,1')}
}
$catalog.apps = @($existingApps) + @($newApps)
$catalog | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $catalogPath -Encoding UTF8
$shortcutRoot = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Apps pessoais'
New-Item -ItemType Directory -Path $shortcutRoot -Force | Out-Null
$shell = New-Object -ComObject WScript.Shell
foreach ($entry in $newApps) {
    $shortcut = $shell.CreateShortcut((Join-Path $shortcutRoot ($entry.nome + '.lnk')))
    $shortcut.TargetPath = Join-Path $env:SystemRoot 'System32\wscript.exe'
    $shortcut.Arguments = '"' + (Join-Path $catalogRoot 'Abrir.vbs') + '" ' + $entry.id
    $shortcut.WorkingDirectory = $catalogRoot
    $shortcut.IconLocation = $entry.icone
    $shortcut.Description = 'apps-pessoais:' + $entry.id
    $shortcut.Save()
    Write-Output ('Atalho criado: ' + $entry.nome)
}
