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
import mpld3

class Procesos(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('pagPrincipal.ui', self)
        #-----------------Variables-----------------#
        self.arregloProceso = []
        self.listaProcesos = []
        self.df = []
        self.auxLista = []
        self.listaProcesosAux = []
        self.nombre = []
        self.popap = Popup(arreglo=self.arregloProceso)
        self.elegirAlgoritmo = SeleccionAlgoritmo(self.nombre)
        #-----------------Inicializar Tabla-----------------#
        self.iniciarTabla()


        #-----------------Botones-----------------#
        self.comenzarButton.clicked.connect(self.generarGrafico)

        self.crearButton.clicked.connect(self.crearProceso)
        #-----------------------------------------#

    def crearTabla(self):
        # print('listaprocesos tabla')
        # print(self.listaProcesos)

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
    
    
    
    def generarGrafico(self):
        # print('-------listaProcesos-------')
        # print(self.listaProcesos)
        self.elegirAlgoritmo.exec_()
        
        if self.nombre[0] == 'SPN':
            self.algoritmoSPN()
            
        elif self.nombre[0] == 'FIFO':
            self.algoritmoFIFO()
        
        elif self.nombre[0] == 'RR':
            self.algoritmoRR()
            
        
        # print("el nombre es: ", self.nombre[0])
        auxNombre = self.nombre[0]
        self.nombre.clear()
        # print(auxNombre)
        self.grafico=GraficWindow(df=self.dfAux, titulo=auxNombre)
        self.grafico.show()



    def algoritmoFIFO(self):
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[1])
        
        
        for i in range(len(self.listaProcesosAux)):
            if i != 0:
                try:
                    if self.listaProcesosAux[i][1] > self.listaProcesosAux[i-1][2]:
                        pass
                            
                    elif self.listaProcesosAux[i][1] == self.listaProcesosAux[i-1][1]:
                        self.listaProcesosAux[i][1] = self.listaProcesosAux[i - 1][1] + self.listaProcesosAux[i - 1][2]
                    else:
                        self.listaProcesosAux[i][1] = self.listaProcesosAux[i - 1][1] + self.listaProcesosAux[i - 1][2]
                        self.listaProcesosAux[i][2] = self.listaProcesosAux[i][2] + self.listaproProcesosAux[i][1]
                except:
                    pass
            else:
                pass

        # print('-------listaProcesosfifo-------')
        # print(self.listaProcesosAux)

        self.dfAux = pd.DataFrame(self.listaProcesosAux, columns=['Proceso', 'Llegada', 'Termina'])

    def algoritmoSPN(self):
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[2])
        self.listaProcesosAux.sort(key=lambda x: x[1])
        colaDeEjecucion = []
        tiempoActual = 0
        print('-------listaProcesosSPN-------')
        print(self.listaProcesosAux)
        colaDeEjecucion.append(self.listaProcesosAux[0])
        tiempoActual = self.listaProcesosAux[0][1]+tiempoActual
        self.listaProcesosAux.pop(0)
        
        for i in range(len(self.listaProcesosAux)):
            try:
                if self.listaProcesosAux[i][1] <= tiempoActual:
                    self.listaProcesosAux.sort(key=lambda x: x[2])
                    colaDeEjecucion.append(self.listaProcesosAux[0])
                    tiempoActual = self.listaProcesosAux[0][1]+tiempoActual
                    self.listaProcesosAux.pop(0)
                else:
                    colaDeEjecucion.append(self.listaProcesosAux[0])
                    tiempoActual = self.listaProcesosAux[0][1]+tiempoActual
                    self.listaProcesosAux.pop(0)
            except:
                pass
        for i in range(len(self.listaProcesosAux)):
            colaDeEjecucion.append(self.listaProcesosAux.pop(0))
        print('-------colaDeEjecucion-------')
        print(colaDeEjecucion)


        for i in range(len(colaDeEjecucion)):
            if i != 0:
                try:
                    if colaDeEjecucion[i][1] > colaDeEjecucion[i-1][2]:
                        pass
                            
                    elif colaDeEjecucion[i][1] == colaDeEjecucion[i-1][1]:
                        colaDeEjecucion[i][1] = colaDeEjecucion[i - 1][1] + colaDeEjecucion[i - 1][2]
                    else:
                        colaDeEjecucion[i][1] = colaDeEjecucion[i - 1][1] + colaDeEjecucion[i - 1][2]
                        
                except:
                    pass


        self.dfAux = pd.DataFrame(colaDeEjecucion, columns=['Proceso', 'Llegada', 'Termina'])
    
    def algoritmoRR(self):
        
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[1])
        colaDeEjecucion = []
        quantum = 3
        matangadijolachanga = len(self.listaProcesosAux)
        k = 0
        m = 0
        tiempoActual = 0
        while True:
            
            try:
                if self.listaProcesosAux[k][2] <= quantum:
                    colaDeEjecucion.append(self.listaProcesosAux[0])
                    self.listaProcesosAux.pop(0)
                    
                else:
                    colaDeEjecucion.append([self.listaProcesosAux[k][0], self.listaProcesosAux[k][1], quantum])
                    self.listaProcesosAux[k][1] = self.listaProcesosAux[k][1] + quantum
                    self.listaProcesosAux[k][2] = self.listaProcesosAux[k][2] - quantum
                    self.listaProcesosAux.sort(key=lambda x: x[1])
            except IndexError:
                pass
  
            k+=1
            if k == len(colaDeEjecucion):
                k = 0
            if len(self.listaProcesosAux) == 0:
                break
        # print('-------colaDeEjecucion-------')
        # print(colaDeEjecucion)

        for i in range(len(colaDeEjecucion)):
            if colaDeEjecucion[i][2] <= quantum:
                pass
            else:
                aux = colaDeEjecucion[i][2] - quantum
                colaDeEjecucion[i][2] = quantum
                colaDeEjecucion.append([colaDeEjecucion[i][0], colaDeEjecucion[i][1]+quantum, aux])
                break
        

        colaDeEjecucion.sort(key=lambda x: x[1])
        # print('-------colaDeEjecucion3erFiltro-------')
        # print(colaDeEjecucion)

        # for i in range(0,len(colaDeEjecucion)):
        #     # print('valor de i: ', i)
        #     if i >= matangadijolachanga:
        #         for j in range(matangadijolachanga):
        #             # print('valor de i comparando: ', i)
        #             print('valor de j: ', j)
        #             print('Estoy comparando: ', colaDeEjecucion[i][0], 'con', colaDeEjecucion[j][0])
        #             if colaDeEjecucion[j][0] == colaDeEjecucion[i][0]:
        #                 colaDeEjecucion[i][1] = colaDeEjecucion[j][1] + m
        #                 m += 1

        for i in range(matangadijolachanga):
            for j in range(matangadijolachanga,len(colaDeEjecucion)):
                if colaDeEjecucion[i][0] == colaDeEjecucion[j][0]:
                    colaDeEjecucion[j][1] = colaDeEjecucion[i][2] + m
                    m += 1
                    
        colaDeEjecucion.sort(key=lambda x: x[1])
        print('-------colaDeEjecucion4toFiltro-------')
        print(colaDeEjecucion)

        for i in range(len(colaDeEjecucion)):
            if i != 0:
                if colaDeEjecucion[i][0] == colaDeEjecucion[i-1][0]:
                    colaDeEjecucion[i][1] = colaDeEjecucion[i][1] + colaDeEjecucion[i-1][1]
        colaDeEjecucion.sort(key=lambda x: x[0])
        print('-------colaDeEjecucion5toFiltro-------')
        print(colaDeEjecucion)
        colaDeEjecucion.sort(key=lambda x: x[1])




        for i in range(len(colaDeEjecucion)):
            if i != 0:
                colaDeEjecucion[i][1] = colaDeEjecucion[i-1][2] + colaDeEjecucion[i-1][1]


        
        self.dfAux = pd.DataFrame(colaDeEjecucion, columns=['Proceso', 'Llegada', 'Termina'])
        











    def extraerDatosTabla(self):
        aux = []
        aux2 = []
        aux.clear()
        aux2.clear()
        for i in range(self.tableWidget.rowCount()):
    
            aux.clear()
            for j in range(3):
                if j != 0:
                    aux.append(int(float(np.float16(self.tableWidget.item(i, j).text()))))
                else:
                    aux.append(self.tableWidget.item(i, j).text())
            aux2.append(aux.copy())
       
        print('-------aux2-------')
        print(aux2)
        
        

        return aux2


        
        
        


        
                                    





        
        


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
    
class SeleccionAlgoritmo(QDialog):
    def __init__(self, nombre):
        QtWidgets.QDialog.__init__(self)
        loadUi('seleccionAlgoritmo.ui', self)
        self.algoritmo = nombre
        self.buttonBox_2.accepted.connect(self.extraerDatos)

    def extraerDatos(self):
        self.algoritmo.clear()
        self.algoritmo.append( self.comboBox.currentText())
        self.close()



class GraficWindow(QMainWindow):
    def __init__(self, df, titulo):
        super().__init__()
        loadUi('grafico2.ui', self)
        self.df = df
        self.titulo = titulo
        
        
        plt.figure(figsize=(10, 5))
        plt.title(("Algoritmo "+self.titulo), size=15)

        for i in range(df.shape[0]):
            color = np.random.rand(3,)
            plt.barh(df['Proceso'][i], df['Termina'][i], left=df['Llegada'][i], color=color, label=df['Proceso'][i])
            plt.text(df['Llegada'][i] + df['Termina'][i] / 2, i, df['Termina'][i], ha='center', va='center', size=15)
            plt.legend()
        plt.xlabel('Tiempo', size=15)
        plt.xticks(np.arange(0, self.df['Termina'].max() + self.df['Llegada'].max() + 1, 1))
        plt.ylabel('Procesos', size=15)
        plt.grid(axis='x', which='major')
        plt.savefig('grafico.png')
        
        
        
        """
        plt.barh(y=self.df.Proceso, left=self.df['Llegada'], width=self.df['Termina'])

        self.listaNomProcesos = []
        for i in range(len(self.df.Proceso)):
            self.listaNomProcesos.append(self.df.Proceso[i])
        
        plt.yticks(self.listaNomProcesos)
        
        plt.xticks(np.arange(0, self.df['Termina'].max() + self.df['Llegada'].max() + 1, 1)) #Dios que grande tengo el chilo
        plt.grid(axis='x')
        plt.xlabel('Tiempo', size=15)
        plt.ylabel('Procesos', size=15)
        plt.savefig('grafico.png')
        """


        
        
        self.labelFoto.setPixmap(QtGui.QPixmap('grafico.png'))
        self.labelFoto.setScaledContents(True)

            











if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Procesos()
    window.show()
    sys.exit(app.exec_())













