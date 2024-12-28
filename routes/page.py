from fasthtml.common import A, Div

from make_app import app


@app.get("/foo", name="foo")
def foo():
    return Div("Hello world!", cls="bg-surface-20")
