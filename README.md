# CALORUSHEX - Gothic Security Blog

A dark, gothic-themed security blog built with Jekyll and hosted on GitHub Pages.

## About

Hi, my name is CJ. I work as a security consultant in financial services. I enjoy playing CTFs and writing up challenges. I also enjoy learning new things and sharing my knowledge with others. I've was lucky to be granted the Community Hero role in Blue Team Labs Online and previously reached rank 1 in the world. With my CTF Team BlueWithNoClue we also finished 47th in the 2023 Huntress CTF.

## Theme

Custom-built gothic/matrix aesthetic featuring:
- Dark backgrounds with matrix green accents
- Monospace fonts for that terminal feel
- Skull imagery and cyberpunk vibes
- Syntax highlighting optimized for security writeups

## Writing Posts

Create new posts in the `_posts/` directory following this naming convention:

```
_posts/YYYY-MM-DD-title-of-post.md
```

### Post Template

```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---

Your content here in markdown...
```

## Local Development

### Install Dependencies

```bash
bundle install --path vendor/bundle
```

### Build the Site

```bash
bundle exec jekyll build
```

### Serve Locally

```bash
bundle exec jekyll serve
```

Then visit `http://localhost:4000` in your browser.

## Deployment

Simply push to the `main` branch (or your configured default branch) on GitHub. GitHub Pages will automatically build and deploy your site.

## File Structure

```
├── _config.yml           # Site configuration
├── _layouts/             # Page templates
│   ├── default.html      # Base layout
│   └── post.html         # Blog post layout
├── _posts/               # Blog posts (markdown files)
├── assets/
│   └── css/
│       └── main.css      # Custom gothic theme styles
├── index.html            # Home page
├── Gemfile               # Ruby dependencies
└── vendor/               # Bundler dependencies (gitignored)
```

## Customization

### Colors

Edit CSS variables in `assets/css/main.css`:

```css
:root {
    --bg-black: #0a0a0a;
    --matrix-green: #00ff41;
    --accent-purple: #8b00ff;
    /* ... */
}
```

### Site Info

Edit `_config.yml` to update:
- Site title
- Description
- Author name
- URL/baseurl

---

*Stay in the shadows* 💀