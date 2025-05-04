document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    // Initialize search index when the page loads
    let searchIndex;
    let searchData;
    
    // Fetch the search data
    fetch('/assets/js/search-data.json')
      .then(response => response.json())
      .then(data => {
        searchData = data;
        
        // Create the lunr index
        searchIndex = lunr(function() {
          this.field('title', { boost: 10 });
          this.field('content');
          this.field('tags', { boost: 5 });
          this.ref('id');
          
          // Add documents to the index
          data.forEach(item => {
            this.add({
              id: item.id,
              title: item.title,
              content: item.content,
              tags: item.tags
            });
          });
        });
      });
    
    // Search input event listener
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      
      if (query.length < 2) {
        searchResults.classList.remove('active');
        searchResults.innerHTML = '';
        return;
      }
      
      // Perform the search
      const results = searchIndex.search(query);
      
      // Display results
      if (results.length > 0) {
        searchResults.innerHTML = '';
        searchResults.classList.add('active');
        
        results.slice(0, 5).forEach(result => {
          const item = searchData.find(item => item.id === result.ref);
          const resultItem = document.createElement('div');
          resultItem.className = 'search-result-item';
          resultItem.innerHTML = `
            <h3>${item.title}</h3>
            <p>${item.content.substring(0, 100)}...</p>
          `;
          resultItem.addEventListener('click', function() {
            window.location.href = item.url;
          });
          searchResults.appendChild(resultItem);
        });
      } else {
        searchResults.innerHTML = '<div class="search-result-item">No results found</div>';
        searchResults.classList.add('active');
      }
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', function(event) {
      if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
        searchResults.classList.remove('active');
      }
    });
    
    // Search form submit event
    document.addEventListener('submit', function(event) {
      if (event.target.contains(searchInput)) {
        event.preventDefault();
        const firstResult = searchResults.querySelector('.search-result-item');
        if (firstResult) {
          firstResult.click();
        }
      }
    });
  });