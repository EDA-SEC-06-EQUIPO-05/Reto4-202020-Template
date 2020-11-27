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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import minpq as pq
from DISClib.Algorithms.Sorting import selectionsort as sel
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def newAnalyzerC():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'graph': None,
                    'stops': None,
                    'components': None,
                    'connections': None,
                    'ages'
                    }

        analyzer["graph"]= gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStopIds)

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer["connections"]= gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStopIds)

        analyzer['ages'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareAges)                

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzerC')

# Funciones para agregar informacion al grafo

def addTrip(analyzer, viaje):
    origen = viaje["start station id"]
    destino = viaje["end station id"]
    duracion = int(viaje["tripduration"])
    addStation(analyzer, origen)
    addStation(analyzer, destino)
    addConnectionC(analyzer, origen, destino, duracion)
    addAges(analyzer, origen)
    addAges(analyzer, destino)

def addStation(analyzer, stationID):
    if not gr.containsVertex(analyzer["graph"], stationID):
        gr.insertVertex(analyzer["graph"], stationID)
    return analyzer

def addStopConnection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = formatVertex(lastservice)
        destination = formatVertex(service)
        cleanServiceDistance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        addStop(analyzer, origin)
        addStop(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        addRouteStop(analyzer, service)
        addRouteStop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addStop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')


def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['stops'], service['BusStopCode'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['ServiceNo'])
        m.put(analyzer['stops'], service['BusStopCode'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['ServiceNo']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer

def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['stops'])
    stopsiterator = it.newIterator(lststops)
    while it.hasNext(stopsiterator):
        key = it.next(stopsiterator)
        lstroutes = m.get(analyzer['stops'], key)['value']
        prevrout = None
        routeiterator = it.newIterator(lstroutes)
        while it.hasNext(routeiterator):
            route = key + '-' + it.next(routeiterator)
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route

def addRouteConnectionsC(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['stops'])
    stopsiterator = it.newIterator(lststops)
    while it.hasNext(stopsiterator):
        key = it.next(stopsiterator)
        lstroutes = m.get(analyzer['stops'], key)['value']
        prevrout = None
        routeiterator = it.newIterator(lstroutes)
        while it.hasNext(routeiterator):
            route = key + '-' + it.next(routeiterator)
            if prevrout is not None:
                addConnectionC(analyzer, prevrout, route, 0)
                addConnectionC(analyzer, route, prevrout, 0)
            prevrout = route


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

def addConnectionC(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['graph'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["graph"], origin, destination, distance)
    return analyzer

# ==============================
# Funciones de consulta
# ==============================
def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])

def mismoCC(analyzer, estacion1, estacion2):
    return scc.stronglyConnected(analyzer["components"], estacion1, estacion2)

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['graph'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg

def estacionesCriticas(analyzer):

    cuenta= 0
    estaciones= gr.vertices(analyzer["graph"])
    listaEntrada= lt.newList("ARRAY_LIST", comparestations)
    listaSalida= lt.newList("ARRAY_LIST", comparestations)
    listaSolitarias= lt.newList("ARRAY_LIST", comparestations)
    entradasConcurridas= lt.newList("ARRAY_LIST", compareSizes)
    salidasConcurridas= lt.newList("ARRAY_LIST", compareSizes)
    estacionesSolitarias= lt.newList("ARRAY_LIST", compareSizes)
    while cuenta<lt.size(estaciones):
        estacion= lt.getElement(estaciones, cuenta)
        entrada= gr.indegree(analyzer["graph"], estacion)        
        lt.addFirst(entradasConcurridas,entrada)
        salida= gr.outdegree(analyzer["graph"], estacion)
        lt.addFirst(salidasConcurridas,salida)
        bidireccional= gr.degree(analyzer["graph"], estacion)
        lt.addFirst(estacionesSolitarias,bidireccional)
        cuenta+= 1

    entradasOrg= sel.selectionSort(entradasConcurridas,lessequal)
    salidasOrg= sel.selectionSort(salidasConcurridas,lessequal)
    solitariasOrg= sel.selectionSort(estacionesSolitarias,lessequal)
    print(entradasOrg)

    for conteo in range(0,3):
        if entrada == lt.getElement(entradasOrg, conteo):
            lt.insertElement(listaEntrada, estacion, conteo)
        if salida == lt.getElement(salidasOrg, conteo):
            lt.insertElement(listaSalida, estacion, conteo)
        if bidireccional == lt.getElement(solitariasOrg, conteo):
            lt.insertElement(listaSolitarias, estacion, conteo)
    if lt.size(listaEntrada) > 3:
        lt.removeLast(listaEntrada)
    if lt.size(listaSalida) > 3:
        lt.removeLast(listaSalida)
    if lt.size(listaSolitarias) > 3:
        lt.removeLast(listaSolitarias)

    return (listaEntrada, listaSalida, listaSolitarias)
    
# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombre del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name


# ==============================
# Funciones de Comparacion
# ==============================


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def comparestations(station1,station2):
    if (station1 == station2):
        return 0
    elif (station1 != station2):
        return 1
    else:
        return -1

def compareSizes(size1, size2):
    if (size1 == size2):
        return 0
    elif (size1 > size2):
        return 1
    else:
        return -1

def lessequal(a,b):

    return a < b

def compareAges(age1, age2):

    if age1 == age2:
        return 0
    elif age1 > age2:
        return 1
    else:
        return -1