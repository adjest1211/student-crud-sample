from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import dbconnect

app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#student
class Student(BaseModel):
    name: str
    email: str
    course: str
    year_level: int


@app.post("/api/students")
def add_student(student: Student):
    db = dbconnect()
    cursor = db.cursor(dictionary=True)

    sql = """
        INSERT INTO students(name, email, course, year_level)
        VALUES (%s, %s, %s, %s)
    """,
    values = (
        student.name,
        student.email,
        student.course,
        student.year_level
    )

    cursor.execute(sql, values)
    db.commit()

    student_id = cursor.lastrowid

    cursor.close()
    db.close()

    return{
        "message": "Student added successfully",
        "id": student_id
    }

@app.get("/api/students")
def get_students():
    db = dbconnect()
    cursor=db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC"
    )

    students = cursor.fetchall()
    db.close()

    return students

@app.get("/api/students/{student_id}")
def get_student(student_id: int):
    db = dbconnect()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.close()
    db.close()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student


@app.put("/api/students/{student_id}")
def update_student(student_id: int, student: Student):
    db = dbconnect()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name = %s,
            email = %s,
            course = %s,
            year_level = %s,
        WHERE id = %s
    """,
    (
        student.name,
        student.email,
        student.course,
        student.year_level,
        student_id
    )
    )
    db.commit()

    affected = cursor.rowcount

    cursor.close()
    db.close()

    if affected == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found or no changes made"
        )

    return {
        "message": "Student updated successfully"
    }

@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    db = dbconnect()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (studet_id,)
    )

    db.commit()
    affected = cursor.rowcount

    cursor.close()
    db.close()

    if affected == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }

@app.get("/")
def home():
    return {
        "message": "Student Management API is running!"
    }