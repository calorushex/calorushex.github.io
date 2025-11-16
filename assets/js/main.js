// Code block copy functionality
document.addEventListener('DOMContentLoaded', function() {
    // Floating hacker text across background
    function createFloatingText() {
        const commands = [
            'nmap -sV 10.10.11.123',
            'gobuster dir -u http://target.htb',
            './exploit.sh',
            'nc -lvnp 4444',
            'sudo -l',
            'cat /etc/passwd',
            'find / -perm -4000 2>/dev/null',
            'python3 -m http.server',
            'ssh user@target.htb',
            'curl http://10.10.11.123',
            'grep -r "password"',
            'chmod +x shell.sh',
            './linpeas.sh',
            'whoami && id',
            'ps aux | grep root',
            'netstat -tulpn',
            'hydra -l admin -P pass.txt',
            'sqlmap -u "http://target"',
            'msfconsole',
            'john --wordlist=rockyou.txt',
            '>> ACCESS GRANTED',
            '>> SYSTEM BREACH',
            '>> EXPLOIT LOADED',
            '>> ROOT SHELL',
            '[+] VULNERABILITY FOUND',
            '[*] SCANNING PORTS...',
            '[!] FIREWALL DETECTED'
        ];
        
        const span = document.createElement('span');
        span.className = 'floating-hacker-text';
        span.textContent = commands[Math.floor(Math.random() * commands.length)];
        
        // Random vertical position
        const top = Math.random() * 100;
        span.style.top = top + '%';
        
        // Constant slow speed (60 seconds)
        const duration = 60;
        span.style.animationDuration = duration + 's';
        
        // Random delay
        const delay = Math.random() * 5;
        span.style.animationDelay = delay + 's';
        
        document.body.appendChild(span);
        
        // Remove after animation completes
        setTimeout(() => {
            span.remove();
        }, (duration + delay) * 1000);
    }
    
    // Create floating text periodically (every 8 seconds)
    setInterval(createFloatingText, 100000);
    
    // Create initial batch
    for (let i = 0; i < 2; i++) {
        setTimeout(createFloatingText, i * 2000);
    }
    
    // Add copy buttons to all code blocks
    const codeBlocks = document.querySelectorAll('div.highlight');
    
    // If no highlight divs (plain markdown code blocks), fall back to pre elements
    const blocks = codeBlocks.length > 0 ? codeBlocks : document.querySelectorAll('pre');
    
    blocks.forEach(function(block) {
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.setAttribute('aria-label', 'Copy code to clipboard');
        
        // Wrap the code block
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(copyButton);
        wrapper.appendChild(block);
        
        // Add click event
        copyButton.addEventListener('click', function() {
            const code = block.querySelector('code') || block.querySelector('pre') || block;
            const text = code.textContent;
            
            navigator.clipboard.writeText(text).then(function() {
                copyButton.textContent = 'Copied!';
                copyButton.classList.add('copied');
                
                setTimeout(function() {
                    copyButton.textContent = 'Copy';
                    copyButton.classList.remove('copied');
                }, 2000);
            }).catch(function(err) {
                console.error('Failed to copy:', err);
            });
        });
    });
});

