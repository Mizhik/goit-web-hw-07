from sqlalchemy.orm import mapped_column, Mapped, relationship, declarative_base
from sqlalchemy import Date, Integer, String, ForeignKey

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    group_id: Mapped[int] = mapped_column("group_id", ForeignKey("groups.id"))
    group = relationship("Group", backref='students')

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(150), nullable=False)
    teacher_id:Mapped[int] = mapped_column("teacher_id", ForeignKey('teachers.id'))
    teacher = relationship("Teacher", backref='subject')

class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grade:Mapped[int] = mapped_column(Integer,nullable=False)
    student_id: Mapped[int] = mapped_column("student_id", ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column("subject_id", ForeignKey("subjects.id"))
    date_received:Mapped[Date] = mapped_column(Date, nullable=False)
    student = relationship("Student", backref='grade')
    subject = relationship("Subject", backref='grade')