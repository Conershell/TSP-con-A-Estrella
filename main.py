import numpy as np
import csv
import time
from math import sqrt


class Nodo:
    # CONSTRUCTOR
    def __init__(self, padre=None, posicion_x=None, posicion_y=None, identificador_ciudad=None):
        self.padre = padre
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.g = 0
        self.h = 0
        self.f = 0
        self.identificador_ciudad = identificador_ciudad


def NumeroCiudades(nombreArchivo):
    f = open(nombreArchivo)
    numeroNodos = f.readline()
    f.close()
    return int(numeroNodos)


def AsignaMatrizCordenadas(nombreArchivo):
    f = open(nombreArchivo)
    numeroNodos = f.readline()
    matrizCordenadas = np.array([[]])
    for linea in f:
        id_ciudad = None
        x_ciudad = None
        y_ciudad = None
        for letra in linea.split(' '):
            if id_ciudad is None:
                id_ciudad = letra
                continue
            if x_ciudad is None:
                x_ciudad = letra
                continue
            if y_ciudad is None:
                y_ciudad = letra.rstrip()
                continue

        if matrizCordenadas.size == 0:
            matrizCordenadas = np.array([[x_ciudad, y_ciudad]])
        else:
            matrizCordenadas = np.append(matrizCordenadas, [[x_ciudad, y_ciudad]], axis=0)

    f.close()
    return matrizCordenadas


def DistanciaEntreCiudades(matrizCordenadas, ciudadA, ciudadB):
    distancia = sqrt(((int(matrizCordenadas[ciudadB][0]) - int(matrizCordenadas[ciudadA][0])) ** 2) + (
            (int(matrizCordenadas[ciudadB][1]) - int(matrizCordenadas[ciudadA][1])) ** 2))
    return distancia


def MatrizAdyacencia(matrizCordenadas):
    numeroCiudades = int(matrizCordenadas.size / 2)
    matrizAdyacencia = np.zeros((numeroCiudades, numeroCiudades))
    for i in range(numeroCiudades):  # FILAS
        for j in range(numeroCiudades):  # COLUMNAS
            matrizAdyacencia[i][j] = DistanciaEntreCiudades(matrizCordenadas, i, j)

    return matrizAdyacencia


def CalculoHeuristica(matrizAdyacencia, numeroCiudades):
    sum = 0
    for i in range(int(numeroCiudades)):  # FILAS
        for j in range(int(numeroCiudades)):  # COLUMNAS
            # ALGORITMO DE CALCULO DE HEURISTICA
            if i != j:
                sum += matrizAdyacencia[i][j]
                heuristica = sum / int(numeroCiudades)

    return heuristica


def NotInList(node_successor_list, nodo_actual):
    for nodo in node_successor_list:
        if nodo_actual.identificador_ciudad == nodo.identificador_ciudad:
            return False
        else:
            return True

    return True


def CiudadExisteEnLista(identificador, lista):
    for nodo in lista:
        if nodo.identificador_ciudad == identificador:
            return True
    return False


def ActualizaGLista(identificador, nuevoCosto, lista, nodo_inicial):
    for nodo in lista:
        if nodo.identificador_ciudad == identificador:
            nodo.g = nuevoCosto
    if(identificador == nodo_inicial.identificador_ciudad):
        nodo_inicial.g = nuevoCosto


def ActualizaPadreLista(identificador, padre, lista):
    for nodo in lista:
        if identificador == nodo.identificador_ciudad:
            nodo.padre = padre


def AEstrella(matrizCordenadas, numeroCiudades, matrizAdyacencia):
    nodo_inicial = Nodo(None, matrizCordenadas[0][0], matrizCordenadas[0][1], 0)
    nodo_final = nodo_inicial
    open_list = []  # LISTA CON POSIBLES NODOS A EXTENDER
    closed_list = []  # LISTA CON NODOS YA EXPANDIDOS
    node_successor_list = []
    heuristica = CalculoHeuristica(matrizAdyacencia, numeroCiudades)
    nodo_inicial.h = heuristica  # SETEO LA HEURSITICA DEL NODO INCIAL AL VALOR DE LA HEURISTICA
    open_list.append(nodo_inicial)
    nodo_actual = nodo_inicial  # INICIALIZO EL NODO ACTUAL PARA EVITAR UN ERROR :/
    global nodos_expandidos

    while open_list.__len__() > 0:
        # ASIGNO COMO NODO ACTUAL AL DE MENOR F()
        minFuncionNodo = 100000000000
        index = 0
        for node in open_list:
            node.f = node.g + node.h
            if node.f < minFuncionNodo:
                minFuncionNodo = node.f
                nodo_actual = node
                index = open_list.index(node)


        open_list.pop(index)
        # AQUI SACAMOS AL NODO ACTUAL DE LA LISTA DE NODOS SUCESORES
        if node_successor_list.__len__() != 0:
            for i in node_successor_list:
                if i.identificador_ciudad == nodo_actual.identificador_ciudad:
                    node_successor_list.pop(node_successor_list.index(i))

        # CONDICION DE SALIDA DEL A ESTRELLA
        if nodo_actual.identificador_ciudad == nodo_final.identificador_ciudad and closed_list.__len__() == numeroCiudades:
            break

        # CREO LOS NODOS SUCESORES DEL NODO ACTUAL
        node_successor_list = []
        if node_successor_list.__len__() == 0 and closed_list.__len__() < (numeroCiudades - 1):
            for i in range(numeroCiudades):
                if nodo_actual.identificador_ciudad != i and nodo_actual not in closed_list and not CiudadExisteEnLista(
                        i, closed_list):
                    nodo_sucesor = Nodo(nodo_actual, matrizCordenadas[i][0], matrizCordenadas[i][1], i)
                    nodo_sucesor.g = nodo_actual.g + DistanciaEntreCiudades(matrizCordenadas, nodo_actual.identificador_ciudad,
                                                    i)
                    nodo_sucesor.h = heuristica
                    node_successor_list.append(nodo_sucesor)  # LISTA DE NODOS SUCESORES DEL NODO ACTUAL
                    nodos_expandidos += 1
        # CUANDO SE TERMINARON DE CREAR LAS CIUDADES SUCESORAS SE VUELVE AGREGAR LA CIUDAD DE ORIGEN A LA LISTA DE SUCESORES
        elif node_successor_list.__len__() == 0 and closed_list.__len__() == (numeroCiudades - 1):
            nodo_sucesor = nodo_inicial
            nodo_sucesor.padre = nodo_actual
            nodo_sucesor.g = DistanciaEntreCiudades(matrizCordenadas, nodo_actual.identificador_ciudad,
                                                    i.identificador_ciudad) + nodo_actual.g
            node_successor_list.append(nodo_sucesor)
            nodos_expandidos += 1

        for i in node_successor_list:
            distProxCiudad = DistanciaEntreCiudades(matrizCordenadas, nodo_actual.identificador_ciudad,
                                                    i.identificador_ciudad)
            successor_current_cost = nodo_actual.g + distProxCiudad
            ActualizaGLista(i.identificador_ciudad, successor_current_cost, open_list, nodo_inicial)
            if CiudadExisteEnLista(i.identificador_ciudad, open_list):
                ActualizaPadreLista(i.identificador_ciudad, i.padre, open_list)
                if i.g <= successor_current_cost:

                    continue
            elif CiudadExisteEnLista(i.identificador_ciudad, closed_list) and i.identificador_ciudad != 0:
                if i.g <= successor_current_cost:

                    continue
                closed_list.pop(closed_list.index(i))
                open_list.append(i)
            else:

                open_list.append(i)

            if i.identificador_ciudad != 0:
                open_list.remove(i)
                i.g = successor_current_cost
                i.padre = nodo_actual
                open_list.append(i)

        # AGREGA LA CIUDAD INICIAL A LA CLOSED LIST
        if closed_list.__len__() == 0:
            closed_list.append(nodo_actual)

        # AGREGO LA CIUDAD ACTUAL (NODO ACTUAL) A LA CLOSED LIST SI ES QUE YA NO ESTABA AGREGADA
        nodoActualEstaEnLaClosedList = False
        for i in closed_list:
            if i.identificador_ciudad == nodo_actual.identificador_ciudad:
                nodoActualEstaEnLaClosedList = True
                break
        if not nodoActualEstaEnLaClosedList:
            closed_list.append(nodo_actual)

    if nodo_actual is not nodo_final:
        print("NO DEBERIA SALIR ESTE ERROR, LA LISTA ESTA VACIA.!!")
    return closed_list


nombreArchivo = None
while nombreArchivo is None:
    nombreArchivo = input("Ingrese el nombre de archivo con extension (Ej: inst1.tsp): ")

numeroCiudades = NumeroCiudades(nombreArchivo)  # OBTIENE EL NUMERO DE CIUDADES
matrizCordenadas = AsignaMatrizCordenadas(nombreArchivo)  # CREA LA MATRIZ DE CORDENADAS DE LAS CIUDADES
matrizAdyacencia = MatrizAdyacencia(matrizCordenadas)  # CREA LA MATRIZ DE COSTOS DE UNA CIUDAD i A LA CIUDAD j
recorridoArbol = []  # INICIALIZO LA LISTA QUE CONTIENE EL RECORRIDO FINAL
nodos_expandidos = 0  # VARIABLE GLOBAL DE NODOS EXPANDIDOS
inicioTiempo = time.time()  # INICIA CONTADOR DE TIEMPO DEL A*
recorridoArbol = AEstrella(matrizCordenadas, numeroCiudades, matrizAdyacencia)  # RETORNA LA RESPUESTA DEL RECORRIDO DEL A*
finTiempo = time.time()  # TERMINA EL CONTADOR DE TIEMPO DEL A*
tiempoEjecutado = finTiempo - inicioTiempo

# AQUI SE CREA Y LLENA UNA LISTA CON LOS IDENTIFICADORES DE CADA CIUDAD RECORRIDA
listaCiudadesAEstrella = []
distanciaTotalTour = recorridoArbol[0].g
for nodo in recorridoArbol:
    listaCiudadesAEstrella.append(nodo.identificador_ciudad)
listaCiudadesAEstrella.append(recorridoArbol[0].identificador_ciudad)

# SE ESCRIBE EN EL CSV LA INSTANCIA, SOLUCION OBTENIDA, NODOS EXPANDIDOS Y EL TIEMPO
with open('AndreDucheylard_FabianCardenas_resultados.csv', 'w', newline='') as csvfile:
    nombreColumnas = ['Instancia', 'Solucion Obtenida', "Nodos Expandidos", "Tiempo Solucion"]
    writer = csv.DictWriter(csvfile, fieldnames=nombreColumnas)

    writer.writerow({"Instancia": "Instancia " + nombreArchivo, "Solucion Obtenida": "Solucion Obtenida: " + str(listaCiudadesAEstrella), "Nodos Expandidos": "Nodos Expandidos: " + str(nodos_expandidos), "Tiempo Solucion": "Tiempo Solucion: " + str(tiempoEjecutado) + " segundos"})
print("Distancia Total Del Tour: " + str(distanciaTotalTour))
print("Tiempo total del A*: " + str(tiempoEjecutado))
print("Nodos Expandidos: " + str(nodos_expandidos))
