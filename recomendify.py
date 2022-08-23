#!/usr/bin/python3

import sys
from biblioteca import *
from grafo import Grafo

COEF_AMORTIGUACION = 0.85 # Coeficiente de amortiguación utilizado en PageRank.
ITERACIONES_PAGE_RANK = 50 #  Cantidad de iteraciones del PageRank.

class Recomendify:
    def __init__(self, grafo1, grafo2 = None):
        self.grafo1 = grafo1 #  Grafo no dir bipartito de usuarios con canciones que tienen en playlists (usuario <-> cancion)
        self.grafo2 = grafo2 #  Grafo no dir (que puede o no existir) que relaciona canciones en una misma playlist
        self.pagerank = None  # Lista ordenada de los pageranks de cada vertice del grafo1. Se guardará trás el primer calculo para no tener que repetirlo.
        self.comandos = {
            'camino': self.ejecutar_camino_mas_corto,
            'mas_importantes': self.ejecutar_canciones_mas_importantes,
            'recomendacion': self.ejecutar_recomendacion_usuarios_o_canciones,
            'ciclo': self.ejecutar_ciclo_n_canciones,
            'rango': self.ejecutar_todos_en_rango,
        }
    
    #   Procesa los comandos de entrada y ejecuta las funciones de Recomendify
    def procesar_comandos_entrada(self):
        
        grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios = cargar_archivo_tsv(self.grafo1, self.grafo2, sys.argv[1])
         
        for linea in sys.stdin:
            entrada = linea.rstrip().split(' ', maxsplit=1) # Separo input en [comando, argumentos]
    
            if len(entrada) == 1:
                print("Por favor ingrese un comando valido (poca cantidad de parámetros).\n")
                
            comando, parametros = entrada
            funcion_comando = self.comandos.get(comando)
            if funcion_comando is not None:
                funcion_comando(parametros, grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios)
        
    #   Busca el camino más corto entre una canción origen y otra destino.
    def ejecutar_camino_mas_corto(self, parametros, grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios): 
        origen, destino = (parametros.strip()).split(' >>>> ')
       
        if parametros_validos_camino(grafo1, origen, destino, canciones) is False:
            return
          
        camino = camino_con_bfs(grafo1, origen, destino)

        if camino is False: 
            print("No se encontro recorrido")
            return 
        else: 
            imprimir_formato_camino(grafo1, camino)
            return     
        
    #   Muestra las n canciones más centrales/importantes del mundo según el algoritmo de pagerank, ordenadas de mayor importancia a menor importancia.
    def ejecutar_canciones_mas_importantes(self, parametros, grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios):
        
        n = parametros_validos_mas_importantes(parametros.split(' '))

        #   Si ya había calculado PageRank, no repito el calculo como es pedido en la consigna
        if self.pagerank is not None:
            imprimir_formato_mas_importantes_y_recomendaciones(self.pagerank, n)   
            return

        if n is False: 
            return

        rankings = pagerank(grafo1, COEF_AMORTIGUACION, ITERACIONES_PAGE_RANK, None)
        lista_rankings = sorted([(rankings[cancion], cancion) for cancion in rankings if cancion in canciones.keys()])[::-1]
        self.pagerank = lista_rankings
        imprimir_formato_mas_importantes_y_recomendaciones(lista_rankings, n)

    #   Recibe una lista de gustos de un usuario y devuelve recomendaciones de canciones o usuarios acordes.
    def ejecutar_recomendacion_usuarios_o_canciones(self, parametros, grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios):
        tipo, cantidad, canciones_o_usuarios = procesar_parametros_recomendacion(parametros.split(' '))
        
        if tipo == 'canciones':
            for cancion in canciones_o_usuarios:
                if cancion is None or grafo1.existe_vertice(cancion) is False:
                    print("La canción {} no está dentro del grafo.\n".format(cancion))
                    return False

        if tipo == 'usuarios':
            for usuario in canciones_o_usuarios:
                if usuario is None or grafo1.existe_vertice(usuario) is False:
                    print("El usuario {} no está dentro del grafo.\n".format(usuario))
                    return False

        recomendaciones(grafo1, int(cantidad), canciones_o_usuarios, tipo, canciones)
        
    #   Obtiene un ciclo de largo n que comience en la canción indicada.
    def ejecutar_ciclo_n_canciones(self, parametros, grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios):

        n, cancion = procesar_parametros_ciclo_y_rango(parametros.split(' '))

        if cancion not in usuarios.keys():
            return 

        if grafo2 == None:
            grafo2 = Grafo()
            self.grafo2 = generar_grafo_canciones(grafo2, usuarios, canciones_usuarios)

        if not grafo2.existe_vertice(cancion):
            return
        
        camino, visitados = list(), set()
        hay_camino, camino = dfs_ciclo_backtracking(grafo2, int(n), cancion, cancion, visitados, camino)

        if hay_camino:
            print(*camino, sep=' --> ')
            return 
        else:
            print("No se encontro recorrido")
            return 

    #   Obtiene la cantidad de canciones que se encuenten a exactamente n saltos desde la canción
    def ejecutar_todos_en_rango(self, parametros, grafo1, grafo2, usuarios, playlists, canciones, canciones_usuarios):
        n, cancion = procesar_parametros_ciclo_y_rango(parametros.split(' '))
        if grafo2 == None:
            grafo2 = Grafo()
            self.grafo2 = generar_grafo_canciones(grafo2, usuarios, canciones_usuarios)
       
        if not grafo2.existe_vertice(cancion):
            return

        resultado = cantidad_de_vertices_en_x_rango(grafo2, cancion, int(n))
        print(resultado)
        return



if __name__ == "__main__":
    grafo1 = Grafo()
    Recomendify(grafo1, None).procesar_comandos_entrada()