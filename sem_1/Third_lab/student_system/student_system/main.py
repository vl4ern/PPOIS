from system.services.registration import Registrar
from system.models.Teacher.Teacher import Teacher
from system.models.Teacher.Office import Office
from system.models.Course.Course import Course
from system.models.Course.Module import Module
from system.models.Course.Syllabus import Syllabus
from system.models.Course.CourseSchedule import CourseSchedule
from system.models.Schedule.TimeSlot import TimeSlot
from system.models.Student import Transcript, GradeRecord
from system.models.Student.Student import Student
import sys


def seed_data(reg: Registrar):
    t1 = Teacher("Ivan", "Petrov", "T100", email="ivan@uni.edu")
    t1.office = Office("A", "101", phone="+100")
    c1 = Course("MATH101", "Calculus I", credits=4)
    c1.schedule_options = [TimeSlot("Mon", "09:00", "10:30", "Group A"), TimeSlot("Wed", "11:00", "12:30", "Group B")]
    c1.syllabus = Syllabus("Calculus basics", ["limits","derivatives","integrals"])
    c1.add_module(Module("Limits", lessons=5))
    c1.add_module(Module("Derivatives", lessons=6))
    t1.add_course(c1)

    t2 = Teacher("Anna", "Sidorova", "T200", email="anna@uni.edu")
    c2 = Course("CS101", "Introduction to Programming", credits=5)
    c2.schedule_options = [TimeSlot("Tue", "10:00", "12:00", "Lab A"), TimeSlot("Thu", "14:00", "16:00", "Lab B")]
    c2.syllabus = Syllabus("Intro to programming", ["syntax","control","data structures"])
    c2.add_module(Module("Python Basics", lessons=8))
    t2.add_course(c2)

    reg.add_teacher(t1)
    reg.add_teacher(t2)
    return [t1, t2]

def choose(prompt, items):
    print(prompt)
    for i, it in enumerate(items):
        print(f"{i+1}. {it}")
    choice = input("Введите номер: ").strip()
    try:
        idx = int(choice)-1
        if idx < 0 or idx >= len(items):
            raise ValueError()
        return idx
    except Exception:
        print("Неверный ввод.")
        return choose(prompt, items)

def main():
    reg = Registrar()
    teachers = seed_data(reg)
    print("Регистрация студента")
    first = input("Имя: ").strip()
    last = input("Фамилия: ").strip()
    uid = input("Уникальный ID: ").strip()
    try:
        student = reg.register_student(first, last, uid, email=f"{first.lower()}@example.com")
    except Exception as e:
        print("Ошибка регистрации:", e)
        sys.exit(1)

    # choose teacher
    t_idx = choose("Выберите преподавателя:", [f"{t.full_name()} ({t.teacher_id})" for t in teachers])
    teacher = teachers[t_idx]
    print(f"Вы выбрали: {teacher.full_name()}")

    # choose course from that teacher
    course_idx = choose("Выберите курс:", [f"{c.code} - {c.title}" for c in teacher.courses])
    course = teacher.courses[course_idx]
    # choose timeslot
    times_idx = choose("Выберите вариант времени:", [t.describe() for t in course.schedule_options])
    timeslot = course.schedule_options[times_idx]

    result = reg.enroll_student(uid, teacher.teacher_id, course.code, times_idx)
    print("\\n=== Результат регистрации ===")
    print("Имя:", first)
    print("Фамилия:", last)
    print("ID:", uid)
    print("Преподаватель:", teacher.full_name())
    print("Курс:", course.code, "-", course.title)
    print("Время:", timeslot.describe())
    print("Спасибо!")

if __name__ == '__main__':
    main()