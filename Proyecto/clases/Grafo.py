import json


#------Importa las clases necesarias para instanciar los objetos-------

from clases.Transporte import *
from clases.Nodo import *
from clases.Obstruccion import *
from heapq import heappop,heappush

class Grafo:


    def __init__(self):
        self.nombre_pais=''
        self.lista_transportes=[]
        #en esta variable se encarga de leer el archivo json
        self.archivo_leido=None
        #Una lista de ciudades para ser ingresadas en el grafo.
        self.lista_ciudades=[]
        self.lista_obstrucciones=[]




    def leer_archivo_json(self):
        """ Se lee y se carga en una variable global el archivo json de el arbol
        :return:
        """
        with open('archivo/archivo.json') as file:
            self.archivo_leido = json.load(file)

            self.interpretar_archivo_cargado()



    def interpretar_archivo_cargado(self):
        """Construye la estructura de el grafo a partir de el diccionario que genera la lectura de el archivo json
        :return: No retorna nada
        """
        #Se extrae el nombre de el país:
        self.extraer_countryTitle()
        #se extraen los medios de transporte:
        self.extraer_transportForm()
        #se extrae y se relaciona las ciudades:
        self.extraer_ciudades()



    def extraer_countryTitle(self):
        """Se extrae el nombre de la ciudad del archivo JSON"""
        self.nombre_pais=self.archivo_leido['countryTitle']


    def extraer_transportForm(self):
        """Se extrae los tipos de transporte del archivo JSON y se convierten en objetos..."""

        for transportes in self.archivo_leido['transportForm']:

            id= transportes['id']
            name= transportes['name']
            valorPorKm= transportes['valueByKm']
            tiempoPorKm= transportes['timeByKm']

            #Aquí se instancia los transportes que se han extraido de el json:
            transportes= Transporte(id,name,valorPorKm,tiempoPorKm)
            self.lista_transportes.append(transportes)


    def extraer_ciudades(self):
        """Se extraen las ciudades del archivo JSON"""
        for ciudad in self.archivo_leido["places"]:

            letra = ciudad['label']
            nombre = ciudad['name']
            tiempo_llegada = ciudad['minTimeHere']

            #Se instancia un objeto tipo ciudad
            nodo = Nodo(letra, nombre, tiempo_llegada)

            #Se añade a la lista de Nodos que en este caso serán ciudades:
            self.lista_ciudades.append(nodo)

            #Se adiciona una actividad:
            self.adicionar_cosas_por_hacer(nodo,ciudad)
            #Se adiciona un trabajo:
            self.adicionar_trabajo(nodo,ciudad)
            #Se general los caminos o vías bidireccionales:
            self.crear_relaciones(nodo,ciudad)


        print(self.lista_ciudades)


    def buscar_ciudad(self,letra):
        """Busca una ciudad proporcionando su la letra que le identifica

        :param letra: Letra de la ciudad que se busca
        :return: Objeto tipo ciudad si se encuentra, de lo contrario retorna None
        """
        for ciudad in self.lista_ciudades:

            if (ciudad.letra==letra):

                return ciudad

        return None

    def buscar_ciudad_por_nombre(self,nombre):
        """Busca una ciudad proporcionando su nombre

        :param nombre: Nombre de la ciudad que se busca
        :return: Objeto tipo ciudad si se encuentra, de lo contrario retorna None
        """
        for ciudad in self.lista_ciudades:

            if (ciudad.nombre==nombre):

                return ciudad

        return None



    def crear_relaciones(self,nodo,ciudad):
        """Crea las relaciones BIDIRECCIONALES para cada nodo

        :param nodo: Ciudad para la cual se decea añadir la relacion
        :param ciudad: Objeto de el archivo json
        :return: No retorna nada
        """

        for relacion in ciudad["goingTo"]:

            #Se extrae los atributos de el archivo JSON:
            destino= relacion["label"]
            distancia_viaje= relacion["travelDistance"]
            formas_de_viaje= relacion["transportForms"]

            self.agregar_relacion(nodo.letra,destino,distancia_viaje,formas_de_viaje)
            self.agregar_relacion(destino,nodo.letra,distancia_viaje,formas_de_viaje)


    def agregar_relacion(self,origen,destino,distancia_viaje,formas_de_viaje):
        """Añade un camino o relación desde dado un origen y un destino

        :param origen: ciudad origen
        :param destino: ciudad destino
        :param distancia_viaje: distancia en km entre las dos ciudades relacionadas
        :param formas_de_viaje: array con los tipos de formas de transporte
        :return: No retorna nada
        """
        #se busca la ciudad a la cual se decea agregar el camino
        ciudad= self.buscar_ciudad(origen)
        #Si existe la ciudad buscada:
        if(ciudad):
            #Se agrega el camino:
            ciudad.agregar_relacion(destino,distancia_viaje,formas_de_viaje)



    def adicionar_trabajo(self,nodo,ciudad):
        """A partir de el archivo json, se extrae los trabajos y adiciona a la ciudad.

        :param ciudad: Elemento de el JSON
        :return: No retorna nada
        """
        for trabajo in ciudad["jobs"]:

            #Se extrae los atributos de cada trabajo:
            nombre= trabajo["name"]
            ganancia= trabajo["gain"]
            tiempo= trabajo["time"]

            #Se adiciona un nuevo trabajo:
            nodo.agregar_trabajo(nombre,ganancia,tiempo)
            print(nodo.lista_trabajos[0].nombre_trabajo)


    def adicionar_cosas_por_hacer(self,nodo,ciudad):
        """A partir de el JSON, extraer las actividades y las adiciona a la ciudad

        :param ciudad: Objeto tipo ciudad extraido de el JSON
        :return: No retorna nada
        """
        for actividad in ciudad["things_to_do"]:

            #Se extrae los atributos de las actividades:
            nombre= actividad["name"]
            costo= actividad["cost"]
            tiempo= actividad["time"]
            tipo= actividad["type"]

            #Se adiciona cada actividad:
            nodo.agregar_actividad(nombre,costo,tiempo,tipo)


    def buscar_transporte(self,id):
        """A partir de un id, retorna un objeto medio de transorte

        :param id: Id de el medio de transporte consultado
        :return:
        """

        for transporte in self.lista_transportes:
            if (transporte.id==id):
                return transporte

        return None

    def buscar_transporte_nombre(self,nombre):
        """A partir de un nombre, retorna un objeto medio de transorte

        :param nombre: nombre de el medio de transporte consultado
        :return:
        """

        for transporte in self.lista_transportes:
            if (transporte.name==nombre):
                return transporte

        return None

    def agregar_obstruccion(self,origen,destino):
        """Genera obstrucciones en el grafo

        :param origen: ciudad origen
        :param destino: ciudad destino
        :return:
        """
        obstruccion= Obstruccion(origen,destino)
        self.lista_obstrucciones.append(obstruccion)


    def existe_obstruccion(self,origen,destino):
        """Evalúa si existe una obstrucción

        :param origen: ciudad origen
        :param destino: ciudad destino
        :return: True si la obstrucción existe
        """
        for obstruccion in self.lista_obstrucciones:
            if(obstruccion.origen==origen and obstruccion.destino==destino):
                return True

        return False

    def buscar_obstruccion(self,origen,destino):
        """Busca y retorna un objeto tipo obstruccion

        :param origen:
        :param destino:
        :return: Objeto tipo obstruccion
        """
        for obstruccion in self.lista_obstrucciones:
            if (obstruccion.origen == origen and obstruccion.destino == destino):
                return obstruccion

        return False

    def eliminar_obstruccion(self,origen,destino):
        """Elimina una obstruccion

        :param origen:
        :param destino:
        :return:
        """
        obstruccion= self.buscar_obstruccion(origen,destino)

        self.lista_obstrucciones.remove(obstruccion)

    def recorrido_prim(self, ciudad_inicio):
        """retorna una lista con el arbol generado por el método prim

        :param ciudad_inicio: ciudad a partir de la cual inicia el algoritmo
        :return: lista de parejas origen:destino
        """

        # Una lista con los nodos que ya están marcados:
        lista_marcados = []

        resultado = []
        self.__recorrido_prim(ciudad_inicio, lista_marcados, [], resultado)
        print(resultado)
        return resultado

    def __recorrido_prim(self, ciudad_inicio, lista_marcados, adyacencias, resultado):
        """Método recursivo que obtiene el arbol de expansión Prim

        :param ciudad_inicio: ciudad donde empieza el algoritmo
        :param lista_marcados: lista con los nodos ya visitados
        :param adyacencias: lista de caminos adyacentes para cada ciudad
        :param resultado: la lista que se va llenando producto de el algoritmo
        :return:
        """
        # se pregunta si aún no han sido recorridos todos los nodos:
        if (len(lista_marcados) < len(self.lista_ciudades)):
            # Primero buscamos el nodo inicial:
            ciudad_inicio = self.buscar_ciudad(ciudad_inicio)

            # se reinicial el diccionario para evitar problemas de sobreescritura:
            diccionario_parejas = {}

            # Añadimos la letra ciudad a la lista de marcados:
            lista_marcados.append(ciudad_inicio.letra)

            # buscamos las adyacencias:
            adyacencias += self.retornar_adyacencias(ciudad_inicio.letra)

            # Ahora vamos a seleccionar la adyacencia con menor valor siempre y cuando no se forme ciclo:
            adyacencia_menor = self.menor_adyacencia(adyacencias, lista_marcados)
            # si el valor retornado es diferente de None
            if (adyacencia_menor):
                ""
                nodo_inicial = self.buscar_nodo_adyacencia(adyacencia_menor.destino, adyacencia_menor.distancia)
                diccionario_parejas[nodo_inicial.letra] = adyacencia_menor.destino
                resultado.append(diccionario_parejas)
                adyacencias.remove(adyacencia_menor)
                # Ahora vamos a ir a dicha adyacencia para repetir el proceso:
                self.__recorrido_prim(adyacencia_menor.destino, lista_marcados, adyacencias, resultado)

    def recorrido_menor_costo(self, ciudad_inicio, presupuesto):
        """retorna una lista con el arbol generado por el método prim

        :param ciudad_inicio: ciudad a partir de la cual inicia el algoritmo
        :return: lista de parejas origen:destino
        """

        # Una lista con los nodos que ya están marcados:
        lista_marcados = []

        resultado = []
        self.__recorrido_menor_costo(ciudad_inicio, lista_marcados, [], resultado, presupuesto)
        print(resultado)
        return resultado

    def __recorrido_menor_costo(self, ciudad_inicio, lista_marcados, adyacencias, resultado, presupuesto):
        """Método recursivo que obtiene el arbol de expansión Prim

        :param ciudad_inicio: ciudad donde empieza el algoritmo
        :param lista_marcados: lista con los nodos ya visitados
        :param adyacencias: lista de caminos adyacentes para cada ciudad
        :param resultado: la lista que se va llenando producto de el algoritmo
        :return:
        """
        # se pregunta si aún no han sido recorridos todos los nodos o si aún se cuenta con presupuesto:
        if ((len(lista_marcados) < len(self.lista_ciudades)) and presupuesto > 0):
            # Primero buscamos el nodo inicial:
            ciudad_inicio = self.buscar_ciudad(ciudad_inicio)

            # se reinicial el diccionario para evitar problemas de sobreescritura:
            diccionario_parejas = {}

            # Añadimos la letra ciudad a la lista de marcados:
            lista_marcados.append(ciudad_inicio.letra)

            # buscamos las adyacencias:
            adyacencias += self.retornar_adyacencias(ciudad_inicio.letra)

            # Ahora vamos a seleccionar la adyacencia con menor valor siempre y cuando no se forme ciclo:
            adyacencia_menor, costo = self.menor_adyacencia_costo(adyacencias, lista_marcados)

            # si el valor retornado es diferente de None
            if (adyacencia_menor):
                ""
                nodo_inicial = self.buscar_nodo_adyacencia(adyacencia_menor.destino, adyacencia_menor.distancia)

                diccionario_parejas[nodo_inicial.letra] = adyacencia_menor.destino
                resultado.append(diccionario_parejas)
                adyacencias.remove(adyacencia_menor)

                presupuesto -= costo
                # Ahora vamos a ir a dicha adyacencia para repetir el proceso:
                self.__recorrido_menor_costo(adyacencia_menor.destino, lista_marcados, adyacencias, resultado,
                                             presupuesto)

    def extraer_menor_costo(self, adyacencia):
        """Retorna el menor costo de viaje de un camino

        :param adyacencia:
        :return:
        """
        menor_costo = 9999999

        for id in adyacencia.forma_transporte:
            transporte = self.buscar_transporte(id)
            # se extrae el costo de viaje y se compara con el menor
            costo_viaje = transporte.valorPorKm * adyacencia.distancia

            if (costo_viaje < menor_costo):
                menor_costo = costo_viaje

        return menor_costo

    def buscar_nodo_adyacencia(self, destino, distancia):
        """A partir de un destino y una distancia intenta recuperar el origen

        :param destino:
        :param distancia:
        :return:
        """
        for nodo in self.lista_ciudades:

            for relacion in nodo.lista_relaciones:

                if (relacion.destino == destino and relacion.distancia == distancia):
                    return nodo

        return None

    def menor_adyacencia_costo(self, adyacencias, lista_marcados):
        """Retorna el camino con menor costo economico

        :param adyacencias: lista de objetos de tipo adyacencia
        :param lista_marcados: lista con letras de las ciudades ya visitadas
        :return: la adyacencia con menor valor y el costo de viajar por allí
        """
        # se crea un menor inicial con un valor lo suficientemente alto
        menor_costo = 999999
        costo = 0
        # La adyacencia menor que se va a retornar al final:
        menor = None
        for adyacencia in adyacencias:
            # Primero preguntamos el destino que vamos a mirar no se encuentra ya marcado:
            if (adyacencia.destino not in lista_marcados):
                # Luego vamos a preguntar si ese camino es el menor de dicha lista:
                costo = self.extraer_menor_costo(adyacencia)
                if (costo < menor_costo):
                    menor = adyacencia
                    menor_costo = costo

        # Retorna la menor de toda la lista:
        return menor, costo



    def menor_adyacencia(self, adyacencias, lista_marcados):
        """Retorna el camino con menor costo economico

        :param adyacencias: lista de objetos de tipo adyacencia
        :param lista_marcados: lista con letras de las ciudades ya visitadas
        :return: la adyacencia con menor valor
        """
        # se crea un menor inicial con un valor lo suficientemente alto
        menor_costo = 999999
        # La adyacencia menor que se va a retornar al final:
        menor = None
        for adyacencia in adyacencias:
            # Primero preguntamos el destino que vamos a mirar no se encuentra ya marcado:
            if (adyacencia.destino not in lista_marcados):
                # Luego vamos a preguntar si ese camino es el menor de dicha lista:
                costo = self.extraer_menor_costo(adyacencia)
                if (costo < menor_costo):
                    menor = adyacencia
                    menor_costo = costo

        # Retorna la menor de toda la lista:
        return menor

    def retornar_adyacencias(self, ciudad):
        """Retorna los caminos posibles de un punto a otro

        :param ciudad:
        :return:
        """
        # se busca la ciudad:
        ciudad = self.buscar_ciudad(ciudad)
        # se retorna sus relaciones
        return ciudad.lista_relaciones





    def recorrido_menor_tiempo(self, ciudad_inicio, tiempo_inicial):
        """retorna una lista con el arbol generado por el método prim

        :param ciudad_inicio: ciudad a partir de la cual inicia el algoritmo
        :return: lista de parejas origen:destino
        """

        # Una lista con los nodos que ya están marcados:
        lista_marcados = []

        resultado = []
        self.__recorrido_menor_tiempo(ciudad_inicio, lista_marcados, [], resultado, tiempo_inicial)
        print(resultado)
        return resultado

    def __recorrido_menor_tiempo(self, ciudad_inicio, lista_marcados, adyacencias, resultado, tiempo_inicial):
        """Método recursivo que obtiene el arbol de expansión Prim

        :param ciudad_inicio: ciudad donde empieza el algoritmo
        :param lista_marcados: lista con los nodos ya visitados
        :param adyacencias: lista de caminos adyacentes para cada ciudad
        :param resultado: la lista que se va llenando producto de el algoritmo
        :return:
        """
        # se pregunta si aún no han sido recorridos todos los nodos o si aún se cuenta con presupuesto:
        if ((len(lista_marcados) < len(self.lista_ciudades)) and tiempo_inicial > 0):
            # Primero buscamos el nodo inicial:
            ciudad_inicio = self.buscar_ciudad(ciudad_inicio)

            # se reinicial el diccionario para evitar problemas de sobreescritura:
            diccionario_parejas = {}

            # Añadimos la letra ciudad a la lista de marcados:
            lista_marcados.append(ciudad_inicio.letra)

            # buscamos las adyacencias:
            adyacencias += self.retornar_adyacencias(ciudad_inicio.letra)

            # Ahora vamos a seleccionar la adyacencia con menor valor siempre y cuando no se forme ciclo:
            adyacencia_menor, tiempo = self.menor_adyacencia_tiempo(adyacencias, lista_marcados)

            # si el valor retornado es diferente de None
            if (adyacencia_menor):
                ""
                nodo_inicial = self.buscar_nodo_adyacencia(adyacencia_menor.destino, adyacencia_menor.distancia)

                diccionario_parejas[nodo_inicial.letra] = adyacencia_menor.destino
                resultado.append(diccionario_parejas)
                adyacencias.remove(adyacencia_menor)

                tiempo_inicial -= tiempo
                # Ahora vamos a ir a dicha adyacencia para repetir el proceso:
                self.__recorrido_menor_tiempo(adyacencia_menor.destino, lista_marcados, adyacencias, resultado,tiempo_inicial)


    def extraer_menor_tiempo(self, adyacencia):
        """Retorna el menor costo de viaje de un camino

        :param adyacencia:
        :return:
        """
        menor_tiempo = 99999999

        for id in adyacencia.forma_transporte:
            transporte = self.buscar_transporte(id)
            # se extrae el costo de viaje y se compara con el menor
            costo_viaje = transporte.tiempoPorKm * adyacencia.distancia

            if (costo_viaje < menor_tiempo):
                menor_tiempo = costo_viaje

        return menor_tiempo



    def menor_adyacencia_tiempo(self, adyacencias, lista_marcados):
        """Retorna el camino con menor costo economico

        :param adyacencias: lista de objetos de tipo adyacencia
        :param lista_marcados: lista con letras de las ciudades ya visitadas
        :return: la adyacencia con menor valor y el costo de viajar por allí
        """
        # se crea un menor inicial con un valor lo suficientemente alto
        menor_tiempo = 9999999
        tiempo = 0
        # La adyacencia menor que se va a retornar al final:
        menor = None
        for adyacencia in adyacencias:
            # Primero preguntamos el destino que vamos a mirar no se encuentra ya marcado:
            if (adyacencia.destino not in lista_marcados):
                # Luego vamos a preguntar si ese camino es el menor de dicha lista:
                tiempo = self.extraer_menor_tiempo(adyacencia)
                if (tiempo < menor_tiempo):
                    menor = adyacencia
                    menor_tiempo = tiempo

        # Retorna la menor de toda la lista:
        return menor, tiempo