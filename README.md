# Учёт сотрудников
![img](https://github.com/RifitGG/employee-manager/blob/main/md%20files/interface.png)


>[!Ссылки для работы с документацией]
+ [Основной синтаксис БД](#Основной синтаксис БД)
> [!ВАЖНО]
> ## Для запуска данного приложения требуется установка зависимостей pip install PyQt5 reportlab sqlite3
pip install PyQt5 reportlab sqlite3
>Приложение основанно на работе с БД SQLite3, которое можно заменить на более сложную базу данных.
> [!ВАЖНО]
>## Основной синтаксис БД
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
## Функция обновления:
Обновляет позиции в таблице. 
Команда UPDATE указывает, что нужно изменить существующую запись.
SET определяет, какие столбцы и какие значения будут обновлены. 
Знак вопроса ? является плейсхолдером для параметров. 
WHERE id=? гарантирует, что обновление произойдёт только для записи с конкретным идентификатором (id).
Метод execute на объекте подключения к базе данных.
Второй аргумент — кортеж с данными, которые заменят плейсхолдеры в запросе. 
Порядок элементов в кортеже соответствует порядку плейсхолдеров в SQL-запросе.
Значения для обновления берутся из словаря data, а идентификатор сотрудника (emp_id) используется для условия WHERE.
```python
 def update_employee(self, emp_id, data):
        query = """
            UPDATE employees
            SET first_name=?, last_name=?, date_of_birth=?, position=?, phone=?, email=?, start_date=?
            WHERE id=?
        """
        self.connection.execute(query, (
            data['first_name'],
            data['last_name'],
            data['date_of_birth'],
            data['position'],
            data['phone'],
            data['email'],
            data['start_date'],
            emp_id
        ))
        self.connection.commit()
```
## Функция удаления:
Удаляет данные из таблиц. 
Where id=? гарантирует удаления только определённых записей с корректными индефикатором id.
```python
    def delete_employee(self, emp_id):
        query = "DELETE FROM employees WHERE id=?"
        self.connection.execute(query, (emp_id,))
        self.connection.commit()
```
## Функция изъятия 
Этот метод извлекает (получает) данные о сотрудниках из таблицы employees в базе данных с возможностью фильтрации по должности. 
Курсор используется для выполнения SQL-запросов и получения результатов.
Цикл if else - проверка наличия фильтра Если передан аргумент filter_by_position (то есть не равен None или пустому значению), формируется SQL-запрос с условием WHERE position=?. Здесь знак вопроса является плейсхолдером для значения фильтра. Если фильтр не задан, выбираются все записи из таблицы employees.
Метод fetchall() возвращает все строки, полученные в результате выполнения запроса, в виде списка кортежей.
```python
    def fetch_employees(self, filter_by_position=None):
        cursor = self.connection.cursor()
        if filter_by_position:
            query = "SELECT * FROM employees WHERE position=?"
            cursor.execute(query, (filter_by_position,))
        else:
            query = "SELECT * FROM employees"
            cursor.execute(query)
        return cursor.fetchall()
```

