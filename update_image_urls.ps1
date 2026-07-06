$apiKey = "ST5KnLuFneugVGRCuZdkeBq4bCH41aQZ13TE8SZ993A4UXJCjUKqYglM"
$jsonPath = "c:/Users/DMT/Documents/GitHub/Api/aarti.json"
# Ensure we read the file as UTF-8
$json = Get-Content -Raw -Path $jsonPath -Encoding UTF8 | ConvertFrom-Json

foreach ($item in $json.Aarti) {
    $query = $item.god_name
    $encodedQuery = [uri]::EscapeDataString($query)
    # Fetch top 5 large images
    $url = "https://api.pexels.com/v1/search?query=$encodedQuery&per_page=5&size=large"

    try {
        $headers = @{ "Authorization" = $apiKey }
        $response = Invoke-RestMethod -Headers $headers -Uri $url -Method Get

        if ($response.photos.Count -gt 0) {
            # Pick a random photo to get a less basic/more artistic image
            $randomIndex = Get-Random -Minimum 0 -Maximum $response.photos.Count
            $item.image_url = $response.photos[$randomIndex].src.original
            Write-Host "Updated $($query)"
        } else {
            Write-Warning "No photo found for $($query)"
        }
    } catch {
        Write-Error "Failed to fetch image for $($query): $_"
    }
}

# Convert back to JSON
$jsonString = $json | ConvertTo-Json -Depth 10

# Windows PowerShell's ConvertTo-Json escapes Unicode characters as \uXXXX.
# This unescapes ONLY \uXXXX sequences to avoid unescaping \n, \r, \t, etc.
$jsonString = [System.Text.RegularExpressions.Regex]::Replace($jsonString, '(?i)\\u([0-9a-f]{4})', {
    param($match)
    return [char][int]("0x" + $match.Groups[1].Value)
})

# Write the file back with UTF8 encoding
$jsonString | Set-Content -Path $jsonPath -Encoding UTF8
Write-Host "All done! aarti.json has been updated."
