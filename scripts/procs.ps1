$totalRAM = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory
$totalCPU = (Get-Process | Measure-Object CPU -Sum).Sum

Get-Process | Group-Object Name | ForEach-Object {
    $cpuSum = ($_.Group | Measure-Object CPU -Sum).Sum
    $ramSum = ($_.Group | Measure-Object WorkingSet64 -Sum).Sum

    [PSCustomObject]@{
        Name = $_.Name
        CPU = if ($totalCPU -ne 0) { [math]::Round(($cpuSum / $totalCPU) * 100) } else { 0 }
        RAM = if ($totalRAM -ne 0) { [math]::Round(($ramSum / $totalRAM) * 100) } else { 0 }
    }
} | Sort-Object RAM -Descending | Select-Object -First 30 | ConvertTo-Csv -NoTypeInformation | Select-Object -Skip 1