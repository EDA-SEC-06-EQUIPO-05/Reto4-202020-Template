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

import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzerC()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(analyzer):
    for nombre in os.listdir(cf.data_dir):
        if nombre.endswith(".csv"):
            loadFiles(analyzer, nombre)
    return analyzer

def loadFiles(analyzer,archive):
    archivo = cf.data_dir + archive
    input_archivo = csv.DictReader(open(archivo, encoding="utf-8"),
                                delimiter=",")
    for viaje in input_archivo:
        if viaje != None and viaje != "" and viaje != " ":
            model.addTrip(analyzer,viaje)
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def ruta_ciclica(analyzer, estacion, tiempo):
    return model.ruta_ciclica(analyzer, estacion, tiempo)
    
def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

def sameCC(analyzer, est1, est2):
    return model.mismoCC(analyzer, est1, est2)

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg

def criticalStations(analyzer):

    estaciones= model.estacionesCriticas(analyzer)
    return estaciones

def popularStationsbyAge(analyzer, ageOption):

    age1= 0
    age2= 0
    if ageOption==1:
        age1= 0
        age2= 10
    elif ageOption==2:
        age1= 11
        age2= 20
    elif ageOption==3:
        age1= 21
        age2= 30
    elif ageOption==4:
        age1= 31
        age2= 40
    elif ageOption==5:
        age1= 41
        age2= 50
    elif ageOption==6:
        age1= 51
        age2= 60
    elif ageOption==7:
        age1= 60
        age2= 0

    tuplaEstacionesOrigen= model.estacionesPopularesporEdadesOrigen(analyzer, age1, age2)
    tuplaEstacionesDestino= model.estacionesPopularesporEdadesDestino(analyzer, age1, age2)

    return (tuplaEstacionesOrigen,tuplaEstacionesDestino)

def localizacion(analyzer, lat1, lon1, lat2, lon2):

    funcion= model.stationbyLocation()