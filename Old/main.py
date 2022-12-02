import pandas
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets, QtGui
import os
from datetime import datetime
import numpy as np
from os import remove
import sys
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly
import plotly.express as px
from plotly.graph_objects import Figure, Scatter, Layout

class GraficWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('grafico2.ui', self)

        self.grafica = plt.figure()

        #-------------------------------------#
        #-------------------------------------#

        df = [dict(Trabajo="Proceso A", Start=self.convert_to_datetime(1), Finish=self.convert_to_datetime(5)),
            dict(Trabajo="Proceso B", Start=self.convert_to_datetime(6), Finish=self.convert_to_datetime(8)),
            dict(Trabajo="Proceso C", Start=self.convert_to_datetime(9), Finish=self.convert_to_datetime(11))]

        num_tick_labels = np.linspace(start=0,stop=11,num=12,dtype=int)
        date_ticks = [self.convert_to_datetime(x) for x in num_tick_labels]

        # fig = ff.create_gantt(df, showgrid_x=True, title='')
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Trabajo", color="Trabajo", title='')

        fig.layout.xaxis.update({
        'tickvals' : date_ticks,
        'ticktext' : num_tick_labels
        })
        
        

        plotly.offline.plot(fig, filename='gantt.html', auto_open=False, show_link=False, config={'displayModeBar': False,
        'staticPlot': True,
        'responsive': True,
        'setBackground': 'transparent',

        })
        
        
        
        # plotly.offline.plot_mpl(fig, include_plotlyjs=False, filename='jorge.html')
        
        
        # self.webEngineView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('temp-plot.html')))
        self.webEngineView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('gantt.html')))
        #self.frameGrafico.layout().addWidget(self.webView)

    def convert_to_datetime(self, x):
        return datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%d-%m")
            
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraficWindow()
    window.show()
    sys.exit(app.exec_())