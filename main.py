from fasthtml.common import *

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
        H2("Posts"),
        Ul(*post_list) if post_list else P("No posts yet."))

# Individual post page
@rt("/post/{slug}")
def view_post(slug: str):
    p = posts(where=f"slug='{slug}'")
    if not p:
        return Titled("Not Found", P("Post not found."))
    p = p[0] # Get the single post
    return Titled(p.title,
        Article(
            P(p.content),
            Small(f"Written on {p.created}")),
        A("← Back to home", href="/"))

serve()