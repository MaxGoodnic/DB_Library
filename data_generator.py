import random
from datetime import datetime, timedelta
from faker import Faker
from database import DatabaseManager

fake = Faker('ru_RU')

class DataGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def generate_departments(self, count=5):
        departments = []
        for _ in range(count):
            dept = {
                'department_name': fake.company() + " факультет",
                'building': random.choice(['А', 'Б', 'В', 'Г', 'Д']) + str(random.randint(1, 10)),
                'budget': round(random.uniform(1000000, 10000000), 2)
            }
            departments.append(dept)
        
        query = """
        INSERT INTO Departments (department_name, building, budget)
        VALUES (%(department_name)s, %(building)s, %(budget)s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Departments (department_name, building, budget)
        VALUES (?, ?, ?)
        """
        
        for dept in departments:
            if self.db.db_type == 'postgresql':
                self.db.execute_query(query, dept)
            else:
                self.db.execute_query(query, (dept['department_name'], dept['building'], dept['budget']))
        
        return departments
    
    def generate_teachers(self, count=20):
        departments = self.db.execute_query("SELECT department_id FROM Departments")
        
        teachers = []
        for _ in range(count):
            teacher = {
                'first_name': fake.first_name_male(),
                'last_name': fake.last_name_male(),
                'birth_date': fake.date_between(start_date='-65y', end_date='-25y'),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'address': fake.address(),
                'hire_date': fake.date_between(start_date='-20y', end_date='today'),
                'department_id': random.choice(departments)['department_id'] if departments else None,
                'position': random.choice(['Профессор', 'Доцент', 'Старший преподаватель', 'Ассистент']),
                'salary': round(random.uniform(50000, 150000), 2)
            }
            teachers.append(teacher)
        
        query = """
        INSERT INTO Teachers (first_name, last_name, birth_date, email, phone, address, 
                            hire_date, department_id, position, salary)
        VALUES (%(first_name)s, %(last_name)s, %(birth_date)s, %(email)s, %(phone)s, 
                %(address)s, %(hire_date)s, %(department_id)s, %(position)s, %(salary)s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Teachers (first_name, last_name, birth_date, email, phone, address, 
                            hire_date, department_id, position, salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        for teacher in teachers:
            if self.db.db_type == 'postgresql':
                self.db.execute_query(query, teacher)
            else:
                self.db.execute_query(query, (
                    teacher['first_name'], teacher['last_name'], teacher['birth_date'],
                    teacher['email'], teacher['phone'], teacher['address'],
                    teacher['hire_date'], teacher['department_id'], teacher['position'], teacher['salary']
                ))
        
        return teachers
    
    def generate_subjects(self, count=15):
        departments = self.db.execute_query("SELECT department_id FROM Departments")
        
        subjects = [
            {'name': 'Математический анализ', 'credits': 6},
            {'name': 'Линейная алгебра', 'credits': 4},
            {'name': 'Программирование', 'credits': 5},
            {'name': 'Базы данных', 'credits': 4},
            {'name': 'Алгоритмы и структуры данных', 'credits': 5},
            {'name': 'Дискретная математика', 'credits': 4},
            {'name': 'Теория вероятностей', 'credits': 3},
            {'name': 'Статистика', 'credits': 3},
            {'name': 'Машинное обучение', 'credits': 5},
            {'name': 'Искусственный интеллект', 'credits': 4},
            {'name': 'Веб-разработка', 'credits': 4},
            {'name': 'Мобильная разработка', 'credits': 3},
            {'name': 'Кибербезопасность', 'credits': 4},
            {'name': 'Операционные системы', 'credits': 4},
            {'name': 'Компьютерные сети', 'credits': 3}
        ]
        
        query = """
        INSERT INTO Subjects (subject_name, description, credits, department_id)
        VALUES (%(subject_name)s, %(description)s, %(credits)s, %(department_id)s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Subjects (subject_name, description, credits, department_id)
        VALUES (?, ?, ?, ?)
        """
        
        for subject in subjects:
            dept_id = random.choice(departments)['department_id'] if departments else None
            description = fake.text(max_nb_chars=200)
            
            if self.db.db_type == 'postgresql':
                self.db.execute_query(query, {
                    'subject_name': subject['name'],
                    'description': description,
                    'credits': subject['credits'],
                    'department_id': dept_id
                })
            else:
                self.db.execute_query(query, (subject['name'], description, subject['credits'], dept_id))
    
    def generate_groups(self, count=10):
        departments = self.db.execute_query("SELECT department_id FROM Departments")
        teachers = self.db.execute_query("SELECT teacher_id FROM Teachers")
        
        groups = []
        for i in range(count):
            group = {
                'group_name': f"ИТ-{i+1:02d}",
                'department_id': random.choice(departments)['department_id'] if departments else None,
                'creation_year': random.randint(2020, 2023),
                'curator_id': random.choice(teachers)['teacher_id'] if teachers else None
            }
            groups.append(group)
        
        query = """
        INSERT INTO Groups (group_name, department_id, creation_year, curator_id)
        VALUES (%(group_name)s, %(department_id)s, %(creation_year)s, %(curator_id)s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Groups (group_name, department_id, creation_year, curator_id)
        VALUES (?, ?, ?, ?)
        """
        
        for group in groups:
            if self.db.db_type == 'postgresql':
                self.db.execute_query(query, group)
            else:
                self.db.execute_query(query, (
                    group['group_name'], group['department_id'], 
                    group['creation_year'], group['curator_id']
                ))
    
    def generate_students(self, count=100):
        groups = self.db.execute_query("SELECT group_id FROM Groups")
        
        students = []
        for _ in range(count):
            student = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'birth_date': fake.date_between(start_date='-25y', end_date='-17y'),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'address': fake.address(),
                'enrollment_date': fake.date_between(start_date='-4y', end_date='today'),
                'group_id': random.choice(groups)['group_id'] if groups else None
            }
            students.append(student)
        
        query = """
        INSERT INTO Students (first_name, last_name, birth_date, email, phone, address, 
                            enrollment_date, group_id)
        VALUES (%(first_name)s, %(last_name)s, %(birth_date)s, %(email)s, %(phone)s, 
                %(address)s, %(enrollment_date)s, %(group_id)s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Students (first_name, last_name, birth_date, email, phone, address, 
                            enrollment_date, group_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        for student in students:
            if self.db.db_type == 'postgresql':
                self.db.execute_query(query, student)
            else:
                self.db.execute_query(query, (
                    student['first_name'], student['last_name'], student['birth_date'],
                    student['email'], student['phone'], student['address'],
                    student['enrollment_date'], student['group_id']
                ))
    
    def generate_courses(self):
        subjects = self.db.execute_query("SELECT subject_id FROM Subjects")
        groups = self.db.execute_query("SELECT group_id FROM Groups")
        teachers = self.db.execute_query("SELECT teacher_id FROM Teachers")
        
        courses = []
        for group in groups:
            for subject in random.sample(subjects, min(5, len(subjects))):
                course = {
                    'subject_id': subject['subject_id'],
                    'group_id': group['group_id'],
                    'teacher_id': random.choice(teachers)['teacher_id'] if teachers else None,
                    'semester': random.randint(1, 8),
                    'academic_year': f"{random.randint(2022, 2024)}/{random.randint(2023, 2025)}"
                }
                courses.append(course)
        
        query = """
        INSERT INTO Courses (subject_id, group_id, teacher_id, semester, academic_year)
        VALUES (%(subject_id)s, %(group_id)s, %(teacher_id)s, %(semester)s, %(academic_year)s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Courses (subject_id, group_id, teacher_id, semester, academic_year)
        VALUES (?, ?, ?, ?, ?)
        """
        
        for course in courses:
            try:
                if self.db.db_type == 'postgresql':
                    self.db.execute_query(query, course)
                else:
                    self.db.execute_query(query, (
                        course['subject_id'], course['group_id'], course['teacher_id'],
                        course['semester'], course['academic_year']
                    ))
            except:
                pass  # Игнорируем дубликаты
    
    def generate_grades(self, count=500):
        students = self.db.execute_query("SELECT student_id FROM Students")
        courses = self.db.execute_query("SELECT course_id FROM Courses")
        
        grade_types = ['exam', 'test', 'lab', 'homework']
        
        for _ in range(count):
            grade = {
                'student_id': random.choice(students)['student_id'] if students else None,
                'course_id': random.choice(courses)['course_id'] if courses else None,
                'grade_value': random.choices([2, 3, 4, 5], weights=[5, 20, 45, 30])[0],
                'grade_date': fake.date_between(start_date='-1y', end_date='today'),
                'grade_type': random.choice(grade_types)
            }
            
            query = """
            INSERT INTO Grades (student_id, course_id, grade_value, grade_date, grade_type)
            VALUES (%(student_id)s, %(course_id)s, %(grade_value)s, %(grade_date)s, %(grade_type)s)
            """ if self.db.db_type == 'postgresql' else """
            INSERT INTO Grades (student_id, course_id, grade_value, grade_date, grade_type)
            VALUES (?, ?, ?, ?, ?)
            """
            
            try:
                if self.db.db_type == 'postgresql':
                    self.db.execute_query(query, grade)
                else:
                    self.db.execute_query(query, (
                        grade['student_id'], grade['course_id'], grade['grade_value'],
                        grade['grade_date'], grade['grade_type']
                    ))
            except:
                pass  # Игнорируем дубликаты
    
    def generate_attendance(self, count=1000):
        students = self.db.execute_query("SELECT student_id FROM Students")
        courses = self.db.execute_query("SELECT course_id FROM Courses")
        
        for _ in range(count):
            attendance = {
                'student_id': random.choice(students)['student_id'] if students else None,
                'course_id': random.choice(courses)['course_id'] if courses else None,
                'attendance_date': fake.date_between(start_date='-6m', end_date='today'),
                'is_present': random.choices([True, False], weights=[80, 20])[0]
            }
            
            query = """
            INSERT INTO Attendance (student_id, course_id, attendance_date, is_present)
            VALUES (%(student_id)s, %(course_id)s, %(attendance_date)s, %(is_present)s)
            """ if self.db.db_type == 'postgresql' else """
            INSERT INTO Attendance (student_id, course_id, attendance_date, is_present)
            VALUES (?, ?, ?, ?)
            """
            
            try:
                if self.db.db_type == 'postgresql':
                    self.db.execute_query(query, attendance)
                else:
                    self.db.execute_query(query, (
                        attendance['student_id'], attendance['course_id'],
                        attendance['attendance_date'], 1 if attendance['is_present'] else 0
                    ))
            except:
                pass  # Игнорируем дубликаты
    
    def generate_all_data(self):
        print("Генерация данных...")
        self.generate_departments()
        print("Факультеты созданы")
        self.generate_teachers()
        print("Преподаватели созданы")
        self.generate_subjects()
        print("Предметы созданы")
        self.generate_groups()
        print("Группы созданы")
        self.generate_students()
        print("Студенты созданы")
        self.generate_courses()
        print("Курсы созданы")
        self.generate_grades()
        print("Оценки созданы")
        self.generate_attendance()
        print("Посещаемость создана")
        print("Все данные успешно сгенерированы!")
