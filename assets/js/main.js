// Code block copy functionality
document.addEventListener('DOMContentLoaded', function() {
    // Streaming hacker code on sides
    function generateHackerStream() {
        const chars = '01';
        const hexChars = '0123456789ABCDEF';
        const symbols = ['0x', '>>', '<<', '&&', '||', '//', 'SYS', 'ERR', 'OK'];
        
        let stream = '';
        // Generate enough lines to fill the screen height
        const lines = Math.ceil(window.innerHeight / 12) + 20; // 12px line height + extra
        
        for (let i = 0; i < lines; i++) {
            for (let j = 0; j < 6; j++) { // 6 chars per line
                const rand = Math.random();
                if (rand < 0.4) {
                    stream += chars[Math.floor(Math.random() * chars.length)];
                } else if (rand < 0.7) {
                    stream += hexChars[Math.floor(Math.random() * hexChars.length)];
                } else {
                    const sym = symbols[Math.floor(Math.random() * symbols.length)];
                    stream += sym.substring(0, 2);
                }
            }
            stream += '\n';
        }
        return stream;
    }
    
    const leftCode = document.querySelector('.left-code');
    const rightCode = document.querySelector('.right-code');
    
    if (leftCode && rightCode) {
        leftCode.textContent = generateHackerStream();
        rightCode.textContent = generateHackerStream();
        
        // Update streams occasionally
        setInterval(() => {
            leftCode.textContent = generateHackerStream();
            rightCode.textContent = generateHackerStream();
        }, 1000);
        
        // Regenerate on window resize
        window.addEventListener('resize', () => {
            leftCode.textContent = generateHackerStream();
            rightCode.textContent = generateHackerStream();
        });
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

