from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك تحديد نطاقات معينة بدلاً من "*" للسماح بها فقط
    allow_credentials=True,
    allow_methods=["*"],  # يمكنك تحديد طرق معينة مثل ["GET", "POST"]
    allow_headers=["*"],  # يمكنك تحديد رؤوس معينة للسماح بها
)

# نموذج بيانات الطالب باستخدام Pydantic
class Student(BaseModel):
    id: int
    name: str
    class_requested: str
    date_requested: datetime = datetime.now()

# قائمة لتخزين بيانات الطلاب
students: List[Student] = []

# إضافة طالبين إلى القائمة
students.append(Student(id=1, name="Ahmed", class_requested="Grade 5"))
students.append(Student(id=2, name="Sara", class_requested="Grade 6"))

# مسار لعرض رسالة ترحيبية
@app.get("/")
def read_root():
    return {"message": "Welcome to the School Management API"}

# مسار لعرض جميع الطلاب
@app.get("/students/")
def get_students():
    return {"students": students}

# مسار لإضافة طالب جديد
@app.post("/students/")
def add_student(student: Student):
    for existing_student in students:
        if existing_student.id == student.id:
            raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    students.append(student)
    return student

# مسار لتحديث بيانات طالب
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for student in students:
        if student.id == student_id:
            student.name = updated_student.name
            student.class_requested = updated_student.class_requested
            student.date_requested = updated_student.date_requested
            return student
    raise HTTPException(status_code=404, detail="Student not found.")

# مسار لحذف طالب
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    global students
    students = [student for student in students if student.id != student_id]
    return {"message": "Student deleted successfully"}
