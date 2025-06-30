import mplcursors
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.image as mplImage
from matplotlib.widgets import Button
from matplotlib.backends.backend_qt5agg import FigureCanvas

from PyQt5.QtWidgets import QWidget


class GraphWidget(QWidget):
    def __init__(
        self,
        graph_type,
        x_data,
        y_data,
        title,
        font_size,
        date_format,
        x_axis="",
        y_axis="",
        enable_zoom=False,
        enable_push_move=False,
        enable_cursor=False,
    ):
        super().__init__()
        self.graph_type = graph_type
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.font_size = font_size
        self.date_format = date_format
        self.is_pushed = None
        self.is_pushed_moving = None
        self.precedent_x_ref = None
        self.precedent_y_ref = None
        self.x_ref = None
        self.y_ref = None
        self.relative_x_ref = None
        self.relative_y_ref = None
        self.recenter_x = 0.9
        self.recenter_y = 0.9
        self.enable_zoom = enable_zoom
        self.enable_push_move = enable_push_move
        self.enable_cursor = enable_cursor

        # load picture of the recenter icon
        self.recenter_icon = mplImage.imread("picture/recenter_icon.png")

        # create figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        # create a Matplotlib canevas to display the graphic inside the graphic interface.
        # Link between matplotlib and PyQt
        self.canvas = FigureCanvas(self.figure)

        # create the graph
        self.ax = self.figure.add_subplot(111)
        if self.graph_type == "plot":
            self.ax.plot(self.x_data, self.y_data)
        elif self.graph_type == "bar":
            x_neg_data = [
                self.x_data[index]
                for index, value in enumerate(self.y_data)
                if value < 0
            ]
            x_pos_data = [
                self.x_data[index]
                for index, value in enumerate(self.y_data)
                if value >= 0
            ]
            y_neg_data = [value for value in self.y_data if value < 0]
            y_pos_data = [value for value in self.y_data if value >= 0]
            self.ax.bar(x_neg_data, y_neg_data, color="red")
            self.ax.bar(x_pos_data, y_pos_data, color="green")
            for x, y in zip(x_neg_data, y_neg_data):
                self.ax.annotate(
                    str(round(y, 2)) + "%",
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, -12),
                    ha="center",
                )
            for x, y in zip(x_pos_data, y_pos_data):
                self.ax.annotate(
                    str(round(y, 2)) + "%",
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, 5),
                    ha="center",
                )

        if self.x_axis != "":
            self.ax.set_xlabel(self.x_axis)
        if self.y_axis != "":
            self.ax.set_ylabel(self.y_axis)
        self.ax.set_title(self.title)

        # define properties of axis
        self.ax.xaxis.set_tick_params(labelsize=self.font_size)

        self.recenter_x = self.ax.get_xlim()[0]
        self.recenter_y = self.ax.get_ylim()[0]

        # enable zoom (connect scroll_event to on_scroll method
        if self.enable_zoom:
            self.canvas.mpl_connect("scroll_event", self.on_scroll)
        # enable PushMove
        if self.enable_push_move:
            self.canvas.mpl_connect("button_press_event", self.on_push)
            self.canvas.mpl_connect("button_release_event", self.on_release)
            self.canvas.mpl_connect("motion_notify_event", self.on_push_move)
        # define a cursor
        if self.enable_cursor:
            self.cursor = mplcursors.cursor(self.ax)
            self.cursor.connect("add", self.on_plot_hover)

    def on_plot_hover(self, sel):
        showLabel = not self.is_pushed_moving
        x = sel.target[0]
        y = sel.target[1]

        if self.graph_type == "plot":
            x_date = mdates.num2date(x).strftime(self.date_format)
            sel.annotation.set_text(f"({x_date}, {y:.2f})")
        elif self.graph_type == "bar":
            x_date = x
            sel.annotation.set_text(f"({x_date:.0f}, {y:.2f})")

        sel.annotation.set_visible(showLabel)
        if self is not None and hasattr(self, "cursor"):
            self.canvas.draw_idle()

    def add_curve(self, x_data, y_data):
        # add another curve
        ax = self.canvas.figure.axes[0]  # existant axis
        ax.plot(x_data, y_data)

        # connect the cursor label to the new data points
        cursor = mplcursors.cursor(ax)
        cursor.connect("add", self.on_plot_hover)
        self.canvas.draw()  # update canvas

    def on_scroll(self, event):
        # manage the zoom
        ax = self.canvas.figure.axes[0]
        zoom_boost = 0.04
        x_cursor = event.xdata
        y_cursor = event.ydata
        # zoom out
        if event.button == "up":
            ax.set_xlim(
                x_cursor - (1 + zoom_boost) * (x_cursor - ax.get_xlim()[0]),
                x_cursor + (1 + zoom_boost) * (ax.get_xlim()[1] - x_cursor),
            )
            ax.set_ylim(
                y_cursor - (1 + zoom_boost) * (y_cursor - ax.get_ylim()[0]),
                y_cursor + (1 + zoom_boost) * (ax.get_ylim()[1] - y_cursor),
            )
        # zoom in
        elif event.button == "down":
            ax.set_xlim(
                x_cursor - (1 - zoom_boost) * (x_cursor - ax.get_xlim()[0]),
                x_cursor + (1 - zoom_boost) * (ax.get_xlim()[1] - x_cursor),
            )
            ax.set_ylim(
                y_cursor - (1 - zoom_boost) * (y_cursor - ax.get_ylim()[0]),
                y_cursor + (1 - zoom_boost) * (ax.get_ylim()[1] - y_cursor),
            )

        if self is not None:
            self.canvas.draw_idle()

    def on_push(self, event):
        if not self.is_pushed or (
            self.x_ref == self.precedent_x_ref and self.y_ref == self.precedent_y_ref
        ):
            # second condition update the ref a the current cursor position after a short break without release
            ax = event.inaxes
            self.x_ref = event.xdata
            self.y_ref = event.ydata

            # to have the same ref position regarless of the xlim and y lim
            self.relative_x_ref = (self.x_ref - ax.get_xlim()[0]) / (
                ax.get_xlim()[1] - ax.get_xlim()[0]
            )
            self.relative_y_ref = (self.y_ref - ax.get_ylim()[0]) / (
                ax.get_ylim()[1] - ax.get_ylim()[0]
            )
            self.is_pushed = True
            if (
                self.x_ref == self.precedent_x_ref
                and self.y_ref == self.precedent_y_ref
            ):
                self.is_pushed_moving = True

    def on_release(self, event):
        self.is_pushed = False
        self.is_pushed_moving = False

    def on_push_move(self, event):
        move_modulate = 0.05

        if event.inaxes and self.is_pushed:
            self.is_pushed_moving = True

            ax = event.inaxes

            x_cursor = event.xdata
            y_cursor = event.ydata

            dx_cursor = (self.x_ref - x_cursor) * move_modulate
            dy_cursor = (self.y_ref - y_cursor) * move_modulate

            ax.set_xlim(ax.get_xlim() + dx_cursor)
            ax.set_ylim(ax.get_ylim() + dy_cursor)

            self.precedent_x_ref = self.x_ref
            self.precedent_y_ref = self.y_ref

            self.x_ref = (
                self.relative_x_ref * (ax.get_xlim()[1] - ax.get_xlim()[0])
                + ax.get_xlim()[0]
            )
            self.y_ref = (
                self.relative_y_ref * (ax.get_ylim()[1] - ax.get_ylim()[0])
                + ax.get_ylim()[0]
            )

            if self is not None:
                self.canvas.draw_idle()

    def drawRecenterIcon(self):
        position = self.ax.get_position()
        x0 = position.x0
        y0 = position.y0
        width = position.width
        height = position.height
        x_right_upon_corner = x0 + width
        y_right_upon_corner = y0 + height

        ax_recenter_icon = self.figure.add_axes(
            [x_right_upon_corner - 0.025, y_right_upon_corner - 0.035, 0.025, 0.035]
        )
        recenter_icon = Button(ax_recenter_icon, "Autoscale")

        self.canvas.draw_idle()

        recenter_icon.on_clicked(self.autoscale)

    def autoscale(self):
        # autoscale of the graph
        ax = self.canvas.figure.axes[0]
        ax.relim()
        ax.autoscale_view()
        self.canvas.draw_idle()
