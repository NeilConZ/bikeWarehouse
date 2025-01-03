import sys

from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                               QTabWidget, QDialog, QFormLayout, QMessageBox, QStackedWidget, QSizePolicy, QHBoxLayout, QInputDialog, QComboBox, QLineEdit)
from PySide6.QtCore import Qt

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Greener-Bikes")
        self.setGeometry(100, 100, 800, 600)

        # setting up the pages
        self.pages = QStackedWidget()

        self.stock = [{
            "Component": "Tubular Steel", "Quantity": 10
        }, {
            "Component": "Wheels", "Quantity": 10
        }, {
            "Component": "Seats", "Quantity": 10
        }, {
            "Component": "Gears", "Quantity": 3
        }, {
            "Component": "Brakes", "Quantity": 10
        }, {
            "Component": "Lights", "Quantity": 10
        }]

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
        self.pages.currentChanged.connect(self.load_stock)
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

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setRowCount(6)
        self.inventory_table.setHorizontalHeaderLabels(["Component", "Quantity"])
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.inventory_table)

        change_stock = QPushButton("Add/Replenish Stock")
        change_stock.clicked.connect(self.change_data)
        layout.addWidget(change_stock)




        page.setLayout(layout)
        return page


    def load_stock (self, index):
        current_page = self.pages.widget(index)
        if current_page == self.inventory_page:
            self.add_table_data()

    def add_table_data(self):
        low_quantity = False

        self.inventory_table.setRowCount(len(self.stock))
        for i, item in enumerate(self.stock):


            quantity_value = QTableWidgetItem(str(item["Quantity"]))

            if item["Quantity"] <= 3:
                quantity_value.setForeground(QBrush(QColor("red")))
                low_quantity = True
            else:
                quantity_value.setForeground(QBrush(QColor("white")))

            self.inventory_table.setItem(i, 0, QTableWidgetItem(item["Component"]))
            self.inventory_table.setItem(i, 1, quantity_value)

        if low_quantity:
            QMessageBox.warning(self, "ALERT", "LOW QUANTITY ALERT", QMessageBox.StandardButton.Ok)



    def change_data(self):

        component, saved = QInputDialog.getText(self, "Add/Replenish Stock", "Enter Component Name : ")
        if not component or not saved:
            return

        quantity, saved = QInputDialog.getInt(self, "Add/Replenish Stock", "Enter Quantity:")
        if not saved:
            return

        for item in self.stock:
            if item["Component"].lower() == component.lower():
                item["Quantity"] = quantity
                self.add_table_data()
                return

        return QMessageBox.warning(self,"Error","Not a valid component.", QMessageBox.StandardButton.Ok)

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



        self.frame_amount = 0
        self.fork_amount = 0
        self.paint_amount = 0
        self.pedal_amount = 0
        self.wheel_amount = 0
        self.gear_amount = 0
        self.brake_amount = 0
        self.light_amount = 0
        self.seat_amount = 0



        frame_welding_layout = QHBoxLayout()
        frame_welding_title = QLabel("Frame Welding Station")

        self.frame_amount_label = QLabel(str(self.frame_amount))
        add_frame = QPushButton("Add Frame")

        frame_welding_layout.addWidget(frame_welding_title)
        frame_welding_layout.addWidget(self.frame_amount_label)
        frame_welding_layout.addWidget(add_frame)
        layout.addLayout(frame_welding_layout)



        fork_welding_layout = QHBoxLayout()
        fork_welding_title = QLabel("Fork Welding Station")

        self.fork_amount_label = QLabel(str(self.fork_amount))
        add_fork = QPushButton("Add Fork")

        fork_welding_layout.addWidget(fork_welding_title)
        fork_welding_layout.addWidget(self.fork_amount_label)
        fork_welding_layout.addWidget(add_fork)
        layout.addLayout(fork_welding_layout)



        paint_welding_layout = QHBoxLayout()
        paint_welding_title = QLabel("Paint Welding Station")

        self.paint_amount_label = QLabel(str(self.paint_amount))
        add_paint = QPushButton("Add Paint")

        paint_welding_layout.addWidget(paint_welding_title)
        paint_welding_layout.addWidget(self.paint_amount_label)
        paint_welding_layout.addWidget(add_paint)
        layout.addLayout( paint_welding_layout)



        pedal_welding_layout = QHBoxLayout()
        pedal_welding_title = QLabel("Pedal Welding Station")

        self.pedal_amount_label = QLabel(str(self.pedal_amount))
        add_pedal = QPushButton("Add Pedal")

        pedal_welding_layout.addWidget(pedal_welding_title)
        pedal_welding_layout.addWidget(self.pedal_amount_label)
        pedal_welding_layout.addWidget(add_pedal)
        layout.addLayout(pedal_welding_layout)



        wheel_welding_layout = QHBoxLayout()
        wheel_welding_title = QLabel("Wheel Welding Station")

        self.wheel_amount_label = QLabel(str(self.wheel_amount))
        add_wheel = QPushButton("Add wheel")

        wheel_welding_layout.addWidget(wheel_welding_title)
        wheel_welding_layout.addWidget(self.wheel_amount_label)
        wheel_welding_layout.addWidget(add_wheel)
        layout.addLayout(wheel_welding_layout)

        gear_welding_layout = QHBoxLayout()
        gear_welding_title = QLabel("Gear Welding Station")

        self.gear_amount_label = QLabel(str(self.gear_amount))
        add_gear = QPushButton("Add Gear")

        gear_welding_layout.addWidget(gear_welding_title)
        gear_welding_layout.addWidget(self.gear_amount_label)
        gear_welding_layout.addWidget(add_gear)
        layout.addLayout(gear_welding_layout)

        brake_welding_layout = QHBoxLayout()
        brake_welding_title = QLabel("Brake Welding Station")

        self.brake_amount_label = QLabel(str(self.brake_amount))
        add_brake = QPushButton("Add Brake")

        brake_welding_layout.addWidget(brake_welding_title)
        brake_welding_layout.addWidget(self.brake_amount_label)
        brake_welding_layout.addWidget(add_brake)
        layout.addLayout(brake_welding_layout)

        light_welding_layout = QHBoxLayout()
        light_welding_title = QLabel("Light Welding Station")

        self.light_amount_label = QLabel(str(self.light_amount))
        add_light = QPushButton("Add Light")

        light_welding_layout.addWidget(light_welding_title)
        light_welding_layout.addWidget(self.light_amount_label)
        light_welding_layout.addWidget(add_light)
        layout.addLayout(light_welding_layout)

        seat_welding_layout = QHBoxLayout()
        seat_welding_title = QLabel("Seat Welding Station")

        self.seat_amount_label = QLabel(str(self.seat_amount))
        add_seat = QPushButton("Add Seat")

        seat_welding_layout.addWidget(seat_welding_title)
        seat_welding_layout.addWidget(self.seat_amount_label)
        seat_welding_layout.addWidget(add_seat)
        layout.addLayout(seat_welding_layout)

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


        self.order_list = []

        form = QFormLayout()

        self.bike_model = QComboBox()
        self.bike_model.addItems(["BMX", "Mountain Bike", "Electric Bike", "Road Bike"])
        form.addRow("Model: ", self.bike_model)

        self.bike_colour = QComboBox()
        self.bike_colour.addItems(["Red", "Blue", "White", "Black", "Yellow", "Green"])
        form.addRow("Colour: ", self.bike_colour)

        self.bike_wheelSize = QComboBox()
        self.bike_wheelSize.addItems(["26 inches", "27.5 inches", "29 inches"])
        form.addRow("Wheel Size: ", self.bike_wheelSize)

        self.bike_gears = QComboBox()
        self.bike_gears.addItems(["Standard Gears", "Race Gears", "Premium Gears"])
        form.addRow("Gears: ", self.bike_gears)

        self.bike_brakes = QComboBox()
        self.bike_brakes.addItems(["Disc Brakes", "Rim Brakes"])
        form.addRow("Brakes: ", self.bike_brakes)

        self.bike_lights = QComboBox()
        self.bike_lights.addItems(["LED Lights", "Standard Lights", "Neon Lights"])
        form.addRow("Lights: ", self.bike_lights)

        self.order_name = QLineEdit()
        form.addRow("Order Name: ", self.order_name)

        self.order_contact_number = QLineEdit()
        form.addRow("Contact Number: ", self.order_contact_number)

        self.order_delivery_address = QLineEdit()
        form.addRow("Delivery Address", self.order_delivery_address)

        layout.addLayout(form)

        complete_order = QPushButton("Complete Order")
        complete_order.clicked.connect(self.complete_order)
        layout.addWidget(complete_order)

        self.table_of_orders = QTableWidget()
        self.table_of_orders.setColumnCount(9)
        self.table_of_orders.setHorizontalHeaderLabels(["Model", "Colour", "Wheel Size","Gears", "Brakes", "Lights", "Customer name", "Contact number", "Delivery Address"])
        layout.addWidget(self.table_of_orders)
        page.setLayout(layout)
        return page

    def complete_order(self):

        bike_model = self.bike_model.currentText()
        bike_colour = self.bike_colour.currentText()
        bike_wheel_size = self.bike_wheelSize.currentText()
        bike_gears = self.bike_gears.currentText()
        bike_brakes = self.bike_brakes.currentText()
        bike_lights = self.bike_lights.currentText()
        order_name = self.order_name.text()
        order_contact_number = self.order_contact_number.text()
        order_delivery_address = self.order_delivery_address.text()

        if not order_name or not order_contact_number or not order_delivery_address:
            QMessageBox.warning(self, "Error", "Information cannot be empty!", QMessageBox.StandardButton.Ok)
            return

        order = {

            "bike model": bike_model,
            "bike colour" : bike_colour,
            "bike wheel size" : bike_wheel_size,
            "bike gears" : bike_gears,
            "bike brakes" : bike_brakes,
            "bike lights" : bike_lights,
            "order name" : order_name,
            "contact number" : order_contact_number,
            "delivery address" : order_delivery_address
        }

        self.order_list.append(order)

        self.add_order_to_table()

        self.order_contact_number.clear()
        self.order_name.clear()
        self.order_delivery_address.clear()

    def add_order_to_table(self):
        self.table_of_orders.setRowCount(len(self.order_list))

        for i, order in enumerate(self.order_list):

            bike_model = QTableWidgetItem(order["bike model"])
            self.table_of_orders.setItem(i,0,bike_model)

            bike_colour = QTableWidgetItem(order["bike colour"])
            self.table_of_orders.setItem(i, 1, bike_colour)

            bike_wheel_size = QTableWidgetItem(order["bike wheel size"])
            self.table_of_orders.setItem(i, 2, bike_wheel_size)

            bike_gears = QTableWidgetItem(order["bike gears"])
            self.table_of_orders.setItem(i, 3, bike_gears)

            bike_brakes = QTableWidgetItem(order["bike brakes"])
            self.table_of_orders.setItem(i, 4, bike_brakes)

            bike_lights = QTableWidgetItem(order["bike lights"])
            self.table_of_orders.setItem(i,5,bike_lights)

            order_name = QTableWidgetItem(order["order name"])
            self.table_of_orders.setItem(i, 6, order_name)

            order_contact_number = QTableWidgetItem(order["contact number"])
            self.table_of_orders.setItem(i, 7, order_contact_number)

            order_delivery_address = QTableWidgetItem(order["delivery address"])
            self.table_of_orders.setItem(i, 8, order_delivery_address)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainScreen()
    main_window.show()
    sys.exit(app.exec())