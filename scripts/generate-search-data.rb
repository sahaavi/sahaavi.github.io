#!/usr/bin/env ruby
require 'json'
require 'yaml'

# Initialize array to store all searchable content
search_data = []

# Process posts
Dir.glob('_site/blog/**/*.html').each do |file|
  content = File.read(file)
  
  # Extract title
  title_match = content.match(/<h1[^>]*>(.*?)<\/h1>/)
  title = title_match ? title_match[1] : File.basename(file, '.html')
  
  # Extract content (strip HTML tags)
  body_text = content.gsub(/<script.*?<\/script>/m, '')
                    .gsub(/<style.*?<\/style>/m, '')
                    .gsub(/<.*?>/m, ' ')
                    .gsub(/\s+/, ' ')
                    .strip
  
  # Create relative URL
  url = "/#{file.sub('_site/', '').sub('.html', '/')}"
  
  # Add to search data
  search_data << {
    id: search_data.length.to_s,
    title: title,
    content: body_text,
    url: url,
    type: 'post'
  }
end

# Process projects
Dir.glob('_site/projects/**/*.html').each do |file|
  content = File.read(file)
  
  title_match = content.match(/<h1[^>]*>(.*?)<\/h1>/)
  title = title_match ? title_match[1] : File.basename(file, '.html')
  
  body_text = content.gsub(/<script.*?<\/script>/m, '')
                    .gsub(/<style.*?<\/style>/m, '')
                    .gsub(/<.*?>/m, ' ')
                    .gsub(/\s+/, ' ')
                    .strip
  
  url = "/#{file.sub('_site/', '').sub('.html', '/')}"
  
  search_data << {
    id: search_data.length.to_s,
    title: title,
    content: body_text,
    url: url,
    type: 'project'
  }
end

# Process books
Dir.glob('_site/books/**/*.html').each do |file|
  content = File.read(file)
  
  title_match = content.match(/<h1[^>]*>(.*?)<\/h1>/)
  title = title_match ? title_match[1] : File.basename(file, '.html')
  
  body_text = content.gsub(/<script.*?<\/script>/m, '')
                    .gsub(/<style.*?<\/style>/m, '')
                    .gsub(/<.*?>/m, ' ')
                    .gsub(/\s+/, ' ')
                    .strip
  
  url = "/#{file.sub('_site/', '').sub('.html', '/')}"
  
  search_data << {
    id: search_data.length.to_s,
    title: title,
    content: body_text,
    url: url,
    type: 'book'
  }
end

# Save search data as JSON
File.open('_site/assets/js/search-data.json', 'w') do |f|
  f.write(JSON.pretty_generate(search_data))
end

puts "Generated search data with #{search_data.length} entries"