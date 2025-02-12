# themes.py
def set_dark_theme(app):
    dark_stylesheet = """
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
        font-size: 12px;
    }
    QLineEdit, QTextEdit, QDateEdit, QTableWidget {
        background-color: #3c3f41;
        color: #ffffff;
        border: 1px solid #76797C;
    }
    QPushButton {
        background-color: #3c3f41;
        color: #ffffff;
        border: 1px solid #76797C;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #484a4c;
    }
    QHeaderView::section {
        background-color: #3c3f41;
        color: #ffffff;
    }
    QToolBar {
        background-color: #3c3f41;
        border: none;
    }
    QMenuBar {
        background-color: #3c3f41;
        color: #ffffff;
    }
    QMenu {
        background-color: #3c3f41;
        color: #ffffff;
    }
    """
    app.setStyleSheet(dark_stylesheet)
