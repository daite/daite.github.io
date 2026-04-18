---
title: "Hello, World — Again"
date: 2026-04-18 09:00:00 +0900
categories: [Blog, Meta]
tags: [go, rust, intro]
pin: true
---

It's been a while.

I started this blog back in 2021 with two posts and then promptly forgot it existed. Classic developer move. So here we are — a fresh start, a new theme, and an actual commitment to writing.

## What this blog is about

I spend my days writing **Go** — services, CLIs, the occasional distributed systems deep-dive. At night (and weekends), I reach for **Rust** whenever I want to think harder about memory, ownership, and what it means to write truly safe systems code.

This blog will cover:

- Go patterns, gotchas, and idioms I find interesting
- Rust explorations — especially the parts that hurt at first and then click
- Shell scripting, Linux tooling, and the small utilities that make a terminal feel like home
- Occasional detours into whatever I'm reading or building

## The new setup

The site now runs on [Jekyll](https://jekyllrb.com/) with the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme. Dark mode works. Search works. Code blocks have line numbers and a copy button. Comments are powered by [giscus](https://giscus.app/) — backed by GitHub Discussions, so no tracking, no ads.

If something is broken, let me know in the comments below.

## A taste of what's coming

Here's a snippet of idiomatic Go error wrapping — the kind of thing I'll be writing about:

```go
func fetchUser(id int) (*User, error) {
    u, err := db.Query(id)
    if err != nil {
        return nil, fmt.Errorf("fetchUser %d: %w", id, err)
    }
    return u, nil
}
```

And a Rust equivalent that makes the borrow checker do the heavy lifting:

```rust
fn fetch_user(id: u32) -> Result<User, DbError> {
    db.query(id).map_err(|e| DbError::Query { id, source: e })
}
```

Both clean. Both correct. Different philosophies.

See you in the next post.
