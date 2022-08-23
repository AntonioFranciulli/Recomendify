from collections import deque
from grafo import Grafo
import re
import sys
import random

ITERACIONES_RANDOMWALKS = 10


##################################################################################
# Utilidades y comandos propios de Recomendify
##################################################################################

#   Función que verifica si un numero es entero o no.
def es_entero(n):
    try: 
        int(n)
        return True
    except ValueError:
        return False

#   Recibe una lista de cadenas e itera sobre ella reconstruyendo nombres de canciones dados por parametro.
def reconstruir_nombres_canciones(lista):
    cancion = ''
    resultado = []
    for i in range(len(lista)):
        if lista[i] != ">>>>":
            cancion+="{} ".format(lista[i])
        else:
            resultado.append(cancion.strip())
            cancion = ''
            continue
    
    resultado.append(cancion.strip())
    return resultado

#   Recibe una lista de parámetros y verifica que sean válidos para el comando canciones.
def parametros_validos_mas_importantes(parametros):
    if len(parametros) != 1 or not es_entero(parametros[0]):
        print("Por favor ingrese un número entero (ej: mas_importantes 20).\n")
        return False

    return int(parametros[0])

#   Recibe una lista de parámetros y verifica que sean validos para el comando recomendación.
def procesar_parametros_recomendacion(parametros):
    if not es_entero(parametros[1]):
        print("Por favor ingrese un número entero (ej: recomendacion canciones 10 Love Story - Taylor Swift).\n")
        return False

    tipo = parametros[0]
    cantidad = parametros[1]
    canciones_o_usuarios = reconstruir_nombres_canciones(parametros[2:])
    
    return tipo, cantidad, canciones_o_usuarios

#   Recibe una lista de parámetros y verifica que sean válidos para el comando ciclo y rango.
def procesar_parametros_ciclo_y_rango(parametros):
    if not es_entero(parametros[0]):
        print("Por favor ingrese un número entero (ej: ciclo 7 By The Way - Red Hot Chili Peppers).\n")
        return False
    n = parametros[0]
    cancion = reconstruir_nombres_canciones(parametros[1:])
    return n, cancion[0]

#   Recibe un origen y un destino y verifica si son válidos para buscar un camino entre ellos.
def parametros_validos_camino(grafo1, origen, destino, canciones):
    if not grafo1.existe_vertice(origen) or not grafo1.existe_vertice(destino) or not origen in canciones.keys() or not destino in canciones.keys():
        print("Tanto el origen como el destino deben ser canciones")
        return False
    return True

#   Recibe una ruta de archivo para agregarlos al grafo
#   El archivo esperado contiene los datos en forma de TSV (valores separados por '\t')
def cargar_archivo_tsv(grafo1, grafo2, archivo):
    
    usuarios = {}           # Diccionario que vincula cancion y artista con los usuarios que tienen esa cancion en sus playlists. Ej: [nombre de playlist] = [user_id1, user_id2, user_id3, ...]
    playlists = {}          # Diccionario que vincula nombre de playlist y una lista con sus canciones. Ej: [nombre_playlist] = [cancion1, cancion2, cancion3, ...]
    canciones = {}          # Diccionario que vincula canciones con los generos a los que pertenece. Ej: [Eraser - Ed Sheeran] = [Pop, Rock, Pop/Rock]]
    canciones_usuarios = {} # Diccionario que vincula Usuarios con las canciones que tienen en sus playlists. Ej: [user_id] = [cancion1, cancion2, cancion3, ...]

    with open(archivo) as datos:
        next(datos)
        for linea in datos:
            linea = linea.strip().split("\t")
            user_id, cancion, artista, id_playlist, nombre_playlist, generos = linea[1], linea[2], linea[3], linea[4], linea[5], linea[6]

            cancion_artista = " - ".join((cancion, artista))

            grafo1.agregar_arista((user_id, cancion_artista), nombre_playlist, True)

            if not cancion_artista in usuarios.keys():
                usuarios[cancion_artista] = [user_id]
            
            if cancion_artista in usuarios.keys():
                usuarios[cancion_artista].append(user_id)

            if not user_id in canciones_usuarios.keys():
                canciones_usuarios[user_id] = [cancion_artista]

            if user_id in canciones_usuarios.keys():
                canciones_usuarios[user_id].append(cancion_artista)

            if not nombre_playlist in playlists.keys():
                playlists[nombre_playlist] = []
            
            if not cancion_artista in playlists[nombre_playlist]:
                playlists[nombre_playlist].append(cancion_artista)

            if not cancion_artista in canciones.keys():
                canciones[cancion_artista] = generos.split(',')
               
    return grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios

#   Recibe un diccionario de playlists y crea un grafo no dirigido con canciones como vertices y aristas uniendolas si esas canciones pertenecen a una misma playlist.
def generar_grafo_canciones(grafo2, usuarios, canciones_usuarios):
    visitados = set()
    for cancion_actual in usuarios.keys():
        usuarios_de_cancion_actual = usuarios[cancion_actual]
        visitados2 = set()
        for usuario_actual in usuarios_de_cancion_actual:
            for canciones_a_agregar in canciones_usuarios[usuario_actual]:
                if (not canciones_a_agregar == cancion_actual) and (not canciones_a_agregar in visitados) and (not canciones_a_agregar in visitados2):
                    grafo2.agregar_arista((cancion_actual, canciones_a_agregar),None,True)
                    visitados2.add(canciones_a_agregar)
        visitados.add(cancion_actual)
    
    return grafo2

#   Función que itera sobre un camino en forma de lista, le da el formato pedido e imprime el resultado.
def imprimir_formato_camino(grafo1, camino):
    cancion = "{} --> aparece en playlist --> {} --> de --> "
    user = "{} --> tiene una playlist --> {} --> donde aparece --> "
    res = ""

    for vertice in range(len(camino)-1):
        if vertice % 2 == 0:
            playlist = grafo1.obtener_peso(camino[vertice],camino[vertice+1])
            res+=(cancion.format(camino[vertice], playlist))
        else:
            playlist = grafo1.obtener_peso(camino[vertice], camino[vertice +1])
            res+=(user.format(camino[vertice], playlist))

        if vertice == len(camino)-2: res+=(camino[vertice+1])
    
    print(res)
    return

#   Función que itera sobre una lista, le da el formato pedido en mas_importantes o recomendaciones e imprime el resultado.
def imprimir_formato_mas_importantes_y_recomendaciones(lista, cantidad_canciones):
    res = "" 
    for i in range(cantidad_canciones):
        if i != (cantidad_canciones - 1):
            res+=("{}; ".format(lista[i][1]))
        else:
            res+=("{}".format(lista[i][1]))
    
    print(res)
    return

#   Función que toma una lista de gustos de un usuario y devuelve recomendaciones acordes.
def recomendaciones(grafo, cantidad_recomendaciones, canciones_o_usuarios, tipo, canciones):
    page_rank = {}
    for cancion_o_usuario in canciones_o_usuarios:
        camino = random_walk(grafo, cantidad_recomendaciones, cancion_o_usuario)
        pagerank_modificado(grafo, page_rank, cantidad_recomendaciones, camino)
    
    if tipo == 'canciones':
        lista_recom = [(page_rank[cancion], cancion) for cancion in page_rank if cancion in canciones.keys() and cancion not in canciones_o_usuarios]
        imprimir_formato_mas_importantes_y_recomendaciones(sorted(lista_recom)[::-1], int(cantidad_recomendaciones))
        return  

    else:
        lista_recom = [(page_rank[usuario], usuario) for usuario in page_rank if usuario not in canciones.keys() and usuario not in canciones_o_usuarios]
        imprimir_formato_mas_importantes_y_recomendaciones(sorted(lista_recom)[::-1], int(cantidad_recomendaciones))
        return 




##################################################################################
#   BFS
##################################################################################
#   Recorrido tipo BFS desde un vertice en particular.
def bfs(grafo, vertice_origen):
    visitados = set()
    padres = {}
    niveles = {}

    padres[vertice_origen] = None
    niveles[vertice_origen] = 0
    visitados.add(vertice_origen)

    q = deque()
    q.append(vertice_origen)

    while not len(q) == 0:
        vertice = q.popleft()

        for adyacente in grafo.obtener_adyacentes(vertice):
            if adyacente not in visitados:
                visitados.add(adyacente)
                nivel = niveles[vertice] + 1
                niveles[adyacente] = nivel
                padres[adyacente] = vertice
                q.append(adyacente)

    return padres, niveles

#   Busqueda de camino minimo mediante un recorrido BFS
def camino_con_bfs(grafo, vertice_origen, vertice_destino):
    visitados = set()
    padres = {}
    niveles = {}

    padres[vertice_origen] = None
    niveles[vertice_origen] = 0
    visitados.add(vertice_origen)

    q = deque()
    q.append(vertice_origen)

    while not len(q) == 0:
        vertice = q.popleft()
        for adyacente in grafo.obtener_adyacentes(vertice):
            if adyacente not in visitados:
                visitados.add(adyacente)
                nivel = niveles[vertice] + 1
                niveles[adyacente] = nivel
                padres[adyacente] = vertice
                q.append(adyacente)
                if adyacente == vertice_destino:
                    return reconstruir_camino(padres, vertice_destino)

    return False

#   Utilidad que permite reconstruir el orden de vertices del camino obtenido en camino_con_bfs
def reconstruir_camino(padres, vertice_destino):
    vertice = vertice_destino
    camino = []
    while vertice is not None:
        camino.append(vertice)
        vertice = padres[vertice]
    return camino[::-1]

#   Función que cuenta la cantidad de vertices que se encuentran a x saltos de un vertice particular.
def cantidad_de_vertices_en_x_rango(grafo2, cancion, rango):
    
    visitados = set()
    niveles = {}

    niveles[cancion] = 0
    visitados.add(cancion)

    q = deque([])
    q.append(cancion)

    cantidad = 0
    while q:
        vertice = q.popleft()
        for adyacente in grafo2.obtener_adyacentes(vertice):
            if adyacente not in visitados:
                visitados.add(adyacente)
                niveles[adyacente] = int(niveles[vertice]) + 1
                if int(niveles[adyacente]) > rango: 
                    break
                if int(niveles[adyacente]) == rango: 
                    cantidad += 1   
                q.append(adyacente)
  
    return cantidad



##################################################################################
#   DFS
##################################################################################
#   Recorrido tipo DFS desde un vertice en particular.
def dfs(grafo, vertice_origen):
    visitados = set()
    padres = {}
    niveles = {}

    padres[vertice_origen] = None
    niveles[vertice_origen] = 0
    
    _dfs(grafo, vertice_origen, visitados, padres, niveles)
    return padres, niveles

#   Función auxiliar para la recursión de DFS
def _dfs(grafo, vertice_origen, visitados, padre, niveles):
    visitados.add(vertice_origen)
    for ady in grafo.obtener_adyacentes(vertice_origen):
        if ady not in visitados:
            padre[ady] = vertice_origen
            niveles[ady] = niveles[vertice_origen] + 1
            _dfs(grafo, ady, visitados, padre, niveles)

#   Función que busca ciclos de n largo mediante un recorrido BFS con Backtracking y devuelve True o False y el camino en cuestión.
def dfs_ciclo_backtracking(grafo, n, origen, actual, visitados, camino):
    visitados.add(actual)
    camino.append(actual)

    if len(camino) == n and len(camino) != 1 and actual != origen:
        for w in grafo.obtener_adyacentes(actual):
            if w == origen:
                camino.append(w)
                return True, camino[::-1]

        camino.pop()
        visitados.remove(actual)
        return False, camino

 
    for w in grafo.obtener_adyacentes(actual):
        if w not in visitados:
            hay_camino, camino = dfs_ciclo_backtracking(grafo, n, origen, w, visitados, camino)
            if hay_camino:
                return True, camino
            visitados.add(w)

    visitados.remove(actual)
    camino.pop()
    return False, camino


##################################################################################
#   PAGERANK
##################################################################################
#   Función que mediante el algoritmo de PageRank, genera un ranking de las vertices más importantes.
def pagerank(grafo, coef_amortiguacion, iteraciones, ranking_ini=None):
    cantidad_vertices = grafo.__len__()
    if ranking_ini is None:
        ranking_ini = {}

    for vertice in grafo.obtener_vertices():
        if not vertice in ranking_ini.keys():
            ranking_ini[vertice] = 1 / cantidad_vertices

    for i in range (iteraciones):
        pagerank = {}
        for v in grafo.obtener_vertices():
            suma_pr_ady = 0
            for w in grafo.obtener_adyacentes(v):
                suma_pr_ady += ranking_ini[w] / len(grafo.obtener_adyacentes(w)) 
                pagerank[v] = (1 - coef_amortiguacion) / cantidad_vertices + coef_amortiguacion * suma_pr_ady

        ranking_ini = pagerank
        
    return pagerank

#   Función que realiza un recorrido tipo RandomWalk de un largo especificado y desde un vertice especificado o aleatorio.
def random_walk(grafo, largo, vertice=None):
    if vertice is None:
        vertice = random.choice(grafo.obtener_vertices())
    camino = [vertice]

    while len(camino) < int(largo):
        vertice = random.choice(grafo.obtener_adyacentes(vertice))
        camino.append(vertice)

    return camino

#   Función PageRank modificado para utilizar en sistema de recomendaciones.
def pagerank_modificado(grafo, ranking, cantidad_recomendaciones, camino):
    for vertice in camino:
        if vertice not in ranking:
            ranking[vertice] = 1

    for i in range(cantidad_recomendaciones):
        for j in range(cantidad_recomendaciones):
            ranking[camino[i-1]] = (ranking[camino[i]] / len(grafo.obtener_adyacentes(camino[i-1])))