import pytest
import tempfile
import os
from database import DatabaseManager
from data_generator import DataGenerator
from queries.basic_queries import BasicQueries
from queries.advanced_queries import AdvancedQueries

@pytest.fixture
def sqlite_db():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    db = DatabaseManager('sqlite')
    db.connection = db._connect_sqlite()
    
    # Создаем схему
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'sqlite_schema.sql')
    db.execute_script(schema_path)
    
    yield db
    
    db.disconnect()
    os.unlink(db_path)

@pytest.fixture
def populated_db(sqlite_db):
    generator = DataGenerator(sqlite_db)
    generator.generate_all_data()
    return sqlite_db

@pytest.fixture
def basic_queries(populated_db):
    return BasicQueries(populated_db)

@pytest.fixture
def advanced_queries(populated_db):
    return AdvancedQueries(populated_db)

class TestDatabaseManager:
    def test_connection(self, sqlite_db):
        assert sqlite_db.connection is not None
    
    def test_execute_query(self, sqlite_db):
        result = sqlite_db.execute_query("SELECT COUNT(*) as count FROM Students")
        assert len(result) == 1
        assert result[0]['count'] >= 0

class TestDataGenerator:
    def test_generate_departments(self, sqlite_db):
        generator = DataGenerator(sqlite_db)
        generator.generate_departments(3)
        
        result = sqlite_db.execute_query("SELECT COUNT(*) as count FROM Departments")
        assert result[0]['count'] == 3
    
    def test_generate_teachers(self, sqlite_db):
        generator = DataGenerator(sqlite_db)
        generator.generate_departments(1)
        generator.generate_teachers(5)
        
        result = sqlite_db.execute_query("SELECT COUNT(*) as count FROM Teachers")
        assert result[0]['count'] == 5
    
    def test_generate_students(self, sqlite_db):
        generator = DataGenerator(sqlite_db)
        generator.generate_departments(1)
        generator.generate_groups(1)
        generator.generate_students(10)
        
        result = sqlite_db.execute_query("SELECT COUNT(*) as count FROM Students")
        assert result[0]['count'] == 10

class TestBasicQueries:
    def test_get_all_students(self, basic_queries):
        students = basic_queries.get_all_students()
        assert len(students) > 0
        assert 'first_name' in students[0]
        assert 'last_name' in students[0]
    
    def test_get_all_teachers(self, basic_queries):
        teachers = basic_queries.get_all_teachers()
        assert len(teachers) > 0
        assert 'first_name' in teachers[0]
        assert 'position' in teachers[0]
    
    def test_add_student(self, basic_queries):
        result = basic_queries.add_student(
            first_name="Тест",
            last_name="Студент",
            email="test@student.com",
            birth_date="2000-01-01"
        )
        assert result is True
    
    def test_update_student(self, basic_queries):
        students = basic_queries.db.execute_query("SELECT student_id FROM Students LIMIT 1")
        if students:
            student_id = students[0]['student_id']
            result = basic_queries.update_student(student_id, email="updated@email.com")
            assert result is True
    
    def test_search_students(self, basic_queries):
        students = basic_queries.search_students("Тест")
        assert isinstance(students, list)
    
    def test_get_department_statistics(self, basic_queries):
        stats = basic_queries.get_department_statistics()
        assert len(stats) > 0
        assert 'department_name' in stats[0]
        assert 'student_count' in stats[0]

class TestAdvancedQueries:
    def test_get_top_students_by_avg_grade(self, advanced_queries):
        top_students = advanced_queries.get_top_students_by_avg_grade(5)
        assert len(top_students) <= 5
        if top_students:
            assert 'avg_grade' in top_students[0]
    
    def test_get_grade_distribution_by_subject(self, advanced_queries):
        distribution = advanced_queries.get_grade_distribution_by_subject()
        assert len(distribution) > 0
        if distribution:
            assert 'subject_name' in distribution[0]
            assert 'avg_grade' in distribution[0]
    
    def test_get_attendance_analysis(self, advanced_queries):
        attendance = advanced_queries.get_attendance_analysis()
        assert isinstance(attendance, list)
    
    def test_get_teacher_performance_analysis(self, advanced_queries):
        performance = advanced_queries.get_teacher_performance_analysis()
        assert len(performance) > 0
        if performance:
            assert 'avg_grade_given' in performance[0]
    
    def test_get_group_performance_comparison(self, advanced_queries):
        comparison = advanced_queries.get_group_performance_comparison()
        assert len(comparison) > 0
        if comparison:
            assert 'group_name' in comparison[0]
            assert 'avg_grade' in comparison[0]

class TestIntegration:
    def test_full_workflow(self, sqlite_db):
        generator = DataGenerator(sqlite_db)
        generator.generate_all_data()
        
        basic = BasicQueries(sqlite_db)
        advanced = AdvancedQueries(sqlite_db)
        
        students = basic.get_all_students()
        assert len(students) > 0
        
        if students:
            student_id = students[0]['student_id']
            grades = basic.get_student_grades(student_id)
            assert isinstance(grades, list)
        
        top_students = advanced.get_top_students_by_avg_grade(3)
        assert len(top_students) <= 3
        
        dept_stats = basic.get_department_statistics()
        assert len(dept_stats) > 0
