
class Grafo:
    def __init__(self):
        self.tabla = {}
        pass
    
    def __len__(self):
        return len(self.tabla)
    

    ###############################################################################
    # Vertices
    ###############################################################################

    # Agrega vertice si no existe
    # Post: Se agrego el vertice si no existia
    def agregar_vertice(self, vertice):
        if not self.existe_vertice(vertice):
            self.tabla[vertice] = {}

    # Borra el vertice
    # Post: El vertice no existe en el grafo, ningun otro vertice lo referencia.
    def borrar_vertice(self, vertice):
        self.tabla.pop(vertice, None)

        for vertices_destino in self.tabla.values():
            vertices_destino.pop(vertice, None)

    # Devuelve verdadero si existe algún vínculo entre vertices.
    def son_vertices_unidos(self, vertice, otroVertice):
        if (self.tabla.get(vertice, {}).get(otroVertice) is not None):
            return True, self.tabla.get(vertice, {}).get(otroVertice)
        elif (self.tabla.get(otroVertice, {}).get(vertice) is not None):
            return True, self.tabla.get(otroVertice, {}).get(vertice)
        else: return False

    # Devuelve verdadero si existe vertice
    def existe_vertice(self, vertice):
        return self.tabla.get(vertice) is not None

    # Devuelve lista de vertices
    def obtener_vertices(self):
        return list(self.tabla.keys())

    # Devuelve lista de los vertices adyacentes al vertice pasado como parámetro
    def obtener_adyacentes(self, vertice):
        adyacentes = self.tabla.get(vertice)
        return list(adyacentes.keys()) if adyacentes is not None else []

  
    ###############################################################################
    # Aristas
    ###############################################################################

    # Recibe una dupla para representar la arista y la agrega al grafo.
    # Post: Se agrego la arista. Si alguno de los vertices no existía, es agregado al grafo.
    def agregar_arista(self, arista, peso=None, NoDirigido=None):
        origen, destino = arista
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self.tabla[origen][destino] = peso if peso is not None else ""
        if NoDirigido is not None:
            self.tabla[destino][origen] = peso if peso is not None else ""

    # Recibe una dupla para representar la arista y eliminarla
    # Post: Si la arista no existe no se elimina.
    def borrar_arista(self, arista):
        origen, destino = arista
        self.tabla.get(origen, {}).pop(destino, None)

    # Devuelve lista de duplas con todas las aristas del grafo.
    def obtener_aristas(self):
        aristas = list()

        # Agregar las duplas en la lista para cada i
        # (origen_i, A), (origen_i, B), ...., (origen_i, N)
        for vertice_origen in self.tabla:
            aristas.extend([(vertice_origen, vertice_destino) for vertice_destino in self.tabla[vertice_origen]])

        return 

    # Devuelve el peso de la arista
    def obtener_peso(self, vertice, otroVertice):
        if self.son_vertices_unidos(vertice, otroVertice):
            return self.tabla[vertice][otroVertice]