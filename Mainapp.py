import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QTabWidget, QDialog, QFormLayout, QMessageBox, QStackedWidget, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Greener-Bikes")
        self.setGeometry(100, 100, 800, 600)

        # setting up the pages
        self.pages = QStackedWidget()

        #creating the pages
        self.main_page = self.main_menu_page()
        self.inventory_page = self.inventory_management_page()
        self.order_page = self.order_management_page()
        self.production_page = self.production_workflow_page()

        #add pages to the stacked widget
        self.pages.addWidget(self.main_page)
        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.production_page)
        self.pages.addWidget(self.order_page)

        self.setCentralWidget(self.pages)

    def main_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        button_layout = QHBoxLayout(page)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Welcome To The Greener-Bikes App!")
        label.setStyleSheet("font-size:40px;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter| Qt.AlignmentFlag.AlignTop)

        #inventory button
        inventory_button = QPushButton("Inventory Management")
        inventory_button.setFixedSize(300, 100)
        inventory_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.inventory_page))
        button_layout.addWidget(inventory_button, alignment= Qt.AlignmentFlag.AlignCenter)

        production_button = QPushButton("Production Workflow")
        production_button.setFixedSize(300, 100)
        production_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.production_page))
        button_layout.addWidget(production_button, alignment=Qt.AlignmentFlag.AlignCenter)

        order_button = QPushButton("Order Management")
        order_button.setFixedSize(300, 100)
        order_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.order_page))
        button_layout.addWidget(order_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(button_layout)
        return page

    def inventory_management_page(self):

        page = QWidget()
        layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        label = QLabel("Inventory Management")
        label.setStyleSheet("font-size:40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        top_bar_layout.addWidget(label)

        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 100)
        back_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.main_page))
        top_bar_layout.addWidget(back_button)

        layout.addLayout(top_bar_layout)

        self.inventory = {
            "Tubular Steel" : 20,
            "Wheels" : 20,
            "Seats" : 20,
            "Gears" : 20,
            "Brakes" : 20,
            "Lights" : 20

        }

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setHorizontalHeaderLabels(["Component", "Quantity"])
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.inventory_table, alignment=Qt.AlignmentFlag.AlignTop)






        page.setLayout(layout)
        return page

    def production_workflow_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Production Workflow")
        label.setStyleSheet("font-size:40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        top_bar_layout.addWidget(label)

        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 100)
        back_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.main_page))
        top_bar_layout.addWidget(back_button)

        layout.addLayout(top_bar_layout)
        page.setLayout(layout)
        return page

    def order_management_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Order Management")
        label.setStyleSheet("font-size:40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        top_bar_layout.addWidget(label)

        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 100)
        back_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.main_page))
        top_bar_layout.addWidget(back_button)

        layout.addLayout(top_bar_layout)
        page.setLayout(layout)
        return page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainScreen()
    main_window.show()
    sys.exit(app.exec())