"""
To-Do backend — FastAPI

Run:
    pip install "fastapi[standard]"
    fastapi run main.py --port 8000        # production
    fastapi dev main.py --port 8000        # dev with auto-reload

Interactive docs: http://localhost:8000/docs

Endpoints (all under /api so nginx can proxy /api/ to this app):
    GET    /api/todos          -> list all todos
    GET    /api/todos/{id}     -> get one todo
    POST   /api/todos          -> create a todo   body: {"name": "Buy milk"}
    DELETE /api/todos/{id}     -> delete a todo
"""

from itertools import count
from threading import Lock

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="To-Do API", version="1.0.0")

# Allows the frontend to call the API if it's served from a different origin.
# Tighten allow_origins to your domain in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


# ---------- Models ----------

class TodoCreate(BaseModel):
    """What the user sends: only the name."""
    name: str = Field(..., min_length=1, max_length=200, examples=["Buy milk"])


class Todo(BaseModel):
    """What the API returns: the name plus the server-generated ID."""
    id: int
    name: str


# ---------- Storage (in memory) ----------

_todos: dict[int, Todo] = {}
_id_counter = count(start=1)   # global ID generator: 1, 2, 3, ...
_lock = Lock()                 # keeps ID generation + writes safe across threads


# ---------- Routes ----------

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=list[Todo])
def list_todos() -> list[Todo]:
    return list(_todos.values())


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    todo = _todos.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todo


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate) -> Todo:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Name cannot be blank")
    with _lock:
        todo = Todo(id=next(_id_counter), name=name)
        _todos[todo.id] = todo
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int) -> None:
    with _lock:
        if _todos.pop(todo_id, None) is None:
            raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")


app.include_router(router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
