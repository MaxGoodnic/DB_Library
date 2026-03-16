from database import DatabaseManager
from typing import List, Dict, Any

class BasicQueries:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        """Получить всех студентов"""
        query = """
        SELECT s.student_id, s.first_name, s.last_name, s.email, s.birth_date,
               g.group_name, d.department_name
        FROM Students s
        LEFT JOIN Groups g ON s.group_id = g.group_id
        LEFT JOIN Departments d ON g.department_id = d.department_id
        ORDER BY s.last_name, s.first_name
        """
        return self.db.execute_query(query)
    
    def get_all_teachers(self) -> List[Dict[str, Any]]:
        """Получить всех преподавателей"""
        query = """
        SELECT t.teacher_id, t.first_name, t.last_name, t.email, t.position,
               t.salary, d.department_name
        FROM Teachers t
        LEFT JOIN Departments d ON t.department_id = d.department_id
        ORDER BY t.last_name, t.first_name
        """
        return self.db.execute_query(query)
    
    def get_student_grades(self, student_id: int) -> List[Dict[str, Any]]:
        """Получить оценки студента"""
        query = """
        SELECT g.grade_value, g.grade_date, g.grade_type,
               sub.subject_name, t.first_name || ' ' || t.last_name as teacher_name
        FROM Grades g
        JOIN Courses c ON g.course_id = c.course_id
        JOIN Subjects sub ON c.subject_id = sub.subject_id
        JOIN Teachers t ON c.teacher_id = t.teacher_id
        WHERE g.student_id = %s
        ORDER BY g.grade_date DESC
        """ if self.db.db_type == 'postgresql' else """
        SELECT g.grade_value, g.grade_date, g.grade_type,
               sub.subject_name, t.first_name || ' ' || t.last_name as teacher_name
        FROM Grades g
        JOIN Courses c ON g.course_id = c.course_id
        JOIN Subjects sub ON c.subject_id = sub.subject_id
        JOIN Teachers t ON c.teacher_id = t.teacher_id
        WHERE g.student_id = ?
        ORDER BY g.grade_date DESC
        """
        
        return self.db.execute_query(query, (student_id,))
    
    def get_teacher_courses(self, teacher_id: int) -> List[Dict[str, Any]]:
        """Получить курсы преподавателя"""
        query = """
        SELECT c.course_id, sub.subject_name, g.group_name,
               c.semester, c.academic_year
        FROM Courses c
        JOIN Subjects sub ON c.subject_id = sub.subject_id
        JOIN Groups g ON c.group_id = g.group_id
        WHERE c.teacher_id = %s
        ORDER BY c.academic_year, c.semester
        """ if self.db.db_type == 'postgresql' else """
        SELECT c.course_id, sub.subject_name, g.group_name,
               c.semester, c.academic_year
        FROM Courses c
        JOIN Subjects sub ON c.subject_id = sub.subject_id
        JOIN Groups g ON c.group_id = g.group_id
        WHERE c.teacher_id = ?
        ORDER BY c.academic_year, c.semester
        """
        
        return self.db.execute_query(query, (teacher_id,))
    
    def add_student(self, first_name: str, last_name: str, email: str, 
                   birth_date: str, group_id: int = None) -> bool:
        """Добавить нового студента"""
        query = """
        INSERT INTO Students (first_name, last_name, email, birth_date, group_id)
        VALUES (%s, %s, %s, %s, %s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Students (first_name, last_name, email, birth_date, group_id)
        VALUES (?, ?, ?, ?, ?)
        """
        
        result = self.db.execute_query(query, (first_name, last_name, email, birth_date, group_id))
        return len(result) > 0
    
    def update_student(self, student_id: int, **kwargs) -> bool:
        """Обновить данные студента"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{key} = %s" if self.db.db_type == 'postgresql' else f"{key} = ?" 
                               for key in kwargs.keys()])
        values = list(kwargs.values()) + [student_id]
        
        query = f"""
        UPDATE Students 
        SET {set_clause}
        WHERE student_id = %s
        """ if self.db.db_type == 'postgresql' else f"""
        UPDATE Students 
        SET {set_clause}
        WHERE student_id = ?
        """
        
        result = self.db.execute_query(query, tuple(values))
        return len(result) > 0
    
    def delete_student(self, student_id: int) -> bool:
        """Удалить студента"""
        query = "DELETE FROM Students WHERE student_id = %s" if self.db.db_type == 'postgresql' else "DELETE FROM Students WHERE student_id = ?"
        result = self.db.execute_query(query, (student_id,))
        return len(result) > 0
    
    def add_grade(self, student_id: int, course_id: int, grade_value: int, 
                 grade_date: str, grade_type: str) -> bool:
        """Добавить оценку"""
        query = """
        INSERT INTO Grades (student_id, course_id, grade_value, grade_date, grade_type)
        VALUES (%s, %s, %s, %s, %s)
        """ if self.db.db_type == 'postgresql' else """
        INSERT INTO Grades (student_id, course_id, grade_value, grade_date, grade_type)
        VALUES (?, ?, ?, ?, ?)
        """
        
        result = self.db.execute_query(query, (student_id, course_id, grade_value, grade_date, grade_type))
        return len(result) > 0
    
    def get_department_statistics(self) -> List[Dict[str, Any]]:
        """Получить статистику по факультетам"""
        query = """
        SELECT d.department_name, 
               COUNT(DISTINCT t.teacher_id) as teacher_count,
               COUNT(DISTINCT g.group_id) as group_count,
               COUNT(DISTINCT s.student_id) as student_count
        FROM Departments d
        LEFT JOIN Teachers t ON d.department_id = t.department_id
        LEFT JOIN Groups g ON d.department_id = g.department_id
        LEFT JOIN Students s ON g.group_id = s.group_id
        GROUP BY d.department_id, d.department_name
        ORDER BY student_count DESC
        """
        return self.db.execute_query(query)
    
    def get_subject_statistics(self) -> List[Dict[str, Any]]:
        """Получить статистику по предметам"""
        query = """
        SELECT sub.subject_name,
               COUNT(DISTINCT c.course_id) as course_count,
               COUNT(DISTINCT g.grade_id) as grade_count,
               AVG(g.grade_value) as avg_grade
        FROM Subjects sub
        LEFT JOIN Courses c ON sub.subject_id = c.subject_id
        LEFT JOIN Grades g ON c.course_id = g.course_id
        GROUP BY sub.subject_id, sub.subject_name
        ORDER BY avg_grade DESC NULLS LAST
        """
        return self.db.execute_query(query)
    
    def search_students(self, search_term: str) -> List[Dict[str, Any]]:
        """Поиск студентов по имени или фамилии"""
        query = """
        SELECT s.student_id, s.first_name, s.last_name, s.email,
               g.group_name, d.department_name
        FROM Students s
        LEFT JOIN Groups g ON s.group_id = g.group_id
        LEFT JOIN Departments d ON g.department_id = d.department_id
        WHERE s.first_name ILIKE %s OR s.last_name ILIKE %s
        ORDER BY s.last_name, s.first_name
        """ if self.db.db_type == 'postgresql' else """
        SELECT s.student_id, s.first_name, s.last_name, s.email,
               g.group_name, d.department_name
        FROM Students s
        LEFT JOIN Groups g ON s.group_id = g.group_id
        LEFT JOIN Departments d ON g.department_id = d.department_id
        WHERE s.first_name LIKE ? OR s.last_name LIKE ?
        ORDER BY s.last_name, s.first_name
        """
        
        search_pattern = f"%{search_term}%"
        return self.db.execute_query(query, (search_pattern, search_pattern))
