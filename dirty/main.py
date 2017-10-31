from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import Binarizer
Ui_MainWindow, QMainWindow = loadUiType('window.ui')
Ui_secWindow, QsecWindow = loadUiType('analysis.ui')


# here goes some serious logic on how passing dataframes and it's
# characteristics, efficiently and with few lines of code...
class Sec(QsecWindow, Ui_secWindow):

    def __init__(self, _parent):
        super(Sec, self).__init__(parent=_parent)
        self.setupUi(self)
        self.aBox.addItems(
            ['Cluster', 'Regression', 'Classify'])  # fix spelling
        self.df = self.parent().currentDF
        self.name = self.parent().current_name
        # here goes the logic of the window
        if self.df is not None:
            self.optList.addItems(self.df.columns)
        self.fitBtn.clicked.connect(self.fit)
        self.optList.itemDoubleClicked.connect(self.addcol)
        self.featList.itemDoubleClicked.connect(self.rmvcol)

    def fit(self):
        if str(self.aBox.currentText()) == 'Cluster':
            try:
                n = int(self.inp.text())
                if n < 1:
                    raise ValueError()
            except ValueError:
                raise ValueError('Enter an integer!. "{}" is not an int'.format(
                    str(self.inp.text())))  # don't do this!
            km = KMeans(n_clusters=n)
            items = [str(self.featList.item(i).text())
                     for i in xrange(self.featList.count())]
            data = self.df[items].values
            labels = km.fit_predict(data)
            self.parent().currentDF['clusterized_' + str(n)] = labels
            print 'Done!'
        elif str(self.aBox.currentText()) == 'Classify':
            pass
        else:
            pass

    def addcol(self):
        items = [self.featList.item(i).text()
                 for i in xrange(self.featList.count())]
        if str(self.optList.currentItem().text()) not in items:
            self.featList.addItem(str(self.optList.currentItem().text()))

    def rmvcol(self):
        self.featList.takeItem(self.featList.row(self.featList.currentItem()))


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        fig = Figure()
        self.addmpl(fig)
        self.rdBtn.clicked.connect(self.read)
        self.pltBtn.clicked.connect(self.plot)
        self.df = {}
        self.dfList.itemDoubleClicked.connect(self.df_selected)
        self.colList.itemDoubleClicked.connect(self.addcol)
        self.stgList.itemDoubleClicked.connect(self.rmvcol)
        self.plotList.itemDoubleClicked.connect(self.show_fig)
        self.currentDF = None
        self.current_name = None
        self.plots = {}
        self.plotBox.addItems(['histogram', 'plot', 'scatter'])
        self.selection = "None"
        self.aBtn.clicked.connect(self.spawn_child)

    def spawn_child(self):
        sec = Sec(self)
        sec.show()

    def read(self):
        try:
            lista = [str(self.dfList.item(i).text())
                     for i in xrange(self.dfList.count())]
            if str(self.inp.text()).split('.')[0] not in lista:
                self.df[str(self.inp.text()).split('.')[0]
                        ] = pd.read_csv(str(self.inp.text()))
                self.dfList.addItem(str(self.inp.text()).split('.')[0])
        except IOError:
            print('No such file')

    def df_selected(self):
        self.current_name = str(self.dfList.currentItem().text())
        self.currentDF = self.df[self.current_name]
        self.filterBox.clear()
        self.filterBox.addItem("None")
        self.plotList.clear()
        self.rmmpl()
        if self.current_name in self.plots.keys():
            self.plotList.addItems(self.plots[self.current_name].keys())
        self.filterBox.addItems(
            self.df[str(self.dfList.currentItem().text())].columns)
        if self.colList.count() == 0:
            self.colList.addItems(
                self.df[str(self.dfList.currentItem().text())].columns)
        else:
            self.colList.clear()
            self.stgList.clear()
            self.colList.addItems(
                self.df[str(self.dfList.currentItem().text())].columns)

    def addcol(self):
        items = [self.stgList.item(i).text()
                 for i in xrange(self.stgList.count())]
        if str(self.colList.currentItem().text()) not in items:
            self.stgList.addItem(str(self.colList.currentItem().text()))

    def plot(self):
        if self.currentDF is None:
            return
        items = [str(self.stgList.item(i).text())
                 for i in xrange(self.stgList.count())]
        # here goes some logic to create different plots depending on the
        # selection of plotBox
        self.selection = str(self.filterBox.currentText())
        if self.selection == "None":
            if str(self.plotBox.currentText()) == 'scatter':
                if self.stgList.count() != 2:
                    raise TypeError('Select just two columns')
                else:
                    if self.current_name not in self.plots.keys():
                        generated_plot = {}
                        col1 = str(self.stgList.item(0).text())
                        col2 = str(self.stgList.item(1).text())
                        data1 = self.currentDF[col1].values
                        data2 = self.currentDF[col2].values
                        f, ax = plt.subplots()
                        ax.scatter(data1, data2, alpha=0.5)
                        ax.set(xlabel=col1, ylabel=col2)
                        ax.set_title(col1 + ' vs ' + col2)
                        generated_plot[col1 + ';' + col2 + ' ' +
                                       str(self.plotBox.currentText())] = f
                        self.plots[self.current_name] = generated_plot
                    else:
                        col1 = str(self.stgList.item(0).text())
                        col2 = str(self.stgList.item(1).text())
                        data1 = self.currentDF[col1].values
                        data2 = self.currentDF[col2].values
                        f, ax = plt.subplots()
                        ax.scatter(data1, data2, alpha=0.5)
                        ax.set(xlabel=col1, ylabel=col2)
                        ax.set_title(col1 + ' vs ' + col2)
                        self.plots[self.current_name][
                            col1 + ';' + col2 + ' ' + str(self.plotBox.currentText())] = f
            elif str(self.plotBox.currentText()) == 'plot':
                if self.current_name not in self.plots.keys():
                    generated_plots = {}
                    for col in items:
                        f, ax = plt.subplots()
                        self.currentDF[col].plot(ax=ax)
                        ax.set(ylabel=col, xlabel='index')
                        ax.set_title(col + ' Plot')
                        generated_plots[col + ' ' +
                                        str(self.plotBox.currentText())] = f
                    self.plots[self.current_name] = generated_plots
                else:
                    for col in items:
                        f, ax = plt.subplots()
                        self.currentDF[col].plot(ax=ax)
                        ax.set(ylabel=col, xlabel='index')
                        ax.set_title(col + ' Plot')
                        self.plots[self.current_name][
                            col + ' ' + str(self.plotBox.currentText())] = f
            elif str(self.plotBox.currentText()) == 'histogram':
                if self.current_name not in self.plots.keys():
                    generated_plots = {}
                    for col in items:
                        f, ax = plt.subplots()
                        self.currentDF[col].hist(ax=ax)
                        ax.set(xlabel=col, ylabel='count')
                        ax.set_title('Histogram of ' + col)
                        generated_plots[col + ' ' +
                                        str(self.plotBox.currentText())] = f
                    self.plots[self.current_name] = generated_plots
                else:
                    for col in items:
                        f, ax = plt.subplots()
                        self.currentDF[col].hist(ax=ax)
                        ax.set(xlabel=col, ylabel='count')
                        ax.set_title('Histogram of ' + col)
                        self.plots[self.current_name][
                            col + ' ' + str(self.plotBox.currentText())] = f
        else:
            if str(self.plotBox.currentText()) == 'scatter':
                if self.stgList.count() != 2:
                    raise TypeError('Select just two columns')
                else:
                    if self.current_name not in self.plots.keys():
                        f, ax = plt.subplots()
                        for value in self.currentDF[self.selection].unique():
                            filtered_df = self.currentDF[
                                self.currentDF[self.selection] == value]
                            generated_plot = {}
                            col1 = str(self.stgList.item(0).text())
                            col2 = str(self.stgList.item(1).text())
                            data1 = filtered_df[col1].values
                            data2 = filtered_df[col2].values
                            ax.scatter(
                                data1, data2, label=str(value), alpha=0.5)
                        ax.set(xlabel=col1, ylabel=col2)
                        f.legend()
                        generated_plot[col1 +
                                       ';' +
                                       col2 +
                                       '; fil= ' +
                                       self.selection +
                                       ' ' +
                                       str(self.plotBox.currentText())] = f
                        self.plots[self.current_name] = generated_plot
                    else:
                        f, ax = plt.subplots()
                        for value in self.currentDF[self.selection].unique():
                            filtered_DF = self.currentDF[
                                self.currentDF[self.selection] == value]
                            col1 = str(self.stgList.item(0).text())
                            col2 = str(self.stgList.item(1).text())
                            data1 = filtered_DF[col1].values
                            data2 = filtered_DF[col2].values
                            ax.scatter(
                                data1, data2, label=str(value), alpha=0.5)
                        ax.set(xlabel=col1, ylabel=col2)
                        f.legend()
                        self.plots[self.current_name][col1 +
                                                      ';' +
                                                      col2 +
                                                      '; fil= ' +
                                                      self.selection +
                                                      ' ' +
                                                      str(self.plotBox.currentText())] = f
            elif str(self.plotBox.currentText()) == 'histogram':
                if self.current_name not in self.plots.keys():
                    generated_plots = {}
                    for col in items:
                        f, ax = plt.subplots()
                        for value in self.currentDF[self.selection].unique():
                            filtered_df = self.currentDF[
                                self.currentDF[self.selection] == value]
                            filtered_df[col].hist(
                                ax=ax, label=str(value), alpha=0.5)
                        ax.set(xlabel=col, ylabel='count')
                        f.legend()
                        generated_plots[col +
                                        ';fil= ' +
                                        self.selection +
                                        ' ' +
                                        str(self.plotBox.currentText())] = f
                    self.plots[self.current_name] = generated_plots
                else:
                    for col in items:
                        f, ax = plt.subplots()
                        for value in self.currentDF[self.selection].unique():
                            filtered_df = self.currentDF[
                                self.currentDF[self.selection] == value]
                            filtered_df[col].hist(
                                ax=ax, alpha=0.5, label=str(value))
                        ax.set(xlabel=col, ylabel='count')
                        f.legend()
                        self.plots[self.current_name][
                            col + ';fil= ' + self.selection + ' ' + str(self.plotBox.currentText())] = f
            else:
                if self.current_name not in self.plots.keys():
                    generated_plots = {}
                    for col in items:
                        f, ax = plt.subplots()
                        for value in self.currentDF[self.selection].unique():
                            # .reset_index() intended to time series, uncomment otherwise
                            filtered_df = self.currentDF[
                                self.currentDF[self.selection] == value]
                            filtered_df[col].plot(
                                ax=ax, label=str(value), alpha=0.5)
                        ax.set(xlabel='index', ylabel=col)
                        f.legend()
                        generated_plots[col +
                                        ';fil= ' +
                                        self.selection +
                                        ' ' +
                                        str(self.plotBox.currentText())] = f
                    self.plots[self.current_name] = generated_plots
                else:
                    for col in items:
                        f, ax = plt.subplots()
                        for value in self.currentDF[self.selection].unique():
                            # .reset_index() intended to time series uncomment otherwise
                            filtered_df = self.currentDF[
                                self.currentDF[self.selection] == value]
                            filtered_df[col].plot(
                                ax=ax, alpha=0.5, label=str(value))
                        ax.set(xlabel='index', ylabel=col)
                        f.legend()
                        self.plots[self.current_name][
                            col + ';fil= ' + self.selection + ' ' + str(self.plotBox.currentText())] = f
        self.plotList.clear()
        for plot_dict in self.plots[self.current_name].keys():
            self.plotList.addItem(plot_dict)

    def show_fig(self):
        self.rmmpl()
        fig_name = str(self.plotList.currentItem().text())
        self.addmpl(self.plots[self.current_name][fig_name])

    def rmvcol(self):
        self.stgList.takeItem(self.stgList.row(self.stgList.currentItem()))

    def clear(self):
        self.mplfigs.clear()
        self.rmmpl()

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwindow,
                                         coordinates=True,
                                         )
        self.mplvl.addWidget(self.toolbar)

    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
