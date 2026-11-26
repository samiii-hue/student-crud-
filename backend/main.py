from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Student CRUD API")

# The backend only serves JSON. The frontend is a separate file that you open
# directly in Chrome, so its "origin" is either:
#   - "null"        (page opened from disk via file://)
#   - a Live Server page (http://127.0.0.1:5500)
# The "*" wildcard allows ALL origins, which every browser accepts as long as
# no cookies/credentials are involved (allow_credentials must stay False).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database" (a plain Python list). On purpose: simplest possible
# CRUD. Every restart empties it. See ../signup-login for SQLite persistence.
students = []
next_id = 1


class Student(BaseModel):
    """Pydantic model: validates the JSON body of POST/PUT automatically."""
    name: str
    age: int
    email: str


@app.get("/")
def root():
    return {"message": "Student CRUD API is running. Open /docs to try the endpoints."}


@app.post("/students")
def create_student(student: Student):
    """CREATE - HTTP POST"""
    global next_id
    new_student = {"id": next_id, **student.model_dump()}
    students.append(new_student)
    next_id += 1
    return new_student


@app.get("/students")
def get_students():
    """READ - HTTP GET"""
    return students


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    """UPDATE - HTTP PUT"""
    for existing in students:
        if existing["id"] == student_id:
            existing.update(student.model_dump())
            return existing
    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """DELETE - HTTP DELETE"""
    for existing in students:
        if existing["id"] == student_id:
            students.remove(existing)
            return {"message": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
