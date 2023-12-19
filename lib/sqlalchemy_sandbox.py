#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

# Indexes are used to speed up lookups on certain column values. 
# Since teachers and administrators don't typically know their student's ID numbers off the top of their heads, it's wise to set up an index for name in preparation for people using it in their database transactions.    
    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

# All classes in Python have a __repr__() instance method that determines their standard output value (i.e. what you see when you print() the object). 
# By default, this shows the classname and an arbitrary ID. This default value is not very helpful in telling different objects apart. (At least not to humans.)
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

#----Outside class-----------------------------------------------------------------------------------------------
# We have all of the data we need to generate a database table, but it won't happen as soon as we save our module. We need to execute a series of Python statements to do persist our schema. 
# You can do this from the Python shell, but we will be using a script for this exercise.
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

#---------------------------------------------------------------------------------------------------------------
#Create session
Session = sessionmaker(bind=engine) # use our engine to configure a 'Session' class
session = Session() # use 'Session' class to create 'session' object

#--------------------------------------------------------------------------------------------------------------
# Creating record/object
student1 = Student(
    name='Alice', 
    email='alice@school.com', 
    grade=9, 
    birthday=datetime(year=1996, month=8, day=27),
    )

student2 = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
)

student3 = Student(
    name="Mark Tylor",
        email="mark.tylor@moringaschool.com",
        grade=7,
        birthday=datetime(
            year=2000,
            month=10,
            day=23
        ),
)
#print the object
# print(f"New student ID is {student1.id}.")
# print(f"New student ID is {student2.id}.")

#-----------------------------------------------------------------------------------------------------------
#Add student to session and commit to save objects
# session.add(student1) - adds single object
session.bulk_save_objects([student1, student2]) # adds multiple objects
session.commit()

#-------------------------------------------------------------------------------------------------------------
# Read records
students = session.query(Student).all()
# print(students)

#-------------------------------------------------------------------------------------------------------------
#Selecting only certain columns
names= session.query(Student.name).all()
# print(f"Names: {names}")

#-------------------------------------------------------------------------------------------------------------
#Ordering in ASC names
students_by_name= session.query(Student.name).order_by(Student.name).all()
print(f"Order: {students_by_name}")
#Ordering in DESC grades
students_by_desc_grade = session.query(Student).order_by(desc(Student.grade)).all()
print(students_by_desc_grade)

#--------------------------------------------------------------------------------------------------------------
# Limiting:- This output the oldest student and DoB
oldest_student = session.query(Student.name, Student.birthday).order_by(Student.birthday).first()
#OR
#oldest_student = session.query(Student.name, Student.birthday).order_by(Student.birthday).limit(1).all()

#-------------------------------------------------------------------------------------------------------------
# Limiting:- Output the youngest student and DoB
youngest_student = session.query(Student.name , Student.birthday).order_by(-Student.birthday).first()
print(f"Youngest: {youngest_student}")

#--------------------------------------------------------------------------------------------------------
#Func: This allow us perform operations for the columns eg COUNT, SUM
#Count of students
student_count = session.query(func.count(Student.id)).first()
print(f"Student count: {student_count}")
#Sum operation for grade
student_total_grade = session.query(func.sum(Student.grade)).first()
print(f"Total grades: {student_total_grade}")

#--------------------------------------------------------------------------------------------------
# Filtering:- Retrieving specific records requires use of the filter() method.
query= session.query(Student).filter(Student.name.like('%Alan%'), Student.grade== 11).all()
for q in query:
    print(f"Filtered: {q.name}")
#maths_students = session.query(Student).filter(Student.subject == 'Math').all()
    
#---------------------------------------------------------------------------------------------------------------
#Updating data
# 1. Use python to modify objects directly and commit changes to session
for student in session.query(Student):
    student.grade+=1
session.commit()
print(f"Changed grades: {[(student.name, student.grade) for student in session.query(Student)]}")

# 2. The update() method allows us to update records without creating objects beforehand. 
# - Here's how we would carry out the same statement with update():
session.query(Student).update({Student.grade: Student.grade+1})
print(f"Second update method: {[(student.name, student.grade) for student in session.query(Student)]}")

#-------------------------------------------------------------------------------------------------------------
# Deleting Data
#1. To delete a record from your database, you can use the delete() method. 
# If you have an object in memory that you want to delete, you can call the delete() method on the object from your session:
query = session.query(Student).filter(Student.name== "Mark Tylor")
#retrieve first matching record as object
mark = query.first() # returns a single instance of Mark Taylor
# Delete mark from database using delete() method on Query object
session.delete(mark)
session.commit()
# try to retireve deleted record
student3 = query.first()
print(f"Deleted record: {student3}") #Give an error of none

#-----Above returned an error-------------------------------------------------------------------------------


#2. If you don't have a single object ready for deletion but you know the criteria for deletion, you can call the delete() method from your query instead:
query = session.query(Student).filter(Student.name== "Mark Tylor")
query.delete()
mark2 = query.first()
print(mark2)