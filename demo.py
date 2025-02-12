# demo.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from main_window import MainWindow
from themes import set_dark_theme


def demo_clear_all_employees(main_window):
    """
    Очищает базу данных: удаляет всех сотрудников.
    """
    employees = main_window.db.fetch_employees()
    for emp in employees:
        main_window.db.delete_employee(emp['id'])
    main_window.load_data()
    print("Демонстрация: очищена база данных от сотрудников")


def demo_add_employee(main_window, employee_data):
    """
    Добавляет сотрудника с переданными данными.
    """
    main_window.db.add_employee(employee_data)
    main_window.load_data()
    print(f"Демонстрация: добавлен сотрудник {employee_data['first_name']} {employee_data['last_name']}")


def get_employee_by_name(main_window, first_name, last_name):
    """
    Ищет сотрудника по имени и фамилии в базе данных.
    """
    employees = main_window.db.fetch_employees()
    for emp in employees:
        if emp["first_name"] == first_name and emp["last_name"] == last_name:
            return emp
    return None


def demo_edit_employee(main_window, first_name, last_name, new_data):
    """
    Редактирует данные сотрудника, найденного по имени и фамилии.
    """
    emp = get_employee_by_name(main_window, first_name, last_name)
    if emp:
        main_window.db.update_employee(emp['id'], new_data)
        main_window.load_data()
        print(f"Демонстрация: обновлён сотрудник {first_name} {last_name}")
    else:
        print(f"Демонстрация: сотрудник {first_name} {last_name} не найден для редактирования")


def demo_delete_employee(main_window, first_name, last_name):
    """
    Удаляет сотрудника, найденного по имени и фамилии.
    """
    emp = get_employee_by_name(main_window, first_name, last_name)
    if emp:
        main_window.db.delete_employee(emp['id'])
        main_window.load_data()
        print(f"Демонстрация: удалён сотрудник {first_name} {last_name}")
    else:
        print(f"Демонстрация: сотрудник {first_name} {last_name} не найден для удаления")


def demo_generate_report(main_window):
    """
    Генерирует PDF‑отчёт по всем сотрудникам.
    """
    filename = "demo_report_all.pdf"
    main_window.create_pdf_report(filename, None)
    print(f"Демонстрация: сгенерирован PDF‑отчёт для всех сотрудников и сохранён как {filename}")


def demo_generate_filtered_report(main_window, filter_by):
    """
    Генерирует PDF‑отчёт по сотрудникам, отфильтрованным по должности.
    """
    filename = f"demo_report_{filter_by}.pdf"
    main_window.create_pdf_report(filename, filter_by)
    print(f"Демонстрация: сгенерирован PDF‑отчёт по фильтру '{filter_by}' и сохранён как {filename}")


def demo_show_help(main_window):
    """
    Показывает встроенную справку (документацию).
    """
    main_window.show_help()
    print("Демонстрация: показана документация")


def run_demo(main_window):
    """
    Последовательно выполняет демонстрацию функционала приложения с интервалами.
    """
    # 1. Очищаем базу данных
    QTimer.singleShot(1000, lambda: demo_clear_all_employees(main_window))

    # 2. Добавляем первого сотрудника через 2 секунды
    QTimer.singleShot(2000, lambda: demo_add_employee(main_window, {
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'date_of_birth': '1980-01-01',
        'position': 'Менеджер',
        'phone': '+7 123 4567890',
        'email': 'ivan.ivanov@example.com',
        'start_date': '2020-01-01'
    }))

    # 3. Добавляем второго сотрудника через 3 секунды
    QTimer.singleShot(3000, lambda: demo_add_employee(main_window, {
        'first_name': 'Петр',
        'last_name': 'Петров',
        'date_of_birth': '1990-02-02',
        'position': 'Инженер',
        'phone': '+7 987 6543210',
        'email': 'petr.petrov@example.com',
        'start_date': '2021-02-02'
    }))

    # 4. Редактируем первого сотрудника (Иванов) через 4000 мс – меняем должность на "Старший менеджер"
    QTimer.singleShot(4000, lambda: demo_edit_employee(main_window, 'Иван', 'Иванов', {
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'date_of_birth': '1980-01-01',
        'position': 'Старший менеджер',
        'phone': '+7 123 4567890',
        'email': 'ivan.ivanov@example.com',
        'start_date': '2020-01-01'
    }))

    # 5. Генерируем PDF‑отчёт для всех сотрудников через 5000 мс
    QTimer.singleShot(5000, lambda: demo_generate_report(main_window))

    # 6. Генерируем PDF‑отчёт с фильтром "Инженер" через 6000 мс
    QTimer.singleShot(6000, lambda: demo_generate_filtered_report(main_window, 'Инженер'))

    # 7. Удаляем сотрудника "Иван Иванов" через 7000 мс
    QTimer.singleShot(7000, lambda: demo_delete_employee(main_window, 'Иван', 'Иванов'))

    # 8. Удаляем сотрудника "Петр Петров" через 8000 мс
    QTimer.singleShot(8000, lambda: demo_delete_employee(main_window, 'Петр', 'Петров'))

    # 9. Показываем справку через 9000 мс
    QTimer.singleShot(9000, lambda: demo_show_help(main_window))

    # 10. Выводим сообщение о завершении демонстрации через 10000 мс
    QTimer.singleShot(10000, lambda: print("Демонстрация завершена."))


def main():
    app = QApplication(sys.argv)
    set_dark_theme(app)
    main_window = MainWindow()
    main_window.show()

    run_demo(main_window)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
