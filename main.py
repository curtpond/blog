import os
from fasthtml.common import *
import frontmatter
from pathlib import Path


app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='/style.css'),
        Script(src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"),
    )
)

def get_posts():
    posts_dir = Path("posts")
    posts = []
    for f in sorted(posts_dir.glob("*.md"), reverse=True):
        if f.name.startswith("_"):
            continue  # Skip template files
        post = frontmatter.load(f)
        post['slug'] = f.stem
        posts.append(post)
    return posts

def get_post(slug):
    path = Path(f"posts/{slug}.md")
    if not path.exists():
        return None
    return frontmatter.load(path)

def page_header():
    return Header(
        H1(A("Curtis Pond", href="/")),
        Nav(
            A("Writing", href="/"),
            A("Books", href="/books"),
            A("About", href="/about"),
        )
    )

def page_footer():
    return Footer(
        P("© 2026 Curtis Pond · Built with FastHTML")
    )

# Home page
@rt
def index():
    posts = get_posts()
    post_items = [
        Li(
            Span(p['date'], cls="post-date"),
            Span(A(p['title'], href=f"/post/{p['slug']}"), cls="post-title"),
            cls="post-item"
        ) for p in posts
    ]
    
    return (
        Title("Curtis Pond - Learning Blog"),
        Div(
            page_header(),
            Div(
                "Welcome! I write to learn. This blog is my way of reinforcing new concepts by explaining them.",
                cls="intro"
            ),
            Div(
                H2("Writing"),
                Ul(*post_items, cls="post-list") if post_items else P("No posts yet."),
                cls="posts-section"
            ),
            page_footer(),
            cls="container"
        )
    )

# About page
@rt
def about():
    return (
        Title("About - Your Name"),
        Div(
            page_header(),
            Article(
                H1("About"),
                Div(
                    P("Write a bit about yourself here. What do you do? What are you learning? Why did you start this blog?"),
                    P("Feel free to add links to your GitHub, LinkedIn, or other places people can find you."),
                    cls="content"
                )
            ),
            A("← Back to home", href="/", cls="back-link"),
            page_footer(),
            cls="container"
        )
    )

# Books page
@rt
def books():
    return (
        Title("Books - Your Name"),
        Div(
            page_header(),
            Article(
                H1("Books & Reading"),
                Div(
                    P("What I'm currently reading and what I've learned from it."),
                    H2("Currently Reading"),
                    P("Nothing listed yet."),
                    H2("Finished"),
                    P("Nothing listed yet."),
                    cls="content"
                )
            ),
            A("← Back to home", href="/", cls="back-link"),
            page_footer(),
            cls="container"
        )
    )

# Individual post page
@rt("/post/{slug}")
def view_post(slug: str):
    p = get_post(slug)
    if not p:
        return Title("Not Found"), Div(page_header(), P("Post not found."), page_footer(), cls="container")
    
    return (
        Title(f"{p['title']} - Your Name"),
        Div(
            page_header(),
            Article(
                H1(p['title']),
                Div(f"Published on {p['date']}", cls="post-meta"),
                Div(p.content, cls="content marked")
            ),
            A("← Back to home", href="/", cls="back-link"),
            page_footer(),
            cls="container"
        ),
        Script("document.querySelectorAll('.marked').forEach(el => el.innerHTML = marked.parse(el.textContent));")
    )

# Serve CSS
@rt("/style.css")
def styles():
    return FileResponse('style.css')

serve(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))