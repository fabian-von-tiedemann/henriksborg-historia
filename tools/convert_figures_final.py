#!/usr/bin/env python3
"""
Final comprehensive script to convert ALL remaining HTML figure tags to Markdown images.
This script handles all possible formats and variations.
"""

import os
import re
import glob

def convert_all_figures(content):
    """Convert ALL HTML figure tags to Markdown images."""
    
    # Pattern 1: Standard figure with figcaption and escaped asterisks
    pattern1 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*<figcaption>\\\*([^*]+)\\\*</figcaption>\s*</figure>'
    
    def replacement1(match):
        src = match.group(1)
        alt = match.group(2)
        caption = match.group(3)
        
        if not alt.strip():
            alt = caption
        
        return f'![{alt}]({src})\n\n*{caption}*'
    
    # Pattern 2: Standard figure with figcaption and regular asterisks
    pattern2 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*<figcaption>\*([^*]+)\*</figcaption>\s*</figure>'
    
    def replacement2(match):
        src = match.group(1)
        alt = match.group(2)
        caption = match.group(3)
        
        if not alt.strip():
            alt = caption
        
        return f'![{alt}]({src})\n\n*{caption}*'
    
    # Pattern 3: Figure with just img tag (no figcaption)
    pattern3 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*</figure>'
    
    def replacement3(match):
        src = match.group(1)
        alt = match.group(2)
        
        if not alt.strip():
            alt = "Bild från Henriksborgs historia"
        
        return f'![{alt}]({src})'
    
    # Pattern 4: Figure with img and any figcaption format
    pattern4 = r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/>\s*<figcaption>([^<]+)</figcaption>\s*</figure>'
    
    def replacement4(match):
        src = match.group(1)
        alt = match.group(2)
        caption = match.group(3).strip()
        
        # Clean up caption (remove any asterisks or backslashes)
        caption = re.sub(r'[\\\*]', '', caption)
        
        if not alt.strip():
            alt = caption
        
        return f'![{alt}]({src})\n\n*{caption}*'
    
    # Apply all patterns in sequence
    content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(pattern3, replacement3, content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(pattern4, replacement4, content, flags=re.MULTILINE | re.DOTALL)
    
    return content

def process_file(file_path):
    """Process a single markdown file."""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert the content
        converted_content = convert_all_figures(content)
        
        # Check if content changed
        if content != converted_content:
            # Create backup
            backup_path = file_path + '.backup2'
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
    
    print("Final conversion complete!")

if __name__ == "__main__":
    main() 