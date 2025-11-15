---
layout: post
title: "Sample Security Writeup: HTB Example Box"
date: 2025-11-15
tags: [htb, security, pentesting, linux]
---

## Overview

This is a sample security writeup demonstrating the markdown format for your blog posts. Simply create files in the `_posts/` directory following the naming convention: `YYYY-MM-DD-title.md`

## Reconnaissance

Initial port scan reveals several interesting services:

```bash
nmap -sC -sV -oA nmap/initial 10.10.11.123

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1
80/tcp   open  http    Apache httpd 2.4.41
443/tcp  open  ssl/http Apache httpd 2.4.41
```

## Enumeration

Browsing to the web server, we find a login portal. Directory enumeration reveals:

```bash
gobuster dir -u http://10.10.11.123 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

/admin                (Status: 302) [Size: 0]
/uploads              (Status: 301) [Size: 318]
/dashboard            (Status: 403) [Size: 279]
```

## Exploitation

Testing for SQL injection in the login form:

```sql
admin' OR '1'='1' --
```

This bypasses authentication and grants us access to the dashboard.

## Privilege Escalation

Checking for SUID binaries:

```bash
find / -perm -4000 2>/dev/null
```

We discover a vulnerable binary that allows us to escalate to root.

## Flags

**User Flag:** `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

**Root Flag:** `z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4`

## Lessons Learned

- Always validate user input
- Implement proper authentication mechanisms
- Regularly audit SUID binaries
- Keep systems patched and updated

---

*Stay curious. Stay in the shadows.* 💀
