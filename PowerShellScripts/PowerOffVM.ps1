$hostip = $args[0]
$username = $args[1]
$password = $args[2]
$vmname = $args[3]

Connect-VIServer -Server $hostip -User $username -Password $password
Stop-VM -VM $vmname -Confirm:$False | Format-Table -Property PowerState | Out-File txtFiles\vmstate.txt -Encoding utf8
