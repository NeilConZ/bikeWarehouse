import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget, QDialog, QFormLayout, QMessageBox

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Greener-Bikes")
        self.setGeometry(100,100,800,600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.inventory_management = self.inventory_management_tab()
        self.production = self.production_tab()
        self.order_management = self.order_management_tab()

        self.tabs.addTab(self.inventory_management, "Inventory")
        self.tabs.addTab(self.production, "production")
        self.tabs.addTab(self.order_management, "Order Management")

    def inventory_management_tab(self):

        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Inventory Management")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def production_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Production")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def order_management_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Order Management")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainScreen()
    main_window.show()
    sys.exit(app.exec())