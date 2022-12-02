import pandas as pd
import queue
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
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



class Procesos(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('pagPrincipal.ui', self)
        #-----------------Variables-----------------#
        self.arregloProceso = []
        self.listaProcesos = []
        self.df = []
        self.auxLista = []
        self.popap = Popup(arreglo=self.arregloProceso)
        #self.grafico = GraficWindow(df=self.df)
        #-----------------Inicializar Tabla-----------------#
        self.iniciarTabla()


        #-----------------Botones-----------------#
        self.comenzarButton.clicked.connect(self.generarGrafico)
        self.crearButton.clicked.connect(self.crearProceso)
        #-----------------------------------------#

    def crearTabla(self):
        print(self.listaProcesos)

        self.tableWidget.setRowCount(len(self.listaProcesos))
        self.tableWidget.setColumnCount(3)
        for i in range(len(self.listaProcesos)):
            for j in range(3):
                celda = QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][j]))
                celda.setTextAlignment(QtCore.Qt.AlignCenter)
                celda.setFont(QFont("Tahoma, sans-serif", 12))
                celda.setForeground(QtGui.QColor(255, 255, 255))
                
                self.tableWidget.setItem(i, j, celda)


    def iniciarTabla(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Proceso", "Llegada", "Tiempo"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


    def crearProceso(self):
        
        self.popap.exec_()
        aux = self.arregloProceso.copy()
        
        self.listaProcesos.append(aux)

        self.crearTabla()
    
    
    def convert_to_datetime(self, x):
        return x
    
    def generarGrafico(self):

        self.algoritmoFIFO()
        self.grafico=GraficWindow(df=self.df)
        self.grafico.show()



    def algoritmoFIFO(self):
        self.df.clear()
        
        self.auxLista.clear()
        self.auxLista = self.listaProcesos.copy()
        self.auxLista.sort(key=lambda x: x[1])
        
        #Calcular cuando comienza el proceso
        for m in range(len(self.auxLista)):
            if m == 0:
                self.auxLista[m].append(self.auxLista[m][1])
            else:
                self.auxLista[m].append(int(self.auxLista[m-1][3])+int(self.auxLista[m-1][2]))

        print(self.auxLista)
        for i in range(len(self.auxLista)):
            aux = dict(Trabajo=self.auxLista[i][0], Start=self.convert_to_datetime(int(self.auxLista[i][3])), Finish=self.convert_to_datetime(int(self.auxLista[i][3])+int(self.auxLista[i][2])))
            self.df.append(aux)
        


class Popup(QDialog):
    def __init__(self, arreglo):
        QtWidgets.QDialog.__init__(self)
        loadUi('popap.ui', self)
        self.nom = ''
        self.lleg = ''
        self.tiem = ''
        self.arreglo = arreglo
        self.buttonBox.accepted.connect(self.extraerDatos)
        self.llegadaProceso.setValidator(QtGui.QIntValidator())
        self.tiempoProceso.setValidator(QtGui.QIntValidator())

    
    def extraerDatos(self):
        self.nom = self.nombreProceso.text()
        self.lleg = self.llegadaProceso.text()
        self.tiem = self.tiempoProceso.text()
        
        #verificar si arreglo esta vacio
        if len(self.arreglo) == 0:
            self.arreglo.append(self.nom)
            self.arreglo.append(self.lleg)
            self.arreglo.append(self.tiem)
        else:
            self.arreglo.clear()
            self.arreglo.append(self.nom)
            self.arreglo.append(self.lleg)
            self.arreglo.append(self.tiem)
    




class GraficWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        loadUi('grafico2.ui', self)
        self.df = df

        self.grafica = plt.figure()

        #-------------------------------------#
        # #-------------------------------------#

        # df = [dict(Trabajo="Proceso A", Start=self.convert_to_datetime(1), Finish=self.convert_to_datetime(5)),
        #     dict(Trabajo="Proceso B", Start=self.convert_to_datetime(6), Finish=self.convert_to_datetime(8)),
        #     dict(Trabajo="Proceso C", Start=self.convert_to_datetime(9), Finish=self.convert_to_datetime(11))]

        
        #-------------------------------------#

        fig = px.timeline(self.df, x_start="Start", x_end="Finish", y="Trabajo", color="Trabajo", title='')
        #xaxis=dict(tickvals=date_ticks, ticktext=date_ticks, tickangle=45, tickfont=dict(size=10))
        #hacer que el eje x sea de tipo entero
        fig.update_xaxes(dtick=1)

        
        

        plotly.offline.plot(fig, filename='gantt.html', auto_open=False, show_link=False, config={'displayModeBar': False,
        'staticPlot': True,
        'responsive': True,
        'setBackground': 'transparent',

        })
        
        
        self.webEngineView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('gantt.html')))
        #self.frameGrafico.layout().addWidget(self.webView)

    def convert_to_datetime(self, x):
        # return datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%d-%m")
        return x
            
            











if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Procesos()
    window.show()
    sys.exit(app.exec_())













