from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Subject
from conf.db import session


def select_01():
    result = (
        session.query(
            Student.id,
            Student.full_name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Student)
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )
    return result


def select_02(id_subject):
    result = (
        session.query(
            Student.id,
            Student.full_name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Student)
        .join(Grade)
        .filter(Grade.subject_id == id_subject)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(1)
        .all()
    )
    return result


def select_03(id_subject):
    result = (
        session.query(
            Subject.name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Subject)
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Grade.subject_id == id_subject)
        .group_by(Subject.name)
        .all()
    )
    return result


def select_04():
    result = session.query(func.avg(Grade.grade).label("average_grade")).scalar()
    return result


def select_05(teacher_id):
    result = session.query(Subject.name).join(Teacher.id == teacher_id).all()
    return result


def select_06(group_id):
    result = session.query(Student.full_name).filter(Student.group_id == group_id).all()
    return result


def select_07(group_id, subject_id):
    result = (
        session.query(Student.full_name.distinct(), Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return result


def select_08(teacher_id):
    result = (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return result


def select_09(student_id):
    result = (
        session.query(Subject.name.distinct())
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .all()
    )
    return result


def select_10(student_id, teacher_id):
    result = (
        session.query(Subject.name.distinct())
        .join(Grade)
        .join(Teacher)
        .filter(Grade.student_id == student_id, Teacher.id == teacher_id)
        .all()
    )
    return result


def select_11(teacher_id, student_id):
    result = (
        session.query(
            Student.full_name,
            Teacher.full_name,
            func.avg(Grade.grade).label("average_grade"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.id == student_id, Teacher.id == teacher_id)
        .group_by(Student.full_name, Teacher.full_name)
        .all()
    )
    return result


def select_12(subject_id, group_id):
    subquery = (
        session.query(func.max(Grade.date_received).label("max_date"))
        .filter(Grade.subject_id == subject_id)
        .scalar_subquery()
    )
    result = (
        session.query(Student.full_name, Grade.grade)
        .join(Grade)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == subquery,
        )
        .all()
    )
    return result
