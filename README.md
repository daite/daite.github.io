# daite.github.io

> *"Day: Go. Night: Rust."*

Personal blog and portfolio of **daite** — a developer based in Seoul, South Korea, writing about Go, Rust, and systems programming.

Live at **[daite.github.io](https://daite.github.io)**.

## About

I'm a developer who writes Go by day and Rust by night. This blog is where I document what I learn, share code walkthroughs, and think out loud about engineering problems — from concurrency patterns and CLI tools to memory safety and performance.

Topics covered:

- **Go** — web services, CLI tools, concurrency patterns
- **Rust** — systems programming, memory safety, performance
- **Linux** — shell scripting, tooling, server administration

## Tech Stack

- **[Jekyll](https://jekyllrb.com/)** — static site generator
- **[Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy)** theme — modern, text-focused, feature-rich
- **GitHub Pages** + **GitHub Actions** for CI/CD

## Features

- Full-text search
- Category and tag browsing
- Syntax-highlighted code blocks with line numbers
- Table of contents on every post
- Responsive, mobile-friendly design
- RSS feed and sitemap
- PWA support (installable, offline caching)

## Local Development

Prerequisites: **Ruby 3.4+** and **Bundler**.

```bash
# install dependencies
bundle install

# serve locally at http://localhost:4000
bundle exec jekyll serve

# production build
JEKYLL_ENV=production bundle exec jekyll build
```

## Writing a Post

Add a new Markdown file to `_posts/` using the `YYYY-MM-DD-title.md` naming convention:

```markdown
---
title: "Your Post Title"
date: 2026-04-18 09:00:00 +0900
categories: [Category]
tags: [tag1, tag2]
---

Your content here...
```

## Project Structure

```
.
├── _config.yml                    # site configuration
├── _posts/                        # blog posts
├── _tabs/                         # sidebar pages (about, categories, tags, archives)
├── assets/
│   ├── css/
│   │   └── jekyll-theme-chirpy.scss  # custom CSS overrides
│   └── img/                       # images
├── .github/workflows/
│   └── pages-deploy.yml           # CI/CD workflow
├── Gemfile                        # Ruby dependencies
└── index.html                     # home page entry
```

## Deployment

Pushes to `main` trigger the `pages-deploy.yml` workflow, which builds the site with Jekyll and deploys to GitHub Pages.

## Links

- GitHub: [github.com/daite](https://github.com/daite)

## License

Content (blog posts) © daite. Theme © [Cotes Chung](https://github.com/cotes2020), MIT-licensed.
