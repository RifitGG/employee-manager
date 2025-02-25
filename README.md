# Учёт сотрудников
![img](https://github.com/RifitGG/employee-manager/blob/main/md%20files/interface.png)

 ## ⚠ **ОГЛАВЛЕНИЕ**
>[Основной синтаксис БД](#Основной-синтаксис-БД)
>> - [Функция добавления](#Функция-добавления)
>> - [Функция обновления](#Функция-обновления)
>> - [Функция удаления](#Функция-удаления)
>> - [Функция изъятия ](#Функция-изъятия)

>[Синтаксис Main_Window](#Синтаксис-Main_Window)
>> - [Метод init_ui и Toolbar](#Метод-init_ui-и-Toolbar)
>> - [Toolbar](#Toolbar)
>> - [Кнопки с действиями для управления сотрудниками](#Кнопки-с-действиями-для-управления-сотрудниками)
>> - [Таблица сотрудников](#Таблиц-сотрудников)
>> - [Метод load_data (загрузка данных)](#Метод-load_data-(-загрузка-данных))
>> - [Функция изъятия ](#Функция-изъятия)
>> - [Функция изъятия ](#Функция-изъятия)
>> - [Функция изъятия ](#Функция-изъятия)
>> - [Функция изъятия ](#Функция-изъятия)
>> - [Функция изъятия ](#Функция-изъятия)
>> - [Функция изъятия ](#Функция-изъятия)

 ## ⚠ **ВАЖНО**
 ### Для запуска данного приложения требуется установка зависимостей:
```console
pip install PyQt5 reportlab sqlite3
```
> #### Запуск следует совершать из файлов Main.py или Demo.py (если требуется демонстрация функционала приложения) 

## Основной синтаксис БД:
>Приложение основанно на работе с БД SQLite3, которое можно заменить на более сложную базу данных.
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
>В самой БД реализован базовый функционал добавления, удаления, обновления и изъятие из базы данных сотрудников для дальнейших отчетов 

### Функция добавления:
>реализованна простым методом внесения информации INSERT INTO и последующим комитом в БД
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
### Функция обновления:
>Обновляет позиции в таблице. 
>Команда UPDATE указывает, что нужно изменить существующую запись.
>SET определяет, какие столбцы и какие значения будут обновлены. 
>Знак вопроса ? является плейсхолдером для параметров. 
>WHERE id=? гарантирует, что обновление произойдёт только для записи с конкретным идентификатором (id).
>Метод execute на объекте подключения к базе данных.
>Второй аргумент — кортеж с данными, которые заменят плейсхолдеры в запросе. 
>Порядок элементов в кортеже соответствует порядку плейсхолдеров в SQL-запросе.
>Значения для обновления берутся из словаря data, а идентификатор сотрудника (emp_id) используется для условия WHERE.
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
### Функция удаления:
>Удаляет данные из таблиц. 
>Where id=? гарантирует удаления только определённых записей с корректными индефикатором id.
```python
    def delete_employee(self, emp_id):
        query = "DELETE FROM employees WHERE id=?"
        self.connection.execute(query, (emp_id,))
        self.connection.commit()
```
### Функция изъятия:
>Этот метод извлекает (получает) данные о сотрудниках из таблицы employees в базе данных с возможностью фильтрации по должности. 
>Курсор используется для выполнения SQL-запросов и получения результатов.
>Цикл if else - проверка наличия фильтра Если передан аргумент filter_by_position (то есть не равен None или пустому значению), формируется SQL-запрос с условием WHERE position=?. Здесь знак вопроса является >плейсхолдером для значения фильтра. Если фильтр не задан, выбираются все записи из таблицы employees.
>Метод fetchall() возвращает все строки, полученные в результате выполнения запроса, в виде списка кортежей.
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
## Синтаксис Main_Window:
> #### В данном фрагменте кода создаётся главное окно и основной функционал
> #### Этот класс наследуется от QMainWindow и отвечает за основное окно программы. При инициализации:
> #### 1. Устанавливается заголовок и размер окна.
> #### 2. Создается объект DatabaseManager для работы с базой данных.
> #### 3. Вызывается метод init_ui() для настройки интерфейса.
> #### 4. Загружаются данные сотрудников в таблицу через load_data().
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер по работе с сотрудниками")
        self.resize(800, 600)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()
```
### Метод init_ui и Toolbar
> #### Этот метод создает элементы интерфейса, включая панель инструментов (QToolBar), таблицу (QTableWidget) и кнопки для управления сотрудниками.
```python
def init_ui(self):
    widget = QWidget()
    layout = QVBoxLayout()
```
### Toolbar:
```python
toolbar = QToolBar()
self.addToolBar(toolbar)
```
### Кнопки с действиями для управления сотрудниками: 
> #### Каждое действие связано с соответствующей функцией.
```python
add_action = QAction("Добавить", self)
add_action.triggered.connect(self.add_employee)
toolbar.addAction(add_action)

edit_action = QAction("Редактировать", self)
edit_action.triggered.connect(self.edit_employee)
toolbar.addAction(edit_action)

delete_action = QAction("Удалить", self)
delete_action.triggered.connect(self.delete_employee)
toolbar.addAction(delete_action)

report_action = QAction("Сгенерировать отчет", self)
report_action.triggered.connect(self.generate_report)
toolbar.addAction(report_action)

help_action = QAction("Документация", self)
help_action.triggered.connect(self.show_help)
toolbar.addAction(help_action)
```
### Таблица сотрудников:
> Таблица:
> 1. Содержит 8 столбцов с заголовками.
> 2. Запрещает редактирование (NoEditTriggers).
> 3. Позволяет выбирать только строки (SelectRows).
```python
self.table = QTableWidget()
self.table.setColumnCount(8)
self.table.setHorizontalHeaderLabels([
    "ID", "Имя", "Фамилия", "Дата рождения",
    "Должность", "Телефон", "Email", "Дата начала"
])
self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
```
### Метод load_data (загрузка данных):
> #### Загружает данные сотрудников из базы (fetch_employees()) и заполняет таблицу.
```python
def load_data(self):
    employees = self.db.fetch_employees()
    self.table.setRowCount(0)
    for row_number, employee in enumerate(employees):
        self.table.insertRow(row_number)
        self.table.setItem(row_number, 0, QTableWidgetItem(str(employee["id"])))
        self.table.setItem(row_number, 1, QTableWidgetItem(employee["first_name"]))
        self.table.setItem(row_number, 2, QTableWidgetItem(employee["last_name"]))
        self.table.setItem(row_number, 3, QTableWidgetItem(employee["date_of_birth"]))
        self.table.setItem(row_number, 4, QTableWidgetItem(employee["position"]))
        self.table.setItem(row_number, 5, QTableWidgetItem(employee["phone"]))
        self.table.setItem(row_number, 6, QTableWidgetItem(employee["email"]))
        self.table.setItem(row_number, 7, QTableWidgetItem(employee["start_date"]))

```
### Метод add_emploeey (добавление сотрудников):
> #### Открывает диалоговое окно EmployeeDialog, получает введенные данные, добавляет их в базу (add_employee()) и обновляет таблицу.
```python
def add_employee(self):
    dialog = EmployeeDialog(self)
    if dialog.exec_() == QDialog.Accepted:
        data = dialog.get_data()
        self.db.add_employee(data)
        self.load_data()
```
### Метод edit_employee (редактирование сотрудников):
```python
def edit_employee(self):
    selected_items = self.table.selectedItems()
    if not selected_items:
        QMessageBox.warning(self, "Выберите сотрудника", "Пожалуйста, выберите сотрудника для редактирования.")
        return
```
> #### Проверяет, выбран ли сотрудник. Если нет, показывает предупреждение.
```python
row = selected_items[0].row()
emp_id = int(self.table.item(row, 0).text())
employee = {
    'first_name': self.table.item(row, 1).text(),
    'last_name': self.table.item(row, 2).text(),
    'date_of_birth': self.table.item(row, 3).text(),
    'position': self.table.item(row, 4).text(),
    'phone': self.table.item(row, 5).text(),
    'email': self.table.item(row, 6).text(),
    'start_date': self.table.item(row, 7).text(),
}
```
> #### Получает данные выбранного сотрудника.
```python
dialog = EmployeeDialog(self, employee)
if dialog.exec_() == QDialog.Accepted:
    new_data = dialog.get_data()
    self.db.update_employee(emp_id, new_data)
    self.load_data()
```
> #### Открывает EmployeeDialog, получает обновленные данные и обновляет их в базе.
### Метод delete_emloyee (удаления сотрудников):
```python
def delete_employee(self):
    selected_items = self.table.selectedItems()
    if not selected_items:
        QMessageBox.warning(self, "Выберите сотрудника", "Пожалуйста, выберите сотрудника для удаления.")
        return
```
> #### Проверяет, выбран ли сотрудник.
```python
row = selected_items[0].row()
emp_id = int(self.table.item(row, 0).text())
confirm = QMessageBox.question(
    self, "Подтверждение",
    "Вы действительно хотите удалить выбранного сотрудника?",
    QMessageBox.Yes | QMessageBox.No
)
if confirm == QMessageBox.Yes:
    self.db.delete_employee(emp_id)
    self.load_data()
```
> #### Запрашивает подтверждение удаления, затем удаляет сотрудника из базы.
### generate_report (генерация отчёта):
```python
def generate_report(self):
    filter_dialog = QDialog(self)
    filter_dialog.setWindowTitle("Генерация отчета")
    layout = QVBoxLayout()
```
> #### Создает диалоговое окно для выбора параметров отчета.
```python
filter_layout = QHBoxLayout()
filter_layout.addWidget(QLabel("Фильтр по должности (оставьте пустым для всех):"))
position_filter_edit = QLineEdit()
filter_layout.addWidget(position_filter_edit)
layout.addLayout(filter_layout)
```
> #### Позволяет фильтровать отчет по должности.
```python
file_layout = QHBoxLayout()
file_layout.addWidget(QLabel("Сохранить как:"))
file_edit = QLineEdit()
file_layout.addWidget(file_edit)
browse_button = QPushButton("Обзор")
file_layout.addWidget(browse_button)
layout.addLayout(file_layout)

browse_button.clicked.connect(lambda: file_edit.setText(
    QFileDialog.getSaveFileName(self, "Сохранить отчет", "", "PDF files (*.pdf)")[0]
))
```
> #### Позволяет выбрать имя и место сохранения отчета.
```python
if filter_dialog.exec_() == QDialog.Accepted:
    position_filter = position_filter_edit.text().strip()
    filename = file_edit.text().strip()
    if not filename:
        QMessageBox.warning(self, "Ошибка", "Не указано имя файла для сохранения отчета.")
        return
    self.create_pdf_report(filename, position_filter if position_filter != "" else None)
    QMessageBox.information(self, "Отчет сохранен", f"Отчет успешно сохранен в {filename}")
```
### Метод create_pdf_report (создание PDF отчёта):
> #### Генерирует PDF-файл с данными сотрудников.
```python
def create_pdf_report(self, filename, position_filter=None):
    employees = self.db.fetch_employees(position_filter)
    c = canvas.Canvas(filename, pagesize=letter)
```
### Метод show_help (открытие справки):
```python
def show_help(self):
    help_dialog = HelpDialog(self)
    help_dialog.exec_()
```


















