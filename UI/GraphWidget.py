import mplcursors
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.image as mplImage
from matplotlib.widgets import Button
from matplotlib.backends.backend_qt5agg import FigureCanvas

from PyQt5.QtWidgets import QWidget
    
class GraphWidget(QWidget):
    def __init__(self,graphType,xData,yData,title,fontSize,dateFormat,xAxis='',yAxis='',enableZoom = False, enablePushMove = False):
        super().__init__()
        self.graphType = graphType
        self.xData = xData
        self.yData = yData
        self.title = title
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.fontSize = fontSize
        self.dateFormat = dateFormat
        self.isPushed = None
        self.isPushedMoving = None 
        self.precedentxRef = None
        self.precedentxRef = None
        self.xRef = None
        self.yRef = None
        self.relativexRef = None
        self.relativeyRef = None
        self.recenterX = 0.9
        self.recenterY = 0.9
        self.enableZoom = enableZoom
        self.enablePushMove = enablePushMove
        # load picture of the recenter icon
        self.recenterIcon = mplImage.imread('picture/recenter_icon.png')

        # create figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        # create a Matplotlib canevas to display the graphic inside the graphic interface.
        # Link between matplotlib and PyQt
        self.canvas = FigureCanvas(self.figure)

        # create the graph
        self.ax = self.figure.add_subplot(111)
        if self.graphType=='plot':
            self.ax.plot(self.xData,self.yData)
        elif self.graphType=='bar':
            xNegData = [self.xData[index] for index,value in enumerate(self.yData) if value <= 0]
            xPosData = [self.xData[index] for index,value in enumerate(self.yData) if value > 0]
            yNegData = [value for value in self.yData if value <= 0]
            yPosData = [value for value in self.yData if value > 0]
            self.ax.bar(xNegData,yNegData,color = 'red')
            self.ax.bar(xPosData,yPosData,color = 'green')

        if self.xAxis != '':
            self.ax.set_xlabel(self.xAxis)
        if self.yAxis != '':
            self.ax.set_ylabel(self.yAxis)
        self.ax.set_title(self.title)

        # define properties of axis
        self.ax.xaxis.set_tick_params(labelsize = self.fontSize)

        self.recenterX = self.ax.get_xlim()[0]
        self.recenterY = self.ax.get_ylim()[0]
        
        # enable zoom (connect scroll_event to onScroll method
        if self.enableZoom :
            self.canvas.mpl_connect('scroll_event', self.onScroll)
        # enable PushMove
        if self.enablePushMove :
            self.canvas.mpl_connect('button_press_event', self.onPush)
            self.canvas.mpl_connect('button_release_event', self.onRelease)
            self.canvas.mpl_connect('motion_notify_event', self.onPushMove)
        # define a cursor
        self.cursor = mplcursors.cursor(self.ax)
        self.cursor.connect("add", self.onPlotHover)

    def onPlotHover(self,sel):
        showLabel = not self.isPushedMoving
        x = sel.target[0]
        y = sel.target[1]

        if self.graphType=='plot':
            x_date = mdates.num2date(x).strftime(self.dateFormat)
            sel.annotation.set_text(f"({x_date}, {y:.2f})")
        elif self.graphType=='bar':
            x_date = x
            sel.annotation.set_text(f"({x_date:.0f}, {y:.2f})")

        sel.annotation.set_visible(showLabel)
        if self != None and hasattr(self, 'cursor'):
            self.canvas.draw_idle()

    def addCurve(self, xData, yData):
        # add another curve
        ax = self.canvas.figure.axes[0]  # existant axis
        ax.plot(xData, yData)

        # connect the cursor label to the new data points
        cursor = mplcursors.cursor(ax)
        cursor.connect("add", self.onPlotHover)
        self.canvas.draw()  # update canvas

    def onScroll(self, event):
        # manage the zoom
        ax = self.canvas.figure.axes[0]
        zoomBoost = 0.04
        xCursor = event.xdata
        yCursor = event.ydata
        # zoom out
        if event.button == 'up':
            ax.set_xlim(xCursor - (1 + zoomBoost) * (xCursor - ax.get_xlim()[0]),xCursor + (1 + zoomBoost) * (ax.get_xlim()[1] - xCursor))
            ax.set_ylim(yCursor - (1 + zoomBoost) * (yCursor - ax.get_ylim()[0]),yCursor + (1 + zoomBoost) * (ax.get_ylim()[1] - yCursor))
        # zoom in
        elif event.button == 'down':
            ax.set_xlim(xCursor - (1 - zoomBoost) * (xCursor - ax.get_xlim()[0]),xCursor + (1 - zoomBoost) * (ax.get_xlim()[1] - xCursor))
            ax.set_ylim(yCursor - (1 - zoomBoost) * (yCursor - ax.get_ylim()[0]),yCursor + (1 - zoomBoost) * (ax.get_ylim()[1] - yCursor))

        if self != None :
            self.canvas.draw_idle()


    def onPush(self,event):
        print(self.isPushedMoving)
        if not self.isPushed or (self.xRef == self.precedentxRef and self.yRef == self.precedentyRef) :
            # second condition update the ref a the current cursor position after a short break without release
            ax = event.inaxes
            self.xRef = event.xdata
            self.yRef = event.ydata

            # to have the same ref position regarless of the xlim and y lim
            self.relativexRef = (self.xRef - ax.get_xlim()[0]) / (ax.get_xlim()[1] - ax.get_xlim()[0])
            self.relativeyRef = (self.yRef - ax.get_ylim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
            self.isPushed = True
            if self.xRef == self.precedentxRef and self.yRef == self.precedentyRef :
                self.isPushedMoving = True
            

    def onRelease(self,event):
        self.isPushed = False
        self.isPushedMoving = False

    def onPushMove(self,event):
        moveModulate = 0.05
        
        if event.inaxes and self.isPushed :
            self.isPushedMoving = True
            
            ax = event.inaxes
    
            xCursor = event.xdata
            yCursor = event.ydata

            dxCursor = (self.xRef - xCursor) * moveModulate
            dyCursor = (self.yRef - yCursor) * moveModulate
        
            ax.set_xlim(ax.get_xlim() + dxCursor)
            ax.set_ylim(ax.get_ylim() + dyCursor)

            self.precedentxRef = self.xRef
            self.precedentyRef = self.yRef

            self.xRef = self.relativexRef * (ax.get_xlim()[1] - ax.get_xlim()[0]) + ax.get_xlim()[0]
            self.yRef = self.relativeyRef * (ax.get_ylim()[1] - ax.get_ylim()[0]) + ax.get_ylim()[0]

            if self != None :
                self.canvas.draw_idle()
                
            
    def drawRecenterIcon(self):
        position = self.ax.get_position()
        x0 = position.x0
        y0 = position.y0
        width = position.width
        height = position.height
        xRightUponCorner = x0 + width
        yRightUponCorner = y0 + height
        
        axRecenterIcon = self.figure.add_axes([xRightUponCorner - 0.025, yRightUponCorner - 0.035, 0.025, 0.035])
        RecenterIcon = Button(axRecenterIcon, 'Autoscale')

        self.canvas.draw_idle()

        RecenterIcon.on_clicked(self.autoscale)

    def autoscale(self):
        # autoscale of the graph
        ax = self.canvas.figure.axes[0]
        ax.relim()
        ax.autoscale_view()
        self.canvas.draw_idle()

