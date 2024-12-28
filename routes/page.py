from dataclasses import dataclass

from fasthtml.common import (
    Button,
    Container,
    Div,
    Form,
    Input,
    Li,
    RedirectResponse,
    Title,
    Ul,
    serve,
)

from make_app import app, rt
from models import Todo


@app.get("/foo", name="foo")
def foo():
    return Div("Hello world!", cls="bg-surface-20")

# Data class for form submission
@dataclass
class TodoForm:
    title: str

# Route to display the list of todos
@rt("/")
def get(request):
    db = request.state.db  # Get the database session from the request
    todos = db.query(Todo).all()
    todo_items = [Li(f"{todo.title} - {'Done' if todo.done else 'Pending'}") for todo in todos]
    form = Form(
        Input(id="title", name="title", placeholder="New Task"),
        Button("Add Task"),
        action="/", method="post"
    )
    return Title("Todo List"), Container(Ul(*todo_items), form)

# Route to add a new todo
@rt("/", methods=["POST"])
def post(request, todo: TodoForm):
    db = request.state.db  # Get the database session from the request
    new_todo = Todo(title=todo.title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return RedirectResponse("/", status_code=303)

# Serve the application
serve()


