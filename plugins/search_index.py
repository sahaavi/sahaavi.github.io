import json
import os
from pelican import signals
from pelican.generators import Generator

class SearchIndexGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def generate_context(self):
        pass
        
    def generate_output(self, writer):
        documents = []
        
        # Index articles
        for article in self.context['articles']:
            doc = {
                'id': article.url,
                'url': article.url,
                'title': article.title,
                'content': article.content,
                'summary': getattr(article, 'summary', ''),
                'category': article.category.name if article.category else '',
                'tags': ', '.join([tag.name for tag in article.tags]) if article.tags else '',
                'date': article.date.strftime('%Y-%m-%d') if article.date else '',
                'author': str(article.author) if article.author else ''
            }
            documents.append(doc)
            
        # Index pages
        for page in self.context['pages']:
            doc = {
                'id': page.url,
                'url': page.url,
                'title': page.title,
                'content': page.content,
                'summary': getattr(page, 'summary', ''),
                'category': 'Page',
                'tags': '',
                'date': '',
                'author': str(page.author) if page.author else ''
            }
            documents.append(doc)
            
        # Write search index
        search_data = {'documents': documents}
        output_path = os.path.join(self.output_path, 'search-index.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(search_data, f, ensure_ascii=False, indent=2)

def get_generators(generators):
    return SearchIndexGenerator

def register():
    signals.get_generators.connect(get_generators)