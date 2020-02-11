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
            curs.execute(f"""insert into Students VALUES(default, '{students}');
                        """)
            curs.execute(f"""insert into Course values(default, {course_id})""")

            curs.execute("""create table student_course(
            id serial PRIMARY KEY,
            student_id INTEGER REFERENCES Students(id),
            course_id INTEGER REFERENCES Course(id));
            """)

            curs.execute("""insert into student_course values(student_id,course_id)""")
    return 'ok'
print(add_students(5, 'Petya'))


