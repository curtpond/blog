from datetime import date

slug = input("Post slug (e.g., my-new-post): ")
title = input("Post title: ")

content = f"""---
title: {title}
date: {date.today()}
---

A brief intro about what you learned and why it matters.

## What I Learned

The main concepts explained in your own words.

## Why It Matters

How this connects to other things you know or why it's useful.

## Key Takeaways

- First insight
- Second insight
- Third insight

## Resources

- [Link to resource](https://example.com)
"""

filename = f"posts/{slug}.md"
with open(filename, "w") as f:
    f.write(content)

print(f"Created {filename}")