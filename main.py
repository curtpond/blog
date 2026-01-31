from fasthtml.common import *

app, rt = fast_app()

@rt
def index():
    return Titled("My Learning Blog", 
        P("Welcome! This is where I write to learn."))

serve()