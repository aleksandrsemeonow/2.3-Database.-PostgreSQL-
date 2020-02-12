import psycopg2

def create_db(name, input):
    with psycopg2.connect(dbname='test_db', user='test_user') as conn:
        with conn.cursor() as curs:
            curs.execute(f"""create table {name}({input})""")
    return f'Таблица {name} создана'
# print(create_db('Students','id serial PRIMARY KEY, name varchar(100) NOT NULL, gpa numeric(10,2), birth timestamp'))
# print(create_db('Course', 'id serial PRIMARY KEY NOT NULL, name character varying(100) NOT NULL'))

def add_student(student):
    with psycopg2.connect(dbname='test_db', user='test_user') as conn:
        with conn.cursor() as curs:
            curs.execute(f"""insert into Students VALUES (default, name '{student}');
            """)
    return f'Студент {student} создан'
# print(add_student('Alexey'))

def add_students(course_id, students):
    with psycopg2.connect(dbname='test_db', user='test_user') as conn:
        with conn.cursor() as curs:
            curs.execute("""insert into Students(name) VALUES(%s) returning id;""", (students,))
            id_from_student = curs.fetchall()[0]
            curs.execute(f"""insert into Course (name) values(%s) returning id;""", (course_id,))
            id_from_cource = curs.fetchall()[0]

            curs.execute("""create table student_course(
                        id serial PRIMARY KEY,
                        student_id INTEGER REFERENCES Students(id),
                        course_id INTEGER REFERENCES Course(id));
                        """)

            curs.execute("""insert into student_course (student_id, course_id) values(%s, %s) returning id;""", (id_from_student,id_from_cource))
    return f'Студент создан и запсиан на курс'

# print(add_students(4,'Ruslan'))

def get_student(student_id):
    with psycopg2.connect(dbname='test_db', user='test_user') as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from Students;""")
            all_students = cur.fetchall()
            for student in all_students:
                if student_id == student[0]:
                    return student
# print(get_student(2))

def get_students(course_id):
    with psycopg2.connect(dbname='test_db', user='test_user') as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student_course;""")
            student_course = cur.fetchall()
            for course in student_course:
                if course_id == course[2]:
                    student_id = course[1]
                    cur.execute("""select * from Students;""")
                    all_students = cur.fetchall()
                    students_of_course = []
                    for student in all_students:
                        if student_id == student[0]:
                            students_of_course.append(student)
            return students_of_course
print(get_students(1))
