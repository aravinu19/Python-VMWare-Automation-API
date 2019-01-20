$server = $args[0]
$username = $args[1]
$password = $args[2]
$vmname = $args[3]
$memory = $args[4]
$vdisk = $args[5]

Connect-VIServer -Server $server -User $username -Password $password
New-VM -Name $vmname -MemoryMB $memory -DiskGB $vdisk
