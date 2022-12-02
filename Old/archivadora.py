

# primero = colaDeEjecucion[0]


# tiempoDeEjecucion = 0


# print('tiempo total de ejecucion: ', obtenerTiempoDeEjecucion(colaDeEjecucion))
                                


# print('primero: ', consigoPrimeroPosta(colaDeEjecucion))

# def conseguirPrimeroYMenorTiempo(colaDeEjecucion):
#         tiempoActual = 0
#         first=[]
#         first = consigoPrimeroPosta(colaDeEjecucion)

#         while obtenerTiempoDeEjecucion(colaDeEjecucion) > tiempoActual:
#                 for j in range(len(colaDeEjecucion)):
                        
                
#                         if first[0] == colaDeEjecucion[j][0]:
#                                 colaDeEjecucion[j][2] = colaDeEjecucion[j][2] -1

#                 first[3] = first[3] + 1
#                 tiempoActual = tiempoActual + 1
#         return colaDeEjecucionAux    


# # def aEjecutar(colaDeEjecucion, tiempoActual):
# #         print(list(filter(lambda x: (x[1] == tiempoActual) and (x[2] == min(colaDeEjecucion, lambda k: k[2])[2]), colaDeEjecucion)))





# def sexoooo(colaDeEjecucion, tiempoActual):
#         primero = consigoPrimeroPosta(colaDeEjecucion)
#         tiempoTotal = obtenerTiempoDeEjecucion(colaDeEjecucion)
#         colaDeEjecucionAux = []

#         while tiempoTotal > tiempoActual:
#                 try:
#                         for i in range(len(colaDeEjecucion)):
#                                 if primero[1] == colaDeEjecucion[i][1]:
#                                         colaDeEjecucion[i][2] = colaDeEjecucion[i][2] - 1
#                                         colaDeEjecucion[i][3] = colaDeEjecucion[i][3] + 1
#                                         primero = min(colaDeEjecucion, key=lambda x: x[2]+ x[1])
#                                 if primero[2] == 0:
#                                         if primero[0] == colaDeEjecucion[i][0]:
#                                                 colaDeEjecucion.pop(i)
#                                                 colaDeEjecucionAux.append([primero[0], primero[1], primero[3]])
#                                                 primero = consigoPrimeroPosta(colaDeEjecucion)
#                                 if primero[2] > colaDeEjecucion[i][2] and colaDeEjecucion[i][1] <= tiempoActual:
#                                         colaDeEjecucionAux.append([primero[0], primero[1], primero[3]])
#                                         primero = colaDeEjecucion[i]
#                 except:
#                         pass
                
#                 print('primero es: ', primero)
#                 if len(colaDeEjecucion) == 0:
#                         break

                             
#                 tiempoActual = tiempoActual + 1
#         return colaDeEjecucionAux

# def sexoooo2(colaDeEjecucion):
#         primero = consigoPrimeroPosta(colaDeEjecucion) #El menor tiempo de llegada con el menor tiempo de ejecucion
#         tiempoTotal = obtenerTiempoDeEjecucion(colaDeEjecucion)
#         colaDeEjecucionAux = []
#         tiempoActual = 0

#         while tiempoTotal > tiempoActual: #primero arranca en tiempo 0 y dura 7, pero despues yo llego a 1 y dura 2 y otro que dura 1
                
#                 primero = conseguirMasChico(colaDeEjecucion, tiempoActual)
#                 print('primero es: ', primero)
#                 try:
#                         colaDeEjecucionAux.append([primero[0], tiempoActual, 1])
#                 except:
#                         pass
                
#                 for k in range(len(colaDeEjecucion)):
#                         try:
#                                 if primero[0] == colaDeEjecucion[k][0]:
#                                         colaDeEjecucion[k][2] = colaDeEjecucion[k][2] -1
#                                 if primero[2] == 0:
#                                         if primero[2] == colaDeEjecucion[k][2]:
#                                                 colaDeEjecucion.pop(k)
#                         except:
#                                 pass

#                 tiempoActual = tiempoActual + 1




#         return colaDeEjecucionAux




# for i in range(tiempoTotal):
            
        #     if (colaDeEjecucion[0][3] > min(colaDeEjecucion, key=lambda x: x[3])[3]) and (min(colaDeEjecucion, key=lambda x: x[3])[1] <= i):
                
        #         colaDeEjecucionAuxiliar.append([colaDeEjecucion[0][0], colaDeEjecucion[0][2]-colaDeEjecucion[0][1], colaDeEjecucion[0][2]-colaDeEjecucion[0][3]])
        #         colaDeEjecucion[0][2] = colaDeEjecucion[0][3]
        #         colaDeEjecucion[0][1] = i

        #         colaDeEjecucion.sort(key=lambda x: x[3])
        #         print('Parte 1 bucle')

        #     if colaDeEjecucion[0][3] > 0:
        #         colaDeEjecucion[0][3] = colaDeEjecucion[0][3] - 1
                
        #         print('Parte 2 bucle')
        #         print('nombre: ', colaDeEjecucion[0][0])
        #     else:
        #         print('Parte 3 bucle')
        #         colaDeEjecucionAuxiliar.append([colaDeEjecucion[0][0], colaDeEjecucion[0][1], colaDeEjecucion[0][2]])
        #         colaDeEjecucion.pop(0)
            
        #         colaDeEjecucion[0][1] = i
        #     if len(colaDeEjecucion) == 1:
        #         colaDeEjecucionAuxiliar.append([colaDeEjecucion[0][0], colaDeEjecucion[0][1], colaDeEjecucion[0][2]])
        #         print('parte 4 bucle')
        #         break
        









colaDeEjecucion = [['Proceso 1', 40, 2], ['Proceso 2', 1, 2], ['Proceso 3',1, 1], ['Proceso 4', 1, 7], ['Proceso 5', 1, 13]]



tiempoActual = 0
colaDeEjecucion.sort(key=lambda x: x[1])

colaDeEjecucionAux = []


#Algoritmo spn

def conseguirMasChico(colaDeEjecucion, tiempoActual):

        colaDeEjecucion.sort(key=lambda x: x[2])
        for i in range(len(colaDeEjecucion)):
                if colaDeEjecucion[i][1] <= tiempoActual:
                        return colaDeEjecucion[i]


def obtenerTiempoDeEjecucion(colaDeEjecucion):
        tiempoTotal = 0
        for i in range(len(colaDeEjecucion)):
                tiempoTotal = tiempoTotal + colaDeEjecucion[i][2] + colaDeEjecucion[i][1]
        return tiempoTotal

def consigoPrimeroPosta(colaDeEjecucion):
        primero = min(colaDeEjecucion, key=lambda x: x[1])
        for i in range(len(colaDeEjecucion)):
                if primero[1] == colaDeEjecucion[i][1] and colaDeEjecucion[i][2] < primero[2]:
                        primero = colaDeEjecucion[i]
        return primero

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


# print(algoritmoSPN(colaDeEjecucion))






#Algoritmo Round Robin
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

print('Round robin3')
# print(algoritmoRoundRobin(colaDeEjecucion, 3))

#Graficar Round Robin
import matplotlib.pyplot as plt
import numpy as np

def graficarRoundRobin(colaDeEjecucion):
        x = []
        y = []
        for i in range(len(colaDeEjecucion)):
                plt.barh(colaDeEjecucion[i][0], colaDeEjecucion[i][2], left=colaDeEjecucion[i][1])
        plt.bar(x, y)
        plt.show()


# def obtenerValoresParaTabla(colaDeEjecucion):



# graficarRoundRobin(algoritmoRoundRobin(colaDeEjecucion, 3))






colaDeEjecucion = [['Proceso 1', 40, 2], ['Proceso 2', 1, 2], ['Proceso 3',1, 1], ['Proceso 4', 1, 7], ['Proceso 5', 1, 13]]
m = 0
for i in range(len(colaDeEjecucion)-1, -1, -1):
        if m == 3:
                i = len(colaDeEjecucion) - 1
        m += 1
        print(i)
        