from fasthtml.common import *
from datetime import date

# Set up database for blog posts
db = database('data/blog.db')

class Post:
    id: int
    title: str
    slug: str
    content: str
    created: str

posts = db.create(Post, transform=True)

app, rt = fast_app()

# Home page - list all posts
@rt
def index():
    post_list = [Li(A(p.title, href=f"/post/{p.slug}")) for p in posts()]
    return Titled("My Learning Blog",
        P("Welcome! This is where I write to learn."),
        A("+ New Post", href="/new"),
        H2("Posts"),
        Ul(*post_list) if post_list else P("No posts yet."))

# Individual post page
@rt("/post/{slug}")
def view_post(slug: str):
    p = posts(where=f"slug='{slug}'")
    if not p:
        return Titled("Not Found", P("Post not found."))
    p = p[0]
    return Titled(p.title,
        Article(
            P(p.content),
            Small(f"Written on {p.created}")),
        A("← Back to home", href="/"))

# New post form
@rt
def new():
    return Titled("New Post",
        Form(method="post", action="/create")(
            Label("Title", Input(name="title", required=True)),
            Label("Slug (url-friendly)", Input(name="slug", required=True, placeholder="my-post-title")),
            Label("Content", Textarea(name="content", rows=10, required=True)),
            Button("Publish")),
        A("← Back to home", href="/"))

# Handle form submission
@rt("/create", methods=["post"])
def create(title: str, slug: str, content: str):
    posts.insert(title=title, slug=slug, content=content, created=str(date.today()))
    return RedirectResponse(f"/post/{slug}", status_code=303)

serve()