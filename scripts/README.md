# Publishing Script

This script converts Obsidian markdown notes to Jekyll blog posts.

## Setup

1. Install Python dependencies:
```bash
pip install pyyaml
```

2. Copy `publish_post.py` to your local scripts folder (this file is gitignored)

## Usage

Basic usage:
```bash
python publish_post.py -f "C:\Users\CJ\Documents\Brain\CyberDefenders\Labs\192-Reveal.md"
```

With tags:
```bash
python publish_post.py -f "path/to/note.md" -t "htb,writeup,linux"
```

Specify publish date:
```bash
python publish_post.py -f "path/to/note.md" -d 2025-11-15
```

Dry run (preview without making changes):
```bash
python publish_post.py -f "path/to/note.md" --dry-run
```

Verbose output:
```bash
python publish_post.py -f "path/to/note.md" -v
```

## What It Does

1. ✅ Converts `![[image.png]]` to `![](/assets/images/image.png)`
2. ✅ Copies all referenced images to `assets/images/`
3. ✅ Converts `[[Wiki Links]]` to markdown links
4. ✅ Adds Jekyll frontmatter with title, date, tags, author
5. ✅ Validates required tags exist
6. ✅ Creates properly named file: `YYYY-MM-DD-title.md` in `_posts/`

## Options

- `-f, --file`: Path to Obsidian markdown file (required)
- `-t, --tags`: Comma-separated tags (required unless file has frontmatter)
- `-d, --date`: Publication date (YYYY-MM-DD, defaults to today)
- `--author`: Author name (defaults to calorushex)
- `--dry-run`: Preview without making changes
- `-v, --verbose`: Show detailed output

## After Publishing

```bash
git add .
git commit -m "New post: Title"
git push
```

The post will appear on your GitHub Pages site within 1-3 minutes.
