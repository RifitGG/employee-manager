# dialogs.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QDate

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника" if employee_data is None else "Редактировать сотрудника")
        self.resize(400, 300)
        self.employee_data = employee_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поля для ввода данных
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.dob_edit = QDateEdit(calendarPopup=True)
        self.dob_edit.setDisplayFormat("yyyy-MM-dd")
        self.dob_edit.setDate(QDate.currentDate())
        self.position_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.start_date_edit = QDateEdit(calendarPopup=True)
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_date_edit.setDate(QDate.currentDate())

        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.first_name_edit)
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.last_name_edit)
        layout.addWidget(QLabel("Дата рождения:"))
        layout.addWidget(self.dob_edit)
        layout.addWidget(QLabel("Должность:"))
        layout.addWidget(self.position_edit)
        layout.addWidget(QLabel("Контактный телефон:"))
        layout.addWidget(self.phone_edit)
        layout.addWidget(QLabel("Электронная почта:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Дата начала работы:"))
        layout.addWidget(self.start_date_edit)

        # Кнопки "Сохранить" и "Отмена"
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Если данные переданы – заполняем поля
        if self.employee_data:
            self.first_name_edit.setText(self.employee_data['first_name'])
            self.last_name_edit.setText(self.employee_data['last_name'])
            dob = QDate.fromString(self.employee_data['date_of_birth'], "yyyy-MM-dd")
            if dob.isValid():
                self.dob_edit.setDate(dob)
            self.position_edit.setText(self.employee_data['position'])
            self.phone_edit.setText(self.employee_data['phone'])
            self.email_edit.setText(self.employee_data['email'])
            start_date = QDate.fromString(self.employee_data['start_date'], "yyyy-MM-dd")
            if start_date.isValid():
                self.start_date_edit.setDate(start_date)

    def get_data(self):
        data = {
            'first_name': self.first_name_edit.text(),
            'last_name': self.last_name_edit.text(),
            'date_of_birth': self.dob_edit.date().toString("yyyy-MM-dd"),
            'position': self.position_edit.text(),
            'phone': self.phone_edit.text(),
            'email': self.email_edit.text(),
            'start_date': self.start_date_edit.date().toString("yyyy-MM-dd")
        }
        return data

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Документация")
        self.resize(600, 400)
        layout = QVBoxLayout()
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText(
            "Инструкция по использованию приложения «Менеджер по работе с сотрудниками»:\n\n"
            "1. Добавление сотрудника:\n"
            "   - Нажмите кнопку «Добавить сотрудника».\n"
            "   - Заполните форму (Имя, Фамилия, Дата рождения, Должность, Телефон, Email, Дата начала работы).\n"
            "   - Нажмите «Сохранить» для добавления сотрудника.\n\n"
            "2. Редактирование сотрудника:\n"
            "   - Выберите сотрудника из списка и нажмите кнопку «Редактировать сотрудника».\n"
            "   - Измените необходимые поля и нажмите «Сохранить».\n\n"
            "3. Удаление сотрудника:\n"
            "   - Выберите сотрудника и нажмите кнопку «Удалить сотрудника».\n"
            "   - Подтвердите удаление.\n\n"
            "4. Генерация PDF-отчета:\n"
            "   - Нажмите кнопку «Сгенерировать отчет».\n"
            "   - При необходимости введите фильтр по должности (или оставьте пустым для всех сотрудников).\n"
            "   - Выберите место и имя файла для сохранения PDF.\n\n"
            "Отчет содержит основные данные: Имя, Фамилия, Должность, Дата начала работы.\n\n"
            "Приложение использует SQLite для хранения данных, ReportLab для создания PDF и PyQt5 для интерфейса."
        )
        layout.addWidget(help_text)
        self.setLayout(layout)
