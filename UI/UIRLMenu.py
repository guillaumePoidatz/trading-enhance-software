from PyQt5 import QtWidgets, QtCore
from UI.CodeEditor import CodeEditor
from UI.highlighter.pyHighlight import PythonHighlighter
from RLTraining.run import run
    
class UIRLMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
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
        self.buttonOK.setFixedSize(180, 30)
        
        editorLayout.addWidget(self.editor)
        
        mainLayout.addWidget(labelCodeEditor, alignment=QtCore.Qt.AlignCenter)
        mainLayout.addLayout(editorLayout)
        mainLayout.addWidget(self.buttonOK,alignment=QtCore.Qt.AlignCenter)
        
        # put sub widgets inside the main widget
        self.setLayout(mainLayout)
        self.adjustSize()

    def startTraining():
        run()
        
        
