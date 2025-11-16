#!/usr/bin/env python3
"""
Obsidian to Jekyll Blog Publisher
Converts Obsidian markdown notes to Jekyll posts with proper formatting.

Usage:
    python publish_post.py -f "path/to/note.md" [options]

Options:
    -f, --file PATH       Path to the Obsidian markdown file
    -d, --date DATE       Publication date (YYYY-MM-DD, defaults to today)
    -t, --tags TAGS       Comma-separated tags (e.g., "htb,writeup,linux")
    --author AUTHOR       Author name (defaults to config)
    --dry-run            Show what would be done without making changes
    -v, --verbose        Verbose output
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
import yaml

# Configuration
DEFAULT_AUTHOR = "calorushex"
REQUIRED_TAGS = True  # Set to False to allow posts without tags
ASSETS_DIR = "assets/images"
POSTS_DIR = "_posts"

class ObsidianPublisher:
    def __init__(self, blog_root, verbose=False):
        self.blog_root = Path(blog_root)
        self.verbose = verbose
        self.assets_dir = self.blog_root / ASSETS_DIR
        self.posts_dir = self.blog_root / POSTS_DIR
        
        # Ensure directories exist
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.posts_dir.mkdir(parents=True, exist_ok=True)
    
    def log(self, message, force=False):
        """Print message if verbose or forced"""
        if self.verbose or force:
            print(message)
    
    def extract_title_from_content(self, content):
        """Extract title from first H1 heading or filename"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None
    
    def has_frontmatter(self, content):
        """Check if content already has Jekyll frontmatter"""
        return content.strip().startswith('---')
    
    def extract_frontmatter(self, content):
        """Extract existing frontmatter and content"""
        if not self.has_frontmatter(content):
            return None, content
        
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                content = parts[2].strip()
                return frontmatter, content
            except yaml.YAMLError:
                return None, content
        return None, content
    
    def create_frontmatter(self, title, date, tags, author):
        """Create Jekyll frontmatter"""
        fm = {
            'layout': 'post',
            'title': title,
            'date': date.strftime('%Y-%m-%d'),
            'author': author
        }
        if tags:
            fm['tags'] = tags
        
        return f"---\n{yaml.dump(fm, default_flow_style=False)}---\n\n"
    
    def convert_obsidian_images(self, content, source_file, dry_run=False):
        """Convert Obsidian image syntax and copy images"""
        source_dir = Path(source_file).parent
        copied_images = []
        
        # Pattern: ![[image.png]] or ![[path/to/image.png]]
        def replace_image(match):
            image_path = match.group(1)
            image_name = Path(image_path).name
            
            # Find the image in common Obsidian locations
            possible_paths = [
                source_dir / image_path,
                source_dir / '..' / '..' / 'Image Store' / image_name,  # Brain/Image Store
                source_dir / '..' / '..' / 'Images' / image_name,       # Brain/Images
                source_dir / '..' / '..' / 'image' / image_name,        # Brain/image
                source_dir / '..' / '..' / 'attachments' / image_name,  # Brain/attachments
                source_dir / '..' / 'attachments' / image_name,
                source_dir / 'attachments' / image_name,
                source_dir / image_name,
            ]
            
            source_image = None
            for path in possible_paths:
                self.log(f"  Checking: {path}")
                if path.exists():
                    source_image = path
                    self.log(f"  ✓ Found: {path}")
                    break
            
            if not source_image:
                self.log(f"⚠️  Warning: Image not found: {image_path}", force=True)
                return f"![Image not found: {image_name}]()"
            
            # Copy image to assets
            dest_image = self.assets_dir / image_name
            if not dry_run:
                shutil.copy2(source_image, dest_image)
                copied_images.append(image_name)
                self.log(f"📎 Copied image: {image_name}")
            else:
                self.log(f"📎 Would copy: {source_image} -> {dest_image}")
            
            # Return Jekyll image syntax
            return f"![](/assets/images/{image_name})"
        
        # Replace Obsidian image syntax
        content = re.sub(r'!\[\[([^\]]+)\]\]', replace_image, content)
        
        return content, copied_images
    
    def convert_wiki_links(self, content):
        """Convert Obsidian wiki-links to Jekyll links (basic conversion)"""
        # This is a simple conversion - wiki links won't work perfectly in Jekyll
        # unless you have the exact post. For now, we'll convert to plain text with a note.
        def replace_link(match):
            link_text = match.group(1)
            # You could enhance this to search for matching posts
            return f"[{link_text}](#)"  # Placeholder link
        
        content = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)
        return content
    
    def validate_tags(self, tags):
        """Validate that tags are provided"""
        if REQUIRED_TAGS and not tags:
            raise ValueError(
                "Tags are required but not found in the file's frontmatter.\n"
                "Please add tags to your Obsidian file's frontmatter like this:\n"
                "---\n"
                "tags:\n"
                "  - tag1\n"
                "  - tag2\n"
                "---\n"
                "Or provide tags via command line: -t 'tag1,tag2'"
            )
        return True
    
    def publish(self, source_file, date=None, tags=None, author=None, dry_run=False):
        """Main publishing function"""
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")
        
        self.log(f"📄 Processing: {source_path.name}", force=True)
        
        # Read content
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract or use provided metadata
        existing_fm, content = self.extract_frontmatter(content)
        
        # Extract date: prioritize frontmatter, then CLI arg, then today
        if existing_fm and 'date' in existing_fm:
            date_value = existing_fm['date']
            if isinstance(date_value, str):
                try:
                    date = datetime.strptime(date_value, '%Y-%m-%d')
                except ValueError:
                    # Try other common date formats
                    try:
                        date = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                    except:
                        self.log(f"⚠️  Warning: Could not parse date from frontmatter: {date_value}", force=True)
                        if not date:
                            date = datetime.now()
            elif hasattr(date_value, 'year'):  # It's already a date/datetime object
                date = date_value
        
        if not date:
            date = datetime.now()
        
        # Extract author: prioritize frontmatter, then CLI arg, then default
        if not author:
            author = existing_fm.get('author') if existing_fm else DEFAULT_AUTHOR
        
        # Extract title: prioritize frontmatter, then H1, then filename
        title = None
        if existing_fm and 'title' in existing_fm:
            title = existing_fm['title']
        else:
            title = self.extract_title_from_content(content)
        
        if not title:
            title = source_path.stem.replace('-', ' ').title()
        
        # Extract tags: prioritize frontmatter, then CLI arg
        if existing_fm and 'tags' in existing_fm:
            fm_tags = existing_fm['tags']
            # Handle both list format and string format
            if isinstance(fm_tags, list):
                tags = fm_tags
            elif isinstance(fm_tags, str):
                tags = [t.strip() for t in fm_tags.split(',')]
            self.log(f"📋 Found tags in frontmatter: {', '.join(tags)}", force=True)
        elif tags:
            # CLI tags override if no frontmatter tags
            tags = [t.strip() for t in tags.split(',')]
        else:
            tags = None
        
        # Validate tags
        self.validate_tags(tags)
        
        # Convert Obsidian syntax
        content, images = self.convert_obsidian_images(content, source_path, dry_run)
        content = self.convert_wiki_links(content)
        
        # Create frontmatter
        frontmatter = self.create_frontmatter(title, date, tags, author)
        full_content = frontmatter + content
        
        # Generate output filename
        date_str = date.strftime('%Y-%m-%d')
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        output_filename = f"{date_str}-{slug}.md"
        output_path = self.posts_dir / output_filename
        
        # Write output
        if not dry_run:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            self.log(f"✅ Published to: {output_path}", force=True)
            if images:
                self.log(f"📸 Copied {len(images)} image(s)", force=True)
        else:
            self.log(f"\n{'='*60}", force=True)
            self.log(f"DRY RUN - Would create: {output_path}", force=True)
            self.log(f"{'='*60}", force=True)
            self.log(full_content, force=True)
            self.log(f"{'='*60}\n", force=True)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Publish Obsidian notes to Jekyll blog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Publish using frontmatter from the Obsidian file
  python publish_post.py -f "C:\\Users\\CJ\\Documents\\Brain\\HTB\\Freelancer.md"
  
  # Override date and tags from command line
  python publish_post.py -f note.md -d 2025-11-15 -t "htb,writeup,windows"
  
  # Preview without making changes
  python publish_post.py -f note.md --dry-run
        """
    )
    
    parser.add_argument('-f', '--file', required=True,
                       help='Path to Obsidian markdown file')
    parser.add_argument('-d', '--date',
                       help='Publication date (YYYY-MM-DD). If not provided, uses date from frontmatter or today.')
    parser.add_argument('-t', '--tags',
                       help='Comma-separated tags (e.g., "htb,writeup,linux"). If not provided, extracts from frontmatter.')
    parser.add_argument('--author', default=DEFAULT_AUTHOR,
                       help=f'Author name (default: {DEFAULT_AUTHOR})')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Parse date if provided
    date = None
    if args.date:
        try:
            date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Error: Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)
    
    # Get blog root (script is in scripts/ folder)
    blog_root = Path(__file__).parent.parent
    
    # Create publisher and publish
    try:
        publisher = ObsidianPublisher(blog_root, verbose=args.verbose)
        output = publisher.publish(
            source_file=args.file,
            date=date,
            tags=args.tags,
            author=args.author,
            dry_run=args.dry_run
        )
        
        if not args.dry_run:
            print(f"\n✨ Success! Post ready at: {output}")
            print(f"📝 Next steps:")
            print(f"   git add .")
            print(f"   git commit -m 'New post: {output.stem}'")
            print(f"   git push")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
