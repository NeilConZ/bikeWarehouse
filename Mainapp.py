import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget, QDialog, QFormLayout, QMessageBox, QStackedWidget, QSizePolicy
from PySide6.QtCore import Qt

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        #Layout and size
        self.setWindowTitle("Greener-Bikes")
        self.setGeometry(100,100,800,600)
        self.label = QLabel("Welcome To The Greener-Bikes App!")
        self.label.setStyleSheet("font-size:40px;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        #setting up buttons
        self.inventory_management_button = QPushButton("Inventory Management")
        self.inventory_management_button.setFixedSize(200,100)


        self.production_workflow_button = QPushButton("Production Workflow")
        self.production_workflow_button.setFixedSize(200,100)


        self.order_management_button = QPushButton("Order Management")
        self.order_management_button.setFixedSize(200,100)

        #connecting buttons to pages
        self.inventory_management_button.clicked.connect(self.inventory_management_page)
        self.production_workflow_button.clicked.connect(self.production_workflow_page)
        self.order_management_button.clicked.connect(self.order_management_page)

        #addng buttons to page
        main_layout.addWidget(self.inventory_management_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.production_workflow_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.order_management_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch()

        # setting up the pages
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        self.inventory_page = self.inventory_management_page()
        self.order_page = self.order_management_page()
        self.production_page = self.production_workflow_page()

        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.production_page)
        self.pages.addWidget(self.order_page)


    def inventory_management_page(self):

        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Inventory Management")
        layout.addWidget(label)
        return page

    def production_workflow_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Production")
        layout.addWidget(label)
        return page

    def order_management_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Order Management")
        layout.addWidget(label)
        return page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainScreen()
    main_window.show()
    sys.exit(app.exec())