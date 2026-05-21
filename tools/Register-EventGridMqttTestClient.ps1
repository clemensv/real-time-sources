<#
.SYNOPSIS
Register a read-only MQTT test client on an Azure Event Grid namespace using
a freshly-generated self-signed certificate.

.DESCRIPTION
Given an Event Grid namespace (resource group + name), this script:

  1. Generates a self-signed RSA 2048 certificate locally (no OpenSSL required).
  2. Writes three PEM files into -OutputDirectory (default: current directory):
        <ClientName>.crt   - client certificate (self-signed; used for auth
                              against the Event Grid namespace)
        <ClientName>.key   - client private key (PKCS#8, unencrypted)
        <ClientName>-ca.crt - the *broker's* server-cert chain (root +
                              intermediates) fetched live from the namespace;
                              point MQTTX / mosquitto at it as the "CA file".
  3. Registers an Event Grid namespace Client with ThumbprintMatch
     authentication so the namespace accepts the cert.
  4. Creates (or reuses) a dedicated client group bound to the new client via
     a custom attribute (default attribute: role=reader-test).
  5. Creates a Subscriber-only permission binding on the chosen topic space.

The resulting identity has *no* publish permission - it can only subscribe.

The Event Grid namespace MUST already have at least one topic space; pass
-TopicSpaceName to pick a specific one, otherwise the first topic space
returned by the API is used.

.PARAMETER ResourceGroup
Azure resource group that contains the Event Grid namespace.

.PARAMETER NamespaceName
Event Grid namespace name.

.PARAMETER SubscriptionId
Optional. Switches the Azure CLI to this subscription for the duration of
the script. If omitted, the currently selected subscription is used.

.PARAMETER ClientName
Optional. Name for the new namespace Client resource and certificate CN.
Defaults to "mqttx-reader-<random>".

.PARAMETER TopicSpaceName
Optional. Topic space to bind Subscriber permission against. Defaults to the
first topic space found in the namespace.

.PARAMETER ClientGroupName
Optional. Client group to create/reuse. Defaults to "readers".

.PARAMETER OutputDirectory
Optional. Directory to write the cert/key/CA files to. Defaults to current
directory.

.PARAMETER CertValidityDays
Optional. Self-signed cert validity in days. Defaults to 365.

.EXAMPLE
PS> ./tools/Register-EventGridMqttTestClient.ps1 `
        -ResourceGroup pegelonline-mqtt-test `
        -NamespaceName pegmqtt-egns

Generates mqttx-reader-<random>.{crt,key} + the CA file in the working
directory, registers the client, grants Subscriber permission, and prints
the broker hostname and MQTTX connection instructions.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [Parameter(Mandatory)]
    [string]$NamespaceName,

    [string]$SubscriptionId,

    [string]$ClientName,

    [string]$TopicSpaceName,

    [string]$ClientGroupName = 'readers',

    [string]$OutputDirectory = (Get-Location).Path,

    [int]$CertValidityDays = 365
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-Az {
    param([Parameter(ValueFromRemainingArguments)][string[]]$AzArgs)
    # Capture stdout only; let stderr pass through so the user sees real errors.
    # The eventgrid extension prints harmless Python SyntaxWarnings to stderr;
    # mixing them with stdout breaks ConvertFrom-Json.
    $out = & az @AzArgs
    if ($LASTEXITCODE -ne 0) {
        throw "az $($AzArgs -join ' ') failed (exit code $LASTEXITCODE)."
    }
    return $out
}

function ConvertTo-Pem {
    param([string]$Label, [byte[]]$Bytes)
    $b64 = [Convert]::ToBase64String($Bytes)
    $lines = @()
    for ($i = 0; $i -lt $b64.Length; $i += 64) {
        $len = [Math]::Min(64, $b64.Length - $i)
        $lines += $b64.Substring($i, $len)
    }
    return "-----BEGIN $Label-----`n" + ($lines -join "`n") + "`n-----END $Label-----`n"
}

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    throw "Azure CLI 'az' not found in PATH."
}

if ($SubscriptionId) {
    Write-Host "Selecting subscription $SubscriptionId..."
    Invoke-Az account set --subscription $SubscriptionId | Out-Null
}

if (-not $ClientName) {
    $rand = -join ((97..122) | Get-Random -Count 6 | ForEach-Object { [char]$_ })
    $ClientName = "mqttx-reader-$rand"
}

# Validate ClientName matches EG client resource naming rules:
#   ^[-a-zA-Z0-9:\._]*$
if ($ClientName -notmatch '^[-a-zA-Z0-9:\._]+$') {
    throw "ClientName '$ClientName' contains characters not allowed for Event Grid namespace clients."
}

if (-not (Test-Path -LiteralPath $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path

Write-Host ""
Write-Host "=== Event Grid MQTT test client registration ==="
Write-Host "  Namespace        : $NamespaceName ($ResourceGroup)"
Write-Host "  Client name      : $ClientName"
Write-Host "  Client group     : $ClientGroupName"
Write-Host "  Output directory : $OutputDirectory"
Write-Host ""

# ── 1. Resolve namespace hostname + optional topic space ──────────────────
Write-Host "Reading namespace properties..."
$nsJson = Invoke-Az eventgrid namespace show `
    --resource-group $ResourceGroup `
    --name $NamespaceName `
    --output json
$ns = ($nsJson -join "`n") | ConvertFrom-Json
$hostname = $ns.topicSpacesConfiguration.hostname
if (-not $hostname) {
    throw "Namespace '$NamespaceName' has no MQTT hostname; is the MQTT broker enabled?"
}
Write-Host "  MQTT broker     : ${hostname}:8883"

if (-not $TopicSpaceName) {
    Write-Host "Looking up first topic space..."
    $tsJson = Invoke-Az eventgrid namespace topic-space list `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --output json
    $tsList = ($tsJson -join "`n") | ConvertFrom-Json
    if (-not $tsList -or $tsList.Count -eq 0) {
        throw "Namespace '$NamespaceName' has no topic spaces. Create one before running this script."
    }
    $TopicSpaceName = $tsList[0].name
    Write-Host "  Topic space     : $TopicSpaceName (auto-selected)"
} else {
    Write-Host "  Topic space     : $TopicSpaceName"
}

# ── 2. Generate self-signed certificate locally ───────────────────────────
Write-Host ""
Write-Host "Generating self-signed RSA 2048 certificate (CN=$ClientName)..."
Add-Type -AssemblyName System.Security
$rsa = [System.Security.Cryptography.RSA]::Create(2048)
try {
    $subject = "CN=$ClientName"
    $req = [System.Security.Cryptography.X509Certificates.CertificateRequest]::new(
        $subject,
        $rsa,
        [System.Security.Cryptography.HashAlgorithmName]::SHA256,
        [System.Security.Cryptography.RSASignaturePadding]::Pkcs1)

    # Basic constraints: not a CA.
    $req.CertificateExtensions.Add(
        [System.Security.Cryptography.X509Certificates.X509BasicConstraintsExtension]::new($false, $false, 0, $true))
    # Key usage: digital signature + key encipherment for TLS client auth.
    $req.CertificateExtensions.Add(
        [System.Security.Cryptography.X509Certificates.X509KeyUsageExtension]::new(
            'DigitalSignature, KeyEncipherment', $true))
    # Enhanced Key Usage: client auth.
    $clientAuthOid = [System.Security.Cryptography.Oid]::new('1.3.6.1.5.5.7.3.2', 'Client Authentication')
    $oidCol = [System.Security.Cryptography.OidCollection]::new()
    $oidCol.Add($clientAuthOid) | Out-Null
    $req.CertificateExtensions.Add(
        [System.Security.Cryptography.X509Certificates.X509EnhancedKeyUsageExtension]::new($oidCol, $true))
    # Subject Key Identifier - good hygiene.
    $req.CertificateExtensions.Add(
        [System.Security.Cryptography.X509Certificates.X509SubjectKeyIdentifierExtension]::new($req.PublicKey, $false))

    $notBefore = [DateTimeOffset]::UtcNow.AddMinutes(-5)
    $notAfter  = [DateTimeOffset]::UtcNow.AddDays($CertValidityDays)
    $cert = $req.CreateSelfSigned($notBefore, $notAfter)
    $thumbprint = $cert.Thumbprint

    # Serialize to PEM via the module-scope ConvertTo-Pem function.
    $certPem = ConvertTo-Pem -Label 'CERTIFICATE' -Bytes $cert.RawData
    $keyPem  = ConvertTo-Pem -Label 'PRIVATE KEY' -Bytes ($rsa.ExportPkcs8PrivateKey())

    $certPath = Join-Path $OutputDirectory "$ClientName.crt"
    $keyPath  = Join-Path $OutputDirectory "$ClientName.key"
    $caPath   = Join-Path $OutputDirectory "$ClientName-ca.crt"

    # Use plain ASCII (no BOM) so OpenSSL/mosquitto/MQTTX parse the PEMs cleanly.
    [System.IO.File]::WriteAllText($certPath, $certPem, [System.Text.UTF8Encoding]::new($false))
    [System.IO.File]::WriteAllText($keyPath,  $keyPem,  [System.Text.UTF8Encoding]::new($false))

    Write-Host "  Thumbprint      : $thumbprint"
    Write-Host "  Cert            : $certPath"
    Write-Host "  Key             : $keyPath"
}
finally {
    $rsa.Dispose()
}

# ── Fetch the broker's server certificate chain so clients can validate TLS ──
# The Event Grid MQTT broker presents a publicly-trusted server cert (issued
# by a Microsoft / DigiCert CA). We write the full chain (root + intermediates)
# to <ClientName>-ca.crt so MQTTX/mosquitto can trust it without relying on
# the OS trust store.
Write-Host ""
Write-Host "Fetching broker server certificate chain from ${hostname}:8883..."
$brokerChainPem = ""
try {
    $tcp = [System.Net.Sockets.TcpClient]::new()
    $tcp.Connect($hostname, 8883)
    $ssl = [System.Net.Security.SslStream]::new(
        $tcp.GetStream(),
        $false,
        [System.Net.Security.RemoteCertificateValidationCallback]{ param($s,$c,$ch,$e) return $true })
    $ssl.AuthenticateAsClient($hostname)
    $remoteCert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new($ssl.RemoteCertificate)
    $chain = [System.Security.Cryptography.X509Certificates.X509Chain]::new()
    $chain.ChainPolicy.RevocationMode = [System.Security.Cryptography.X509Certificates.X509RevocationMode]::NoCheck
    [void]$chain.Build($remoteCert)
    foreach ($el in $chain.ChainElements) {
        $brokerChainPem += ConvertTo-Pem -Label 'CERTIFICATE' -Bytes $el.Certificate.RawData
    }
    $ssl.Dispose(); $tcp.Dispose()
}
catch {
    Write-Warning "Could not fetch broker chain ($_). The -ca.crt file will be empty; MQTTX may fall back to the OS trust store."
}
[System.IO.File]::WriteAllText($caPath, $brokerChainPem, [System.Text.UTF8Encoding]::new($false))
Write-Host "  Broker CA chain : $caPath"

# ── 3. Register / update the Event Grid namespace client ───────────────────
Write-Host ""
Write-Host "Registering namespace client '$ClientName'..."
$attrJson = '{"role":"reader-test"}'
$authJson = "{`"validationScheme`":`"ThumbprintMatch`",`"allowedThumbprints`":[`"$thumbprint`"]}"

$existing = $null
try {
    $existingRaw = & az eventgrid namespace client show `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $ClientName `
        --output json 2>$null
    if ($LASTEXITCODE -eq 0 -and $existingRaw) {
        $existing = ($existingRaw -join "`n") | ConvertFrom-Json
    }
}
catch { $existing = $null }

if ($existing) {
    Write-Host "  Client already exists; updating thumbprint allow-list..."
    Invoke-Az eventgrid namespace client update `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $ClientName `
        --client-certificate-authentication $authJson `
        --attributes $attrJson `
        --state Enabled | Out-Null
} else {
    Invoke-Az eventgrid namespace client create `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $ClientName `
        --authentication-name $ClientName `
        --client-certificate-authentication $authJson `
        --attributes $attrJson `
        --state Enabled | Out-Null
}

# ── 4. Ensure the client group exists ─────────────────────────────────────
Write-Host "Ensuring client group '$ClientGroupName' exists..."
$cgQuery = "attributes.role = 'reader-test'"

$cgExists = $false
try {
    & az eventgrid namespace client-group show `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $ClientGroupName `
        --output none 2>$null
    if ($LASTEXITCODE -eq 0) { $cgExists = $true }
}
catch { $cgExists = $false }

if (-not $cgExists) {
    Invoke-Az eventgrid namespace client-group create `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $ClientGroupName `
        --group-query $cgQuery | Out-Null
} else {
    Write-Host "  (reusing existing client group)"
}

# ── 5. Ensure the Subscriber permission binding exists ────────────────────
$bindingName = "$ClientGroupName-sub-$TopicSpaceName"
# Trim to <= 50 chars; EG namespace binding names allow letters/digits/dashes.
if ($bindingName.Length -gt 50) { $bindingName = $bindingName.Substring(0,50) }

Write-Host "Ensuring Subscriber permission binding '$bindingName'..."
$pbExists = $false
try {
    & az eventgrid namespace permission-binding show `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $bindingName `
        --output none 2>$null
    if ($LASTEXITCODE -eq 0) { $pbExists = $true }
}
catch { $pbExists = $false }

if (-not $pbExists) {
    Invoke-Az eventgrid namespace permission-binding create `
        --resource-group $ResourceGroup `
        --namespace-name $NamespaceName `
        --name $bindingName `
        --client-group-name $ClientGroupName `
        --topic-space-name $TopicSpaceName `
        --permission Subscriber | Out-Null
} else {
    Write-Host "  (reusing existing permission binding)"
}

# ── 6. Print connection summary ───────────────────────────────────────────
Write-Host ""
Write-Host "=== Done ==="
Write-Host ""
Write-Host "MQTT broker         : ${hostname}:8883 (TLS, MQTT 5)"
Write-Host "Client ID / Username: $ClientName"
Write-Host "Auth                : X.509 client certificate (Thumbprint match)"
Write-Host "Permission          : Subscriber only (topic space '$TopicSpaceName')"
Write-Host ""
Write-Host "MQTTX setup:"
Write-Host "  Host          : $hostname"
Write-Host "  Port          : 8883"
Write-Host "  SSL/TLS       : enabled"
Write-Host "  SSL Secure    : enabled"
Write-Host "  CA file       : $caPath"
Write-Host "  Client cert   : $certPath"
Write-Host "  Client key    : $keyPath"
Write-Host "  Client ID     : $ClientName"
Write-Host "  Username      : $ClientName"
Write-Host "  MQTT version  : 5.0"
Write-Host ""
Write-Host "Try subscribing to '#' once connected. Publishing will be rejected."
