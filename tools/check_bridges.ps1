Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*inventor*" -or $_.Path -like "*revit*" } | Format-Table Id, Path, StartTime -AutoSize

Write-Host ""
Write-Host "Puertos activos:"
netstat -ano | findstr ":8766" | findstr "LISTEN"
netstat -ano | findstr ":8767" | findstr "LISTEN"
netstat -ano | findstr ":8765" | findstr "LISTEN"
