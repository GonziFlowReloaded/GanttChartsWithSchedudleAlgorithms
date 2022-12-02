import pandas as pd

from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
import os
from datetime import datetime
import numpy as np
from os import remove
import sys
import matplotlib.pyplot as plt

class Procesos(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('pagPrincipal.ui', self)
        
        # self.setWindowTitle("Simulador de algoritmos de planificación")
        self.setWindowIcon(QIcon('icono.ico'))

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
        #-----------------Menu---------------------#
        self.actionGuardar.triggered.connect(self.guardarDatos)
        self.actionAbrir.triggered.connect(self.abrirArchivo)
        self.actionAcerca_de.triggered.connect(self.acercaDe)

    def crearTabla(self):
        

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
        try:
            self.popap.exec_()
            aux = self.arregloProceso.copy()
            
            self.listaProcesos.append(aux)

            self.crearTabla()
        except:
            pass
        # self.listaProcesos = self.extraerDatosTabla()
    
    
    
    def generarGrafico(self):
        self.quantumIngreso = QInputDialog()
        self.quantumIngreso.setWindowTitle("Seleccionar Quantum")
        self.quantumIngreso.setLabelText("Ingrese el Quantum")
        self.quantumIngreso.setOkButtonText("Aceptar")
        self.quantumIngreso.setCancelButtonText("Cancelar")
        self.quantumIngreso.InputMode = QInputDialog.IntInput

        
        self.elegirAlgoritmo.exec_()
        try:

            if self.nombre[0] == 'SPN':
                self.algoritmoSPNObjeto()
                
            elif self.nombre[0] == 'FIFO':
                self.algoritmoFIFO()
            
            elif self.nombre[0] == 'RR':
                
                self.quantumIngreso.exec_()
                self.auxQuantum = self.quantumIngreso.textValue()
                print(self.auxQuantum)
                self.algoritmoRR(quantum=int(self.auxQuantum))
                
            elif self.nombre[0] == 'SRT':
                self.algoritmoSRT()
            
        
            auxNombre = self.nombre[0]
            self.nombre.clear()
            # print(auxNombre)
            arregloOriginal = self.extraerDatosTabla()
            self.grafico=GraficWindow(df=self.dfAux, titulo=auxNombre, arregloOriginal=arregloOriginal)
            self.grafico.show()
        except:
            pass



    def algoritmoFIFO(self):
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[1])
        
        
        for i in range(len(self.listaProcesosAux)):
            if i == 0:
                pass
            else:
                if self.listaProcesosAux[i][1] > self.listaProcesosAux[i-1][1] + self.listaProcesosAux[i-1][2]:
                    pass
                else:
                    self.listaProcesosAux[i][1] = self.listaProcesosAux[i-1][1] + self.listaProcesosAux[i-1][2]

        self.dfAux = pd.DataFrame(self.listaProcesosAux, columns=['Proceso', 'Llegada', 'Termina'])

    def algoritmoSPNObjeto(self):
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[1])
        colaDeEjecucion = []
        colaDeEjecucion = self.listaProcesosAux.copy()

        self.dfAux = pd.DataFrame(algoritmoSPN(colaDeEjecucion), columns=['Proceso', 'Llegada', 'Termina'])
    
    def algoritmoRR(self, quantum=3):
        
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[1])
        colaDeEjecucion = []
        colaDeEjecucion = self.listaProcesosAux.copy()
        


        self.dfAux = pd.DataFrame(algoritmoRoundRobin(colaDeEjecucion, quantum), columns=['Proceso', 'Llegada', 'Termina'])
        


    def algoritmoSRT(self):
        self.listaProcesosAux = self.extraerDatosTabla()
        self.listaProcesosAux.sort(key=lambda x: x[1])
        colaDeEjecucion = []
        colaDeEjecucion = self.listaProcesosAux.copy()



        

        self.dfAux = pd.DataFrame(sexoooo2(colaDeEjecucion), columns=['Proceso', 'Llegada', 'Termina'])
    
    def guardarDatos(self):
        try:
            self.listaProcesos = self.extraerDatosTabla()
            self.df = pd.DataFrame(self.listaProcesos, columns=['Proceso', 'Llegada', 'Termina'])
            fileName = QFileDialog.getSaveFileName(self, 'Guardar Archivo', os.getenv('HOME'), 'CSV(*.csv)')
            #Darle formato a los datos
            
            self.df.to_csv(fileName[0], index=False)
            #Informar al usuario que se guardo el archivo
            QMessageBox.information(self, "Información", "Archivo guardado con éxito")
        except:
            pass
    
    def abrirArchivo(self):
        try:
            fileName = QFileDialog.getOpenFileName(self, 'Abrir Archivo', os.getenv('HOME'), 'CSV(*.csv)')
            self.df = pd.read_csv(fileName[0])
            self.listaProcesos = self.df.values.tolist()
            self.crearTabla()
        except:
            pass

    def acercaDe(self):
        QMessageBox.about(self, "Acerca de", "Trabajo practico integrador Sistemas Operativos\nCreado por: José Gonzalo Scali")

        

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

        return aux2


        
    


class Popup(QDialog):
    def __init__(self, arreglo):
        QtWidgets.QDialog.__init__(self)
        loadUi('popap.ui', self)
        self.setWindowIcon(QIcon('icono.ico'))
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
        self.setWindowIcon(QIcon('icono.ico'))
        self.algoritmo = nombre
        self.buttonBox_2.accepted.connect(self.extraerDatos)
        self.buttonBox_2.rejected.connect(self.close)

    def extraerDatos(self):
        self.algoritmo.clear()
        self.algoritmo.append( self.comboBox.currentText())
        self.close()



class GraficWindow(QMainWindow):
    def __init__(self, df, titulo, arregloOriginal):
        super().__init__()
        loadUi('grafico2.ui', self)
        self.setWindowIcon(QIcon('icono.ico'))
        self.df = df
        self.titulo = titulo
        self.listaProcesosTabla = []
        self.arregloOriginal = arregloOriginal
        #-----------------Grafico-----------------#
        plt.figure(figsize=(10, 5))
        plt.title(("Algoritmo "+self.titulo), size=15)

        for i in range(df.shape[0]):
            color = np.random.rand(3,)
            plt.barh(df['Proceso'][i], df['Termina'][i], left=df['Llegada'][i], color=color, label=df['Proceso'][i])
            # plt.text(df['Llegada'][i] + df['Termina'][i] / 2, i, df['Termina'][i], ha='center', va='center', size=15)
            plt.legend()
        plt.xlabel('Tiempo', size=15)
        plt.xticks(np.arange(0, self.df['Termina'].max() + self.df['Llegada'].max() + 1, 1))
        plt.ylabel('Procesos', size=15)
        plt.grid(axis='x', which='major')
        plt.savefig('grafico.png')
        
        self.labelFoto.setPixmap(QtGui.QPixmap('grafico.png'))
        self.labelFoto.setScaledContents(True)

        #-----------------Tabla-----------------#
        
        self.listaProcesosTabla = self.df.values.tolist()
        self.tableWidget.setRowCount(len(self.arregloOriginal))
        print(self.listaProcesosTabla)
        self.tableWidget.setColumnWidth(5, 200)
        if self.titulo == 'FIFO':
            self.insertarDatosTablaFifo()
        elif self.titulo == 'SPN':
            self.insertarDatosTablaSPN()
        elif self.titulo == 'RR':
            print('aña')
            self.insertarDatosTablaRR()
        elif self.titulo == 'SRT':
            self.insertarDatosTablaSRT()
        
    
    def insertarDatosTablaFifo(self):
        # self.tableWidget.setRowCount(len(self.listaProcesosTabla))
        tiemposFinalizacion = []
        trts = []
        #Agrandar la 5ta columna
        
        for i in range(len(self.listaProcesosTabla)):
            tiemposFinalizacion.append(self.listaProcesosTabla[i][2] + self.listaProcesosTabla[i][1]) 
        
        self.insertarDatosGenericos()    
        
        for i in range(len(tiemposFinalizacion)):
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(tiemposFinalizacion[i]))) 
        
        for i in range(len(self.listaProcesosTabla)):
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(tiemposFinalizacion[i]-self.arregloOriginal[i][1]-1))) #Tiempo estancia
        #Calcular trts
        try:
            for i in range(len(self.listaProcesosTabla)):
                trts.append( (tiemposFinalizacion[i]-self.arregloOriginal[i][1]-1)/self.arregloOriginal[i][2] )
            for i in range(len(self.listaProcesosTabla)):
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(trts[i])))
        except Exception as e:
            print(e)
    
    def insertarDatosGenericos(self):
        for i in range(len(self.arregloOriginal)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.arregloOriginal[i][0]))) #Nombres
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(self.arregloOriginal[i][1]))) #Llegada
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(self.arregloOriginal[i][2]))) #Tiempo servicio

    def insertarDatosTablaSPN(self):
        
        self.insertarDatosGenericos()
        
        trts = []
        self.listaProcesosTabla.sort(key=lambda x: x[0])
        for i in range(len(self.listaProcesosTabla)):
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(int(self.listaProcesosTabla[i][2]) + int(self.listaProcesosTabla[i][1])))) 
        
        for i in range(len(self.listaProcesosTabla)):
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str((int(self.listaProcesosTabla[i][2]) + int(self.listaProcesosTabla[i][1]))-self.arregloOriginal[i][1]-1))) #Tiempo estancia
        #Calcular trts
        try:
            for i in range(len(self.listaProcesosTabla)):
                trts.append( ((int(self.listaProcesosTabla[i][2]) + int(self.listaProcesosTabla[i][1]))-self.arregloOriginal[i][1]-1)/self.arregloOriginal[i][2] )
            for i in range(len(self.listaProcesosTabla)):
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(trts[i])))
        except Exception as e:
            print(e)
    
    def insertarDatosTablaRR(self):
        try:
            self.insertarDatosGenericos()
            trts = []
            listaAuxiliar = self.listaProcesosTabla.copy()
            ultimosProcesos = []

            m = 0
            k = -1
            while m < len(self.arregloOriginal):
                if listaAuxiliar[k][0] == self.arregloOriginal[m][0]:
                    ultimosProcesos.append(listaAuxiliar[k])
                    m += 1
                    k = -1
                else:
                    k -= 1
                
            print(ultimosProcesos)
            ultimosProcesos.sort(key=lambda x: x[0])
            tFinalizacion = []
            for i in range(len(ultimosProcesos)):
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(ultimosProcesos[i][2]+ultimosProcesos[i][1]-1)))
                tFinalizacion.append(ultimosProcesos[i][2]+ultimosProcesos[i][1]-1)
            
            tEstancia = []
            for i in range(len(ultimosProcesos)):
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(tFinalizacion[i]-self.arregloOriginal[i][1])))
                tEstancia.append(tFinalizacion[i]-self.arregloOriginal[i][1])

            for i in range(len(ultimosProcesos)):
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(tEstancia[i]/self.arregloOriginal[i][2])))


        except Exception as e:
            print(e)
    
    def insertarDatosTablaSRT(self):
        self.insertarDatosGenericos()
        trts = []
        listaAuxiliar = self.listaProcesosTabla.copy()
        ultimosProcesos = []
        m = 0
        k = -1
        while m < len(self.arregloOriginal):
                if listaAuxiliar[k][0] == self.arregloOriginal[m][0]:
                    ultimosProcesos.append(listaAuxiliar[k])
                    print('agrego caca')
                    m += 1
                    k = 0
                else:
                    k -= 1
        
        ultimosProcesos.sort(key=lambda x: x[0])
        print(ultimosProcesos)
        tFinalizacion = []
        for i in range(len(ultimosProcesos)):
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(ultimosProcesos[i][2]+ultimosProcesos[i][1]-1)))
            tFinalizacion.append(ultimosProcesos[i][2]+ultimosProcesos[i][1]-1)
        
        tEstancia = []
        for i in range(len(ultimosProcesos)):
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(tFinalizacion[i]-self.arregloOriginal[i][1])))
            tEstancia.append(tFinalizacion[i]-self.arregloOriginal[i][1])
        
        for i in range(len(ultimosProcesos)):
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(tEstancia[i]/self.arregloOriginal[i][2])))
            

            
def sexoooo2(colaDeEjecucion):
        primero = consigoPrimeroPosta(colaDeEjecucion) #El menor tiempo de llegada con el menor tiempo de ejecucion
        tiempoTotal = obtenerTiempoDeEjecucion(colaDeEjecucion)
        colaDeEjecucionAux = []
        tiempoActual = 0

        while tiempoTotal > tiempoActual: #primero arranca en tiempo 0 y dura 7, pero despues yo llego a 1 y dura 2 y otro que dura 1
                
                primero = conseguirMasChico(colaDeEjecucion, tiempoActual)
                print('primero es: ', primero)
                try:
                        colaDeEjecucionAux.append([primero[0], tiempoActual, 1])
                except:
                        pass
                
                for k in range(len(colaDeEjecucion)):
                        try:
                                if primero[0] == colaDeEjecucion[k][0]:
                                        colaDeEjecucion[k][2] = colaDeEjecucion[k][2] -1
                                if primero[2] == 0:
                                        if primero[2] == colaDeEjecucion[k][2]:
                                                colaDeEjecucion.pop(k)
                        except:
                                pass

                tiempoActual = tiempoActual + 1




        return colaDeEjecucionAux

def conseguirMasChico(colaDeEjecucion, tiempoActual):

        colaDeEjecucion.sort(key=lambda x: x[2])
        for i in range(len(colaDeEjecucion)):
                if colaDeEjecucion[i][1] <= tiempoActual:
                        return colaDeEjecucion[i]

def consigoPrimeroPosta(colaDeEjecucion):
        primero = min(colaDeEjecucion, key=lambda x: x[1])
        for i in range(len(colaDeEjecucion)):
                if primero[1] == colaDeEjecucion[i][1] and colaDeEjecucion[i][2] < primero[2]:
                        primero = colaDeEjecucion[i]
        return primero

def obtenerTiempoDeEjecucion(colaDeEjecucion):
        tiempoTotal = 0
        for i in range(len(colaDeEjecucion)):
                tiempoTotal = tiempoTotal + colaDeEjecucion[i][2] + colaDeEjecucion[i][1]
        return tiempoTotal


def algoritmoSPN(colaDeEjecucion):
        tiempoTotal = obtenerTiempoDeEjecucion(colaDeEjecucion)
        tiempoActual = 0
        colaDeEjecucionAux = []
        while tiempoActual < tiempoTotal:
                primero = conseguirMasChico(colaDeEjecucion, tiempoActual)
                try:
                    colaDeEjecucionAux.append([primero[0], tiempoActual, primero[2]])
                    tiempoActual = tiempoActual + primero[2] -1
                    for k in range(len(colaDeEjecucion)):
                            if primero[0] == colaDeEjecucion[k][0]:
                                    colaDeEjecucion.pop(k)
                                    break
                except:
                    pass




                tiempoActual += 1 
        return colaDeEjecucionAux

def conseguirPrimero(colaDeEjecucion, tiempoActual):
        for i in range(len(colaDeEjecucion)):
                if colaDeEjecucion[i][1] <= tiempoActual:
                        return colaDeEjecucion[i]



def algoritmoRoundRobin(colaDeEjecucion, quantum=3):
        # tiempoTotal = obtenerTiempoDeEjecucion(colaDeEjecucion)
        # print(tiempoTotal)
        tiempoActual = 0
        colaDeEjecucionAux = []
        tiempoTotal= obtenerTiempoDeEjecucion(colaDeEjecucion)

        while tiempoActual < tiempoTotal:
                
                primero = conseguirPrimero(colaDeEjecucion, tiempoActual)

                try:
                        if primero[2] > quantum:
                                colaDeEjecucionAux.append([primero[0], tiempoActual, quantum])
                                tiempoActual = tiempoActual + quantum -1
                                primero[2] = primero[2] - quantum
                                
                                for k in range(len(colaDeEjecucion)):
                                        if primero[0] == colaDeEjecucion[k][0]:
                                                colaDeEjecucion[k][2] = primero[2]
                                                colaDeEjecucion[k][1] = tiempoActual
                                                break
                        else:
                                colaDeEjecucionAux.append([primero[0], tiempoActual, primero[2]])
                                tiempoActual = tiempoActual + primero[2] -1
                                for k in range(len(colaDeEjecucion)):
                                        if primero[0] == colaDeEjecucion[k][0]:
                                                colaDeEjecucion.pop(k)
                                                break
                except:
                        pass
                colaDeEjecucion.sort(key=lambda x: x[1])
                if len(colaDeEjecucion) == 1:
                        
                        if colaDeEjecucion[0][1] > tiempoActual:
                                colaDeEjecucionAux.append([colaDeEjecucion[0][0], colaDeEjecucion[0][1], colaDeEjecucion[0][2]])
                        else:
                                colaDeEjecucionAux.append([colaDeEjecucion[0][0], tiempoActual, colaDeEjecucion[0][2]])
                        break
                tiempoActual += 1
        return arreglarTiempos(colaDeEjecucionAux)

def arreglarTiempos(colaDeEjecucion):
        for i in range(len(colaDeEjecucion)):
                if i == 0:
                        pass
                else:
                        if colaDeEjecucion[i-1][1] + colaDeEjecucion[i-1][2] < colaDeEjecucion[i][1]:
                            pass
                        else:
                            colaDeEjecucion[i][1] = colaDeEjecucion[i-1][1] + colaDeEjecucion[i-1][2]
        return colaDeEjecucion

def guardarDatosEnArchivo(colaDeEjecucion):
        archivo = open("datos.txt", "w")
        for i in range(len(colaDeEjecucion)):
                archivo.write(str(colaDeEjecucion[i][0]) + " " + str(colaDeEjecucion[i][1]) + " " + str(colaDeEjecucion[i][2]))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Procesos()
    window.show()
    sys.exit(app.exec_())













