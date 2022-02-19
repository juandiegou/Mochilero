
class Mochilero:

    def __init__(self,nombre,logo,x,y,ciudad_actual,presupuesto,tiempo_disponible):
        #nombre de el mochilero
        self.nombre=nombre
        #saldo actual de el mochlero:
        self.presupuesto= int(presupuesto)
        #presupuesto inicial
        self.presupuesto_inicial= int(presupuesto)
        self.tiempo_disponible_inicial= int(tiempo_disponible)
        self.tiempo_disponible= int(tiempo_disponible)
        #coordenadas X y Y de el mochilero
        self.x=x
        self.y=y
        self.logo=logo
        self.ciudad_actual=ciudad_actual
        self.kilometros_recorridos=0