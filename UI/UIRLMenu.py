from PyQt5 import QtWidgets, QtCore
from UI.CodeEditor import CodeEditor
from UI.highlighter.pyHighlight import PythonHighlighter
import subprocess
import os
    
class UIRLMenu(QtWidgets.QWidget):
    def __init__(self,strategies_path):
        super().__init__()

        self.strategies_path = strategies_path
        
        # configure the main window
        self.setWindowTitle('Build your own RL environment')

        mainLayout = QtWidgets.QVBoxLayout()
        labelCodeEditor = QtWidgets.QLabel("Python Code For Your Reinforcement Learning Environment")
        editorLayout = QtWidgets.QHBoxLayout()
        self.editor = CodeEditor()
        self.editor.load_RL_code() 
        self.highlighter = PythonHighlighter(self.editor.document())
        self.editor.show()
        self.buttonOK = QtWidgets.QPushButton('train the RL-algorithm')
        self.buttonOK.clicked.connect(self.startTrainingMultiAsset)
        self.buttonOK.setFixedSize(180, 30)
        self.buttonOKOneAsset = QtWidgets.QPushButton('train the one asset RL-algorithm')
        self.buttonOKOneAsset.clicked.connect(self.startTrainingOneAsset)
        self.buttonOKOneAsset.setFixedSize(220, 30)
        layoutButton = QtWidgets.QHBoxLayout()

        editorLayout.addWidget(self.editor)
        layoutButton.addWidget(self.buttonOK)
        layoutButton.addWidget(self.buttonOKOneAsset)
        mainLayout.addWidget(labelCodeEditor, alignment=QtCore.Qt.AlignCenter)
        mainLayout.addLayout(editorLayout)
        mainLayout.addLayout(layoutButton)
        
        # put sub widgets inside the main widget
        self.setLayout(mainLayout)
        self.adjustSize()

    def startTrainingOneAsset(self):
        cd = os.getcwd()
        command = [
            "python",
            cd+"/RLTraining/oneAssetTrading.py"]

        result = subprocess.run(command)

    def startTrainingMultiAsset(self):
        cd = os.getcwd()
        command = [
            "python",
            cd+"/RLTraining/multipleAssetManagement.py",
            "--alg=ddpg",
            "--env=RLStock-v0",
            "--network=MlpPolicy",
            "--num_timesteps=1e4",
            "--log_path="+cd+"/strategies/RL_strat"]

        result = subprocess.run(command)

    
