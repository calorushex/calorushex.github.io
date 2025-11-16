---
author: calorushex
date: '2025-11-16'
excerpt: "TechNova Systems\u2019 SOC has detected suspicious outbound traffic from\
  \ a public-facing IIS server in its cloud platform\u2014activity suggestive of a\
  \ web-shell drop and covert connections to an unknown host."
layout: post
tags:
- cyberdefenders
- memoryforensics
- writeup
- networkforensics
- malwareanalysis
title: CyberDefenders - Lockdown Writeup - Retired
---

## Scenario

TechNova Systems’ SOC has detected suspicious outbound traffic from a public-facing IIS server in its cloud platform—activity suggestive of a web-shell drop and covert connections to an unknown host.

As the forensic examiner, you have three critical artefacts in hand: a PCAP capturing the initial traffic, a full memory image of the server, and a malware sample recovered from disk. Reconstruct the intrusion and all of the attacker’s activities so TechNova can contain the breach and strengthen its defenses.

---
## Pcap Analysis

### Q1
After flooding the IIS host with rapid-fire probes, the attacker reveals their origin. Which IP address generated this reconnaissance traffic?

![](/assets/images/Pasted image 20251108121041.png)

Attacker host is 10.0.2.4 attacking the IIS site on 10.0.2.15

As well as looking at Conversations tab to determine large numbers of connections you can also see the the address sending mass SYN probes to different ports on the server (port scan)

**A:** 10.0.2.4

### Q2
Zeroing in on a single open service to gain a foothold, the attacker carries out targeted enumeration. Which MITRE ATT&CK technique ID covers this activity?

**A:** T1046

### Q3
While reviewing the SMB traffic, you observe two consecutive Tree Connect requests that expose the first shares the intruder probes on the IIS host. Which two full UNC paths are accessed?

![](/assets/images/Pasted image 20251108123225.png)

Filtering for the addresses and SMBv2 you can see two connection requests to Documents and IPC$ shares.

**A:** \\10.0.2.15\Documents, \\10.0.2.15\IPC$

### Q4
Inside the share, the attacker plants a web-accessible payload that will grant remote code execution. What is the filename of the malicious file they uploaded, and what byte length is specified in the corresponding SMB2 Write Request?

![](/assets/images/Pasted image 20251108123741.png)

**A:** shell.aspx, 1015024

### Q5
The newly planted shell calls back to the attacker over an uncommon but firewall-friendly port. Which listening port did the attacker use for the reverse shell?

![](/assets/images/Pasted image 20251108124008.png)

**A:** 4443

---
## Memory Dump Analysis

### Q6
Your memory snapshot captures the system’s kernel in situ, providing vital context for the breach. What is the kernel base address in the dump?

![](/assets/images/Pasted image 20251108161436.png)

Need to just run the windows.info plugin to get this information from the image

``` bash
vol.exe -f memdump.mem windows.info
```

**A:** 0xf80079213000

### Q7
A trusted service launches an unfamiliar executable residing outside the usual IIS stack, signalling a persistence implant. What is the final full on-disk path of that executable, and which MITRE ATT&CK persistence technique ID corresponds to this behaviour?

![](/assets/images/Pasted image 20251108162105.png)

To get the command line execution for processes you can use the windows.cmdline plugin

``` bash
vol.exe -f memdump.mem windows.cmdline
```

**A:** C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\updatenow.exe, T1574


### Q8
The reverse shell’s outbound traffic is handled by a built-in Windows process that also spawns the implanted executable. What is the name of this process, and what PID does it run under?

![](/assets/images/Pasted image 20251108163144.png)

This one can be seen in the process tree with the windows.pstree plugin

``` bash
vol.exe -f memdump.mem windows.pstree
```

**A:** w3wp.exe, 4332

--- 
## Malware Analysis

### Q9
Static inspection reveals the binary has been packed to hinder analysis. Which packer was used to obfuscate it?

![](/assets/images/Pasted image 20251108163427.png)

**A:** upx

### Q10
Threat-intel analysis shows the malware beaconing to its command-and-control host. Which fully qualified domain name (FQDN) does it contact?

SHA256: c25a6673a24d169de1bb399d226c12cdc666e0fa534149fc9fa7896ee61d406f

https://any.run/report/c25a6673a24d169de1bb399d226c12cdc666e0fa534149fc9fa7896ee61d406f/cb60e2bd-c643-4791-b1be-cefcbb68a5c0

**A:** icp8nl.hyperhost.ua

### Q11
Open-source intel associates that hash with a well-known commodity RAT. To which malware family does the sample belong?

**A:** Agent Tesla

---
<br>
I successfully completed Lockdown Blue Team Lab at @CyberDefenders!
https://cyberdefenders.org/blueteam-ctf-challenges/achievements/0xC/lockdown/