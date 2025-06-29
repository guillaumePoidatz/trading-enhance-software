"""
https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html#the-linenumberarea-class
https://doc.qt.io/qtforpython/examples/example_widgets__codeeditor.html
"""

from PyQt5 import QtCore, QtGui, QtWidgets

DARK_BLUE = QtGui.QColor(118, 150, 185)


class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self._code_editor = editor

    def sizeHint(self):
        return QtCore.QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_editor.lineNumberAreaPaintEvent(event)


class CodeTextEdit(QtWidgets.QPlainTextEdit):
    is_first = False
    pressed_keys = list()

    indented = QtCore.pyqtSignal(object)
    unindented = QtCore.pyqtSignal(object)
    commented = QtCore.pyqtSignal(object)
    uncommented = QtCore.pyqtSignal(object)

    def __init__(self):
        super(CodeTextEdit, self).__init__()

        self.indented.connect(self.do_indent)
        self.unindented.connect(self.undo_indent)
        self.commented.connect(self.do_comment)
        self.uncommented.connect(self.undo_comment)

    def clear_selection(self):
        """
        Clear text selection on cursor
        """
        pos = self.textCursor().selectionEnd()
        self.textCursor().movePosition(pos)

    def get_selection_range(self):
        """
        Get text selection line range from cursor
        Note: currently only support continuous selection

        :return: (int, int). start line number and end line number
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return 0, 0

        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()

        cursor.setPosition(start_pos)
        start_line = cursor.blockNumber()
        cursor.setPosition(end_pos)
        end_line = cursor.blockNumber()

        return start_line, end_line

    def remove_line_start(self, string, line_number):
        """
        Remove certain string occurrence on line start

        :param string: str. string pattern to remove
        :param line_number: int. line number
        """
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        if text.startswith(string):
            cursor.removeSelectedText()
            cursor.insertText(text.split(string, 1)[-1])

    def insert_line_start(self, string, line_number):
        """
        Insert certain string pattern on line start

        :param string: str. string pattern to insert
        :param line_number: int. line number
        """
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
        self.setTextCursor(cursor)
        self.textCursor().insertText(string)

    def keyPressEvent(self, event):
        """
        Extend the key press event to create key shortcuts
        """
        self.is_first = True
        self.pressed_keys.append(event.key())
        start_line, end_line = self.get_selection_range()

        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            cursor = self.textCursor()
            current_line_number = cursor.blockNumber()
            indentation = self.get_line_indentation(current_line_number)
            line_text = self.get_line_text(current_line_number)

            if line_text.endswith(":"):
                indentation += "\t"
            cursor.insertText("\n" + indentation)

            return

        super(CodeTextEdit, self).keyPressEvent(event)

    def get_line_indentation(self, line_number):
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
        text = cursor.block().text()
        indentation = len(text) - len(text.lstrip())
        return text[:indentation]

    def get_line_text(self, line_number):
        cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
        return cursor.block().text()

    def keyReleaseEvent(self, event):
        """
        Extend the key release event to catch key combos
        """
        if self.is_first:
            self.process_multi_keys(self.pressed_keys)

        self.is_first = False
        self.pressed_keys.pop()
        super(CodeTextEdit, self).keyReleaseEvent(event)

    def process_multi_keys(self, keys):
        """
        Placeholder for processing multiple key combo events

        :param keys: [QtCore.Qt.Key]. key combos
        """
        # toggle comments indent event
        if keys == [QtCore.Qt.Key_Control, QtCore.Qt.Key_Slash]:
            pass

    def do_indent(self, lines):
        """
        Indent lines

        :param lines: [int]. line numbers
        """
        for line in lines:
            self.insert_line_start("\t", line)

    def undo_indent(self, lines):
        """
        Un-indent lines

        :param lines: [int]. line numbers
        """
        for line in lines:
            self.remove_line_start("\t", line)

    def do_comment(self, lines):
        """
        Comment out lines

        :param lines: [int]. line numbers
        """
        for line in lines:
            pass

    def undo_comment(self, lines):
        """
        Un-comment lines

        :param lines: [int]. line numbers
        """
        for line in lines:
            pass


class CodeEditor(CodeTextEdit):
    def __init__(self):
        super(CodeEditor, self).__init__()

        self.line_number_area = LineNumberArea(self)

        self.font = QtGui.QFont()
        self.font.setFamily("Courier New")
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.tab_size = 4
        self.setTabStopWidth(self.tab_size * self.fontMetrics().width(" "))

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 30 + self.fontMetrics().width("9") * digits
        return space

    def resizeEvent(self, e):
        super(CodeEditor, self).resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QtCore.QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        # painter.fillRect(event.rect(), QtCore.Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number)
                painter.setPen(DARK_BLUE)
                width = self.line_number_area.width() - 10
                height = self.fontMetrics().height()
                painter.drawText(
                    0, int(top), int(width), int(height), QtCore.Qt.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def highlight_current_line(self):
        extra_selections = list()
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = DARK_BLUE.lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def load_strat_code(self):
        strat_code = """import ta
# add your own indicator and conditions to take the trade
class YourStrategy():
    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point = 0,
        type=["long"],
        leverage = 1,
        longCondition = False,
        shortCondition = False,
        closeLongCondition = False,
        closeShortCondition = False,
        isLong = False,
        isShort = False,
        enterPriceShort = None,
        enterPriceLong = None,
        closePriceShort = None,
        closePriceLong = None,
        leverage = 1
    ):
        # dataFrame for testing
        self.df = df
        # just for backtesting (k_point of the simulation)
        self.k_point = k_point
        # do we want only long, short or both ?
        self.use_long = True if "long" in type else False
        self.use_short = True if "short" in type else False

        # condition for long/short
        self.longCondition = longCondition
        self.shortCondition = shortCondition
        self.closeLongCondition = closeLongCondition
        self.closeShortCondition = closeShortCondition
        self.isLong = isLong
        self.isShort = isShort
        self.usdt = usdt
        self.coin = coin
        self.enterPriceShort = enterPriceShort
        self.enterPriceLong = enterPriceLong
        self.closePriceShort = closePriceShort
        self.closePriceLong = closePriceLong

        # set the leverage you want
        self.leverage = leverage

def setIndicators(self):
    # -- Clear dataset --
    df = self.df

    # your indicators

    self.df = df    
    return self.df

def setShortLong(self): 
    df = self.df
    # -- Initiate populate --
    self.longCondition = False
    self.shortCondition = False
    self.closeLongCondition = False
    self.closeShortCondition = False
    
    if self.use_long:
        # -- open long market --
        # write your conditions here
        condition4 = (self.usdt>0)
        if  :
            self.longCondition = True
            self.isLong = True
        
        # -- close long market --
        # write your conditions here
        condition2 = self.isLong
        if condition1 and condition2:
            self.closeLongCondition = True
            self.isLong = False
    
    if self.use_short:
        # -- open short market --
        # write your conditions here
        condition4 = (self.usdt>0)
        if :
            self.shortCondition = True
            self.isShort = True

        # -- close short market --
        # write your conditions here
        condition2 = self.isShort
        if :
            self.closeShortCondition = True
            self.isShort = False

    return None
"""
        self.setPlainText(strat_code)

    def load_RL_code(self):
        RL_code = """import numpy as np
import pandas as pd
from gym.utils import seeding
import gym
from gym import spaces

import matplotlib.pyplot as plt

df = pd.read_csv('/Users/guillaumepoidatz/Documents/VENV/baselinesTest2/lib/python3.11/site-packages/gym/envs/rlstock/Data_Daily_Stock_Dow_Jones_30/dow_jones_30_daily_price.csv')

def data_preprocess_train(df):
    data_1=df.copy()
    equal_4711_list = list(data_1.tic.value_counts() == 4711)
    names = data_1.tic.value_counts().index

    # select_stocks_list = ['NKE','KO']
    select_stocks_list = list(names[equal_4711_list])+['NKE','KO']

    data_2 = data_1[data_1.tic.isin(select_stocks_list)][~data_1.datadate.isin(['20010912','20010913'])]

    data_3 = data_2[['iid','datadate','tic','prccd','ajexdi']]

    data_3['adjcp'] = data_3['prccd'] / data_3['ajexdi']

    train_data = data_3[(data_3.datadate > 20090000) & (data_3.datadate < 20160000)]
    train_daily_data = []
    for date in np.unique(train_data.datadate):
        train_daily_data.append(train_data[train_data.datadate == date])


    return train_daily_data

train_daily_data = data_preprocess_train(df)


class StockEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, day = 0, money = 10 , scope = 1):
        self.day = day

        # buy or sell maximum 5 shares
        self.action_space = spaces.Box(low = -5, high = 5,shape = (28,),dtype=np.int8)

        # [money]+[prices 1-28]*[owned shares 1-28]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape = (57,))

        # # [money]+[prices 1-28]*[owned shares 1-28]
        # self.observation_space = spaces.Box(low=0, high=np.inf, shape = (5,))

        self.data = train_daily_data[self.day]

        self.terminal = False

        # intial [money]+[prices 1-28]*[owned shares 1-28]
        self.state = [10000] + self.data.adjcp.values.tolist() + [0 for i in range(28)]
        self.reward = 0

        self.asset_memory = [10000]

        self.reset()
        self._seed()


    def _sell_stock(self, index, action):
        # possess stock of action[indeex]?
        if self.state[index+29] > 0:
            self.state[0] += self.state[index+1]*min(abs(action), self.state[index+29])
            self.state[index+29] -= min(abs(action), self.state[index+29])
        else:
            pass

    def _buy_stock(self, index, action):
        available_amount = self.state[0] // self.state[index+1]
        # print('available_amount:{}'.format(available_amount))
        self.state[0] -= self.state[index+1]*min(available_amount, action)
        # print(min(available_amount, action))

        self.state[index+29] += min(available_amount, action)

    def step(self, actions):
        # print(self.day)
        self.terminal = self.day >= 1761
        # print(actions)

        if self.terminal:
            plt.plot(self.asset_memory,'r')
            plt.savefig('result_training.png')
            plt.close()
            print("total_reward:{}".format(self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))- 10000 ))


            # print('total asset: {}'.format(self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))))
            return self.state, self.reward, self.terminal,{}

        else:
            # print(np.array(self.state[1:29]))


            begin_total_asset = self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))
            # print("begin_total_asset:{}".format(begin_total_asset))
            argsort_actions = np.argsort(actions)
            sell_index = argsort_actions[:np.where(actions < 0)[0].shape[0]]
            buy_index = argsort_actions[::-1][:np.where(actions > 0)[0].shape[0]]

            for index in sell_index:
                # print('take sell action'.format(actions[index]))
                self._sell_stock(index, actions[index])

            for index in buy_index:
                # print('take buy action: {}'.format(actions[index]))
                self._buy_stock(index, actions[index])

            self.day += 1
            self.data = train_daily_data[self.day]


            # print("stock_shares:{}".format(self.state[29:]))
            self.state =  [self.state[0]] + self.data.adjcp.values.tolist() + list(self.state[29:])
            end_total_asset = self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))
            # print("end_total_asset:{}".format(end_total_asset))

            self.reward = end_total_asset - begin_total_asset
            # print("step_reward:{}".format(self.reward))

            self.asset_memory.append(end_total_asset)


        return self.state, self.reward, self.terminal, {}

    def reset(self):
        self.asset_memory = [10000]
        self.day = 0
        self.data = train_daily_data[self.day]
        self.state = [10000] + self.data.adjcp.values.tolist() + [0 for i in range(28)]

        # iteration += 1
        return self.state

    def render(self, mode='human'):
        return self.state

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

"""
        self.setPlainText(RL_code)
