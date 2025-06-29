from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from trading_enhance_software.ui.graph_widget import GraphWidget


class UITabYearWidget(QWidget):
    def __init__(self, year_profits_for_each_month, font_size, date_format):
        super().__init__()
        self.year_profits_for_each_month = year_profits_for_each_month
        self.font_size = font_size
        self.date_format = date_format

        # -- Create the Matplotlib graphic for displaying the profits along the year --
        profits_bar_graph = GraphWidget(
            "bar",
            list(self.year_profits_for_each_month.keys()),
            list(self.year_profits_for_each_month.values()),
            "PnL per month (%)",
            self.font_size,
            self.date_format,
        )

        # create the horizontal layout (container) to organize the display of the widgets
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(profits_bar_graph.canvas)

        # create the vertical layout (container) to organize the display of the widgets
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout)

        # Set the vertical layout as the main layout for the widget
        self.setLayout(vertical_layout)
