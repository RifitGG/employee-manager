# db_manager.py
import sqlite3

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

    def delete_employee(self, emp_id):
        query = "DELETE FROM employees WHERE id=?"
        self.connection.execute(query, (emp_id,))
        self.connection.commit()

    def fetch_employees(self, filter_by_position=None):
        cursor = self.connection.cursor()
        if filter_by_position:
            query = "SELECT * FROM employees WHERE position=?"
            cursor.execute(query, (filter_by_position,))
        else:
            query = "SELECT * FROM employees"
            cursor.execute(query)
        return cursor.fetchall()
