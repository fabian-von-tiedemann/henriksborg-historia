#!/usr/bin/env python3
"""
Script to convert HTML figure tags to Markdown images in all markdown files.
Converts:
<figure>
  <img src="..." alt="" />
  <figcaption>...</figcaption>
</figure>

To:
![alt text](image_path)

*description*
"""

import os
import re
import glob

def convert_figure_to_markdown(content):
    """Convert HTML figure tags to Markdown images."""
    
    # First, handle figures with figcaption that have escaped asterisks
    pattern1 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*<figcaption>\\\*([^*]+)\\\*</figcaption>\s*</figure>'
    
    def replacement1(match):
        src = match.group(1)
        alt = match.group(2)
        caption = match.group(3)
        
        # If alt is empty, use caption as alt text
        if not alt.strip():
            alt = caption
        
        # Create markdown image with alt text
        markdown_image = f'![{alt}]({src})'
        
        # Add caption below in italics
        markdown_caption = f'\n\n*{caption}*'
        
        return markdown_image + markdown_caption
    
    # Apply the first conversion
    converted_content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE | re.DOTALL)
    
    # Handle figures with regular figcaption (no escaped asterisks)
    pattern2 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*<figcaption>\*([^*]+)\*</figcaption>\s*</figure>'
    
    def replacement2(match):
        src = match.group(1)
        alt = match.group(2)
        caption = match.group(3)
        
        # If alt is empty, use caption as alt text
        if not alt.strip():
            alt = caption
        
        # Create markdown image with alt text
        markdown_image = f'![{alt}]({src})'
        
        # Add caption below in italics
        markdown_caption = f'\n\n*{caption}*'
        
        return markdown_image + markdown_caption
    
    converted_content = re.sub(pattern2, replacement2, converted_content, flags=re.MULTILINE | re.DOTALL)
    
    # Handle figures without figcaption (just img tags)
    pattern3 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*</figure>'
    
    def replacement3(match):
        src = match.group(1)
        alt = match.group(2)
        
        # If alt is empty, use a generic description
        if not alt.strip():
            alt = "Bild från Henriksborgs historia"
        
        return f'![{alt}]({src})'
    
    converted_content = re.sub(pattern3, replacement3, converted_content, flags=re.MULTILINE | re.DOTALL)
    
    return converted_content

def process_file(file_path):
    """Process a single markdown file."""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert the content
        converted_content = convert_figure_to_markdown(content)
        
        # Check if content changed
        if content != converted_content:
            # Create backup
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Created backup: {backup_path}")
            
            # Write converted content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            print(f"  Converted successfully")
        else:
            print(f"  No changes needed")
            
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")

def main():
    """Main function to process all markdown files."""
    # Find all markdown files in src/pages
    markdown_files = glob.glob('src/pages/*.md')
    
    if not markdown_files:
        print("No markdown files found in src/pages/")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process:")
    print()
    
    for file_path in markdown_files:
        process_file(file_path)
        print()
    
    print("Conversion complete!")

if __name__ == "__main__":
    main() 