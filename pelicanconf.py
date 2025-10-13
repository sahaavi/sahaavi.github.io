#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Avishek Saha'
SITENAME = "Avishek's Lab"
SITEURL = 'https://sahaavi.github.io/'
SITESUBTITLE = 'ML Engineer & Data Scientist'

PATH = 'content'
TIMEZONE = 'America/Vancouver'
DEFAULT_LANG = 'en'

# Feed generation
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('GitHub', 'https://github.com/sahaavi'),
    ('LinkedIn', 'https://linkedin.com/in/sahaavi'),
    # ('Papers', '#papers'),
)

# Social widget
SOCIAL = (
    ('Twitter', 'https://x.com/avi_in_tech'),
    ('GitHub', 'https://github.com/sahaavi'),
)

DEFAULT_PAGINATION = 10

# Theme and plugins
THEME = 'themes/ml-theme'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['plugins.search_index', 'pelican.plugins.render_math']

# Math rendering
MATH_JAX = {
    'tex_extensions': ['color.js','mhchem.js'],
    'responsive': True,
}

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
