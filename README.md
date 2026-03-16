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

