
class Reporte:

    def __init__(self):

        self.ciudades_visitadas=[]
        self.trabajos_realizados=[]
        self.actividades_realizadas=[]
        self.total_dinero_gastado=0
        self.kilometros_recorridos=0
        self.total_ganancias_registradas=0
        self.costos_por_viaje=[]



    def adicionar_ciudad_visitada(self,ciudad):
        """Almacena la información reelevante sobre una ciudad visitada

        :param ciudad: Objeto ciudad
        :return:
        """
        datos_ciudad={'letra':ciudad.letra,'nombre':ciudad.nombre,'estadía_minima':ciudad.tiempo_llegada}
        self.ciudades_visitadas.append(datos_ciudad)


    def adicionar_gastos(self,dinero):
        """Incrementa el saldo total de el dinero gastado en el viaje.

        :param dinero:
        :return:
        """
        self.total_dinero_gastado+=dinero

    def adicionar_actividad_realizada(self,nombre_actividad,costo_actividad,tiempo_invertido,ciudad):
        """Agrega una actividad realizada a la lista de actividades:

        :param nombre_actividad:
        :param costo_actividad:
        :param tiempo_invertido:
        :param ciudad:
        :return:
        """
        actividad= {'nombre_actividad':nombre_actividad,'costo_actividad':costo_actividad,'tiempo_invertido':tiempo_invertido,'ciudad':ciudad}
        self.actividades_realizadas.append(actividad)



    def adicionar_trabajo_realizado(self,nombre_trabajo,pago_trabajo,tiempo_invertido,ciudad):
        """Adiciona un trabajo realizado a el reporte.

        :param nombre_trabajo:
        :param pago_trabajo:
        :param tiempo_invertido:
        :param ciudad:
        :return:
        """

        trabajo={'nombre_trabajo':nombre_trabajo,'pago_trabajo':pago_trabajo,'tiempo_invertido':tiempo_invertido,'ciudad':ciudad}
        self.trabajos_realizados.append(trabajo)

    def adicionar_costo_por_viaje(self,origen,destino,costo,tiempo):
        """Adiciona el costo de un viaje

        :param origen:
        :param destino:
        :param costo:
        :return:
        """

        viaje={'origen':origen,'destino':destino,'costo':costo,'tiempo':tiempo}
        self.costos_por_viaje.append(viaje)



    def adicionar_kilometraje(self,kilometros):
        """Incrementa los kilometros recorridos por el mochilero:

        :param kilometros:
        :return:
        """
        self.kilometros_recorridos+=kilometros

