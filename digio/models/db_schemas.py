# GiG

from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


class College(SQLModel, table=True):
    __tablename__: str = "colleges"  #  type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    short_name: str


class Department(SQLModel, table=True):
    __tablename__: str = "departments"  #  type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    short_name: str
    college_id: int = Field(foreign_key="colleges.id")


class Batch(SQLModel, table=True):
    __tablename__: str = "batches"  #  type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    short_name: str
    college_id: int = Field(foreign_key="colleges.id")
    department_id: int = Field(foreign_key="departments.id")


class Course(SQLModel, table=True):
    __tablename__: str = "courses"  #  type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    short_name: str
    language: str
    concepts: str
    is_archived: bool = Field(default=False)


class Faculty(SQLModel, table=True):
    __tablename__: str = "faculties"  #  type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    # Keeping password as optional to make update easy
    hashed_pwd: Optional[str] = Field(default="")
    first_name: str
    last_name: Optional[str]
    email_id: Optional[str]
    phone_number: Optional[str]
    # Probably space efficient to use CHAR but its okay
    gender: Optional[str] = Field(default="M")
    college_id: int = Field(foreign_key="colleges.id")
    department_id: int = Field(foreign_key="departments.id")
    is_admin: bool = Field(default=False)


class Student(SQLModel, table=True):
    __tablename__: str = "students"  #  type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    # Keeping password as optional to make update easy
    hashed_pwd: Optional[str] = Field(default="")
    first_name: str
    last_name: Optional[str]
    email_id: Optional[str]
    phone_number: Optional[str]
    # Probably space efficient to use CHAR but its okay
    gender: Optional[str] = Field(default="M")

    # college_id and department_id could be inferred from batch_id
    # but storing it here so that we can do processing easily
    # with some minor space wastage
    college_id: int = Field(foreign_key="colleges.id")
    department_id: int = Field(foreign_key="departments.id")
    batch_id: int = Field(foreign_key="batches.id")


class BatchCourseAssignments(SQLModel, table=True):
    __tablename__: str = "course_batch_assignments"  #  type: ignore
    # This indirect method is needed as the unique constraint
    #   is over two columns
    __table_args__ = (UniqueConstraint("batch_id", "course_id", name="uq_batch_id_course_id"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="batches.id")
    course_id: int = Field(foreign_key="courses.id")
    faculty_id: int = Field(foreign_key="faculties.id")
