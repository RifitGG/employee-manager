# main_window.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QToolBar, QAction, QMessageBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog
)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from db_manager import DatabaseManager
from dialogs import EmployeeDialog, HelpDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер по работе с сотрудниками")
        self.resize(800, 600)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        toolbar = QToolBar()
        self.addToolBar(toolbar)

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

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Имя", "Фамилия", "Дата рождения",
            "Должность", "Телефон", "Email", "Дата начала"
        ])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        layout.addWidget(self.table)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.db.add_employee(data)
            self.load_data()

    def edit_employee(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Выберите сотрудника", "Пожалуйста, выберите сотрудника для редактирования.")
            return
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
        dialog = EmployeeDialog(self, employee)
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.get_data()
            self.db.update_employee(emp_id, new_data)
            self.load_data()

    def delete_employee(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Выберите сотрудника", "Пожалуйста, выберите сотрудника для удаления.")
            return
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

    def generate_report(self):
        filter_dialog = QDialog(self)
        filter_dialog.setWindowTitle("Генерация отчета")
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр по должности (оставьте пустым для всех):"))
        position_filter_edit = QLineEdit()
        filter_layout.addWidget(position_filter_edit)
        layout.addLayout(filter_layout)

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

        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("Сгенерировать")
        cancel_button = QPushButton("Отмена")
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)

        filter_dialog.setLayout(layout)
        ok_button.clicked.connect(filter_dialog.accept)
        cancel_button.clicked.connect(filter_dialog.reject)

        if filter_dialog.exec_() == QDialog.Accepted:
            position_filter = position_filter_edit.text().strip()
            filename = file_edit.text().strip()
            if not filename:
                QMessageBox.warning(self, "Ошибка", "Не указано имя файла для сохранения отчета.")
                return
            self.create_pdf_report(filename, position_filter if position_filter != "" else None)
            QMessageBox.information(self, "Отчет сохранен", f"Отчет успешно сохранен в {filename}")

    def create_pdf_report(self, filename, position_filter=None):
        employees = self.db.fetch_employees(position_filter)
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "Отчет по сотрудникам")
        c.setFont("Helvetica", 12)
        y = height - 80
        headers = ["Имя", "Фамилия", "Должность", "Дата начала работы"]
        x_positions = [50, 150, 300, 450]
        for i, header in enumerate(headers):
            c.drawString(x_positions[i], y, header)
        y -= 20
        for emp in employees:
            c.drawString(x_positions[0], y, emp["first_name"])
            c.drawString(x_positions[1], y, emp["last_name"])
            c.drawString(x_positions[2], y, emp["position"])
            c.drawString(x_positions[3], y, emp["start_date"])
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()

    def show_help(self):
        help_dialog = HelpDialog(self)
        help_dialog.exec_()
