# Script PowerShell pour ajouter Python312 au PATH utilisateur

$pythonPath = "C:\Users\lumiere\AppData\Local\Programs\Python\Python312"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -notlike "*$pythonPath*") {
    $newPath = "$currentPath;$pythonPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Output "Le chemin Python312 a été ajouté au PATH utilisateur."
} else {
    Write-Output "Le chemin Python312 est déjà présent dans le PATH utilisateur."
}
