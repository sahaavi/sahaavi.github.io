#!/bin/bash

# Build the Jekyll site
bundle exec jekyll build

# Generate the search data
ruby scripts/generate-search-data.rb

# Copy the search data to the correct location
cp _site/assets/js/search-data.json assets/js/search-data.json

echo "Build completed successfully!"