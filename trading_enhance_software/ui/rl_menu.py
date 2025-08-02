from PyQt5 import QtWidgets, QtCore
from trading_enhance_software.ui.code_editor import CodeEditor
from trading_enhance_software.ui.highlighter.py_highlight import PythonHighlighter
import subprocess
import os
from trading_enhance_software.utils.google_cloud_utils import GoogleCloudTrainer
from rl_finance_framework import one_asset_trading, multiple_asset_management

class UIRLMenu(QtWidgets.QWidget):
    """User interface for the Reinforcement Learning menu.

    Args:
        QtWidgets (_type_): 
    """
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

        cd = os.getcwd()
        parent_cd = os.path.dirname(cd)
        self.google_cloud_trainer = GoogleCloudTrainer(parent_cd + "/trading-enhance-software-pog-admin.json")

    def start_training_one_asset(self):
        """start the training of the one asset RL algorithm.
        """

        project_id = "trading-enhance-software"
        bucket_name = "trading-enhance-software-one-asset"
        trainer_blob_name = "code/trainer_one_asset.tar.gz"
        region = "europe-west1"
        local_training_code_directory = "rl_finance_framework"
        display_name = "training-one-asset-rl"
        code_entry_point = "one_asset_trading"

        self.google_cloud_trainer.set_bucket_lifecycle(bucket_name)

        self.google_cloud_trainer.upload_training_package(local_training_code_directory, bucket_name, trainer_blob_name)
        
        self.google_cloud_trainer.submit_vertex_job(project_id, region, bucket_name, trainer_blob_name,display_name,code_entry_point)

    def start_training_multi_asset(self):
        """start the training of the multi asset RL algorithm.
        """
        cd = os.getcwd()
        command = [
            "python",
            cd + "/multiple_asset_management.py",
            "--alg=ddpg",
            "--env=RLStock-v0",
            "--network=MlpPolicy",
            "--num_timesteps=1e4",
            "--log_path=" + cd + "/strategies/RL_strat",
        ]

        result = subprocess.run(command)
