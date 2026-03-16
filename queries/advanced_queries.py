from database import DatabaseManager
from typing import List, Dict, Any

class AdvancedQueries:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_top_students_by_avg_grade(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получить топ студентов по среднему баллу с использованием оконных функций"""
        if self.db.db_type == 'postgresql':
            query = """
            WITH student_avg_grades AS (
                SELECT 
                    s.student_id,
                    s.first_name,
                    s.last_name,
                    g.group_name,
                    d.department_name,
                    AVG(gd.grade_value) as avg_grade,
                    COUNT(gd.grade_id) as grade_count,
                    ROW_NUMBER() OVER (ORDER BY AVG(gd.grade_value) DESC) as rank
                FROM Students s
                JOIN Groups g ON s.group_id = g.group_id
                JOIN Departments d ON g.department_id = d.department_id
                JOIN Grades gd ON s.student_id = gd.student_id
                GROUP BY s.student_id, s.first_name, s.last_name, g.group_name, d.department_name
                HAVING COUNT(gd.grade_id) >= 3
            )
            SELECT * FROM student_avg_grades
            ORDER BY rank
            LIMIT %s
            """
        else:
            query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                g.group_name,
                d.department_name,
                AVG(gd.grade_value) as avg_grade,
                COUNT(gd.grade_id) as grade_count
            FROM Students s
            JOIN Groups g ON s.group_id = g.group_id
            JOIN Departments d ON g.department_id = d.department_id
            JOIN Grades gd ON s.student_id = gd.student_id
            GROUP BY s.student_id, s.first_name, s.last_name, g.group_name, d.department_name
            HAVING COUNT(gd.grade_id) >= 3
            ORDER BY avg_grade DESC
            LIMIT ?
            """
        
        return self.db.execute_query(query, (limit,))
    
    def get_grade_distribution_by_subject(self) -> List[Dict[str, Any]]:
        """Получить распределение оценок по предметам"""
        if self.db.db_type == 'postgresql':
            query = """
            SELECT 
                sub.subject_name,
                COUNT(*) FILTER (WHERE gd.grade_value = 5) as grade_5_count,
                COUNT(*) FILTER (WHERE gd.grade_value = 4) as grade_4_count,
                COUNT(*) FILTER (WHERE gd.grade_value = 3) as grade_3_count,
                COUNT(*) FILTER (WHERE gd.grade_value = 2) as grade_2_count,
                COUNT(*) as total_grades,
                ROUND(AVG(gd.grade_value), 2) as avg_grade
            FROM Subjects sub
            JOIN Courses c ON sub.subject_id = c.subject_id
            JOIN Grades gd ON c.course_id = gd.course_id
            GROUP BY sub.subject_id, sub.subject_name
            ORDER BY avg_grade DESC
            """
        else:
            query = """
            SELECT 
                sub.subject_name,
                SUM(CASE WHEN gd.grade_value = 5 THEN 1 ELSE 0 END) as grade_5_count,
                SUM(CASE WHEN gd.grade_value = 4 THEN 1 ELSE 0 END) as grade_4_count,
                SUM(CASE WHEN gd.grade_value = 3 THEN 1 ELSE 0 END) as grade_3_count,
                SUM(CASE WHEN gd.grade_value = 2 THEN 1 ELSE 0 END) as grade_2_count,
                COUNT(*) as total_grades,
                ROUND(AVG(gd.grade_value), 2) as avg_grade
            FROM Subjects sub
            JOIN Courses c ON sub.subject_id = c.subject_id
            JOIN Grades gd ON c.course_id = gd.course_id
            GROUP BY sub.subject_id, sub.subject_name
            ORDER BY avg_grade DESC
            """
        
        return self.db.execute_query(query)
    
    def get_attendance_analysis(self) -> List[Dict[str, Any]]:
        """Анализ посещаемости с оконными функциями"""
        if self.db.db_type == 'postgresql':
            query = """
            WITH attendance_stats AS (
                SELECT 
                    s.student_id,
                    s.first_name,
                    s.last_name,
                    g.group_name,
                    COUNT(*) as total_classes,
                    COUNT(*) FILTER (WHERE a.is_present = true) as attended_classes,
                    ROUND(COUNT(*) FILTER (WHERE a.is_present = true) * 100.0 / COUNT(*), 2) as attendance_percentage,
                    ROW_NUMBER() OVER (PARTITION BY g.group_id ORDER BY COUNT(*) FILTER (WHERE a.is_present = true) * 100.0 / COUNT(*) DESC) as rank_in_group
                FROM Students s
                JOIN Groups g ON s.group_id = g.group_id
                JOIN Attendance a ON s.student_id = a.student_id
                GROUP BY s.student_id, s.first_name, s.last_name, g.group_name
            )
            SELECT * FROM attendance_stats
            ORDER BY attendance_percentage DESC
            """
        else:
            query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                g.group_name,
                COUNT(*) as total_classes,
                SUM(CASE WHEN a.is_present = 1 THEN 1 ELSE 0 END) as attended_classes,
                ROUND(SUM(CASE WHEN a.is_present = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as attendance_percentage
            FROM Students s
            JOIN Groups g ON s.group_id = g.group_id
            JOIN Attendance a ON s.student_id = a.student_id
            GROUP BY s.student_id, s.first_name, s.last_name, g.group_name
            ORDER BY attendance_percentage DESC
            """
        
        return self.db.execute_query(query)
    
    def get_monthly_grade_trends(self) -> List[Dict[str, Any]]:
        """Месячные тренды оценок"""
        if self.db.db_type == 'postgresql':
            query = """
            SELECT 
                TO_CHAR(g.grade_date, 'YYYY-MM') as month,
                COUNT(*) as total_grades,
                AVG(g.grade_value) as avg_grade,
                MIN(g.grade_value) as min_grade,
                MAX(g.grade_value) as max_grade,
                LAG(AVG(g.grade_value)) OVER (ORDER BY TO_CHAR(g.grade_date, 'YYYY-MM')) as prev_month_avg
            FROM Grades g
            WHERE g.grade_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY TO_CHAR(g.grade_date, 'YYYY-MM')
            ORDER BY month
            """
        else:
            query = """
            SELECT 
                strftime('%Y-%m', g.grade_date) as month,
                COUNT(*) as total_grades,
                AVG(g.grade_value) as avg_grade,
                MIN(g.grade_value) as min_grade,
                MAX(g.grade_value) as max_grade
            FROM Grades g
            WHERE g.grade_date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', g.grade_date)
            ORDER BY month
            """
        
        return self.db.execute_query(query)
    
    def get_teacher_performance_analysis(self) -> List[Dict[str, Any]]:
        """Анализ эффективности преподавателей"""
        if self.db.db_type == 'postgresql':
            query = """
            WITH teacher_stats AS (
                SELECT 
                    t.teacher_id,
                    t.first_name,
                    t.last_name,
                    d.department_name,
                    COUNT(DISTINCT c.course_id) as courses_count,
                    COUNT(DISTINCT g.student_id) as students_count,
                    COUNT(g.grade_id) as grades_count,
                    AVG(g.grade_value) as avg_grade_given,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY g.grade_value) as median_grade,
                    ROW_NUMBER() OVER (ORDER BY AVG(g.grade_value) DESC) as performance_rank
                FROM Teachers t
                JOIN Departments d ON t.department_id = d.department_id
                JOIN Courses c ON t.teacher_id = c.teacher_id
                JOIN Grades g ON c.course_id = g.course_id
                GROUP BY t.teacher_id, t.first_name, t.last_name, d.department_name
            )
            SELECT * FROM teacher_stats
            ORDER BY performance_rank
            """
        else:
            query = """
            SELECT 
                t.teacher_id,
                t.first_name,
                t.last_name,
                d.department_name,
                COUNT(DISTINCT c.course_id) as courses_count,
                COUNT(DISTINCT g.student_id) as students_count,
                COUNT(g.grade_id) as grades_count,
                AVG(g.grade_value) as avg_grade_given
            FROM Teachers t
            JOIN Departments d ON t.department_id = d.department_id
            JOIN Courses c ON t.teacher_id = c.teacher_id
            JOIN Grades g ON c.course_id = g.course_id
            GROUP BY t.teacher_id, t.first_name, t.last_name, d.department_name
            ORDER BY avg_grade_given DESC
            """
        
        return self.db.execute_query(query)
    
    def get_group_performance_comparison(self) -> List[Dict[str, Any]]:
        """Сравнение производительности групп"""
        if self.db.db_type == 'postgresql':
            query = """
            SELECT 
                g.group_id,
                g.group_name,
                d.department_name,
                COUNT(DISTINCT s.student_id) as student_count,
                COUNT(gd.grade_id) as total_grades,
                AVG(gd.grade_value) as avg_grade,
                STDDEV(gd.grade_value) as grade_std_dev,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gd.grade_value) as median_grade,
                FIRST_VALUE(s.first_name || ' ' || s.last_name) OVER (
                    PARTITION BY g.group_id 
                    ORDER BY AVG(gd.grade_value) DESC 
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ) as top_student
            FROM Groups g
            JOIN Departments d ON g.department_id = d.department_id
            JOIN Students s ON g.group_id = s.group_id
            JOIN Grades gd ON s.student_id = gd.student_id
            GROUP BY g.group_id, g.group_name, d.department_name
            ORDER BY avg_grade DESC
            """
        else:
            query = """
            SELECT 
                g.group_id,
                g.group_name,
                d.department_name,
                COUNT(DISTINCT s.student_id) as student_count,
                COUNT(gd.grade_id) as total_grades,
                AVG(gd.grade_value) as avg_grade
            FROM Groups g
            JOIN Departments d ON g.department_id = d.department_id
            JOIN Students s ON g.group_id = s.group_id
            JOIN Grades gd ON s.student_id = gd.student_id
            GROUP BY g.group_id, g.group_name, d.department_name
            ORDER BY avg_grade DESC
            """
        
        return self.db.execute_query(query)
    
    def get_running_total_grades(self) -> List[Dict[str, Any]]:
        """Накопительная сумма оценок по времени"""
        if self.db.db_type == 'postgresql':
            query = """
            SELECT 
                grade_date,
                grade_value,
                SUM(grade_value) OVER (ORDER BY grade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total,
                COUNT(*) OVER (ORDER BY grade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_count,
                AVG(grade_value) OVER (ORDER BY grade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_avg
            FROM Grades
            WHERE grade_date >= CURRENT_DATE - INTERVAL '3 months'
            ORDER BY grade_date
            """
        else:
            query = """
            SELECT 
                grade_date,
                grade_value,
                SUM(grade_value) OVER (ORDER BY grade_date) as running_total,
                COUNT(*) OVER (ORDER BY grade_date) as running_count,
                AVG(grade_value) OVER (ORDER BY grade_date) as running_avg
            FROM Grades
            WHERE grade_date >= date('now', '-3 months')
            ORDER BY grade_date
            """
        
        return self.db.execute_query(query)
    
    def get_student_rank_in_subject(self, subject_id: int) -> List[Dict[str, Any]]:
        """Рейтинг студентов по конкретному предмету"""
        if self.db.db_type == 'postgresql':
            query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                g.group_name,
                AVG(gd.grade_value) as avg_grade,
                COUNT(gd.grade_id) as grade_count,
                RANK() OVER (ORDER BY AVG(gd.grade_value) DESC) as subject_rank,
                COUNT(*) OVER () as total_students
            FROM Students s
            JOIN Groups g ON s.group_id = g.group_id
            JOIN Grades gd ON s.student_id = gd.student_id
            JOIN Courses c ON gd.course_id = c.course_id
            WHERE c.subject_id = %s
            GROUP BY s.student_id, s.first_name, s.last_name, g.group_name
            HAVING COUNT(gd.grade_id) >= 2
            ORDER BY subject_rank
            """
        else:
            query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                g.group_name,
                AVG(gd.grade_value) as avg_grade,
                COUNT(gd.grade_id) as grade_count
            FROM Students s
            JOIN Groups g ON s.group_id = g.group_id
            JOIN Grades gd ON s.student_id = gd.student_id
            JOIN Courses c ON gd.course_id = c.course_id
            WHERE c.subject_id = ?
            GROUP BY s.student_id, s.first_name, s.last_name, g.group_name
            HAVING COUNT(gd.grade_id) >= 2
            ORDER BY avg_grade DESC
            """
        
        return self.db.execute_query(query, (subject_id,))
