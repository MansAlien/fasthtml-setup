from dataclasses import dataclass
from components.button import button
from fasthtml.common import (
    A,
    Button,
    Div,
    Form,
    Input,
    Li,
    Ul,
    H1,
    Span,
    Style,
    serve,
)
from make_app import app, rt
from models import Todo

@app.get("/foo", name="foo")
def foo():
    return Div("Hello world!", cls="bg-surface-20")

@dataclass
class TodoForm:
    title: str

@rt("/")
def get(request):
    db = request.state.db
    todos = db.query(Todo).all()
    
    todo_items = [
        Li(
            Div(
                Div(
                    Span(todo.title, cls="text-lg truncate max-w-sm block"),
                    Span(
                        "✓ Done" if todo.done else "○ Pending",
                        cls=f"mx-8 text-sm {'text-green-400' if todo.done else 'text-yellow-400'}"
                    ),
                    title=todo.title,
                    cls="flex items-center justify-between flex-1"
                ),
                Div(
                    A(
                        "✎",
                        href="#",
                        cls="text-blue-400 hover:text-blue-300 text-xl transition-colors px-2",
                        hx_get=f"/todos/{todo.id}/edit",
                        hx_target="closest div"
                    ),
                    A(
                        "×",
                        href="#",
                        cls="text-red-400 hover:text-red-300 text-xl font-bold transition-colors px-2",
                        hx_delete=f"/todos/{todo.id}",
                        hx_target="closest li",
                        hx_swap="outerHTML"
                    ),
                    cls="flex items-center border-l border-l-surface-50"
                ),
                cls="flex items-center justify-between p-4 mb-2 rounded-lg bg-surface-20 hover:bg-surface-30 transition-all"
            ),
            cls="list-none"
        ) for todo in todos
    ]

    form = Form(
        Div(
            Input(
                id="title",
                name="title",
                placeholder='What needs to be done?',
                cls="""
                    border text-sm rounded-lg block w-full
                    p-4 bg-surface-20 border-surface-30 placeholder-surface-50
                    text-white focus:ring-blue-500 focus:border-blue-500
                    transition-all hover:bg-surface-30
                """
            ),
            Button(
                "Add Task",
                cls="px-6 py-4 whitespace-nowrap bg-blue-600 text-white w-30 rounded-lg hover:bg-blue-700 transition-all"
            ),
            cls="flex gap-4 w-full"
        ),
        cls="w-full mb-8",
        hx_post="/",
        target_id="todo_list",
        hx_swap="beforeend"
    )

    return Div(
        Style("""
            .custom-scrollbar::-webkit-scrollbar {
                width: 6px;
            }
            .custom-scrollbar::-webkit-scrollbar-track {
                background: rgb(24, 24, 27);
                border-radius: 3px;
            }
            .custom-scrollbar::-webkit-scrollbar-thumb {
                background: rgb(39, 39, 42);
                border-radius: 3px;
            }
            .custom-scrollbar::-webkit-scrollbar-thumb:hover {
                background: rgb(63, 63, 70);
            }
        """),
        Div(
            H1(
                "Todo List",
                cls="text-5xl font-bold text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
            ),
            cls="bg-surface-10 p-12 items-center content-center shadow-lg"
        ),
        Div(
            Div(
                form,
                cls="max-w-2xl mx-auto"
            ),
            Div(
                Ul(
                    *todo_items,
                    id="todo_list",
                    cls="space-y-2 max-h-96 overflow-y-auto custom-scrollbar"
                ),
                cls="max-w-2xl mx-auto"
            ),
            cls="p-8 md:p-12 bg-surface-5"
        ),
        cls="min-h-screen bg-surface-0 text-white font-rubik"
    )

@rt("/", methods=["POST"])
def post(request, todo: TodoForm):
    db = request.state.db
    new_todo = Todo(title=todo.title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return Li(
        Div(
            Div(
                Span(new_todo.title, cls="text-lg max-w-md truncate block"),
                Span(
                    "○ Pending",
                    cls="mx-8 text-sm text-yellow-400"
                ),
                cls="flex items-center justify-between flex-1"
            ),
            Div(
                A(
                    "✎",
                    href="#",
                    cls="text-blue-400 hover:text-blue-300 text-xl transition-colors px-2",
                    hx_get=f"/todos/{new_todo.id}/edit",
                    hx_target="closest div"
                ),
                A(
                    "×",
                    href="#",
                    cls="text-red-400 hover:text-red-300 text-xl font-bold transition-colors px-2",
                    hx_delete=f"/todos/{new_todo.id}",
                    hx_target="closest li",
                    hx_swap="outerHTML"
                ),
                cls="flex items-center border-l border-l-surface-50"
            ),
            cls="flex items-center justify-between p-4 mb-2 rounded-lg bg-surface-20 hover:bg-surface-30 transition-all"
        ),
        cls="list-none"
    )

@rt("/todos/{todo_id}", methods=["DELETE"])
def delete_todo(request, todo_id: int):
    db = request.state.db
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return ""

@rt("/todos/{todo_id}/edit", methods=["GET"])
def edit_todo_form(request, todo_id: int):
    db = request.state.db
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    return Div(
        Form(
            Div(
                Input(
                    name="title",
                    value=todo.title,
                    cls="""
                        border text-sm rounded-lg flex-1
                        p-2 bg-surface-20 border-surface-30
                        text-white focus:ring-blue-500 focus:border-blue-500
                        transition-all hover:bg-surface-30
                    """
                ),
                Button(
                    "Save",
                    cls="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all ml-2"
                ),
                cls="flex items-center"
            ),
            hx_put=f"/todos/{todo_id}",
            hx_target="closest div",
        ),
        cls="p-4 mb-2 rounded-lg bg-surface-20"
    )

@rt("/todos/{todo_id}", methods=["PUT"])
def update_todo(request, todo_id: int, todo: TodoForm):
    db = request.state.db
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title
        db.commit()
        return Div(
            Div(
                Span(todo.title, cls="text-lg"),
                Span(
                    "✓ Done" if db_todo.done else "○ Pending",
                    cls=f"ml-8 text-sm {'text-green-400' if db_todo.done else 'text-yellow-400'}"
                ),
                cls="flex items-center flex-1"
            ),
            Div(
                A(
                    "✎",
                    href="#",
                    cls="text-blue-400 hover:text-blue-300 text-xl transition-colors px-2",
                    hx_get=f"/todos/{todo_id}/edit",
                    hx_target="closest div"
                ),
                A(
                    "×",
                    href="#",
                    cls="text-red-400 hover:text-red-300 text-xl font-bold transition-colors px-2",
                    hx_delete=f"/todos/{todo_id}",
                    hx_target="closest li",
                    hx_swap="outerHTML"
                ),
                cls="flex items-center"
            ),
            cls="flex items-center justify-between p-4 mb-2 rounded-lg bg-surface-20 hover:bg-surface-30 transition-all"
        )
    return ""

serve()
