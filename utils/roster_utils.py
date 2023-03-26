import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, QToolBar, QComboBox, QLineEdit, QPushButton, QScrollArea, QVBoxLayout
from utils.db_utils import add_player, add_db, add_roster_table, view_all


WINDOW_SIZE = 700

class RosterViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Manager - Roster")
        self.setBaseSize(WINDOW_SIZE, WINDOW_SIZE)
        # Default year - can be updated as appropriate
        self.selected_year = '2022-23'
        # Sets the secondary window default
        self.w = None

        layout = QGridLayout()
        layout.addWidget(QLabel("<h1>Ice Manager - Roster</h1>"), 0, 0, 1, 5)
        layout.addWidget(QLabel("<p>Here you can view and update your roster, change your lineup, and make keep track of any roster notes.</p>"), 1, 0, 1, 5)
        
        self.year_dropdown = QComboBox()
        self.year_dropdown.addItems(['2022-23', '2023-24', '2024-25'])
        self.year_dropdown.currentIndexChanged.connect(self.year_selection)
        layout.addWidget(QLabel("<p>Select Year:</p>"), 2,0)
        layout.addWidget(self.year_dropdown, 2, 1)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("save files/test.db") # If this works, I'll need to change the file name at some point
        if not db.open():
            print("Could not open database")

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self._createToolBar()

         
        scroll = QScrollArea()
        layout.addWidget(scroll, 3, 0, 1, 5)

        # Create a vertical layout to add the labels to the scrollable area
        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        v_layout.setSpacing(10)
        v_layout.setContentsMargins(10, 10, 10, 10)

        # Get all the entries from the database table
        query = QSqlQuery(f"SELECT * FROM 'roster_{self.selected_year.replace('-', '_')}'", db=db)
        forward_label = QLabel(f"Forwards:")
        forward_label.setStyleSheet("font-size: 24px;")
        v_layout.addWidget(forward_label)
        while query.next():
            if query.value('position') == 'C' or query.value('position') == 'LW' or query.value('position') == 'RW':
                # Create a label for each entry and add it to the vertical layout
                label = QLabel(f"#{query.value('number')} - {query.value('first_name')} {query.value('last_name')} - {query.value('position')}")
                label.setStyleSheet("font-size: 18px;")
                v_layout.addWidget(label)

        query = QSqlQuery(f"SELECT * FROM 'roster_{self.selected_year.replace('-', '_')}'", db=db)
        defense_label = QLabel(f"Defense:")
        defense_label.setStyleSheet("font-size: 24px;")
        v_layout.addWidget(defense_label)
        while query.next():
            if query.value('position') == 'LD' or query.value('position') == 'RD':
                # Create a label for each entry and add it to the vertical layout
                label = QLabel(f"#{query.value('number')} - {query.value('first_name')} {query.value('last_name')} - {query.value('position')}")
                label.setStyleSheet("font-size: 18px;")
                v_layout.addWidget(label)

        query = QSqlQuery(f"SELECT * FROM 'roster_{self.selected_year.replace('-', '_')}'", db=db)
        goalie_label = QLabel(f"Goalies:")
        goalie_label.setStyleSheet("font-size: 24px;")
        v_layout.addWidget(goalie_label)
        while query.next():
            if query.value('position') == 'G':
                # Create a label for each entry and add it to the vertical layout
                label = QLabel(f"#{query.value('number')} - {query.value('first_name')} {query.value('last_name')} - {query.value('position')}")
                label.setStyleSheet("font-size: 18px;")
                v_layout.addWidget(label)

        # Add the vertical layout to the scrollable area
        scroll_widget = QWidget()
        scroll_widget.setLayout(v_layout)
        scroll.setWidget(scroll_widget)


    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Add Player", self.add_player)
        tools.addAction("Update Player", self.update_player)
        tools.addAction("Set Lineup", self.set_lineup)
        tools.addAction("Roster Notes", self.roster_notes)
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)
    
    def add_player(self):
        if self.w is None:
            self.w = AddPlayerWindow(self.selected_year)
        self.w.show()
    
    def update_player(self, checked):
        # I'll want to add something here for deleting the player
        pass

    def set_lineup(self, checked):
        pass

    def roster_notes(self, checked):
        pass

    def year_selection(self, i):
        self.selected_year = self.year_dropdown.currentText()

# Add player window
class AddPlayerWindow(QWidget):
    def __init__(self, selected_year):
        super().__init__()
        self.selected_year = selected_year
        layout = QGridLayout()

        self.label = layout.addWidget(QLabel(f"<h2>Add New Player ({selected_year})</h2>"), 0, 0, 1, 5)

        self.first_label = layout.addWidget(QLabel('<p>First name:</p>'), 1, 0)
        self.first_name = QLineEdit(self)
        layout.addWidget(self.first_name, 1, 1)

        self.last_label = layout.addWidget(QLabel('<p>Last name:</p>'), 2, 0)
        self.last_name = QLineEdit(self)
        layout.addWidget(self.last_name, 2, 1)

        self.number_label = layout.addWidget(QLabel('<p>Number:</p>'), 3, 0)
        self.number = QLineEdit(self)
        layout.addWidget(self.number, 3, 1)

        self.position_label = layout.addWidget(QLabel('<p>Position:</p>'), 4, 0)
        self.position = QLineEdit(self)
        layout.addWidget(self.position, 4, 1)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(lambda: self.add_new_player(self.first_name.text(), self.last_name.text(), self.number.text(), self.position.text(), self.selected_year))
        layout.addWidget(self.submit_button, 5, 0, 1, 2)

        self.setLayout(layout)

        # Need to add a check to make sure all fields are filled
    def add_new_player(self, first_name, last_name, number, position, selected_year):
        file = 'test' # NEEDS TO BE REPLACED AFTER TESTING
        selected_year = selected_year.replace('-','_')
        add_db(file)
        add_roster_table(file, selected_year)
        add_player(file, first_name, last_name, number, position, selected_year)
        