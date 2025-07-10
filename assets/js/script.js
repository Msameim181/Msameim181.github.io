/**
 * Minimalist Personal Website JavaScript
 * Contains interactive elements for the website
 */

/**
 * Sets the theme on all relevant elements
 * @param {string} theme - The theme to apply ('dark' or 'light')
 */
function applyTheme(theme) {
  // Apply to both document element and body for maximum compatibility
  document.documentElement.setAttribute('data-theme', theme);
  document.body.setAttribute('data-theme', theme);
  
  // Update the toggle button if it exists
  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) themeToggle.setAttribute('data-theme', theme);
}

document.addEventListener('DOMContentLoaded', function() {
  // Dark Mode Toggle Functionality
  const themeToggle = document.querySelector('.theme-toggle');
  
  // Get the theme that was set in the head script
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  
  // Apply theme consistently to all elements
  applyTheme(currentTheme);
  
  // Theme Toggle Event Listener
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      // Apply theme using our utility function
      applyTheme(newTheme);
      
      // Save preference
      localStorage.setItem('theme', newTheme);
    });
  }
  // Handle fallback for Font Awesome icons if needed
  if (typeof FontAwesome === 'undefined') {
    document.querySelectorAll('.fa-arrow-up-right-from-square').forEach(icon => {
      icon.classList.remove('fa-arrow-up-right-from-square');
      icon.classList.add('fa-external-link');
    });
    
    document.querySelectorAll('.fa-turn-up').forEach(icon => {
      icon.classList.remove('fa-turn-up');
      icon.classList.add('fa-angle-up');
    });
  }
  
  // Add smooth scrolling for footnote references and back links
  document.querySelectorAll('.footnote-ref, .footnote-backref').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        // Highlight the target briefly
        const originalBackground = targetElement.style.backgroundColor;
        targetElement.style.backgroundColor = 'rgba(0, 102, 204, 0.1)';
        targetElement.style.transition = 'background-color 0.5s ease';
        
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        });
        
        setTimeout(() => {
          targetElement.style.backgroundColor = originalBackground;
        }, 1500);
      }
    });
  });
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Dynamic copyright year in footer
  const yearElement = document.getElementById('copyright-year');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
  
  // Blog post URL copy functionality
  const copyLinkBtn = document.querySelector('.blog-copy-link');
  if (copyLinkBtn) {
    copyLinkBtn.addEventListener('click', function() {
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        const originalText = this.textContent;
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.textContent = originalText;
        }, 2000);
      });
    });
  }
  
  // New blog URL copy functionality
  document.querySelectorAll('.copy-url').forEach(copyUrlElement => {
    copyUrlElement.addEventListener('click', function() {
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        const originalText = this.textContent;
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.innerHTML = '<i class="fa-regular fa-copy"></i> Copy URL';
        }, 2000);
      });
    });
  });
  
  // Code block copy functionality
  document.querySelectorAll('pre').forEach(pre => {
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-button';
    copyBtn.textContent = 'Copy';
    pre.appendChild(copyBtn);
    
    copyBtn.addEventListener('click', function() {
      const code = pre.querySelector('code').textContent;
      navigator.clipboard.writeText(code).then(() => {
        const originalText = this.textContent;
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.textContent = originalText;
        }, 2000);
      });
    });
  });
  
  // Copyable text elements
  document.querySelectorAll('.copyable').forEach(element => {
    element.addEventListener('click', function() {
      const textToCopy = this.getAttribute('data-copy') || this.textContent;
      navigator.clipboard.writeText(textToCopy).then(() => {
        const overlay = document.createElement('span');
        overlay.textContent = 'Copied!';
        overlay.style.position = 'absolute';
        overlay.style.backgroundColor = 'rgba(0, 102, 204, 0.8)';
        overlay.style.color = 'white';
        overlay.style.padding = '0.25rem 0.5rem';
        overlay.style.borderRadius = '3px';
        overlay.style.fontSize = '0.75rem';
        overlay.style.pointerEvents = 'none';
        overlay.style.zIndex = '100';
        overlay.style.opacity = '0';
        overlay.style.transition = 'opacity 0.3s ease';
        
        document.body.appendChild(overlay);
        
        // Position the overlay near the element
        const rect = this.getBoundingClientRect();
        overlay.style.top = `${window.scrollY + rect.top - 30}px`;
        overlay.style.left = `${window.scrollX + rect.left + rect.width/2 - 30}px`;
        
        // Show then hide
        setTimeout(() => overlay.style.opacity = '1', 10);
        setTimeout(() => {
          overlay.style.opacity = '0';
          setTimeout(() => document.body.removeChild(overlay), 300);
        }, 1500);
      });
    });
  });
  
  // Share icons next to links
  document.querySelectorAll('.share-icon').forEach(icon => {
    icon.addEventListener('click', function(e) {
      e.preventDefault();
      const url = this.parentNode.querySelector('a').href;
      
      if (navigator.share) {
        navigator.share({
          title: document.title,
          url: url
        });
      } else {
        navigator.clipboard.writeText(url).then(() => {
          const overlay = document.createElement('span');
          overlay.textContent = 'Link copied!';
          overlay.style.position = 'absolute';
          overlay.style.backgroundColor = 'rgba(0, 102, 204, 0.8)';
          overlay.style.color = 'white';
          overlay.style.padding = '0.25rem 0.5rem';
          overlay.style.borderRadius = '3px';
          overlay.style.fontSize = '0.75rem';
          overlay.style.pointerEvents = 'none';
          overlay.style.zIndex = '100';
          
          document.body.appendChild(overlay);
          
          // Position the overlay near the element
          const rect = this.getBoundingClientRect();
          overlay.style.top = `${window.scrollY + rect.top - 30}px`;
          overlay.style.left = `${window.scrollX + rect.left}px`;
          
          // Remove after a delay
          setTimeout(() => document.body.removeChild(overlay), 1500);
        });
      }
    });
  });
  
  // Calculate reading time
  const readingTimeElement = document.querySelector('.reading-time-value');
  if (readingTimeElement) {
    const content = document.querySelector('.blog-content');
    if (content) {
      const text = content.textContent;
      const wordCount = text.split(/\s+/).length;
      // Average reading speed: 200 words per minute
      const readingTime = Math.ceil(wordCount / 200);
      readingTimeElement.textContent = readingTime;
    }
  }
  
  // Updated reading time calculation for new blog layout
  const readingTimeSpan = document.querySelector('.reading-time');
  if (readingTimeSpan && !readingTimeElement) {
    const content = document.querySelector('.blog-content');
    if (content) {
      const text = content.textContent;
      const wordCount = text.split(/\s+/).length;
      // Average reading speed: 200 words per minute
      const readingTime = Math.ceil(wordCount / 200);
      readingTimeSpan.textContent = `${readingTime} min read`;
    }
  }
  
  // Copy button for copyable-text blocks
  document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', function() {
      const codeBlock = this.previousElementSibling;
      const code = codeBlock.textContent;
      
      navigator.clipboard.writeText(code).then(() => {
        const originalText = this.textContent;
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.textContent = originalText;
        }, 2000);
      });
    });
  });
});
