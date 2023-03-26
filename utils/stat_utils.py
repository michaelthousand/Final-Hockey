from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, QToolBar

WINDOW_SIZE = 700

class StatViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Manager - View Stats")
        self.setBaseSize(WINDOW_SIZE, WINDOW_SIZE)

        layout = QGridLayout()
        layout.addWidget(QLabel("<h1>Ice Manager - View Stats</h1>"), 0, 0, 1, 5)
        layout.addWidget(QLabel("<p>Here you can view stats for individual players, team leaders, or the team as a whole.</p>"), 1, 0, 1, 5)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self._createToolBar()

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)
