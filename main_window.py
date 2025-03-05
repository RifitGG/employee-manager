from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QToolBar, QAction, QMessageBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog
)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from db_manager import DatabaseManager
from dialogs import EmployeeDialog, HelpDialog

# Регистрация шрифта с поддержкой кириллицы
try:
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
except:
    print("Шрифт Arial не найден, попытка использовать стандартный шрифт")


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

        actions = [
            ("Добавить", self.add_employee),
            ("Редактировать", self.edit_employee),
            ("Удалить", self.delete_employee),
            ("Сгенерировать отчет", self.generate_report),
            ("Документация", self.show_help)
        ]

        for text, handler in actions:
            action = QAction(text, self)
            action.triggered.connect(handler)
            toolbar.addAction(action)

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
            for col, key in enumerate(["id", "first_name", "last_name",
                                       "date_of_birth", "position",
                                       "phone", "email", "start_date"]):
                self.table.setItem(row_number, col, QTableWidgetItem(str(employee[key])))

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.db.add_employee(dialog.get_data())
            self.load_data()

    def edit_employee(self):
        if not (row := self._get_selected_row()):
            return
        emp_id = int(self.table.item(row, 0).text())
        employee = {key: self.table.item(row, col).text()
                    for col, key in enumerate(["id", "first_name", "last_name",
                                               "date_of_birth", "position",
                                               "phone", "email", "start_date"])}
        dialog = EmployeeDialog(self, employee)
        if dialog.exec_() == QDialog.Accepted:
            self.db.update_employee(emp_id, dialog.get_data())
            self.load_data()

    def delete_employee(self):
        if not (row := self._get_selected_row()):
            return
        emp_id = int(self.table.item(row, 0).text())
        if QMessageBox.Yes == QMessageBox.question(
                self, "Подтверждение",
                "Удалить выбранного сотрудника?",
                QMessageBox.Yes | QMessageBox.No
        ):
            self.db.delete_employee(emp_id)
            self.load_data()

    def generate_report(self):
        dialog = ReportDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename, position_filter = dialog.get_data()
            self.create_pdf_report(filename, position_filter)
            QMessageBox.information(self, "Успех", f"Отчет сохранен в:\n{filename}")

    def create_pdf_report(self, filename, position_filter=None):
        employees = self.db.fetch_employees(position_filter)
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Настройка шрифтов
        font_name = 'Arial' if 'Arial' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        c.setFont(font_name, 16)
        c.drawCentredString(width / 2, height - 50, "Отчет по сотрудникам")

        c.setFont(font_name, 12)
        y = height - 80
        headers = ["Имя", "Фамилия", "Должность", "Дата начала"]
        x_positions = [50, 150, 300, 450]

        # Заголовки
        for i, header in enumerate(headers):
            c.drawString(x_positions[i], y, header)

        # Данные
        for emp in employees:
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont(font_name, 12)

            c.drawString(x_positions[0], y, emp["first_name"])
            c.drawString(x_positions[1], y, emp["last_name"])
            c.drawString(x_positions[2], y, emp["position"])
            c.drawString(x_positions[3], y, emp["start_date"])

        c.save()

    def show_help(self):
        HelpDialog(self).exec_()

    def _get_selected_row(self):
        if not (selected := self.table.selectedItems()):
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
            return None
        return selected[0].row()


class ReportDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Генерация отчета")
        layout = QVBoxLayout()

        # Фильтр по должности
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр по должности:"))
        self.position_filter = QLineEdit()
        filter_layout.addWidget(self.position_filter)
        layout.addLayout(filter_layout)

        # Выбор файла
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Файл для сохранения:"))
        self.file_edit = QLineEdit()
        file_layout.addWidget(self.file_edit)
        browse_btn = QPushButton("Обзор")
        browse_btn.clicked.connect(self._browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        # Кнопки
        btn_box = QHBoxLayout()
        ok_btn = QPushButton("Создать")
        ok_btn.clicked.connect(self.accept)
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(QPushButton("Отмена", clicked=self.reject))
        layout.addLayout(btn_box)

        self.setLayout(layout)

    def _browse_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет", "", "PDF Files (*.pdf)")
        if filename:
            self.file_edit.setText(filename)

    def get_data(self):
        return (
            self.file_edit.text(),
            self.position_filter.text().strip() or None
        )
