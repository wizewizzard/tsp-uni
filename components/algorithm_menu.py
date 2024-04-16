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
        dp_button = QPushButton(cfg['text']['dp_btn_text'])
        dp_button.clicked.connect(self.calc_with_dynamic_programming)
        layout.addWidget(dp_button)
        branch_and_bound_btn = QPushButton(cfg['text']['branch_and_bound_btn_text'])
        branch_and_bound_btn.clicked.connect(self.calc_with_branch_and_bound)
        layout.addWidget(branch_and_bound_btn)

        self.setLayout(layout)


    def calc_all_paths(self):
        self.parent.calc_all_paths()

    def calc_with_brute_force(self):
        self.parent.calc_with_brute_force()

    def calc_with_greedy_search(self):
        self.parent.calc_with_greedy_search()

    def calc_with_dynamic_programming(self):
        self.parent.calc_with_dynamic_programming()

    def calc_with_branch_and_bound(self):
        self.parent.calc_with_branch_and_bound()