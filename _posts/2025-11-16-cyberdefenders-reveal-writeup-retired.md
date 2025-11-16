---
author: calorushex
date: '2025-11-16'
layout: post
tags:
- cyberdefenders
- memoryforensics
- writeup
title: CyberDefenders - Reveal Writeup - Retired
excerpt: "You are a forensic investigator at a financial institution, and your SIEM flagged unusual activity on a workstation with access to sensitive financial data. Suspecting a breach, you received a memory dump from the compromised machine. Your task is to analyze the memory for signs of compromise, trace the anomaly's origin, and assess its scope to contain the incident effectively."
---

## Scenario

You are a forensic investigator at a financial institution, and your SIEM flagged unusual activity on a workstation with access to sensitive financial data. Suspecting a breach, you received a memory dump from the compromised machine. Your task is to analyze the memory for signs of compromise, trace the anomaly's origin, and assess its scope to contain the incident effectively.

![](/assets/images/Pasted image 20251109221339.png)

---

## Questions

Using the windows.pstree plugin for volatility3 the malicious process stuck out like a sore thumb using powershell and net use to grab the next stage payload.

``` bash
vol.exe -f 192-reveal.dmp windows.pstree
```

### Q1

Identifying the name of the malicious process helps in understanding the nature of the attack. What is the name of the malicious process?

### A

**powershell.exe**

### Q2

Knowing the parent process ID (PPID) of the malicious process aids in tracing the process hierarchy and understanding the attack flow. What is the parent PID of the malicious process?

### A

**4120**

### Q3

Determining the file name used by the malware for executing the second-stage payload is crucial for identifying subsequent malicious activities. What is the file name that the malware uses to execute the second-stage payload?

### A

**3435.dll**

### Q4

Identifying the shared directory on the remote server helps trace the resources targeted by the attacker. What is the name of the shared directory being accessed on the remote server?

**davwwwroot**

### Q5

What is the MITRE ATT&CK sub-technique ID that describes the execution of a second-stage payload using a Windows utility to run the malicious file?

T1218.011 - Signed Binary Proxy Execution: Rundll32
This is the most specific and accurate technique for what's happening. The attacker is:

Using rundll32.exe
Loading a DLL from a remote WebDAV share (\\45.9.74.32@8888\davwwwroot\3435.dll)
Executing the entry export function from that DLL

### A

**T1218.011**

### Q6

Identifying the username under which the malicious process runs helps in assessing the compromised account and its potential impact. What is the username that the malicious process runs under?

![](/assets/images/Pasted image 20251109223200.png)

The user can be acquired using the windows.getsids plugin along with the process id of the malicious process.

``` bash
vol.exe -f 192-Reveal.dmp windows.getsids --pid 3692
```

### A

**Elon**

### Q7

Knowing the name of the malware family is essential for correlating the attack with known threats and developing appropriate defenses. What is the name of the malware family?

To get this you might either try dump the process and get the dump hash or try using the filescan plugin but filescan didn't seem to work in this instance and the hash of the process running in memory won't be the same as the hash of the file on disk or on the file share.

Instead the easy solution was just to search for the file name. It's unique enough that google search could pop up some malware analysis reports.

I found one on Any.run using this method which said it was [StrelaStealer](https://any.run/report/e19b6144d7da72a97f5468fade0ed971a798359ed2f1dcb1e5e28f2d6b540175/28ba4903-16e2-44b1-bcdc-2eb686ad3dcf).

### A

**StrelaStealer**

<br>

---
<br>

I successfully completed Reveal Blue Team Lab at @CyberDefenders!

<https://cyberdefenders.org/blueteam-ctf-challenges/achievements/0xC/reveal/>