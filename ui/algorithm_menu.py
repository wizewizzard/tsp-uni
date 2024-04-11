from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout,QPushButton

class AlgorithmMenu(QWidget):
    def __init__(self,cfg, parent=None):
        super().__init__(parent)

        self.parent = parent
        layout = QVBoxLayout()
        all_paths = QPushButton(cfg['text']['all_paths_btn_text'])
        all_paths.clicked.connect(self.calc_all_paths)
        layout.addWidget(all_paths)
        brute_force_button = QPushButton(cfg['text']['bruteforce_btn_text'])
        brute_force_button.clicked.connect(self.calc_with_brute_force)
        layout.addWidget(brute_force_button)
        greedy_button = QPushButton(cfg['text']['greedy_btn_text'])
        greedy_button.clicked.connect(self.calc_with_greedy_search)
        layout.addWidget(greedy_button)

        self.setLayout(layout)


    def calc_all_paths(self):
        self.parent.calc_all_paths()

    def calc_with_brute_force(self):
        self.parent.calc_with_brute_force()

    def calc_with_greedy_search(self):
        self.parent.calc_with_greedy_search()