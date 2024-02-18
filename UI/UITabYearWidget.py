from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from UI.GraphWidget import GraphWidget

class UITabYearWidget(QWidget):

    def __init__(self,yearProfitsForEachMonth,fontSize,dateFormat):
        super().__init__()
        self.yearProfitsForEachMonth = yearProfitsForEachMonth
        self.fontSize = fontSize
        self.dateFormat = dateFormat
        
        # -- Create the Matplotlib graphic for displaying the profits along the year --
        profitsBarGraph = GraphWidget(
            'bar',
            list(self.yearProfitsForEachMonth.keys()),
            list(self.yearProfitsForEachMonth.values()),
            'PnL per month (%)',
            self.fontSize,
            self.dateFormat
            )

        # create the horizontal layout (container) to organize the display of the widgets
        HLayout = QHBoxLayout()
        HLayout.addWidget(profitsBarGraph.canvas)

        # create the vertical layout (container) to organize the display of the widgets
        VLayout = QVBoxLayout()
        VLayout.addLayout(HLayout)
        
        # Set the vertical layout as the main layout for the widget
        self.setLayout(VLayout)
