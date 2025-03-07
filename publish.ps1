# Parameter für GitHub-Benutzernamen
param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername
)

Write-Host "Initialisiere Git-Repository..." -ForegroundColor Green
git init

Write-Host "Füge Remote-Repository hinzu..." -ForegroundColor Green
git remote add origin "https://github.com/$GitHubUsername/ha-soyosource.git"

Write-Host "Aktualisiere Dateien mit GitHub-Benutzernamen..." -ForegroundColor Green
(Get-Content README.md) -replace 'yourusername', $GitHubUsername | Set-Content README.md
(Get-Content INFO.md) -replace 'yourusername', $GitHubUsername | Set-Content INFO.md
(Get-Content custom_components/soyosource/manifest.json) -replace 'yourusername', $GitHubUsername | Set-Content custom_components/soyosource/manifest.json
(Get-Content LICENSE) -replace 'yourusername', $GitHubUsername | Set-Content LICENSE

Write-Host "Füge Dateien zum Repository hinzu..." -ForegroundColor Green
git add .

Write-Host "Erstelle ersten Commit..." -ForegroundColor Green
git commit -m "Initial commit: Soyosource Controller Integration"

Write-Host "Erstelle main Branch..." -ForegroundColor Green
git branch -M main

Write-Host "Pushe Code zu GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "Erstelle Release v1.0.0..." -ForegroundColor Green
git tag -a v1.0.0 -m "Erste Version der Soyosource Controller Integration"
git push origin v1.0.0

Write-Host "Fertig! Repository wurde erfolgreich auf GitHub veröffentlicht." -ForegroundColor Green
Write-Host "Besuchen Sie https://github.com/$GitHubUsername/ha-soyosource" -ForegroundColor Green 