#!/usr/bin/env python3
"""
Главный файл для демонстрации работы с университетской базой данных
"""

import sys
import os
from database import DatabaseManager
from data_generator import DataGenerator
from queries.basic_queries import BasicQueries
from queries.advanced_queries import AdvancedQueries

def print_separator(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def demo_basic_queries(basic_queries):
    print_separator("ДЕМО: БАЗОВЫЕ ЗАПРОСЫ")
    
    print("\n1. Все студенты:")
    students = basic_queries.get_all_students()
    for i, student in enumerate(students[:5]):
        print(f"   {i+1}. {student['last_name']} {student['first_name']} - {student['group_name']}")
    print(f"   ... всего {len(students)} студентов")
    
    print("\n2. Все преподаватели:")
    teachers = basic_queries.get_all_teachers()
    for i, teacher in enumerate(teachers[:3]):
        print(f"   {i+1}. {teacher['last_name']} {teacher['first_name']} - {teacher['position']}")
    print(f"   ... всего {len(teachers)} преподавателей")
    
    print("\n3. Статистика по факультетам:")
    dept_stats = basic_queries.get_department_statistics()
    for stat in dept_stats:
        print(f"   {stat['department_name']}: {stat['student_count']} студентов, {stat['teacher_count']} преподавателей")
    
    print("\n4. Статистика по предметам:")
    subject_stats = basic_queries.get_subject_statistics()
    for stat in subject_stats[:5]:
        avg_grade = stat['avg_grade'] or 'N/A'
        print(f"   {stat['subject_name']}: средний балл {avg_grade}")

def demo_advanced_queries(advanced_queries):
    print_separator("ДЕМО: ПРОДВИНУТЫЕ ЗАПРОСЫ С ОКОННЫМИ ФУНКЦИЯМИ")
    
    print("\n1. Топ студентов по среднему баллу:")
    top_students = advanced_queries.get_top_students_by_avg_grade(5)
    for i, student in enumerate(top_students):
        print(f"   {i+1}. {student['last_name']} {student['first_name']} - средний балл: {student['avg_grade']:.2f}")
    
    print("\n2. Распределение оценок по предметам:")
    grade_dist = advanced_queries.get_grade_distribution_by_subject()
    for dist in grade_dist[:3]:
        print(f"   {dist['subject_name']}: 5-{dist['grade_5_count']}, 4-{dist['grade_4_count']}, 3-{dist['grade_3_count']}, 2-{dist['grade_2_count']}")
    
    print("\n3. Анализ посещаемости:")
    attendance = advanced_queries.get_attendance_analysis()
    if attendance:
        best_attendance = attendance[0]
        print(f"   Лучшая посещаемость: {best_attendance['first_name']} {best_attendance['last_name']} - {best_attendance['attendance_percentage']}%")
    
    print("\n4. Анализ эффективности преподавателей:")
    teacher_perf = advanced_queries.get_teacher_performance_analysis()
    for i, teacher in enumerate(teacher_perf[:3]):
        print(f"   {i+1}. {teacher['last_name']} {teacher['first_name']} - средний балл: {teacher['avg_grade_given']:.2f}")
    
    print("\n5. Сравнение производительности групп:")
    group_comp = advanced_queries.get_group_performance_comparison()
    for i, group in enumerate(group_comp[:3]):
        print(f"   {i+1}. {group['group_name']} - средний балл: {group['avg_grade']:.2f}")

def demo_crud_operations(basic_queries):
    print_separator("ДЕМО: CRUD ОПЕРАЦИИ")
    
    print("\n1. Добавление нового студента:")
    success = basic_queries.add_student(
        first_name="Иван",
        last_name="Петров",
        email="ivan.petrov@university.edu",
        birth_date="2000-05-15"
    )
    print(f"   Студент добавлен: {success}")
    
    print("\n2. Поиск студентов по имени 'Иван':")
    ivan_students = basic_queries.search_students("Иван")
    for student in ivan_students:
        print(f"   Найден: {student['last_name']} {student['first_name']} - {student['email']}")
    
    if ivan_students:
        student_id = ivan_students[0]['student_id']
        print(f"\n3. Обновление email студента (ID: {student_id}):")
        success = basic_queries.update_student(student_id, email="ivan.petrov@newemail.edu")
        print(f"   Email обновлен: {success}")
        
        print(f"\n4. Удаление студента (ID: {student_id}):")
        success = basic_queries.delete_student(student_id)
        print(f"   Студент удален: {success}")

def main():
    print("УНИВЕРСИТЕТСКАЯ БАЗА ДАННЫХ - ДЕМО")
    
    # Выбор типа базы данных
    if len(sys.argv) > 1 and sys.argv[1] == 'postgresql':
        db_type = 'postgresql'
        print("Используется PostgreSQL")
    else:
        db_type = 'sqlite'
        print("Используется SQLite")
    
    # Инициализация базы данных
    db = DatabaseManager(db_type)
    
    try:
        # Подключение
        if not db.connect():
            print("Ошибка подключения к базе данных")
            return
        
        print("\nПодключение к базе данных успешно установлено")
        
        # Создание схемы
        schema_file = f"schemas/{db_type}_schema.sql"
        if os.path.exists(schema_file):
            print(f"\nСоздание схемы из файла: {schema_file}")
            db.execute_script(schema_file)
        else:
            print(f"Файл схемы не найден: {schema_file}")
            return
        
        # Генерация тестовых данных
        print("\nГенерация тестовых данных...")
        generator = DataGenerator(db)
        generator.generate_all_data()
        
        # Инициализация запросов
        basic_queries = BasicQueries(db)
        advanced_queries = AdvancedQueries(db)
        
        # Демонстрация
        demo_basic_queries(basic_queries)
        demo_advanced_queries(advanced_queries)
        demo_crud_operations(basic_queries)
        
        print_separator("ДЕМО ЗАВЕРШЕНО")
        print("Все функции успешно продемонстрированы!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.disconnect()
        print("\nПодключение к базе данных закрыто")

if __name__ == "__main__":
    main()
