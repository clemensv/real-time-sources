param(
    [Parameter(Mandatory = $true)]
    [string]$XregPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-JsonPropertyValue {
    param(
        [Parameter(Mandatory = $true)]
        [object]$InputObject,

        [Parameter(Mandatory = $true)]
        [string]$PropertyName
    )

    if ($InputObject -is [System.Collections.IDictionary]) {
        return $InputObject[$PropertyName]
    }

    if ($InputObject -is [System.Array]) {
        return $InputObject[[int]$PropertyName]
    }

    $property = $InputObject.PSObject.Properties[$PropertyName]
    if ($null -eq $property) {
        throw "Property '$PropertyName' was not found while resolving JSON pointer."
    }

    return $property.Value
}

function Resolve-JsonPointer {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Document,

        [Parameter(Mandatory = $true)]
        [string]$Pointer
    )

    if (-not $Pointer.StartsWith("#/")) {
        throw "Only local JSON pointers are supported. Got '$Pointer'."
    }

    $current = $Document
    foreach ($segment in $Pointer.Substring(2).Split('/')) {
        $token = $segment.Replace('~1', '/').Replace('~0', '~')
        $current = Get-JsonPropertyValue -InputObject $current -PropertyName $token
    }

    return $current
}

function Get-SchemaVersionEntry {
    param(
        [Parameter(Mandatory = $true)]
        [object]$XregDocument,

        [Parameter(Mandatory = $true)]
        [string]$SchemaUri
    )

    $schemaEntry = Resolve-JsonPointer -Document $XregDocument -Pointer $SchemaUri
    if ($schemaEntry.PSObject.Properties["versions"]) {
        $defaultVersionId = [string]$schemaEntry.defaultversionid
        if ([string]::IsNullOrWhiteSpace($defaultVersionId)) {
            throw "Schema '$SchemaUri' does not declare a defaultversionid."
        }

        return Get-JsonPropertyValue -InputObject $schemaEntry.versions -PropertyName $defaultVersionId
    }

    if ($schemaEntry.PSObject.Properties["schema"]) {
        return $schemaEntry
    }

    throw "Schema '$SchemaUri' does not resolve to a schema version entry."
}

function Get-RecordTypeName {
    param(
        [Parameter(Mandatory = $true)]
        [object]$SchemaObject,

        [string]$SchemaEntryName
    )

    $rootProperty = $SchemaObject.PSObject.Properties['$root']
    if ($rootProperty -and -not [string]::IsNullOrWhiteSpace([string]$rootProperty.Value)) {
        $rootPointer = [string]$rootProperty.Value
        $rootDefinition = Resolve-JsonPointer -Document $SchemaObject -Pointer $rootPointer
        if ($rootDefinition.PSObject.Properties["name"] -and -not [string]::IsNullOrWhiteSpace([string]$rootDefinition.name)) {
            return [string]$rootDefinition.name
        }

        $segments = $rootPointer.Substring(2).Split('/')
        return $segments[$segments.Length - 1]
    }

    if (-not [string]::IsNullOrWhiteSpace($SchemaEntryName)) {
        return $SchemaEntryName
    }

    if ($SchemaObject.PSObject.Properties["name"] -and -not [string]::IsNullOrWhiteSpace([string]$SchemaObject.name)) {
        return [string]$SchemaObject.name
    }

    throw "Schema '$($SchemaObject.'$id')' does not declare a `$root pointer and has no usable fallback name."
}

function ConvertTo-NormalizedSchemaJson {
    param(
        [Parameter(Mandatory = $true)]
        [object]$SchemaObject,

        [Parameter(Mandatory = $true)]
        [string]$RecordType
    )

    $schemaHash = $SchemaObject | ConvertTo-Json -Depth 100 | ConvertFrom-Json -AsHashtable

    function Normalize-SchemaNode {
        param(
            [object]$Node
        )

        if ($null -eq $Node) {
            return $null
        }

        if ($Node -is [System.Collections.IDictionary]) {
            foreach ($key in @($Node.Keys)) {
                $Node[$key] = Normalize-SchemaNode -Node $Node[$key]
            }

            if ($Node.Contains('type')) {
                $typeValue = $Node['type']

                if ($typeValue -is [System.Collections.IList] -and $typeValue -isnot [string]) {
                    $branches = @($typeValue)
                    $nonNullBranches = @($branches | Where-Object { -not ($_ -is [string] -and $_ -eq 'null') })

                    if ($branches.Count -eq 2 -and $nonNullBranches.Count -eq 1) {
                        $nonNullBranch = $nonNullBranches[0]
                        if ($nonNullBranch -is [System.Collections.IDictionary] -and $nonNullBranch.Contains('$ref')) {
                            $Node.Remove('type') | Out-Null
                            $Node['$ref'] = $nonNullBranch['$ref']
                        }
                        else {
                            $Node['type'] = $nonNullBranch
                        }
                    }
                }
                elseif ($typeValue -is [System.Collections.IDictionary] -and $typeValue.Contains('$ref')) {
                    $Node.Remove('type') | Out-Null
                    $Node['$ref'] = $typeValue['$ref']
                }
            }

            return $Node
        }

        if ($Node -is [System.Collections.IList] -and $Node -isnot [string]) {
            for ($index = 0; $index -lt $Node.Count; $index++) {
                $Node[$index] = Normalize-SchemaNode -Node $Node[$index]
            }

            return $Node
        }

        return $Node
    }

    $schemaHash = Normalize-SchemaNode -Node $schemaHash
    if (-not $schemaHash.ContainsKey('$root') -and $schemaHash.ContainsKey('type') -and $schemaHash['type'] -eq 'object') {
        $schemaHash['name'] = $RecordType
    }

    return $schemaHash | ConvertTo-Json -Depth 100
}

function Get-MessageEventType {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Message,

        [Parameter(Mandatory = $true)]
        [string]$FallbackType
    )

    if ($Message.PSObject.Properties["envelopemetadata"]) {
        $typeMetadata = $Message.envelopemetadata.PSObject.Properties["type"]
        if ($typeMetadata -and $typeMetadata.Value.PSObject.Properties["value"]) {
            $typeValue = [string]$typeMetadata.Value.value
            if (-not [string]::IsNullOrWhiteSpace($typeValue)) {
                return $typeValue
            }
        }
    }

    return $FallbackType
}

function Set-KqlEventTypes {
    param(
        [Parameter(Mandatory = $true)]
        [string]$KqlContent,

        [Parameter(Mandatory = $true)]
        [string[]]$EventTypes,

        [Parameter(Mandatory = $true)]
        [string]$RecordType
    )

    if ($EventTypes.Count -eq 0) {
        return $KqlContent
    }

    $eventTypeExpression = if ($EventTypes.Count -eq 1) {
        "type == '$($EventTypes[0].Replace("'", "''"))'"
    }
    else {
        $quotedTypes = $EventTypes | ForEach-Object { "'$($_.Replace("'", "''"))'" }
        "type in (" + ($quotedTypes -join ", ") + ")"
    }

    $pattern = "type\s*==\s*'" + [System.Text.RegularExpressions.Regex]::Escape($RecordType) + "'"
    return [System.Text.RegularExpressions.Regex]::Replace($KqlContent, $pattern, $eventTypeExpression, 1)
}

function Split-KqlChunks {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $chunks = New-Object System.Collections.Generic.List[string]
    $buffer = New-Object System.Collections.Generic.List[string]
    $insideFence = $false

    foreach ($line in ($Content -split "`r?`n")) {
        if ($line.Trim() -eq '```') {
            $insideFence = -not $insideFence
        }

        if (-not $insideFence -and [string]::IsNullOrWhiteSpace($line)) {
            if ($buffer.Count -gt 0) {
                $chunks.Add(($buffer -join "`r`n").TrimEnd())
                $buffer.Clear()
            }
            continue
        }

        $buffer.Add($line)
    }

    if ($buffer.Count -gt 0) {
        $chunks.Add(($buffer -join "`r`n").TrimEnd())
    }

    return $chunks
}

function Test-IsDispatchChunk {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Chunk
    )

    $firstLine = (($Chunk -split "`r?`n" | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -First 1).Trim())
    return (
        $firstLine -match '^[.]create-merge table \[_cloudevents_dispatch\]' -or
        $firstLine -match '^[.]create-or-alter table \[_cloudevents_dispatch\] ingestion json mapping' -or
        $firstLine -match '^[.]alter table \[_cloudevents_dispatch\] policy'
    )
}

$resolvedXregPath = (Resolve-Path $XregPath).Path
$resolvedOutputPath = [System.IO.Path]::GetFullPath($OutputPath)
$xregDocument = Get-Content $resolvedXregPath -Raw | ConvertFrom-Json

$schemaUris = New-Object System.Collections.Generic.List[string]
$seenSchemaUris = New-Object 'System.Collections.Generic.HashSet[string]'
$schemaEventTypes = @{}

foreach ($messageGroupProperty in $xregDocument.messagegroups.PSObject.Properties) {
    foreach ($messageProperty in $messageGroupProperty.Value.messages.PSObject.Properties) {
        $message = $messageProperty.Value
        if ($message.dataschemaformat -notlike 'JsonStructure*') {
            continue
        }

        $schemaUri = [string]$message.dataschemauri
        if ([string]::IsNullOrWhiteSpace($schemaUri)) {
            throw "Message '$($messageProperty.Name)' does not declare a dataschemauri."
        }

        if ($seenSchemaUris.Add($schemaUri)) {
            $schemaUris.Add($schemaUri)
            $schemaEventTypes[$schemaUri] = New-Object System.Collections.Generic.List[string]
        }

        $eventType = Get-MessageEventType -Message $message -FallbackType $messageProperty.Name
        if (-not $schemaEventTypes[$schemaUri].Contains($eventType)) {
            $schemaEventTypes[$schemaUri].Add($eventType)
        }
    }
}

if ($schemaUris.Count -eq 0) {
    throw "No JsonStructure dataschemauri references were found in '$resolvedXregPath'."
}

$outputDirectory = Split-Path -Parent $resolvedOutputPath
if (-not [string]::IsNullOrWhiteSpace($outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("kqlgen-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempRoot | Out-Null

try {
    $generatedPartFiles = New-Object System.Collections.Generic.List[string]
    $index = 0

    foreach ($schemaUri in $schemaUris) {
        $schemaEntry = Resolve-JsonPointer -Document $xregDocument -Pointer $schemaUri
        $schemaVersionEntry = Get-SchemaVersionEntry -XregDocument $xregDocument -SchemaUri $schemaUri
        $schemaObject = $schemaVersionEntry.schema
        $schemaEntryName = if ($schemaEntry.PSObject.Properties["name"]) { [string]$schemaEntry.name } else { "" }
        $recordType = Get-RecordTypeName -SchemaObject $schemaObject -SchemaEntryName $schemaEntryName
        $normalizedSchemaJson = ConvertTo-NormalizedSchemaJson -SchemaObject $schemaObject -RecordType $recordType

        $safeName = ($recordType -replace '[^A-Za-z0-9._-]', '_')
        $schemaFile = Join-Path $tempRoot ("{0:D3}-{1}.json" -f $index, $safeName)
        $kqlPartFile = Join-Path $tempRoot ("{0:D3}-{1}.kql" -f $index, $safeName)

        $normalizedSchemaJson | Set-Content -Path $schemaFile -Encoding UTF8
        & avrotize s2k $schemaFile --out $kqlPartFile --record-type $recordType --emit-cloudevents-columns --emit-cloudevents-dispatch
        if ($LASTEXITCODE -ne 0) {
            throw "avrotize s2k failed for schema '$schemaUri'."
        }

        $kqlContent = Get-Content $kqlPartFile -Raw
        $kqlContent = Set-KqlEventTypes -KqlContent $kqlContent -EventTypes $schemaEventTypes[$schemaUri].ToArray() -RecordType $recordType
        $kqlContent | Set-Content -Path $kqlPartFile -Encoding UTF8

        $generatedPartFiles.Add($kqlPartFile)
        $index++
    }

    $mergedChunks = New-Object System.Collections.Generic.List[string]
    $dispatchChunksSeen = New-Object 'System.Collections.Generic.HashSet[string]'

    foreach ($partFile in $generatedPartFiles) {
        foreach ($chunk in (Split-KqlChunks -Content (Get-Content $partFile -Raw))) {
            if (Test-IsDispatchChunk -Chunk $chunk) {
                $signature = (($chunk -split "`r?`n" | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -First 1).Trim())
                if (-not $dispatchChunksSeen.Add($signature)) {
                    continue
                }
            }

            $mergedChunks.Add($chunk)
        }
    }

    ($mergedChunks -join "`r`n`r`n") + "`r`n" | Set-Content -Path $resolvedOutputPath -Encoding UTF8
}
finally {
    if (Test-Path $tempRoot) {
        Remove-Item -Path $tempRoot -Recurse -Force
    }
}
