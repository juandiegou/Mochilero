
from clases.Trabajo import *
from clases.Actividad import *
from clases.Relacion import *


class Nodo:


    def __init__(self,letra,nombre,tiempo_llegada):
        self.letra=letra
        self.nombre=nombre
        self.tiempo_llegada=tiempo_llegada
        self.lista_trabajos=[]
        self.lista_cosas_por_hacer=[]
        self.lista_relaciones=[]

        #Coordenadas X y Y en el canvas:
        self.x=0
        self.y=0


    def agregar_actividad(self,nombre,costo,tiempo,tipo):
        """Adiciona una actividad a la ciudad en cuestion

        :return:
        """
        actividad = Actividad(nombre, costo, tiempo, tipo)
        self.lista_cosas_por_hacer.append(actividad)

        pass



    def agregar_trabajo(self,nombre,ganancia,tiempo):
        """Adiciona un trabajo a la ciudad

        :return: no retorna nada
        """
        trabajo= Trabajo(nombre,ganancia,tiempo)
        self.lista_trabajos.append(trabajo)


    def buscar_trabajo(self,nombre):
        """Busca y retorna un trabajo

        :param nombre: Nombre de el trabajo consultado
        :return: Objeto tipo trabajo
        """

        for trabajo in self.lista_trabajos:
            if (nombre==trabajo.nombre_trabajo):
                return trabajo

        return None


    def buscar_actividad(self,nombre):
        """Busca una actividad para la ciudad

        :param nombre: Nombre de la actividad buscada
        :return: Un objeto tipo Actividad.
        """
        
        for actividad in self.lista_cosas_por_hacer:
            if(nombre==actividad.nombre_actividad):
                return actividad
            
        None


    def agregar_relacion(self,destino,distancia_viaje,formas_de_transporte):
        """ Agrega una relación a la ciudad actual

        :return: True: si la arista fué almacenada con éxito
        """

        #Si no existe la relacion:
        if( not self.existe_relacion(destino)):

            #Se crea una nueva relacion o camino que conduzca a otra ciudad
            relacion= Relacion(destino,distancia_viaje,formas_de_transporte)
            #Se adiciona la nueva relación a la lista de nodos encontrados
            self.lista_relaciones.append(relacion)


    def existe_relacion(self,destino):
        """Indica si ya existe una ruta hacia el destino indicado

        :param destino: ciudad destino hacia la cual se realiza la consulta
        :return: True si existe la ruta, False de lo contrario
        """

        for relacion in self.lista_relaciones:
            if (destino== relacion.destino):
                return True

        return False


    def buscar_relacion(self,destino):
        """Retorna un objeto tipo arista con la información de la relación con la ciudad consultada

        :param destino: Ciudad de destino consultada
        :return:
        """
        for relacion in self.lista_relaciones:
            if (relacion.destino==destino):
                return relacion

        return None


    def retornar_lista_destinos(self):
        """Retorna una lista con los destinos disponibles para la ciudad

        :return:
        """
        lista_destinos=[]
        for relacion in self.lista_relaciones:
            lista_destinos.append(relacion.destino)

        return lista_destinos


    def retornar_lista_medios(self,ciudad):
        """Retorna una lista con los medios disponibles por un camino

        :param ciudad: Ciudad destino consultada
        :return:
        """
        #Se busca la relacion
        camino=self.buscar_relacion(ciudad)

        #Si existe la relación:
        if (camino):
            return  camino.forma_transporte


    def retornar_lista_trabajos(self):
        """Retorna una lista con los nombres de los trabajos en la ciudad

        :return:
        """
        lista_nombres=[]
        for trabajo in self.lista_trabajos:
            lista_nombres.append(trabajo.nombre_trabajo)

        return lista_nombres


    def retornar_lista_actividades(self):
        """Retorna una lista con las actividades disponibles para realizar

        :return:
        """
        lista_nombres=[]
        for actividad in self.lista_cosas_por_hacer:
            lista_nombres.append(actividad.nombre_actividad)

        return lista_nombres
