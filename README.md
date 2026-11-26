# Student CRUD — FastAPI backend + vanilla JavaScript frontend

Two separate parts that talk to each other over HTTP:

```
student-crud/
├── backend/
│   ├── main.py           # FastAPI app: only JSON endpoints, no HTML
│   └── requirements.txt  # fastapi + uvicorn
├── frontend/
│   └── index.html        # plain HTML/JS, calls the API with fetch()
└── README.md
```

## 1. Run the backend (terminal)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is now on **http://127.0.0.1:8000** (uvicorn's default port).

FastAPI also gives you interactive API documentation for free:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 2. Open the frontend (Chrome)

Just open the file directly — double-click `frontend/index.html` or drag it
into a Chrome tab (`file:///…/student-crud/frontend/index.html`).

**Why there is no CORS error:** a page opened from `file://` sends the header
`Origin: null`, and the backend answers `Access-Control-Allow-Origin: *`
(see `allow_origins=["*"]` in `main.py`). Wildcards are accepted by browsers
as long as the request carries no cookies (`allow_credentials=False`).

Two alternatives that work with the same backend setting:

- VS Code **Live Server** (http://127.0.0.1:5500) — right-click `index.html` → "Open with Live Server".
- Any static server, e.g. `python -m http.server 5500` inside the `frontend/` folder.

> If you ever run the backend on another port (`uvicorn main:app --reload --port 8081`),
> update the `API` constant at the top of `frontend/index.html` to match.

## 3. The API

| Method | Path | Body | Does |
|---|---|---|---|
| POST | `/students` | `{"name": "Sara", "age": 20, "email": "sara@example.com"}` | CREATE |
| GET | `/students` | – | READ (all) |
| PUT | `/students/{id}` | same body as POST | UPDATE |
| DELETE | `/students/{id}` | – | DELETE |

### Try it without the frontend (curl)

```bash
# CREATE
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Sara", "age": 20, "email": "sara@example.com"}'

# READ
curl http://127.0.0.1:8000/students

# UPDATE id 1
curl -X PUT http://127.0.0.1:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Sara Updated", "age": 21, "email": "sara@example.com"}'

# DELETE id 1
curl -X DELETE http://127.0.0.1:8000/students/1
```

## 4. How the pieces fit together

One CRUD operation = one HTTP verb, on both sides:

| App action | HTTP verb | Backend function | Frontend call |
|---|---|---|---|
| Add student | POST | `create_student()` | `fetch(API, { method: "POST", ... })` |
| List students | GET | `get_students()` | `fetch(API)` |
| Edit (prompt → PUT) | PUT | `update_student()` | `fetch(API/id, { method: "PUT", ... })` |
| Delete (confirm → DELETE) | DELETE | `delete_student()` | `fetch(API/id, { method: "DELETE" })` |

Pydantic (`class Student(BaseModel)`) validates every POST/PUT body: a missing
or wrongly-typed field automatically returns `422 Unprocessable Entity` —
try sending a broken body in `/docs` and watch the response.

## 5. Limits on purpose (and what to learn next)

- Data lives in a Python list → every restart wipes it. Next step: persist it
  in a real database — exactly what the companion project does with SQLite.
- No users: anyone can edit anything. Next step: `../signup-login` adds
  accounts, hashed passwords and login tokens — afterwards you can protect
  these endpoints so only logged-in users can call them.
