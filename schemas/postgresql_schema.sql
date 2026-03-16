-- PostgreSQL схема для университетской базы данных

-- Таблица студентов
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    enrollment_date DATE NOT NULL,
    group_id INTEGER REFERENCES Groups(group_id)
);

-- Таблица групп
CREATE TABLE Groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(20) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES Departments(department_id),
    creation_year INTEGER NOT NULL,
    curator_id INTEGER REFERENCES Teachers(teacher_id)
);

-- Таблица факультетов/департаментов
CREATE TABLE Departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    dean_id INTEGER REFERENCES Teachers(teacher_id),
    building VARCHAR(50),
    budget DECIMAL(15,2)
);

-- Таблица преподавателей
CREATE TABLE Teachers (
    teacher_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    hire_date DATE NOT NULL,
    department_id INTEGER REFERENCES Departments(department_id),
    position VARCHAR(50) NOT NULL,
    salary DECIMAL(10,2)
);

-- Таблица предметов
CREATE TABLE Subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    credits INTEGER NOT NULL CHECK (credits > 0),
    department_id INTEGER REFERENCES Departments(department_id)
);

-- Таблица курсов (связь предметов и групп)
CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES Subjects(subject_id),
    group_id INTEGER REFERENCES Groups(group_id),
    teacher_id INTEGER REFERENCES Teachers(teacher_id),
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    academic_year VARCHAR(9) NOT NULL, -- Формат: 2023/2024
    UNIQUE(subject_id, group_id, semester, academic_year)
);

-- Таблица оценок
CREATE TABLE Grades (
    grade_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES Students(student_id),
    course_id INTEGER REFERENCES Courses(course_id),
    grade_value INTEGER NOT NULL CHECK (grade_value BETWEEN 2 AND 5),
    grade_date DATE NOT NULL,
    grade_type VARCHAR(20) NOT NULL CHECK (grade_type IN ('exam', 'test', 'lab', 'homework')),
    UNIQUE(student_id, course_id, grade_date, grade_type)
);

-- Таблица посещаемости
CREATE TABLE Attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES Students(student_id),
    course_id INTEGER REFERENCES Courses(course_id),
    attendance_date DATE NOT NULL,
    is_present BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE(student_id, course_id, attendance_date)
);

-- Индексы для оптимизации запросов
CREATE INDEX idx_students_group ON Students(group_id);
CREATE INDEX idx_teachers_department ON Teachers(department_id);
CREATE INDEX idx_courses_subject ON Courses(subject_id);
CREATE INDEX idx_courses_group ON Courses(group_id);
CREATE INDEX idx_courses_teacher ON Courses(teacher_id);
CREATE INDEX idx_grades_student ON Grades(student_id);
CREATE INDEX idx_grades_course ON Grades(course_id);
CREATE INDEX idx_attendance_student ON Attendance(student_id);
CREATE INDEX idx_attendance_course ON Attendance(course_id);
