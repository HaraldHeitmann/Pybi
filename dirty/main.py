from PyQt4.uic import loadUiType
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar) 
Ui_MainWindow, QMainWindow = loadUiType('window.ui')
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        fig = Figure()
        self.addmpl(fig)
        self.rdBtn.clicked.connect(self.read)
        self.df = {}
        self.dfList.itemDoubleClicked.connect(self.df_selected)
        self.colList.itemDoubleClicked.connect(self.addcol)
        self.stgList.itemDoubleClicked.connect(self.rmvcol)
    def read(self):
        try:
	    lista=[str(self.dfList.item(i).text()) for i in xrange(self.dfList.count())]
            if str(self.inp.text()).split('.')[0] not in lista:    
                    self.df[str(self.inp.text()).split('.')[0]]=pd.read_csv(str(self.inp.text()))
		    self.dfList.addItem(str(self.inp.text()).split('.')[0])
		    print('File read')
        except IOError:
            print('No such file')
    def df_selected(self):
        if self.colList.count()==0:
            self.colList.addItems(self.df[str(self.dfList.currentItem().text())].columns)
        else:
            self.colList.clear()
            self.stgList.clear()
            self.colList.addItems(self.df[str(self.dfList.currentItem().text())].columns)
    def addcol(self):

        items=[self.stgList.item(i).text() for i in xrange(self.stgList.count())]

        if str(self.colList.currentItem().text()) not in items:
            self.stgList.addItem(str(self.colList.currentItem().text()))
        
    
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
