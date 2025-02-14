# Учёт сотрудников
![img](https://github.com/RifitGG/employee-manager/blob/main/md%20files/interface.png)


>[!Ссылки для работы с документацией]
+
> [!ВАЖНО]
> ## Для запуска данного приложения требуется установка зависимостей pip install PyQt5 reportlab sqlite3
pip install PyQt5 reportlab sqlite3
>Приложение основанно на работе с БД SQLite3, которое можно заменить на более сложную базу данных.
> [!ВАЖНО]
## Основной синтаксис БД
```python
class DatabaseManager:
    def __init__(self, db_filename="employees.db"):
        self.connection = sqlite3.connect(db_filename)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT,
            position TEXT,
            phone TEXT,
            email TEXT,
            start_date TEXT
        )
        """
        self.connection.execute(query)
        self.connection.commit()
```
### В самой БД реализован базовый функционал добавления, удаления, обновления и изъятие из базы данных сотрудников для изъятия из бд для дальнейших отчетов 
## Функция добавления:
реализованна простым методом внесения информации INSERT INTO и последующим комитом в БД
```python
    def add_employee(self, data):
        query = """
            INSERT INTO employees
            (first_name, last_name, date_of_birth, position, phone, email, start_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.connection.execute(query, (
            data['first_name'],
            data['last_name'],
            data['date_of_birth'],
            data['position'],
            data['phone'],
            data['email'],
            data['start_date']
        ))
        self.connection.commit()
```

