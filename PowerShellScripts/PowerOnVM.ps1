$hostip = $args[0]
$username = $args[1]
$password = $args[2]
$vmname = $args[3]

Connect-VIServer -Server $hostip -User $username -Password $password
Start-VM $vmname | Format-Table -Property PowerState | Out-File txtFiles\vmstate.txt -Encoding utf8
