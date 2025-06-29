from PyQt5 import QtWidgets, QtCore
from trading_enhance_software.ui.code_editor import CodeEditor
from trading_enhance_software.ui.highlighter.py_highlight import PythonHighlighter
import subprocess
import os


class UIRLMenu(QtWidgets.QWidget):
    def __init__(self, strategies_path):
        super().__init__()

        self.strategies_path = strategies_path

        # configure the main window
        self.setWindowTitle("Build your own RL environment")

        main_layout = QtWidgets.QVBoxLayout()
        label_code_editor = QtWidgets.QLabel(
            "Python Code For Your Reinforcement Learning Environment"
        )
        editor_layout = QtWidgets.QHBoxLayout()
        self.editor = CodeEditor()
        self.editor.load_RL_code()
        self.highlighter = PythonHighlighter(self.editor.document())
        self.editor.show()
        self.button_ok = QtWidgets.QPushButton("train the RL-algorithm")
        self.button_ok.clicked.connect(self.start_training_multi_asset)
        self.button_ok.setFixedSize(180, 30)
        self.button_ok_one_asset = QtWidgets.QPushButton(
            "train the one asset RL-algorithm"
        )
        self.button_ok_one_asset.clicked.connect(self.start_training_one_asset)
        self.button_ok_one_asset.setFixedSize(220, 30)
        layout_button = QtWidgets.QHBoxLayout()

        editor_layout.addWidget(self.editor)
        layout_button.addWidget(self.button_ok)
        layout_button.addWidget(self.button_ok_one_asset)
        main_layout.addWidget(label_code_editor, alignment=QtCore.Qt.AlignCenter)
        main_layout.addLayout(editor_layout)
        main_layout.addLayout(layout_button)

        # put sub widgets inside the main widget
        self.setLayout(main_layout)
        self.adjustSize()

    def start_training_one_asset(self):
        cd = os.getcwd()
        command = ["python", cd + "/RLTraining/oneAssetTrading.py"]

        result = subprocess.run(command)

    def start_training_multi_asset(self):
        cd = os.getcwd()
        command = [
            "python",
            cd + "/RLTraining/multipleAssetManagement.py",
            "--alg=ddpg",
            "--env=RLStock-v0",
            "--network=MlpPolicy",
            "--num_timesteps=1e4",
            "--log_path=" + cd + "/strategies/RL_strat",
        ]

        result = subprocess.run(command)
