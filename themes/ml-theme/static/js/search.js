// ML Portfolio Search Implementation
class MLSearch {
    constructor() {
        this.index = null;
        this.documents = [];
        this.searchInput = document.getElementById('search-input');
        this.suggestions = document.getElementById('search-suggestions');
        this.resultsContainer = document.getElementById('search-results');
        
        this.init();
    }
    
    async init() {
        try {
            const response = await fetch('/search-index.json');
            const data = await response.json();
            this.documents = data.documents;
            
            // Build Lunr index
            this.index = lunr(function () {
                this.ref('id');
                this.field('title', { boost: 10 });
                this.field('content', { boost: 5 });
                this.field('tags', { boost: 8 });
                this.field('category', { boost: 6 });
                
                data.documents.forEach(doc => this.add(doc));
            });
            
            this.setupEventListeners();
        } catch (error) {
            console.error('Failed to load search index:', error);
        }
    }
    
    setupEventListeners() {
        let debounceTimer;
        
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                this.handleSearch(e.target.value);
            }, 300);
        });
        
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performFullSearch(e.target.value);
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    handleSearch(query) {
        if (!query || query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        const results = this.searchDocuments(query);
        this.showSuggestions(results.slice(0, 5));
    }
    
    searchDocuments(query) {
        if (!this.index) return [];
        
        try {
            // Fuzzy search with wildcard
            const searchQuery = query.split(' ').map(term => `${term}*`).join(' ');
            const results = this.index.search(searchQuery);
            
            return results.map(result => {
                const doc = this.documents.find(d => d.id === result.ref);
                return { ...doc, score: result.score };
            });
        } catch (error) {
            console.error('Search error:', error);
            return [];
        }
    }
    
    showSuggestions(results) {
        if (results.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        const html = results.map(result => `
            <li class="search-suggestion" data-url="${result.url}">
                <div class="suggestion-title">${result.title}</div>
                <div class="suggestion-meta">${result.category} • ${result.date}</div>
            </li>
        `).join('');
        
        this.suggestions.innerHTML = html;
        this.suggestions.style.display = 'block';
        
        // Add click handlers
        this.suggestions.querySelectorAll('.search-suggestion').forEach(item => {
            item.addEventListener('click', () => {
                window.location.href = item.dataset.url;
            });
        });
    }
    
    hideSuggestions() {
        this.suggestions.style.display = 'none';
    }
    
    performFullSearch(query) {
        const results = this.searchDocuments(query);
        this.displaySearchResults(query, results);
    }
    
    displaySearchResults(query, results) {
        if (!this.resultsContainer) return;
        
        const html = `
            <h2>Search Results for "${query}"</h2>
            <p>${results.length} result(s) found</p>
            <div class="search-results-list">
                ${results.map(result => `
                    <article class="search-result">
                        <h3><a href="${result.url}">${result.title}</a></h3>
                        <p class="result-meta">${result.category} • ${result.date}</p>
                        <p class="result-excerpt">${result.summary || result.content.substring(0, 200)}...</p>
                        <div class="result-tags">
                            ${result.tags.split(',').map(tag => `<span class="tag">${tag.trim()}</span>`).join('')}
                        </div>
                    </article>
                `).join('')}
            </div>
        `;
        
        this.resultsContainer.innerHTML = html;
    }
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MLSearch();
});