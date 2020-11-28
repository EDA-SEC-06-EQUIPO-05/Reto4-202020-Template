"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de rutas de citibike")
    print("3- Calcular componentes conectados")
    print('4- Calcular la ruta circular')
    print("5- Buscar estaciones criticas")
    print("6- Ruta turistica por resistencia")
    print('7- Recomendador de rutas')
    print("8- Ruta de interes turistico")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de rutas de citibike ....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    estacionInicial = input("Inserte la estación de salida: ")
    estacionFinal = input("Inserte la estación de llegada: ")
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))
    conexion = controller.sameCC(cont, estacionInicial, estacionFinal)
    if conexion == True:
        print("La estación "+estacionInicial+" esta conectada fuertemente con la estación "+estacionFinal)
    elif conexion == False:
        print("La estación "+estacionInicial+" no esta conectada fuertemente con la estación "+estacionFinal)

def optionFour():
    estacionInicial = input("Inserte la estación de salida: ")
    tiempo = input('Digite el rango de tiempo en minutos (ej:180-240): ')
    print(controller.ruta_ciclica(cont, estacionInicial, tiempo))
    
def optionFive():

    resultado= controller.criticalStations(cont)
    print("Las estaciones mas transitadas de partida son "+resultado[0]+"\n")
    print("Las estaciones mas transitadas de llegada son "+resultado[1]+"\n")
    print("Las estaciones menos transitadas son "+resultado[2]+"\n")

def optionSix():

    print("resultado")

def optionSeven():
    print("Rango de edades: Digite un número según su rango de edad.")
    print('0-10 años: 1\n11-20 años: 2\n21-30 años: 3\n31-40 años: 4\n41-50 años: 5\n51-60 años: 6\n60 años o mayor: 7')
    opcionEdad = input("Ingrese su rango de edad: ")
    estaciones= controller.popularStationsbyAge(cont, opcionEdad)
    estInicial= controller.minimumCostPaths(cont,estaciones[0][0])
    caminoMasCorto= controller.minimumCostPath(cont,estaciones[1][0])
    print("La estación de la que mas personas de esa edad salen es: "+estaciones[0][0]+", con un registro de "+str(estaciones[0][1])+" personas. \n")
    print("La estación a la que mas llegan personas de esa edad es: "+estaciones[1][0]+", con un registro de "+str(estaciones[1][1])+" personas. \n")
    print("El camino mas corto desde "+estaciones[0][0]+ "hasta la estacion" +estaciones[1][0]+" es: \n"+caminoMasCorto)

def optionEight():
    lato= input("Inserte la latitud del origen: ")
    lono= input("Ingrese la longitud del origen: ")
    latd= input("Inserte la latitud del destino: ")
    lond= input("Ingrese la longitud del destino: ")
    funcion= controller.localizacion(cont,lato,lono,latd,lond)
    print(funcion)


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))    

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
