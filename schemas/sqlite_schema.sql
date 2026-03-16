-- SQLite схема для университетской базы данных

-- Таблица студентов
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    enrollment_date TEXT NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);

-- Таблица групп
CREATE TABLE Groups (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT UNIQUE NOT NULL,
    department_id INTEGER,
    creation_year INTEGER NOT NULL,
    curator_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (curator_id) REFERENCES Teachers(teacher_id)
);

-- Таблица факультетов/департаментов
CREATE TABLE Departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL,
    dean_id INTEGER,
    building TEXT,
    budget REAL,
    FOREIGN KEY (dean_id) REFERENCES Teachers(teacher_id)
);

-- Таблица преподавателей
CREATE TABLE Teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    hire_date TEXT NOT NULL,
    department_id INTEGER,
    position TEXT NOT NULL,
    salary REAL,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Таблица предметов
CREATE TABLE Subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT UNIQUE NOT NULL,
    description TEXT,
    credits INTEGER NOT NULL CHECK (credits > 0),
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Таблица курсов (связь предметов и групп)
CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    group_id INTEGER,
    teacher_id INTEGER,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    academic_year TEXT NOT NULL, -- Формат: 2023/2024
    UNIQUE(subject_id, group_id, semester, academic_year),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (group_id) REFERENCES Groups(group_id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- Таблица оценок
CREATE TABLE Grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    grade_value INTEGER NOT NULL CHECK (grade_value BETWEEN 2 AND 5),
    grade_date TEXT NOT NULL,
    grade_type TEXT NOT NULL CHECK (grade_type IN ('exam', 'test', 'lab', 'homework')),
    UNIQUE(student_id, course_id, grade_date, grade_type),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Таблица посещаемости
CREATE TABLE Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    attendance_date TEXT NOT NULL,
    is_present INTEGER NOT NULL DEFAULT 1, -- 1 для TRUE, 0 для FALSE
    UNIQUE(student_id, course_id, attendance_date),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
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
