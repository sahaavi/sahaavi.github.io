document.addEventListener('DOMContentLoaded', function() {
    // Initialize neural network background animation
    initNeuralNetBg();
    
    // Initialize MathJax for LaTeX rendering
    if (typeof MathJax !== 'undefined') {
      MathJax.typesetPromise();
    }
    
    // Initialize syntax highlighting
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightBlock(block);
    });
  });
  
  // Neural network background animation
  function initNeuralNetBg() {
    const neuralBg = document.querySelector('.neural-net-bg');
    if (!neuralBg) return;
    
    // Animation will be handled mostly by CSS, but we can add nodes dynamically
    const numNodes = Math.floor(window.innerWidth / 30) * Math.floor(window.innerHeight / 30);
    for (let i = 0; i < numNodes; i++) {
      const node = document.createElement('div');
      node.className = 'neural-node';
      node.style.left = `${Math.random() * 100}%`;
      node.style.top = `${Math.random() * 100}%`;
      neuralBg.appendChild(node);
    }
  }
  
  // GitHub code fetching
  async function fetchGithubCode(repo, path, elementId) {
    try {
      const response = await fetch(`https://api.github.com/repos/${repo}/contents/${path}`);
      if (!response.ok) {
        throw new Error('Failed to fetch from GitHub API');
      }
      
      const data = await response.json();
      let content;
      
      if (data.encoding === 'base64') {
        content = atob(data.content);
      } else {
        content = data.content;
      }
      
      // Get language from file extension
      const fileExtension = path.split('.').pop();
      let language = '';
      
      switch(fileExtension) {
        case 'py': language = 'python'; break;
        case 'js': language = 'javascript'; break;
        case 'html': language = 'html'; break;
        case 'css': language = 'css'; break;
        case 'md': language = 'markdown'; break;
        case 'json': language = 'json'; break;
        default: language = '';
      }
      
      // Create code element
      const codeElement = document.getElementById(elementId);
      codeElement.innerHTML = `<pre><code class="language-${language}">${escapeHtml(content)}</code></pre>`;
      
      // Initialize syntax highlighting
      hljs.highlightElement(codeElement.querySelector('code'));
      
    } catch (error) {
      console.error('Error fetching GitHub code:', error);
      document.getElementById(elementId).innerHTML = `<div class="error-message">Error loading code from GitHub: ${error.message}</div>`;
    }
  }
  
  // Helper function to escape HTML
  function escapeHtml(unsafe) {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
  
  // For PDF.js integration
  function loadPDFViewer(pdfUrl, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Create iframe to PDF.js viewer
    const iframe = document.createElement('iframe');
    iframe.src = `/assets/js/pdfjs/web/viewer.html?file=${encodeURIComponent(pdfUrl)}`;
    iframe.width = '100%';
    iframe.height = '800px';
    iframe.frameBorder = '0';
    
    container.appendChild(iframe);
  }
  
//   // For Notion integration
//   async function loadNotionPage(pageId, containerId) {
//     const container = document.getElementById(containerId);
//     if (!container) return;
    
//     try {
//       // Use Notion's public API (requires a public page)
//       const response = await fetch(`/api/notion-proxy?pageId=${pageId}`);
//       if (!response.ok) {
//         throw new Error('Failed to fetch Notion page');
//       }
//     }
// }