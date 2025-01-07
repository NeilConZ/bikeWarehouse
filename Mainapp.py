import sys

from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTableWidget,
                               QTableWidgetItem,
                               QFormLayout, QMessageBox, QStackedWidget, QHBoxLayout, QInputDialog, QComboBox,
                               QLineEdit)
from PySide6.QtCore import Qt


class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.alert = False

        # sets up the main window, giving it a name and initialises the size
        self.setWindowTitle("Greener-Bikes")
        self.setGeometry(100, 100, 800, 600)

        # setting up the pages
        self.pages = QStackedWidget()

        # sets up the stock parts and respective quantities for later use
        self.stock = [{
            "Part": "Tubular Steel", "Quantity": 10
        }, {
            "Part": "Wheel", "Quantity": 10
        }, {
            "Part": "Seat", "Quantity": 10
        }, {
            "Part": "Gear", "Quantity": 10
        }, {
            "Part": "Brake", "Quantity": 10
        }, {
            "Part": "Light", "Quantity": 10
        }, {
            "Part": "Paint", "Quantity": 10
        },
            {
                "Part": "Pedal", "Quantity": 10
            }]

        # sets up variables to store the users choices when they order a bike
        self.bike_model_chosen = None
        self.bike_colour_chosen = None
        self.bike_wheelSize_chosen = None
        self.bike_gear_chosen = None
        self.bike_brake_chosen = None
        self.bike_light_chosen = None

        # assigns variables to the main screen pages
        self.main_page = self.main_menu_page()
        self.inventory_page = self.inventory_management_page()
        self.order_page = self.order_management_page()
        self.production_page = self.production_workflow_page()

        # adds the pages to the stacked widget for changing screens
        self.pages.addWidget(self.main_page)
        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.production_page)
        self.pages.addWidget(self.order_page)
        self.pages.currentChanged.connect(self.load_stock)
        self.setCentralWidget(self.pages)

    def main_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # sets up the layout for the buttons connecting to other pages
        button_layout = QHBoxLayout(page)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # gives the main screen a title
        label = QLabel("Welcome To The Greener-Bikes App!")
        label.setStyleSheet("font-size:40px;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # creates the inventory button
        inventory_button = QPushButton("Inventory Management")
        inventory_button.setFixedSize(300, 100)
        inventory_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.inventory_page))
        button_layout.addWidget(inventory_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # creates the production button
        production_button = QPushButton("Production Workflow")
        production_button.setFixedSize(300, 100)
        production_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.production_page))
        button_layout.addWidget(production_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # creates the order button
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

        # gives the inventory page its title
        label = QLabel("Inventory Management")
        label.setStyleSheet("font-size:40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        top_bar_layout.addWidget(label)

        # adds a back button to the page
        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 100)
        back_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.main_page))
        top_bar_layout.addWidget(back_button)

        layout.addLayout(top_bar_layout)

        # creates an inventory table called "inventory table" that stores the respective parts and quantities
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setRowCount(8)
        self.inventory_table.setHorizontalHeaderLabels(["Part", "Quantity"])
        # makes the table not editable
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.inventory_table)

        # adds a button that allows users to adjust the held stock by connecting to a function that changes it's data
        change_stock = QPushButton("Adjust Stock")
        change_stock.clicked.connect(self.change_data)
        layout.addWidget(change_stock)

        page.setLayout(layout)
        return page

    def load_stock(self, index):

        # sets the variable "alert" to true so that it sets the alert off only when the user enters the inventory page
        self.alert = True
        current_page = self.pages.widget(index)
        if current_page == self.inventory_page:
            self.add_table_data()

    def add_table_data(self):
        # assigns a variable called low_quantity and sets it to false
        low_quantity = False

        self.inventory_table.setRowCount(len(self.stock))
        # loops for the self.stock
        for i, item in enumerate(self.stock):

            # checks the quantity of an item and assigns it to the "quantity_value"
            quantity_value = QTableWidgetItem(str(item["Quantity"]))

            # checks if the quantity is less than or equal to 3 and if so, changes to red, otherwise leaves it white
            if item["Quantity"] <= 3:
                quantity_value.setForeground(QBrush(QColor("red")))
                low_quantity = True
            else:
                quantity_value.setForeground(QBrush(QColor("white")))

            # adds the part name in the first column and its quantity in the second column
            self.inventory_table.setItem(i, 0, QTableWidgetItem(item["Part"]))
            self.inventory_table.setItem(i, 1, quantity_value)

        # if low quantity is true (a part has a quantity of less than 3) it creates the alert
        if low_quantity and self.alert == True:
            QMessageBox.warning(self, "ALERT", "LOW QUANTITY ALERT", QMessageBox.StandardButton.Ok)

    def change_data(self):

        # asks the user for the part name they want to adjust
        part, saved = QInputDialog.getText(self, "Adjust Stock", "Enter Part Name: ")
        # if the input is not a part or the user doesn't click okay it returns and doesn't continue
        if not part or not saved:
            return

        # asks the user for the quantity amount they want to adjust
        quantity, saved = QInputDialog.getInt(self, "Adjust Stock", "Enter Quantity:")
        # if they don't click okay it returns and doesn't continue
        if not saved:
            return

        # loops through the stock and if the part matches one in the stock it adds it to the quantity
        for item in self.stock:
            if item["Part"].lower() == part.lower():
                item["Quantity"] = quantity
                # updates the inventory table live
                self.add_table_data()
                return

        # if the part doesn't match one it stocks an error message is displayed
        return QMessageBox.warning(self, "Error", "Not a valid Part.", QMessageBox.StandardButton.Ok)

    def track_active_orders(self):
        # tracks the amount of current orders
        return len(self.order_list)

    def production_workflow_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # gives the production page its title
        label = QLabel("Production Workflow")
        label.setStyleSheet("font-size:40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        top_bar_layout.addWidget(label)

        # adds a back button
        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 100)
        back_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.main_page))
        top_bar_layout.addWidget(back_button)

        layout.addLayout(top_bar_layout)

        # tracks the amount of bikes in each section of the production value and assigns it a value
        self.bike_with_frame_added_amount = 0
        self.bike_with_fork_added_amount = 0
        self.bike_with_paint_added_amount = 0
        self.bike_with_pedal_added_amount = 0
        self.bike_with_wheel_added_amount = 0
        self.bike_with_gear_added_amount = 0
        self.bike_with_brake_added_amount = 0
        self.bike_with_light_added_amount = 0
        self.bike_with_seat_added_amount = 0

        # creates the welding station layout and gives it a label
        frame_welding_layout = QHBoxLayout()
        frame_welding_title = QLabel("Frame Welding station")

        # shows the amount of frames in the station
        self.bike_with_frame_added_amount_label = QLabel(str(self.bike_with_frame_added_amount))

        # creates the button to let the user put the part in the station
        add_frame = QPushButton("Add Frame")
        add_frame.clicked.connect(self.frame_welding_station)

        # adds the layout to the page
        frame_welding_layout.addWidget(frame_welding_title)
        frame_welding_layout.addWidget(self.bike_with_frame_added_amount_label)
        frame_welding_layout.addWidget(add_frame)
        layout.addLayout(frame_welding_layout)

        # creates the welding station layout and gives it a label
        fork_welding_layout = QHBoxLayout()
        fork_welding_title = QLabel("Fork Welding station")

        # shows the amount of frames in the station
        self.bike_with_fork_added_amount_label = QLabel(str(self.bike_with_fork_added_amount))

        # creates the button to let the user put the part in the station
        add_fork = QPushButton("Add Fork")
        add_fork.clicked.connect(self.fork_welding_station)

        # adds the layout to the page
        fork_welding_layout.addWidget(fork_welding_title)
        fork_welding_layout.addWidget(self.bike_with_fork_added_amount_label)
        fork_welding_layout.addWidget(add_fork)
        layout.addLayout(fork_welding_layout)

        # creates the welding station layout and gives it a label
        paint_welding_layout = QHBoxLayout()
        paint_welding_title = QLabel("Paint Welding station")

        # shows the amount of paint in the station
        self.bike_with_paint_added_amount_label = QLabel(str(self.bike_with_paint_added_amount))

        # creates the button to let the user put the part in the station
        add_paint = QPushButton("Add Paint")
        add_paint.clicked.connect(self.paint_welding_station)

        # adds the layout to the page
        paint_welding_layout.addWidget(paint_welding_title)
        paint_welding_layout.addWidget(self.bike_with_paint_added_amount_label)
        paint_welding_layout.addWidget(add_paint)
        layout.addLayout(paint_welding_layout)

        # creates the welding station layout and gives it a label
        pedal_welding_layout = QHBoxLayout()
        pedal_welding_title = QLabel("Pedal Welding station")

        # shows the amount of pedals in the station
        self.bike_with_pedal_added_amount_label = QLabel(str(self.bike_with_pedal_added_amount))

        # creates the button to let the user put the part in the station
        add_pedal = QPushButton("Add Pedal")
        add_pedal.clicked.connect(self.pedal_welding_station)

        # adds the layout to the page
        pedal_welding_layout.addWidget(pedal_welding_title)
        pedal_welding_layout.addWidget(self.bike_with_pedal_added_amount_label)
        pedal_welding_layout.addWidget(add_pedal)
        layout.addLayout(pedal_welding_layout)

        # creates the welding station layout and gives it a label
        wheel_welding_layout = QHBoxLayout()
        wheel_welding_title = QLabel("Wheel Welding station")

        # shows the amount of wheels in the station
        self.bike_with_wheel_added_amount_label = QLabel(str(self.bike_with_wheel_added_amount))

        # creates the button to let the user put the part in the station
        add_wheel = QPushButton("Add wheel")
        add_wheel.clicked.connect(self.wheel_welding_station)

        # adds the layout to the page
        wheel_welding_layout.addWidget(wheel_welding_title)
        wheel_welding_layout.addWidget(self.bike_with_wheel_added_amount_label)
        wheel_welding_layout.addWidget(add_wheel)
        layout.addLayout(wheel_welding_layout)

        # creates the welding station layout and gives it a label
        gear_welding_layout = QHBoxLayout()
        gear_welding_title = QLabel("Gear Welding station")

        # shows the amount of gears in the station
        self.bike_with_gear_added_amount_label = QLabel(str(self.bike_with_gear_added_amount))

        # creates the button to let the user put the part in the station
        add_gear = QPushButton("Add Gear")
        add_gear.clicked.connect(self.gear_welding_station)

        # adds the layout to the page
        gear_welding_layout.addWidget(gear_welding_title)
        gear_welding_layout.addWidget(self.bike_with_gear_added_amount_label)
        gear_welding_layout.addWidget(add_gear)
        layout.addLayout(gear_welding_layout)

        # creates the welding station layout and gives it a label
        brake_welding_layout = QHBoxLayout()
        brake_welding_title = QLabel("Brake Welding station")

        # shows the amount of brakes in the station
        self.bike_with_brake_added_amount_label = QLabel(str(self.bike_with_brake_added_amount))

        # creates the button to let the user put the part in the station
        add_brake = QPushButton("Add Brake")
        add_brake.clicked.connect(self.brake_welding_station)

        # adds the layout to the page
        brake_welding_layout.addWidget(brake_welding_title)
        brake_welding_layout.addWidget(self.bike_with_brake_added_amount_label)
        brake_welding_layout.addWidget(add_brake)
        layout.addLayout(brake_welding_layout)

        # creates the welding station layout and gives it a label
        light_welding_layout = QHBoxLayout()
        light_welding_title = QLabel("Light Welding station")

        # shows the amount of lights in the station
        self.bike_with_light_added_amount_label = QLabel(str(self.bike_with_light_added_amount))

        # creates the button to let the user put the part in the station
        add_light = QPushButton("Add Light")
        add_light.clicked.connect(self.light_welding_station)

        # adds the layout to the page
        light_welding_layout.addWidget(light_welding_title)
        light_welding_layout.addWidget(self.bike_with_light_added_amount_label)
        light_welding_layout.addWidget(add_light)
        layout.addLayout(light_welding_layout)

        # creates the welding station layout and gives it a label
        seat_welding_layout = QHBoxLayout()
        seat_welding_title = QLabel("Seat Welding station")

        # shows the amount of seats in the station
        self.bike_with_seat_added_amount_label = QLabel(str(self.bike_with_seat_added_amount))

        # creates the button to let the user put the part in the station
        add_seat = QPushButton("Add Seat")
        add_seat.clicked.connect(self.seat_welding_station)

        # adds the layout to the page
        seat_welding_layout.addWidget(seat_welding_title)
        seat_welding_layout.addWidget(self.bike_with_seat_added_amount_label)
        seat_welding_layout.addWidget(add_seat)
        layout.addLayout(seat_welding_layout)

        page.setLayout(layout)
        return page

    def frame_welding_station(self):
        self.alert = False
        frame_steel_cost = 0
        found_item = None
        model = self.bike_model_chosen

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_frame_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return

        # checks if the user has ordered a bike on the order page by checking if there is something stored in model
        if model == None:
            QMessageBox.warning(self, "Error", "No bike has been ordered.", QMessageBox.StandardButton.Ok)
            return

        # assigns tubular steel as the item needed to make the frame
        for item in self.stock:
            if item["Part"].lower() == "tubular steel":
                found_item = item
                break

        # if there is no tubular steel shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", "There is no tubular steel remaining.", QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if model.lower() == "road bike":
            frame_steel_cost = 1
        elif model.lower() == "bmx":
            frame_steel_cost = 2
        elif model.lower() == "mountain bike":
            frame_steel_cost = 3
        elif model.lower() == "electric bike":
            frame_steel_cost = 4

        # if there is not enough steel it displays this error message
        if found_item["Quantity"] < frame_steel_cost:
            QMessageBox.warning(self, "Error", "Not enough steel remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= frame_steel_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to the frame assemble station
        self.bike_with_frame_added_amount += 1

        # updates their total
        self.bike_with_frame_added_amount_label.setText(str(self.bike_with_frame_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def fork_welding_station(self):
        self.alert = False
        fork_steel_cost = 0
        found_item = None
        model = self.bike_model_chosen

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_fork_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # assigns tubular steel as the item needed to make the frame
        for item in self.stock:
            if item["Part"].lower() == "tubular steel":
                found_item = item
                break

        # if there is no tubular steel shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There is no tubular steel remaining.",
                                QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if model.lower() == "road bike":
            fork_steel_cost = 1
        elif model.lower() == "bmx":
            fork_steel_cost = 2
        elif model.lower() == "mountain bike":
            fork_steel_cost = 3
        elif model.lower() == "electric bike":
            fork_steel_cost = 4

        # if there is not enough steel it displays this error message
        if found_item["Quantity"] < fork_steel_cost:
            QMessageBox.warning(self, "Error", f"Not enough tubular steel remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= fork_steel_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to the fork assemble station
        self.bike_with_fork_added_amount += 1

        # updates their total
        self.bike_with_fork_added_amount_label.setText(str(self.bike_with_fork_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def paint_welding_station(self):
        self.alert = False

        found_item = None
        paint_cost = 0
        paint = self.bike_colour_chosen

        # checks that there is one frame and fork in each assembly station
        if self.bike_with_frame_added_amount < 1 or self.bike_with_fork_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a bike with a frame and fork to continue.",
                                QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_paint_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the paint part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "paint":
                found_item = item
                break

        # if there is no paint (quantity = 0) then displays this message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There is no paint remaining.", QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if paint.lower() == "red":
            paint_cost = 1
        elif paint.lower() == "blue":
            paint_cost = 1
        elif paint.lower() == "white":
            paint_cost = 1
        elif paint.lower() == "black":
            paint_cost = 1
        elif paint.lower() == "yellow":
            paint_cost = 1
        elif paint.lower() == "green":
            paint_cost = 1

        # if the quantity of paint is less than the cost it shows this error
        if found_item["Quantity"] < paint_cost:
            QMessageBox.warning(self, "Error", f"Not enough paint remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= paint_cost
        # updates the table
        self.add_table_data()

        # adds 1 to the paint assembly station amount
        self.bike_with_paint_added_amount += 1

        # takes 1 away from the frame and fork assembly stations
        self.bike_with_frame_added_amount -= 1
        self.bike_with_fork_added_amount -= 1

        # updates their total
        self.bike_with_frame_added_amount_label.setText(str(self.bike_with_frame_added_amount))
        self.bike_with_fork_added_amount_label.setText(str(self.bike_with_fork_added_amount))
        self.bike_with_paint_added_amount_label.setText(str(self.bike_with_paint_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def pedal_welding_station(self):
        self.alert = False

        found_item = None
        pedal_cost = 1

        # checks that there is one paint in the assembly station
        if self.bike_with_paint_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a Painted Bike to continue.", QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_pedal_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the pedal part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "pedal":
                found_item = item
                break

        # if there are no pedals shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There are no pedals remaining.", QMessageBox.StandardButton.Ok)
            return

        # if there is not enough pedals it displays this error message
        if found_item["Quantity"] < pedal_cost:
            QMessageBox.warning(self, "Error", f"Not enough pedals remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= pedal_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to pedal assemble station
        self.bike_with_pedal_added_amount += 1

        # takes 1 away from the paint assemble station
        self.bike_with_paint_added_amount -= 1

        # updates their totals
        self.bike_with_pedal_added_amount_label.setText(str(self.bike_with_pedal_added_amount))
        self.bike_with_paint_added_amount_label.setText(str(self.bike_with_paint_added_amount))

        self.change_amount_colours()

    def wheel_welding_station(self):
        self.alert = False
        found_item = None
        wheel_cost = 0
        wheel = self.bike_wheelSize_chosen

        # checks that there is one pedal in the assembly station
        if self.bike_with_pedal_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a Bike with a pedal to continue.",
                                QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_wheel_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the wheel part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "wheel":
                found_item = item
                break

        # if there are no wheels shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There are no wheels remaining.", QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if wheel.lower() == "26 inches":
            wheel_cost = 1
        elif wheel.lower() == "27.5 inches":
            wheel_cost = 2
        elif wheel.lower() == "29 inches":
            wheel_cost = 3

        # if there is not enough wheels it displays this error message
        if found_item["Quantity"] < wheel_cost:
            QMessageBox.warning(self, "Error", f"Not enough wheels remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= wheel_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to wheel assemble station
        self.bike_with_wheel_added_amount += 1

        # takes 1 from pedal assemble station
        self.bike_with_pedal_added_amount -= 1

        # updates their totals
        self.bike_with_pedal_added_amount_label.setText(str(self.bike_with_pedal_added_amount))
        self.bike_with_wheel_added_amount_label.setText(str(self.bike_with_wheel_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def gear_welding_station(self):
        self.alert = False
        found_item = None
        gear_cost = 0
        gear = self.bike_gear_chosen

        # checks that there is one wheel in the assembly station
        if self.bike_with_wheel_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a Bike with a wheel to continue.",
                                QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_gear_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the wheel part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "gear":
                found_item = item
                break

        # if there are no gears shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There are no gears remaining.", QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if gear.lower() == "standard gears":
            gear_cost = 1
        elif gear.lower() == "race gears":
            gear_cost = 2
        elif gear.lower() == "premium gears":
            gear_cost = 3

        # if there is not enough gears it displays this error message
        if found_item["Quantity"] < gear_cost:
            QMessageBox.warning(self, "Error", f"Not enough gears remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= gear_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to gear assemble station
        self.bike_with_gear_added_amount += 1

        # takes 1 away from wheel assemble station
        self.bike_with_wheel_added_amount -= 1

        # updates their totals
        self.bike_with_gear_added_amount_label.setText(str(self.bike_with_gear_added_amount))
        self.bike_with_wheel_added_amount_label.setText(str(self.bike_with_wheel_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def brake_welding_station(self):
        self.alert = False
        found_item = None
        brake_cost = 1
        brake = self.bike_brake_chosen

        # checks that there is one gear in the assembly station
        if self.bike_with_gear_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a bike with a gear to continue.",
                                QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_brake_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the brake part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "brake":
                found_item = item
                break

        # if there are no brakes shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There are no brakes remaining.",
                                QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if brake.lower() == "disc brakes":
            brake_cost = 1
        elif brake.lower() == "rim brakes":
            brake_cost = 2

        # if there is not enough brakes it displays this error message
        if found_item["Quantity"] < brake_cost:
            QMessageBox.warning(self, "Error", f"Not enough brakes remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= brake_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to brake assemble station
        self.bike_with_brake_added_amount += 1

        # tales 1 away from gear station
        self.bike_with_gear_added_amount -= 1

        # updates their totals
        self.bike_with_brake_added_amount_label.setText(str(self.bike_with_brake_added_amount))
        self.bike_with_gear_added_amount_label.setText(str(self.bike_with_gear_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def light_welding_station(self):
        self.alert = False

        found_item = None
        light_cost = 0
        light = self.bike_light_chosen

        # checks that there is one brake in the assembly station
        if self.bike_with_brake_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a Bike with a brake to continue.",
                                QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_light_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the light part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "light":
                found_item = item
                break

        # if there are no lights shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There are no lights remaining.", QMessageBox.StandardButton.Ok)
            return

        # assigns a different cost based on which choice the user for their bike
        if light.lower() == "standard lights":
            light_cost = 1
        elif light.lower() == "led lights":
            light_cost = 2
        elif light.lower() == "neon lights":
            light_cost = 3

        # if there is not enough lights it displays this error message
        if found_item["Quantity"] < light_cost:
            QMessageBox.warning(self, "Error", f"Not enough lights remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= light_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to light assemble station
        self.bike_with_light_added_amount += 1

        # takes 1 from brake assemble station
        self.bike_with_brake_added_amount -= 1

        # updates their totals
        self.bike_with_light_added_amount_label.setText(str(self.bike_with_light_added_amount))
        self.bike_with_brake_added_amount_label.setText(str(self.bike_with_brake_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def seat_welding_station(self):
        self.alert = False

        found_item = None
        seat_cost = 1

        # checks that there is one light in the assembly station
        if self.bike_with_light_added_amount < 1:
            QMessageBox.warning(self, "Error", f"You need a bike with lights to continue.",
                                QMessageBox.StandardButton.Ok)
            return

        # checks how many active orders there are so that no necessary parts are made
        active_orders = self.track_active_orders()
        if self.bike_with_seat_added_amount >= active_orders:
            QMessageBox.warning(self, "Error", "Limit Reached as there are no more current orders",
                                QMessageBox.StandardButton.Ok)
            return
        # loops through self.stock to find the seat part and assigns it to found_item
        for item in self.stock:
            if item["Part"].lower() == "seat":
                found_item = item
                break

        # if there are no seats shows the error message
        if found_item == None:
            QMessageBox.warning(self, "Error", f"There are no seats remaining.", QMessageBox.StandardButton.Ok)
            return

        # if there is not enough seats it displays this error message
        if found_item["Quantity"] < seat_cost:
            QMessageBox.warning(self, "Error", f"Not enough seats remaining", QMessageBox.StandardButton.Ok)
            return

        # takes the cost away from the quantity of the item
        found_item["Quantity"] -= seat_cost

        # updates the inventory table
        self.add_table_data()

        # adds 1 to seat assemble station
        self.bike_with_seat_added_amount += 1

        # takes 1 from light assemble station
        self.bike_with_light_added_amount -= 1

        # updates their total
        self.bike_with_seat_added_amount_label.setText(str(self.bike_with_seat_added_amount))
        self.bike_with_light_added_amount_label.setText(str(self.bike_with_light_added_amount))

        # checks for quantities > 3 to display red
        self.change_amount_colours()

    def change_amount_colours(self):

        amounts = [

            # stores the amounts in each station value and its label that displays it
            (self.bike_with_frame_added_amount, self.bike_with_frame_added_amount_label),
            (self.bike_with_fork_added_amount, self.bike_with_fork_added_amount_label),
            (self.bike_with_paint_added_amount, self.bike_with_paint_added_amount_label),
            (self.bike_with_pedal_added_amount, self.bike_with_pedal_added_amount_label),
            (self.bike_with_wheel_added_amount, self.bike_with_wheel_added_amount_label),
            (self.bike_with_gear_added_amount, self.bike_with_gear_added_amount_label),
            (self.bike_with_brake_added_amount, self.bike_with_brake_added_amount_label),
            (self.bike_with_light_added_amount, self.bike_with_light_added_amount_label),
            (self.bike_with_seat_added_amount, self.bike_with_seat_added_amount_label)]

        # loops through the list of tuples and if the amount value is more than or equal to 3 sets it to red
        for amount, label in amounts:
            if amount >= 3:
                label.setStyleSheet("color: red; font-weight: bold;")
            else:
                label.setStyleSheet("color: white;")

    def order_management_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # creates the title for the order management page
        label = QLabel("Order Management")
        label.setStyleSheet("font-size:40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        top_bar_layout.addWidget(label)

        # adds a back button
        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 100)
        back_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.main_page))
        top_bar_layout.addWidget(back_button)

        layout.addLayout(top_bar_layout)

        # creates an empty list for future orders
        self.order_list = []

        form = QFormLayout()

        # creates the box which allows to user to choose a bike model
        self.bike_model = QComboBox()
        self.bike_model.addItems(["BMX", "Mountain Bike", "Electric Bike", "Road Bike"])
        form.addRow("Model: ", self.bike_model)

        # creates the box which allows to user to choose a bike colour
        self.bike_colour = QComboBox()
        self.bike_colour.addItems(["Red", "Blue", "White", "Black", "Yellow", "Green"])
        form.addRow("Colour: ", self.bike_colour)

        # creates the box which allows to user to choose a bike wheel size
        self.bike_wheelSize = QComboBox()
        self.bike_wheelSize.addItems(["26 inches", "27.5 inches", "29 inches"])
        form.addRow("Wheel Size: ", self.bike_wheelSize)

        # creates the box which allows to user to choose a bike gear
        self.bike_gear = QComboBox()
        self.bike_gear.addItems(["Standard Gears", "Race Gears", "Premium Gears"])
        form.addRow("Gears: ", self.bike_gear)

        # creates the box which allows to user to choose a bike brake
        self.bike_brake = QComboBox()
        self.bike_brake.addItems(["Disc Brakes", "Rim Brakes"])
        form.addRow("Brakes: ", self.bike_brake)

        # creates the box which allows to user to choose a bike light
        self.bike_light = QComboBox()
        self.bike_light.addItems(["LED Lights", "Standard Lights", "Neon Lights"])
        form.addRow("Lights: ", self.bike_light)

        # creates the box which allows to user to input their name
        self.order_name = QLineEdit()
        form.addRow("Order Name: ", self.order_name)

        # creates the box which allows to user to input their contact number
        self.order_contact_number = QLineEdit()
        form.addRow("Contact Number: ", self.order_contact_number)

        # creates the box which allows to user to input their address
        self.order_delivery_address = QLineEdit()
        form.addRow("Delivery Address", self.order_delivery_address)

        # adds the form to the layout
        layout.addLayout(form)

        # creates the complete order button
        complete_order = QPushButton("Complete Order")
        complete_order.clicked.connect(self.complete_order)
        layout.addWidget(complete_order)

        # creates the table that shows the inputted order information
        self.table_of_orders = QTableWidget()
        self.table_of_orders.setColumnCount(9)
        self.table_of_orders.setHorizontalHeaderLabels(
            ["Model", "Colour", "Wheel Size", "Gears", "Brakes", "Lights", "Customer name", "Contact number",
             "Delivery Address"])
        layout.addWidget(self.table_of_orders)

        page.setLayout(layout)
        return page

    def complete_order(self):

        # stores the user's inputs as variables
        bike_model = self.bike_model.currentText()
        bike_colour = self.bike_colour.currentText()
        bike_wheel_size = self.bike_wheelSize.currentText()
        bike_gears = self.bike_gear.currentText()
        bike_brakes = self.bike_brake.currentText()
        bike_lights = self.bike_light.currentText()
        order_name = self.order_name.text()
        order_contact_number = self.order_contact_number.text()
        order_delivery_address = self.order_delivery_address.text()

        # if the user leaves some of their information blank it shows this error message
        if not order_name or not order_contact_number or not order_delivery_address:
            QMessageBox.warning(self, "Error", "Information cannot be empty!", QMessageBox.StandardButton.Ok)
            return

        # assign these variables to self for future use
        self.bike_model_chosen = bike_model
        self.bike_colour_chosen = bike_colour
        self.bike_wheelSize_chosen = bike_wheel_size
        self.bike_gear_chosen = bike_gears
        self.bike_brake_chosen = bike_brakes
        self.bike_light_chosen = bike_lights

        # saves the users order in a dictionary
        order = {

            "bike model": bike_model,
            "bike colour": bike_colour,
            "bike wheel size": bike_wheel_size,
            "bike gears": bike_gears,
            "bike brakes": bike_brakes,
            "bike lights": bike_lights,
            "order name": order_name,
            "contact number": order_contact_number,
            "delivery address": order_delivery_address
        }

        # adds their order to the empty list
        self.order_list.append(order)

        # displays the new order in the table
        self.add_order_to_table()

        # clears the inputted information for the next order
        self.order_contact_number.clear()
        self.order_name.clear()
        self.order_delivery_address.clear()

    def add_order_to_table(self):

        # adjust the tables row count so that all orders are included
        self.table_of_orders.setRowCount(len(self.order_list))

        # loops over each order in the list while storing its index and item
        for i, order in enumerate(self.order_list):
            # gets the variable assigned to "bike model" in the order dictionary
            bike_model = QTableWidgetItem(order["bike model"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 0, bike_model)

            # gets the variable assigned to "bike colour" in the order dictionary
            bike_colour = QTableWidgetItem(order["bike colour"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 1, bike_colour)

            # gets the variable assigned to "bike wheel" in the order dictionary
            bike_wheel_size = QTableWidgetItem(order["bike wheel size"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 2, bike_wheel_size)

            # gets the variable assigned to "bike gears" in the order dictionary
            bike_gears = QTableWidgetItem(order["bike gears"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 3, bike_gears)

            # gets the variable assigned to "bike brakes" in the order dictionary
            bike_brakes = QTableWidgetItem(order["bike brakes"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 4, bike_brakes)

            # gets the variable assigned to "bike lights" in the order dictionary
            bike_lights = QTableWidgetItem(order["bike lights"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 5, bike_lights)

            # gets the variable assigned to "order name" in the order dictionary
            order_name = QTableWidgetItem(order["order name"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 6, order_name)

            # gets the variable assigned to "contact number" in the order dictionary
            order_contact_number = QTableWidgetItem(order["contact number"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 7, order_contact_number)

            # gets the variable assigned to "delivery address" in the order dictionary
            order_delivery_address = QTableWidgetItem(order["delivery address"])
            # gets the current row of the order list with i and puts the variable value in the right column in the table
            self.table_of_orders.setItem(i, 8, order_delivery_address)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainScreen()
    main_window.show()
    sys.exit(app.exec())