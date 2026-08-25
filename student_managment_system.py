"""Simple Student management student"""

import sqlite3

import re
#============================
#Admin Credentials
#============================
USERNAME = "admin"
PASSWORD = "admin123"

conn = sqlite3.connect("student_managment.db")
cursor = conn.cursor()

print("Database is connection build successfully")

#===============Create student table==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
student_id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
mobile TEXT,
email TEXT,
course TEXT,
attendance INTEGER DEFAULT 0)
""")
print("Students Table is created")

# Add the attendance column if it doesn't exist (for schema evolution)
try:
    cursor.execute("ALTER TABLE students ADD COLUMN attendance INTEGER DEFAULT 0")
    conn.commit()
    print("Added 'attendance' column to students table (if it was missing).")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("'attendance' column already exists.")
    else:
        raise # Re-raise other operational errors

#==============Student Class==================
class Student:
  def __init__(self,name,mobile,email,course):
    self.name = name
    self.mobile = mobile
    self.email = email
    self.course = course

  #===========Name Validation==================
  @staticmethod
  def validate_name(name):
    if name.strip() == " ":
      print("Name cannot be empty")
      return False

    if not name.replace(" ","").isalpha():
      print("Name should contain only alphabets")
      return False

    if len(name.strip()) < 3:
      print("Name should be at least 3 characters long")
      return False

    return True

  #======Mobile Validation==========
  @staticmethod
  def validate_mobile(mobile):
    if not mobile.isdigit():
      print("Mobile should contain only digits")
      return False
    if len(mobile) != 10:
      print("Mobile should be 10 digits long")
      return False
    if mobile[0] not in ["6","7","8","9"]:
      print("Mobile should start with 6,7,8,9")
      return False
    return True

  #======EMail Validation===========
  @staticmethod
  def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern,email):
      print("Invalid Email")
      return False
    return True

  #======Course Validation==========
  @staticmethod
  def validate_course(course):
    courses =["Python","Java","AI&ML","Data Science","Full Stack"]
    if course not in courses:
      print("Invalid Course")
      print("Available Courses are :")
      for course in courses:
        print("-",course)
      return False

    return True

  #===========Student Registration==========================
  def register(self):
    #Name Validation
    if not Student.validate_name(self.name):
      return

    #Mobile Validation
    if not Student.validate_mobile(self.mobile):
      return

    #Email Validation
    if not Student.validate_email(self.email):
      return

    #Course Validation
    if not Student.validate_course(self.course):
      return

    #Duplicate Mobile Check
    cursor.execute("""
    SELECT COUNT(*) FROM students
    WHERE mobile = ?
    """,(self.mobile,))

    if cursor.fetchone()[0]:
      print("Mobile number is already registered")
      return

    #Duplicate Mail Check
    cursor.execute("""
    SELECT COUNT(*) FROM students
    WHERE email = ?
    """,(self.email,))


    if cursor.fetchone()[0]:
      print("Email is already registered")
      return

    cursor.execute("""
    INSERT INTO students(name,mobile,email,course)
    VALUES(?,?,?,?)""",
    (self.name,
     self.mobile,
     self.email,
     self.course
    ))

    conn.commit()

  #=============Display Students============
  @staticmethod
  def display_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if len(students) == 0:
      print("No students data is found")
    else:
      print("===========Available Students List===========")
      for student in students:
        print(f"""
        Student ID : {student[0]}
        Name : {student[1]}
        Mobile : {student[2]}
        Email : {student[3]}
        Course : {student[4]}
        Attendance : {student[5]}
        """)

  #=========Student Search by id============
  @staticmethod
  def search_by_id():
    try:
      student_id = int(input("Enter the student ID :"))
    except ValueError:
      print("Invalid Student ID")
      print("Please Enter a number")
      return

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Student Details=========")

      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
        """)
    else:
      print("Student is not found")

  #=========Student Search by name================
  @staticmethod
  def search_by_name():
    name = input("Enter the student name :")
    cursor.execute("""
    SELECT * FROM students
    WHERE name LIKE ?
    """,("%" + name + "%",))

    students = cursor.fetchall()

    if students:
      print("=========Student Details=========")

      for student in students:
        print(f"""
        Student ID : {student[0]}
        Name : {student[1]}
        Mobile : {student[2]}
        Email : {student[3]}
        Course : {student[4]}
        Attendance : {student[5]}
         """)
    else:
      print("Student is not found")

  #==========Update Student===============
  @staticmethod
  def update_student():
    try:
      student_id = int(input("Enter the student ID :"))
    except ValueError:
      print("Invalid Student ID")
      print("Please Enter a number")
      return

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Current Student Details=========")
      print("----------------------------------------")
      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
        """)
      print("----------------------------------------")
      print("Update Student Details")
      print("----------------------------------------")

      name = input("Enter the name :")
      mobile = input("Enter the mobile no :")
      email = input("Enter the email :")
      course = input("Enter the course :")

      cursor.execute("""
      UPDATE students

      SET
      name = ?,
      mobile = ?,
      email = ?,
      course = ?
      WHERE student_id = ?
      """,(
        name,
        mobile,
        email,
        course,
        student_id
      ))

      conn.commit()

      print("Student data is updated successfully")
    else:
      print("Student is not found")

  #==========Delete Student===============
  @staticmethod
  def delete_student():
    try:
      student_id = int(input("Enter the student ID :"))
    except ValueError:
      print("Invalid Student ID")
      print("Please Enter a number")
      return

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Current Student Details=========")
      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
      """)

      confirm = input("Are you sure about to delete this particular student?(Y/N): ").upper()

      if confirm == "Y" :
        cursor.execute("""
        DELETE FROM students
        WHERE student_id = ?
        """,(student_id,))

        conn.commit()
        print("Student data is deleted successfully")

      else:
        print("Student data is not deleted")
    else:
      print("Student data is not found by the ID")

  #=========Mark Attendance============
  @staticmethod
  def mark_attendance():
    try:
      student_id = int(input("Enter the student ID :"))
    except ValueError:
      print("Invalid Student ID")
      print("Please Enter a number")
      return

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """,(student_id,))

    student = cursor.fetchone()

    if student:
      print("=========Current Student Details=========")
      print(f"""
      Student ID : {student[0]}
      Name : {student[1]}
      Mobile : {student[2]}
      Email : {student[3]}
      Course : {student[4]}
      Attendance : {student[5]}
      """)

      print("""
      Attendance Status
      1 -> Present
      0 -> Absent
      """)
      #======Attendance Validation=======
      try:
        attendance = int(input("Enter Attenadance :"))
      except ValueError:
        print("Invalid Attendance")
        print("Please enter 0 for absent and 1 for present")
        return

      if attendance not in (0,1):
        print("Invalid Attendance value")
        return

      cursor.execute("""
      UPDATE students

      SET attendance = ?
      WHERE student_id = ?
      """,
       (attendance,
        student_id))

      conn.commit()

      print("Student Attendance is successfully updated")

    else:
      print("Student is not found")

  #=========Attendance Report============
  @staticmethod
  def attendance_report():
    cursor.execute("""
    SELECT student_id,
        name,
        course,
        attendance
    FROM students""")

    students = cursor.fetchall()

    if len(students) == 0:
      print("No students data is found")
    else:
      print("===========Attendance Report===========")
      for student in students:

        status = "Present" if student[3] == 1 else "Absent"

        print(f"""
        Student ID : {student[0]}
        Name : {student[1]}
        Course : {student[2]}
        Attendance : {status}
        """)
  #============= Dashboard ====================
  @staticmethod
  def dashboard():
    #Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    #Present Students
    cursor.execute("SELECT COUNT(*) FROM students WHERE attendance = 1")
    present_students = cursor.fetchone()[0]

    #Absent Students
    cursor.execute("SELECT COUNT(*) FROM students WHERE attendance = 0")
    absent_students = cursor.fetchone()[0]

    #Attendance Percentage
    if total_students > 0:
      attendance_percentage = (present_students / total_students) * 100
    else:
      attendance_percentage = 0

    print("=========================")
    print("Students Dashboard")
    print("========================")

    print(f"Total Students :{total_students}")
    print(f"Present Students :{present_students}")
    print(f"Absent Students :{absent_students}")
    print(f"Attendance Percentage :{attendance_percentage:}")
    print("=========================")

  #========= LogIn ====================
  @staticmethod
  def login():
    attempts = 5

    while attempts > 0:
      print("===============Admin Login====================")
      username = input("Username :")
      password = input("Password :")

      if (username == USERNAME) and (password == PASSWORD):
        print("LogIn is Successfull")
        print("Welcome Admin")

        return True

      else:
        attempts -= 1
        print("Invalid Username or Password")

        if attempts > 0:
          print(f"Remaining attempts :{attempts}")

    print("Your attempts exceed the Maximum")      # This line should be outside the while loop


if Student.login(): # Changed login() to Student.login()
  while True:
    print("""
    =========Student Mangement System============
    1.Register Students
    2.View students
    3.Search by id
    4.Search by name
    5.Update Student
    6.Delete Student
    7.Attendance
    8.Attendance Report
    9.Dashboard
    10.Exit
    """)

    choice = input("Enter the choice :")

    if choice == "1":
      print("=========student registration===========")
      name = input("Enter the name :")
      mobile = input("Enter the mobile no :")
      email = input("Enter the email :")
      print("""Available Courses are :
      1.Python
      2.Java
      3.AI&ML
      4.Data Science
      5.Full Stack""")

      course = input("Enter the course :")


      student = Student(name,mobile,email,course)

      student.register()

    elif choice == "2":
      Student.display_students()

    elif choice =="3":
      Student.search_by_id()

    elif choice == "4":
      Student.search_by_name()

    elif choice == "5":
      Student.update_student()

    elif choice == "6":
      Student.delete_student()

    elif choice == "7":
      Student.mark_attendance()

    elif choice == "8":
      Student.attendance_report()

    elif choice == "9":
      Student.dashboard()

    elif choice == "10":
      print("Thank you")
      break
    
    else:
      print("Invalid Choice")

  conn.close()

  print("Database is closed successfully")
