from fasthtml.common import *
import frontmatter
from pathlib import Path

app, rt = fast_app()

def get_posts():
    """Read all markdown files from posts folder"""
    posts_dir = Path("posts")
    posts = []
    for f in sorted(posts_dir.glob("*.md"), reverse=True):
        post = frontmatter.load(f)
        post['slug'] = f.stem  # filename without .md
        posts.append(post)
    return posts

def get_post(slug):
    """Get a single post by slug"""
    path = Path(f"posts/{slug}.md")
    if not path.exists():
        return None
    return frontmatter.load(path)

# Home page
@rt
def index():
    posts = get_posts()
    post_list = [Li(A(p['title'], href=f"/post/{p['slug']}")) for p in posts]
    return Titled("My Learning Blog",
        P("Welcome! This is where I write to learn."),
        H2("Posts"),
        Ul(*post_list) if post_list else P("No posts yet."))

# Individual post page
@rt("/post/{slug}")
def view_post(slug: str):
    p = get_post(slug)
    if not p:
        return Titled("Not Found", P("Post not found."))
    return Titled(p['title'],
        Article(
            Div(p.content, cls="marked"),
            Small(f"Written on {p['date']}")),
        A("← Back to home", href="/"),
        Script(src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"),
        Script("document.querySelectorAll('.marked').forEach(el => el.innerHTML = marked.parse(el.textContent));"))

serve()