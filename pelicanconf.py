#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Your Name'
SITENAME = 'ML Engineer\'s Lab'
SITEURL = ''
SITESUBTITLE = 'From Models to Production'

PATH = 'content'
TIMEZONE = 'UTC'
DEFAULT_LANG = 'en'

# Feed generation
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('GitHub', 'https://github.com/yourusername'),
    ('LinkedIn', 'https://linkedin.com/in/yourprofile'),
    ('Papers', '#papers'),
)

# Social widget
SOCIAL = (
    ('Twitter', 'https://twitter.com/yourusername'),
    ('GitHub', 'https://github.com/yourusername'),
)

DEFAULT_PAGINATION = 10

# Theme and plugins
THEME = 'themes/ml-theme'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['search', 'render_math']

# Math rendering
MATH_JAX = {
    'tex_extensions': ['color.js','mhchem.js'],
    'responsive': True,
}

# Search configuration
SEARCH_MODE = "output"
SEARCH_HTML_SELECTOR = "main"

# Static paths
STATIC_PATHS = ['images', 'pdfs', 'extra']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

# Article settings
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# Categories and tags
CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'