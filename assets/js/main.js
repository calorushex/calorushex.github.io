// Code block copy functionality
document.addEventListener('DOMContentLoaded', function() {
    // Target only the outermost code containers
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

