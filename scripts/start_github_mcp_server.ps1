param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ServerArgs
)

$ErrorActionPreference = "Stop"

function Set-TokenFromDotEnv {
    param(
        [string]$EnvPath
    )

    if (-not (Test-Path -LiteralPath $EnvPath)) {
        return $false
    }

    foreach ($rawLine in Get-Content -LiteralPath $EnvPath) {
        $line = $rawLine.Trim()
        if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
            continue
        }

        $parts = $line.Split("=", 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim("'").Trim('"')
        if ($key -eq "GITHUB_PERSONAL_ACCESS_TOKEN" -and $value) {
            $env:GITHUB_PERSONAL_ACCESS_TOKEN = $value
            return $true
        }
    }

    return $false
}

function Set-TokenFromGitCredential {
    $query = "protocol=https`nhost=github.com`nusername=Semih702`n`n"
    $credentialOutput = $query | git credential fill
    $tokenLine = ($credentialOutput | Select-String '^password=').Line
    if ($tokenLine) {
        $env:GITHUB_PERSONAL_ACCESS_TOKEN = $tokenLine.Substring(9)
        return $true
    }

    return $false
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $repoRoot "mcp_attack_lab/.env.local"

if (-not $env:GITHUB_PERSONAL_ACCESS_TOKEN) {
    $loaded = Set-TokenFromDotEnv -EnvPath $envPath
    if (-not $loaded) {
        $loaded = Set-TokenFromGitCredential
    }

    if (-not $loaded -or -not $env:GITHUB_PERSONAL_ACCESS_TOKEN) {
        throw "GITHUB_PERSONAL_ACCESS_TOKEN could not be resolved from .env.local or Git Credential Manager."
    }
}

$serverBin = "D:/github-mcp-server-official/github-mcp-server.exe"
if (-not (Test-Path -LiteralPath $serverBin)) {
    throw "GitHub MCP server binary not found at $serverBin"
}

& $serverBin @ServerArgs
exit $LASTEXITCODE
