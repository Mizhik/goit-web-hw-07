import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, Group, Subject, Grade


fake = Faker("uk-UA")

def insert_data():
    groups = ["Група 1", "Група 2", "Група 3"]
    for group_name in groups:
        group = Group(name=group_name)
        session.add(group)

    # Створюємо предмети
    subjects = ["Математика", "Фізика", "Хімія", "Історія", "Література"]
    for subject_name in subjects:
        subject = Subject(name=subject_name, teacher_id=random.randint(1, 3))
        session.add(subject)

    # Створюємо викладачів
    for _ in range(3):
        teacher = Teacher(full_name=fake.name())
        session.add(teacher)

    # Створюємо студентів
    for _ in range(30):
        student = Student(full_name=fake.name(), group_id=random.randint(1, 3))
        session.add(student)

    # Додаємо оцінки для кожного студента з усіх предметів
    for student in session.query(Student).all():
        for subject in session.query(Subject).all():
            for _ in range(random.randint(1, 5)):
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=random.randint(1, 12),
                    date_received=fake.date_between(start_date="-1y", end_date="today"),
                )
                session.add(grade)

if __name__ == "__main__":
    try:
        insert_data()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
