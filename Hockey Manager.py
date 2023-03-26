import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QToolBar, QLabel, QPushButton, QVBoxLayout
from utils.roster_utils import RosterViewWindow
from utils.game_utils import GameViewWindow
from utils.stat_utils import StatViewWindow

# Fixed window size
WINDOW_SIZE = 700

# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Ice Manager - Home")
        self.setBaseSize(WINDOW_SIZE, WINDOW_SIZE)

        layout = QGridLayout()
        layout.addWidget(QLabel("<h1>Ice Manager</h1>"), 0, 0, 1, 5)
        layout.addWidget(QLabel("<p>This app allows you to track roster changes, set lineups, monitor live games, view advanced statistics, and more!</p>"), 1, 0, 1, 5)
        
        roster_button = QPushButton("Roster")
        roster_button.setFixedSize(150, 150)
        roster_button.clicked.connect(self.roster_view)
        layout.addWidget(roster_button, 3, 0)

        game_button = QPushButton("Live Game")
        game_button.setFixedSize(150, 150)
        game_button.clicked.connect(self.game_view)
        layout.addWidget(game_button, 3, 2)

        stats_button = QPushButton("View Stats")
        stats_button.setFixedSize(150, 150)
        stats_button.clicked.connect(self.stats_view)
        layout.addWidget(stats_button, 3, 4)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #self._createMenu()
        self._createToolBar()
    
    # Not currently using
    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def roster_view(self, checked):
        self.w = RosterViewWindow()
        self.w.show()

    def game_view(self, checked):
        self.w = GameViewWindow()
        self.w.show()

    def stats_view(self, checked):
        self.w = StatViewWindow()
        self.w.show()


# Defines the application's main function
def main():
    mainApp = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(mainApp.exec())

# Calls the main function
if __name__ == "__main__":
    main()