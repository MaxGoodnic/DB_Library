# Университетская база данных

Проект по базам данных, реализующий систему управления университетом с поддержкой PostgreSQL и SQLite.

## Описание проекта

Система представляет собой полноценную базу данных университета со следующими возможностями:
- Управление студентами, преподавателями, группами и факультетами
- Ведение учета успеваемости и посещаемости
- Расписание курсов и предметов
- Продвинутая аналитика с использованием оконных функций
- Генерация тестовых данных
- Комплексное тестирование

## Структура базы данных

### Основные таблицы:
- **Students** - информация о студентах
- **Teachers** - информация о преподавателях  
- **Departments** - факультеты/департаменты
- **Groups** - учебные группы
- **Subjects** - учебные предметы
- **Courses** - связь предметов, групп и преподавателей
- **Grades** - оценки студентов
- **Attendance** - посещаемость занятий

## Установка и настройка

### Требования
- Python 3.8+
- PostgreSQL (опционально)
- Git

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка PostgreSQL (опционально)
1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE university_db;
```
3. Скопируйте `.env.example` в `.env` и настройте параметры подключения:
```bash
cp .env.example .env
```

## Использование

### Запуск с SQLite (по умолчанию)
```bash
python main.py
```

### Запуск с PostgreSQL
```bash
python main.py postgresql
```

### Запуск тестов
```bash
pytest tests/
```

## Примеры использования

### Базовые операции
```python
from database import DatabaseManager
from queries.basic_queries import BasicQueries

# Инициализация
db = DatabaseManager('sqlite')
db.connect()

# Создание запросов
queries = BasicQueries(db)

# Получение всех студентов
students = queries.get_all_students()

# Добавление студента
queries.add_student(
    first_name="Иван",
    last_name="Петров", 
    email="ivan@university.edu",
    birth_date="2000-01-01"
)
```

### Продвинутые запросы с оконными функциями
```python
from queries.advanced_queries import AdvancedQueries

advanced = AdvancedQueries(db)

# Топ студентов по среднему баллу
top_students = advanced.get_top_students_by_avg_grade(10)

# Анализ посещаемости
attendance = advanced.get_attendance_analysis()

# Сравнение групп
group_comparison = advanced.get_group_performance_comparison()
```

## Возможности системы

### Базовые запросы:
- CRUD операции для всех сущностей
- Поиск и фильтрация данных
- Статистические отчеты
- Валидация данных

### Продвинутые функции:
- Оконные функции (ROW_NUMBER, RANK, LAG)
- Аналитические запросы
- Агрегация с группировкой
- Временной анализ данных

### Генерация данных:
- Автоматическая генерация тестовых данных
- Реалистичные данные с использованием Faker
- Настройка объемов генерации

## Структура проекта

```
database_project/
├── main.py                 # Главный файл демонстрации
├── database.py            # Менеджер подключения к БД
├── config.py              # Конфигурация
├── data_generator.py      # Генератор тестовых данных
├── requirements.txt       # Зависимости Python
├── .env.example          # Пример конфигурации
├── schemas/              # SQL схемы
│   ├── postgresql_schema.sql
│   └── sqlite_schema.sql
├── queries/              # Модули запросов
│   ├── basic_queries.py
│   └── advanced_queries.py
└── tests/                # Тесты
    └── test_database.py
```

## Примеры запросов

### Базовые запросы:
```sql
-- Получение всех студентов с группами
SELECT s.first_name, s.last_name, g.group_name 
FROM Students s 
JOIN Groups g ON s.group_id = g.group_id;

-- Статистика по факультетам
SELECT d.department_name, COUNT(s.student_id) as student_count
FROM Departments d
LEFT JOIN Groups g ON d.department_id = g.department_id  
LEFT JOIN Students s ON g.group_id = s.group_id
GROUP BY d.department_name;
```

### Оконные функции:
```sql
-- Рейтинг студентов по среднему баллу
SELECT student_name, avg_grade,
       RANK() OVER (ORDER BY avg_grade DESC) as rank
FROM student_avg_grades;

-- Накопительная сумма оценок
SELECT grade_date, grade_value,
       SUM(grade_value) OVER (ORDER BY grade_date) as running_total
FROM Grades;
```

## Тестирование

Проект включает комплексные тесты:
- Модульные тесты для всех компонентов
- Интеграционные тесты
- Тесты с временными базами данных
- Проверка корректности данных

Запуск тестов:
```bash
pytest -v
```

## Автор

Проект создан в качестве демонстрации работы с базами данных и SQL.

## Лицензия

MIT License
