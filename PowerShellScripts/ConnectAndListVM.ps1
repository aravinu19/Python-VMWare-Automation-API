$hostip = $args[0]
$username = $args[1]
$password = $args[2]

Connect-VIServer -Server $hostip -User $username -Password $password
Get-VM | Format-Table -Property Name, PowerState | Out-File txtFiles\vmlist.txt -Encoding utf8
