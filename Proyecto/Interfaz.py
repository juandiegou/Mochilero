from tkinter import *
from unicodedata import east_asian_width
from clases.Grafo import *
from clases.Transporte import *
from clases.Nodo import *
from clases.Mochilero import *
from clases.Reporte import *
from tkinter import ttk
from tkinter import messagebox
from easygui import *

import datetime
# permite la ejecución de hilos:
import threading
import queue
import math

import time

# Cola para el manejo de Threads:
cola = queue.Queue

# variable importante para detener el hilo de el contador de segundos:
condicion_parada = True

"""--------------------------------------Zona de instanciación de objetos y variables globales------------------------------------------------"""
# Se instancia el objeto tipo arbol:
grafo = Grafo()

# Aquí se hará manejo de reportes:
reporte = Reporte()

# Diccionario de coordenadas para pintar los Nodos:
diccionario_coordenadas = {1: [400, 100], 2: [700, 100], 3: [550, 300], 4: [900, 250], 5: [300, 270], 6: [100, 250],
                           7: [450, 420], 8: [750, 400], 9: [500, 600], 10: [200, 400], 11: [10, 150], 12: [930, 10],
                           13: [50, 550], 14: [100, 400]}

# El mochilero:
mochilero = None

# la referencia a los objetos tipo imagen que se van desplazando en pantalla:
person = None
car = None
airplane = None
donkey = None

"""----------------------------------------------------Diseño de interfaz de el proyecto------------------------------------------------------"""

# Se crea la ventana:
ventana = Tk()

# Se le da un tamaño:
ventana.geometry("1350x700")

# Agregando un titulo a la ventana
ventana.title("Mapa De Ciudades")

# En este canvas colocaremos las herramientas que nos permitan manipular el programa
canvas_principal = Canvas(ventana, width=300, height=700, bg="#2E065E")
canvas_principal.place(x=1050, y=0)

# En este canvas se va a dibujar el arbol que se genere:
canvas_dibujo = Canvas(ventana, width=1050, height=700, bg="#2E065E")
canvas_dibujo.place(x=0, y=0)

# Titulo del proyecto
etiqueta = Label(canvas_dibujo, text="Ciudades", fg="white", bg="#2E065E", font=("Arial", 15))
etiqueta.place(x=350, y=0)

lbl_presupuesto = Label(canvas_dibujo, width=30, bg="#2E065E", fg="#ffffff", text=f"Saldo: {0}",
                        font=("Arial", 10))
lbl_presupuesto.place(x=790, y=630)
lbl_tiempo_disponible = Label(canvas_dibujo, width=30, bg="#2E065E", fg="#ffffff", text=f"Tiempo: {0}",
                              font=("Arial", 10))
lbl_tiempo_disponible.place(x=790, y=650)

"""-------------------------------------------------Botonera y Menús de la zona izquierda---------------------------------------------------"""

lbl_menu = Label(canvas_principal, width=35, text="Menú Principal", fg="white",bg="#2E065E", font=("Arial", 10)).place(x=10, y=10)

lbl_seleccion_origen = Label(canvas_principal, width=35, fg="white",bg="#2E065E",text="Seleccionar Origen", font=("Arial", 8)).place(
    x=25, y=110)
select_origen = StringVar()

combo_origen = ttk.Combobox(canvas_principal, width=35, state="readonly", values=("Seleccione una opción"),
                            textvariable=select_origen)
combo_origen.place(x=35, y=140)

lbl_ingreso_nombre = Label(canvas_principal, width=21, height=1, fg="white",bg="#2E065E",text="Ingrese Nombre",
                           font=("Arial", 8)).place(x=10, y=180)
nombre_user = StringVar()
txt_nombre = Entry(canvas_principal, width=22, textvariable=nombre_user)
txt_nombre.place(x=165, y=180)

lbl_ingreso_presupuesto = Label(canvas_principal, width=21, height=1, fg="white",bg="#2E065E", text="Ingrese Presupuesto",
                                font=("Arial", 8))
lbl_ingreso_presupuesto.place(x=10, y=210)
presupuesto_user = StringVar()
txt_presupuesto = Entry(canvas_principal, width=22, textvariable=presupuesto_user)
txt_presupuesto.place(x=165, y=210)

lbl_ingreso_tiempo = Label(canvas_principal, width=21, height=1, fg="white",bg="#2E065E", text="Ingrese Tiempo Estipulado",
                           font=("Arial", 8))
lbl_ingreso_tiempo.place(x=10, y=240)
tiempo_estipulado = StringVar()
txt_tiempo = Entry(canvas_principal, width=22, textvariable=tiempo_estipulado)
txt_tiempo.place(x=165, y=240)

lbl_obstruccion = Label(canvas_principal, width=35, text="Generar Obstrucciones", fg="white",bg="#2E065E", font=("Arial", 8)).place(x=25,
                                                                                                                   y=310)

select_obstruccion_origen = StringVar()
combo_ostruccion_origen = ttk.Combobox(canvas_principal, width=35, state="readonly", values=("Seleccione una opción"),
                                       textvariable=select_obstruccion_origen)
combo_ostruccion_origen.place(x=35, y=340)

select_obstruccion_destino = StringVar()
combo_obstruccion_destino = ttk.Combobox(canvas_principal, width=35, state="readonly", values=("Seleccione una opción"),
                                         textvariable=select_obstruccion_destino)
combo_obstruccion_destino.place(x=35, y=370)

"""---------------------------------------------------------------Carga De Imagenes-------------------------------------------------------"""

img_mochilero = PhotoImage(file="Imagenes/user.png")
img_burro = PhotoImage(file="Imagenes/donkey.png")
img_avion = PhotoImage(file="Imagenes/avion.png")
img_carro = PhotoImage(file="Imagenes/car.png")

img_fondo_opciones = PhotoImage(file="Imagenes/fondo.png")



"""--------------------------------------------------------------------Métodos--------------------------------------------------------------"""


def onCanvasClick(event):
    """Genera la ventana de opciones para cada ciudad:

    :param event: Evento producido al realizar doble click
    :return: Nada
    """
    global mochilero

    # se genera una ventana independiente:
    ventana_opciones = Toplevel()

    # Se le da un tamaño:
    ventana_opciones.geometry("700x700")

    # Agregando un titulo a la ventana
    ventana_opciones.title("Opciones")

    # En este canvas colocaremos las herramientas que nos permitan manipular el programa
    canvas_opciones = Canvas(ventana_opciones, width=700, height=700, bg="#8B94A7")
    canvas_opciones.place(x=5, y=0)

    canvas_opciones.create_image(0, 0, image=img_fondo_opciones, anchor=NW)
    # Nombre de la ciudad
    etiqueta = Label(canvas_opciones, text="Opciones", font=("Arial", 15),bg="#2E065E", fg="white").place(x=250, y=0)

    # se busca la ciudad para la cual se decea cargar la información:
    ciudad = grafo.buscar_ciudad(mochilero.ciudad_actual)

    crear_opciones_ciudad(ventana_opciones, canvas_opciones, ciudad)

    ventana_opciones.mainloop()


def crear_opciones_ciudad(ventana, canvas_opciones, ciudad):
    global mochilero
    # Lista que muestra la informacion de la ciudad
    lstInformacion = Listbox(canvas_opciones, bg="#2E065E", width=80, height=10, font=("Arial", 11),
                             fg="#ffffff")
    lstInformacion.place(x=30, y=500)
    # Ahora se muestra la información en la ventana de información:
    lstInformacion.insert(END, " ")
    lstInformacion.insert(END, f"ID: {ciudad.letra}")
    lstInformacion.insert(END, f"Nombre: {ciudad.nombre}")
    lstInformacion.insert(END, f"Tiempo Mínimo: {ciudad.tiempo_llegada}")
    lstInformacion.insert(END, " ")
    # Los datos de el mochilero:
    lstInformacion.insert(END, f"Mochilero {mochilero.nombre}:")
    lstInformacion.insert(END, f"Presupuesto Actual: {mochilero.presupuesto}")
    lbl_presupuesto["text"] = f"Saldo Actual: {mochilero.presupuesto}"
    lstInformacion.insert(END, f"Km Recorridos: {mochilero.kilometros_recorridos}")
    lstInformacion.insert(END, " ")

    lista_trabajos = ciudad.retornar_lista_trabajos()
    lbl_seleccion_trabajo = Label(canvas_opciones, width=35, text="Buscar Trabajo", bg="#2E065E", fg="white",font=("Arial", 8)).place(
        x=20, y=50)
    select_trabajo = StringVar()

    combo_trabajo = ttk.Combobox(canvas_opciones, width=35, state="readonly", values=lista_trabajos,
                                 textvariable=select_trabajo)
    combo_trabajo.place(x=20, y=80)

    lista_actividades = ciudad.retornar_lista_actividades()
    lbl_seleccion_actividad = Label(canvas_opciones, width=35, text="Actividad", bg="#2E065E", fg="white",
                                    font=("Arial", 8)).place(x=350, y=50)
    select_actividad = StringVar()

    combo_actividad = ttk.Combobox(canvas_opciones, width=35, state="readonly", values=lista_actividades,
                                   textvariable=select_actividad)
    combo_actividad.place(x=350, y=80)

    # Lista que muestra la informacion del Maquina_Turing
    lst_informacion_trabajo = Listbox(canvas_opciones, width=35, height=7, bg="#2E065E", font=("Arial", 11),
                                      fg="#ffffff")
    lst_informacion_trabajo.place(x=20, y=120)

    # Lista que muestra la informacion del Maquina_Turing
    lst_informacion_actividad = Listbox(canvas_opciones, width=35, height=7, bg="#2E065E", font=("Arial", 11),
                                        fg="#ffffff")
    lst_informacion_actividad.place(x=350, y=120)

    # Botón para cerrar la ventana de opciones
    btn_cerrar_opciones = Button(canvas_opciones, width=25, text="Cerrar Ventana",
                                 font=("Arial", 11), fg="#ffffff", command=lambda: cerrar_opciones(ventana),
                                 background="#1E6F4A")
    btn_cerrar_opciones.place(x=380, y=640)

    # Botón para cerrar la ventana de opciones
    btn_realizar_trabajo = Button(canvas_opciones, width=25, text="Tomar Trabajo", font=("Arial", 11),
                                  fg="#ffffff",
                                  command=lambda: realizar_trabajo(lst_informacion_trabajo, select_trabajo, ciudad),
                                  background="#1E6F4A")
    btn_realizar_trabajo.place(x=40, y=255)

    # Botón para cerrar la ventana de opciones
    btn_realizar_actividad = Button(canvas_opciones, width=25, text="Tomar Actividad", font=("Arial", 11),
                                    fg="#ffffff",
                                    command=lambda: realizar_actividad(lst_informacion_actividad, select_actividad,
                                                                       ciudad), background="#1E6F4A")
    btn_realizar_actividad.place(x=370, y=255)

    lista_destinos = ciudad.retornar_lista_destinos()
    lbl_seleccion_ciudad_destino = Label(canvas_opciones, width=35, text="Viajar A Un Destino",bg="#2E065E", fg="white",
                                         font=("Arial", 8)).place(x=20, y=290)
    select_ciudad = StringVar()

    combo_destino = ttk.Combobox(canvas_opciones, width=35, state="readonly", values=lista_destinos,
                                 textvariable=select_ciudad)
    combo_destino.place(x=20, y=320)

    lista_medios_transporte = []
    lbl_seleccion_actividad = Label(canvas_opciones, width=35, text="Seleccionar Medio De Transporte",bg="#2E065E", fg="white",
                                    font=("Arial", 8)).place(x=350, y=290)
    select_medio = StringVar()

    combo_medio_transporte = ttk.Combobox(canvas_opciones, width=35, state="readonly", values=lista_medios_transporte,
                                          textvariable=select_medio)
    combo_medio_transporte.place(x=350, y=320)

    # Lista que muestra la informacion del Maquina_Turing
    lst_destino = Listbox(canvas_opciones, width=35, height=5, bg="#2E065E", font=("Arial", 11), fg="#ffffff")
    lst_destino.place(x=20, y=350)

    # Lista que muestra la informacion del Maquina_Turing
    lst_medio_transporte = Listbox(canvas_opciones, width=35, height=5, bg="#2E065E", font=("Arial", 11),
                                   fg="#ffffff")
    lst_medio_transporte.place(x=350, y=350)

    # Botón para iniciar un recorrido hacia la ciudad destino
    btn_realizar_recorrido = Button(canvas_opciones, width=25, state="disabled", text="Viajar",
                                    font=("Arial", 11), fg="#ffffff",
                                    command=lambda: realizar_viaje(ciudad, select_ciudad, select_medio,
                                                                   btn_realizar_recorrido), background="#1E6F4A")
    btn_realizar_recorrido.place(x=370, y=450)

    # Evento que se dispara cuando se selecciona un item de el combobox, note como se usa una función lambda para evitar errores en la ejecución:
    combo_actividad.bind("<<ComboboxSelected>>",
                         lambda _: mostrar_info_actividad(lst_informacion_actividad, select_actividad, ciudad))
    combo_trabajo.bind("<<ComboboxSelected>>",
                       lambda _: mostrar_info_trabajo(lst_informacion_trabajo, select_trabajo, ciudad))

    combo_destino.bind("<<ComboboxSelected>>",
                       lambda _: mostrar_info_destino(lst_destino, combo_medio_transporte, select_ciudad, ciudad))
    combo_medio_transporte.bind("<<ComboboxSelected>>",
                                lambda _: mostrar_info_medio_transporte(lst_medio_transporte, select_medio,
                                                                        btn_realizar_recorrido))


def realizar_actividad(lst_informacion_actividad, select_actividad, ciudad):
    """Realiza una actividad elegida por el usuario:

    :param lst_informacion_actividad:
    :param select_actividad:
    :param ciudad:
    :return:
    """
    global mochilero
    global reporte
    # Se busca la información de la actividad a mostrar:
    actividad = ciudad.buscar_actividad(select_actividad.get())
    # verificando que haya presupuesto:
    if (mochilero.presupuesto >= 10):
        if (mochilero.presupuesto >= actividad.costo_actividad):
            if (mochilero.tiempo_disponible >= actividad.tiempo_actividad):
                mochilero.presupuesto -= int(actividad.costo_actividad)
                mochilero.tiempo_disponible -= int(actividad.tiempo_actividad)

                lst_informacion_actividad.delete(0, END)

                time.sleep(2)

                lst_informacion_actividad.insert(END, "Presupuesto actualizado!")
                lst_informacion_actividad.insert(END, f"Ahora cuentas con ${mochilero.presupuesto}")
                lbl_presupuesto["text"] = f"Saldo Actual: {mochilero.presupuesto}"
                lst_informacion_actividad.insert(END, f"Tiempo disponible  {mochilero.tiempo_disponible}")

                messagebox.showinfo(message="Actividad cumplida a satisfacción", title="OK")

                # se guardan registros de la actividad realizada:
                reporte.adicionar_actividad_realizada(actividad.nombre_actividad, actividad.costo_actividad,
                                                      actividad.tiempo_actividad, ciudad.letra)
                reporte.adicionar_gastos(actividad.costo_actividad)

            else:
                messagebox.showinfo(
                    message="El tiempo asignado se ha agotado! ¡Es necesario ingresar tiempo adicional!", title="Alerta")
                # Cuando el presupuesto ha sido agotado se muestra una ventana indicando ingresar tiempo adicional
                mochilero.tiempo_disponible = integerbox(msg='Ingrese nuevo tiempo', title='Tiempo', default=0,
                                                         lowerbound=10, upperbound=999999, image=None)


        else:
            messagebox.showinfo(
                message="No cuentas con suficiente presupuesto para esta actividad, te recomendamos tomar un trabajo",
                title="Error")

    else:
        messagebox.showinfo(
            message="No cuentas con suficiente presupuesto para esta actividad, te recomendamos tomar un trabajo",
            title="Error")


def realizar_trabajo(lst_informacion_trabajo, select_trabajo, ciudad):
    """Realiza el trabajo escogido por el usuario

    :param lst_informacion_trabajo:
    :param select_trabajo:
    :param ciudad:
    :return:
    """
    global mochilero
    global reporte
    # Se busca la información de el trabajo a mostrar:
    trabajo = ciudad.buscar_trabajo(select_trabajo.get())

    # se calcula el porcentaje de el presupuesto actual con relación a el inicial:
    porcentaje_salario = (mochilero.presupuesto * 100) / mochilero.presupuesto_inicial
    # Si el porcentaje de el salario es menor o igual a el 40% permite realizar el trabajo, de lo contrario,no:
    if (porcentaje_salario <= 40):
        # Se agrega efectúa el pago a el mochilero
        mochilero.presupuesto += trabajo.pago_trabajo
        # Se descuenta el tiempo invertido:
        mochilero.tiempo_disponible -= trabajo.tiempo_invertido
        # Se realiza una espera prudente:
        time.sleep(2)
        # se limpia y se escribe información sobre el trabajo realizado
        lst_informacion_trabajo.delete(0, END)
        lst_informacion_trabajo.insert(END,
                                       f"En hora buena! Has ganado ${trabajo.pago_trabajo} realizando este trabajo!")
        # se actualiza la información de el presupuesto de el mochilero:
        lst_informacion_trabajo.insert(END, f"Presupuesto actualizado! ahora cuentas con ${mochilero.presupuesto}")
        lbl_presupuesto["text"] = f"Saldo Actual: {mochilero.presupuesto}"
        messagebox.showinfo(message="Trabajo cumplido a satisfaccion!", title="OK")

        # Se deja registro de la actividad realizada:
        reporte.adicionar_trabajo_realizado(trabajo.nombre_trabajo, trabajo.pago_trabajo, trabajo.tiempo_invertido,
                                            ciudad.letra)
        reporte.total_ganancias_registradas += trabajo.pago_trabajo

    else:

        messagebox.showinfo(message="Debes contar con 40% ó menos de tu presupuesto inicial para realizar este trabajo",
                            title="Error")


def realizar_viaje(ciudad, select_ciudad, select_medio, btn_realizar_recorrido):
    """simula el desplazamiento desde una Ciudad origen hacia otra

    :param ciudad: objeto ciudad actual
    :param select_ciudad: letra de la ciudad destino
    :param select_medio: medio de transporte seleccionado
    :return: Nada
    """

    # Regula la velocidad de el desplazamiento de las figuras:
    velocidad = 0
    medio = select_medio.get()
    # se obtiene la ciudad destino:
    destino = grafo.buscar_ciudad(select_ciudad.get())
    origen = ciudad.letra
    # se pregunta si no existe una obstrucción en el camino indicado:
    if (not grafo.existe_obstruccion(origen, destino.letra)):
        # se desactiva el botón para evitar que se generen nuevos hilos
        btn_realizar_recorrido["state"] = "disabled"
        if (medio == "By plane"):
            def run():
                """Este submetodo me permite iniciar una cola de ejecución con el hilo que me dirige a la función que
                    deceo ejecutar en segundo plano:

                :return: Nada
                """
                # agregar a la cola de ejecución que permite el uso de thread-safe:
                try:
                    velocidad = 0.05
                    cola.put(
                        (iniciar_desplazamiento(ciudad, destino, medio, img_avion, velocidad, btn_realizar_recorrido)))
                except:
                    pass

            # se inicia el hilo
            hilo = threading.Thread(target=run)
            hilo.start()


        elif (medio == "By car"):

            def run():
                # Necesario, encerrar dentro de condición try-catch para control de excepciones:
                try:
                    velocidad = 0.1
                    cola.put(
                        iniciar_desplazamiento(ciudad, destino, medio, img_carro, velocidad, btn_realizar_recorrido))

                except:
                    pass

            hilo = threading.Thread(target=run)
            hilo.start()
        else:
            def run():
                try:
                    velocidad = 0.3
                    cola.put(
                        (iniciar_desplazamiento(ciudad, destino, medio, img_burro, velocidad, btn_realizar_recorrido)))

                except:
                    pass

            hilo = threading.Thread(target=run)
            hilo.start()


    else:

        messagebox.showinfo(message="No es posible realizar el viaje hacia este destino ya que se encuentra obstruído",
                            title="Error")


def tkloop():
    """Dado que no es tan simple como parece usar hilos en Tkinter este loop permite relizar una ejecución multihilada
        Permitiendo así que al ejecutar una tarea en segundo plano no se bloquee la ventana principal

    :return: Nada
    """
    try:
        while True:
            funcion, args, kwargs = cola.get_nowait()
            funcion(*args, **kwargs)
    except:
        pass

    ventana.after(100, tkloop)


def iniciar_desplazamiento(ciudad_origen, destino, medio, imagen_medio, velocidad, btn_realizar_recorrido):
    """simular el viaje de un punto a otro

    :param ciudad_origen:
    :param destino:
    :param medio:
    :param imagen_medio:
    :return:
    """
    global mochilero
    global person

    # Se busca la ciudad destino:
    ciudad_destino = destino
    # se obtiene referencia de la ruta para luego calcular costos de viaje
    ruta = ciudad_origen.buscar_relacion(ciudad_destino.letra)

    # se busca el medio de transporte para obtener información reelevante sobre este:
    transporte = grafo.buscar_transporte_nombre(medio)
    # se pregunta si el mochilero cuenta con recursos para realizar el viaje:
    if mochilero.presupuesto >= (transporte.valorPorKm * ruta.distancia):
        # Obteniendo referencias de posiciones de el origen:
        origenx = ciudad_origen.x
        origeny = ciudad_origen.y

        # Obteniendo referencias de las posiciones de el destino:
        destinox = ciudad_destino.x
        destinoy = ciudad_destino.y

        # se elimina la imagen de la persona en pantalla:
        canvas_dibujo.delete(person)

        # se genera la imagen de el medio de transporte en pantalla:
        medio_transporte = canvas_dibujo.create_image(origenx, origeny, image=imagen_medio, anchor=NW)
        canvas_dibujo.update()

        animar_desplazamiento(origenx, origeny, destinox, destinoy, medio_transporte, imagen_medio, velocidad)
        # se actualizan los datos del mochilero:
        actualizar_datos_viaje(ciudad_destino, transporte, ruta)
        # se pinta el mochilero:
        pintar_mochilero()
        # se vuelve a activar el botón de viaje para evitar errores:
        btn_realizar_recorrido["state"] = "normal"

    else:
        messagebox.showinfo(
            message="No cuentas con suficiente presupuesto para esta actividad, te recomendamos viajar en otro medio o buscar un trabajo",
            title="Error")


def actualizar_datos_viaje(ciudad_destino, transporte, ruta):
    """Luego de realizar el viaje, actualiza los datos de el mochilero

    :param ciudad_destino:
    :param transporte:
    :param ruta:
    :return:
    """
    global reporte
    # se calcula el costo de el viaje:
    costo_viaje = transporte.valorPorKm * ruta.distancia
    # se calcula el tiempo invertido en el viaje:
    tiempo_viaje = transporte.tiempoPorKm * ruta.distancia
    # se descuenta el tiempo de viaje de el tiempo disponible:
    mochilero.tiempo_disponible -= tiempo_viaje

    mochilero.presupuesto -= costo_viaje

    reporte.adicionar_costo_por_viaje(mochilero.ciudad_actual, ciudad_destino.letra, costo_viaje, tiempo_viaje)
    # se va adicionando los kilometros recorridos por cada viaje:

    reporte.adicionar_kilometraje(ruta.distancia)
    reporte.adicionar_gastos(costo_viaje)
    reporte.adicionar_ciudad_visitada(ciudad_destino)
    # Estableciendo la ciudad destino como ciudad actual para el mochilero:
    mochilero.ciudad_actual = ciudad_destino.letra
    # se actualizan las coordenadas de el mochilero
    mochilero.x = ciudad_destino.x
    mochilero.y = ciudad_destino.y

    lbl_presupuesto['text'] = f"Saldo Actual: {mochilero.presupuesto}"
    lbl_tiempo_disponible['text'] = f"Tiempo Restante: {mochilero.tiempo_disponible}"


def animar_desplazamiento(origenx, origeny, destinox, destinoy, medio_transporte, imagen_medio_transporte, velocidad):
    """A partir de las coordenadas proporcionadas realiza el ejercicio de desplazamiento de el objeto por pantalla:

    :param origenx: coordenada x de ciudad origen
    :param origeny: coordenada y de ciudad origen
    :param destinox: coordenada x de ciudad destino
    :param destinoy: coordenada y de ciudad destino
    :param medio_transporte: imagen que se va a desplazar
    :return: Nada
    """
    # Calculo las distancias en los componentes X y Y:
    componente_x = destinox - origenx
    componente_y = destinoy - origeny

    # Ahora calculo la hipotemusa:
    hipotemusa = int(math.sqrt((componente_x ** 2) + (componente_y ** 2)))

    for i in range(0, hipotemusa):
        try:
            cx = int((origenx + 2) + (i * (componente_x / hipotemusa))) - 10
            cy = int((origeny + 2) + (i * (componente_y / hipotemusa))) - 10

            canvas_dibujo.delete(medio_transporte)
            medio_transporte = canvas_dibujo.create_image(cx, cy, image=imagen_medio_transporte, anchor=NW)

            canvas_dibujo.update()
            time.sleep(velocidad)
        except NameError:
            print(f"Ha ocurrido un error: {NameError}")

    canvas_dibujo.delete(medio_transporte)


def mostrar_info_medio_transporte(lst_medio_transporte, select_ciudad, btn_realizar_recorrido):
    """Carga la información de un medio de transporte

    :param lst_medio_transporte: lista en la cual se muestra la información
    :param select_ciudad: ciudad destino seleccionada
    :return: Nada
    """

    # se obtiene una referencia de el medio de transporte:
    medio_transporte = grafo.buscar_transporte_nombre(select_ciudad.get())

    lst_medio_transporte.delete(0, END)
    lst_medio_transporte.insert(END, " ")
    lst_medio_transporte.insert(END, f"Id: {medio_transporte.id}")
    lst_medio_transporte.insert(END, f"medio: {medio_transporte.name}")
    lst_medio_transporte.insert(END, f"Valor Por Km: {medio_transporte.valorPorKm}")
    lst_medio_transporte.insert(END, f"Tiempo Por Km: {medio_transporte.tiempoPorKm}")
    lst_medio_transporte.insert(END, " ")

    # hasta que no se selecciona un medio de transporte no se activa el botón para iniciar recorrido:
    btn_realizar_recorrido["state"] = "normal"


def mostrar_info_destino(lst_informacion_destino, combo_medio_transporte, select_ciudad, ciudad):
    """Carga la informacion de un camino determinado

    :param lst_informacion_destino: donde se muestra la informacion de el camino
    :param combo_medio_transporte: combo en el cual se carga la información de los medios disponibles para ese camino
    :param select_ciudad: ciudad elegida
    :param ciudad: objeto ciudad actual
    :return:
    """

    # Se busca la lista de medios de transporte disponibles para esa ciudad:
    lista_medios = ciudad.retornar_lista_medios(select_ciudad.get())

    lista_nombres = retornar_nombres_medios_transporte(lista_medios)
    combo_medio_transporte["values"] = lista_nombres

    # Se relacion con la ciudad en cuestion:
    relacion = ciudad.buscar_relacion(select_ciudad.get())
    # Se limpia la lista de información:
    lst_informacion_destino.delete(0, END)

    lst_informacion_destino.insert(END, " ")
    # Se insertan los datos de la relación consultada:
    lst_informacion_destino.insert(END, f"Destino: {relacion.destino}")
    lst_informacion_destino.insert(END, f"Distancia: {relacion.distancia}")
    lst_informacion_destino.insert(END, " ")


def retornar_nombres_medios_transporte(lista_medios):
    """Retorna una lista con los nombres de los medios de transporte

    :param lista_medios: lista con los id de los medios de transporte
    :return:
    """
    lista_nombres_medios = []

    for id in lista_medios:
        transporte = grafo.buscar_transporte(id)
        lista_nombres_medios.append(transporte.name)

    return lista_nombres_medios


def mostrar_info_trabajo(lst_informacion_trabajo, select_trabajo, ciudad):
    """Carga la información de un trabajo a partir de un elemento seleccionado

    :return:
    """
    # Se busca la información de el trabajo a mostrar:
    trabajo = ciudad.buscar_trabajo(select_trabajo.get())
    # Se limpia el cuadro de informacion:
    lst_informacion_trabajo.delete(0, END)
    # Se inserta la información de los datos de el trabajo:
    lst_informacion_trabajo.insert(END, f"Nombre de Trabajo: {trabajo.nombre_trabajo}")
    lst_informacion_trabajo.insert(END, f"Pago Economico: {trabajo.pago_trabajo}")
    lst_informacion_trabajo.insert(END, f"Tiempo Requerido: {trabajo.tiempo_invertido}")


def mostrar_info_actividad(lst_informacion_actividad, select_actividad, ciudad):
    """Carga la información de una actividad a partir de un elemento seleccionado

    :param event:
    :return:
    """
    # Se busca la información de el trabajo a mostrar:
    actividad = ciudad.buscar_actividad(select_actividad.get())
    # Se limpia el cuadro de informacion:
    lst_informacion_actividad.delete(0, END)
    # Se inserta la información de los datos de el trabajo:
    lst_informacion_actividad.insert(END, f"Nombre De Actividad: {actividad.nombre_actividad}")
    lst_informacion_actividad.insert(END, f"Costo De La Actividad: {actividad.costo_actividad}")
    lst_informacion_actividad.insert(END, f"Tiempo De Inversión: {actividad.tiempo_actividad}")
    lst_informacion_actividad.insert(END, f"Tipo De Actividad: {actividad.tipo_actividad}")


def cerrar_opciones(ventana):
    """Cierra la ventana proporcionada

    :param ventana:
    :return:
    """
    ventana.destroy()


def cargar_grafo():
    # Se llama el método  de la clase arbol  que me permite cargar el JSON:
    grafo.leer_archivo_json()
    # se grafica el grafo de ciudades:
    graficar_grafo()


def graficar_grafo():
    """Pinta el grafo en pantalla

    :return: Nada
    """

    graficar_nodos()
    graficar_aristas()
    # se activa el botón para iniciar el recorrido de el mochilero:
    btn_iniciar_recorrido['state'] = "normal"
    btn_generar_obstruccion['state'] = "normal"
    btn_eliminar_obstruccion['state'] = "normal"


def graficar_nodos():
    """Pinta los nodos en el canvas

    :return: Nada
    """
    global diccionario_coordenadas

    lista_nombres_ciudad = ["Seleccione Una Opcion"]

    contador = 1;
    for ciudad in grafo.lista_ciudades:
        # Coordenadas en X y Y: de cada ciudad
        x = diccionario_coordenadas[contador][0]
        y = diccionario_coordenadas[contador][1]

        # se pinta el Cada nodo que representa a cada ciudad
        canvas_dibujo.create_oval(x, y, x + 50, y + 50, fill="#1E6F4A")
        canvas_dibujo.create_text((x + 25), y + 25, fill="white", font=("Arial", 15), text=ciudad.letra)

        # se guardan las coordenadas:
        ciudad.x = x + 25
        ciudad.y = y

        contador += 1

        # Añadiendo valores a el ComboBox mediante una lista:
        lista_nombres_ciudad.append(ciudad.nombre)

    # se cargan los combos con los valores de las ciudades:
    combo_origen["values"] = lista_nombres_ciudad
    combo_ostruccion_origen["values"] = lista_nombres_ciudad
    combo_obstruccion_destino["values"] = lista_nombres_ciudad


def graficar_aristas():
    """Pinta los caminos de el grafo

    :return: Nada
    """
    for ciudad in grafo.lista_ciudades:

        x1 = ciudad.x
        y1 = ciudad.y

        for arista in ciudad.lista_relaciones:
            # se busca la ciudad destino
            destino = grafo.buscar_ciudad(arista.destino)
            # se crean sus coordenadas:
            x2 = destino.x
            y2 = destino.y

            pintar_camino(x1, y1, x2, y2, "white")
            canvas_dibujo.create_text(((x1 + x2) / 2), ((y1 + y2) / 2) - 10, fill="white", font=("Arial", 15),
                                      text=arista.distancia)


def pintar_camino(x1, y1, x2, y2, color):
    """Pinta una linea en las coordenadas proporcionadas

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param color:
    :return:
    """
    # se crea la relación:
    canvas_dibujo.create_line(x1, y1, x2, y2, width=3, fill=color, dash=(4, 1))


def iniciar_recorrido():
    global mochilero
    global reporte
    global condicion_parada
    condicion_parada = True

    nombre = nombre_user.get()
    presupuesto = int(presupuesto_user.get())
    tiempo_disponible = float(tiempo_estipulado.get())

    ciudad = grafo.buscar_ciudad_por_nombre(select_origen.get())
    x = ciudad.x - 25
    y = ciudad.y - 25

    # se crea un objeto tipo mochilero para guardar registro de este:
    mochilero = Mochilero(nombre, img_mochilero, x, y, ciudad.letra, presupuesto, tiempo_disponible)
    # Se actualiza la información de el mochilero:
    lbl_presupuesto['text'] = f"Saldo Actual: {mochilero.presupuesto}"
    lbl_tiempo_disponible['text'] = f"Tiempo Transcurrido: {mochilero.tiempo_disponible}"

    # se pinta en pantalla
    pintar_mochilero()
    canvas_dibujo.bind('<Double-1>', onCanvasClick)
    # el tiempo empieza a correr y se va visualizando en el indicador:
    actualizar_tiempo()
    # se desactiva el boton para evitar que se creen nuevos personajes:
    btn_iniciar_recorrido["state"] = "disabled"

    reporte.adicionar_ciudad_visitada(ciudad)


def pintar_mochilero():
    # Dispara un evento al dar doble click sobre el canvas:
    global person
    # Pinta el mochilero en pantalla:
    person = canvas_dibujo.create_image(mochilero.x, mochilero.y, image=img_mochilero, anchor=NW)


def generar_obstruccion():
    """Genera una obstruccion en un camino determinado

    :return:
    """
    # obteniendo referencia a el origen y destino seleccionados:
    origen = grafo.buscar_ciudad_por_nombre(select_obstruccion_origen.get())
    destino = grafo.buscar_ciudad_por_nombre(select_obstruccion_destino.get())

    # si existe un camino entre el origen y destino seleccionados:
    if (origen.existe_relacion(destino.letra)):
        # se crea la obstruccion:
        grafo.agregar_obstruccion(origen.letra, destino.letra)
        # se pinta la obstruccion:
        pintar_obstruccion(origen, destino)


    else:
        messagebox.showinfo(message="No Existe una ruta entre los destinos seleccionados", title="Error")


def pintar_obstruccion(origen, destino):
    """Pinta una linea con la obstruccion generada

    :param origen:
    :param destino:
    :return:
    """
    x1 = origen.x
    y1 = origen.y
    x2 = destino.x
    y2 = destino.y
    # Pinta una linea con las obstrucciones
    pintar_camino(x1, y1, x2, y2, "red")


def retirar_obstruccion():
    # obteniendo referencia a el origen y destino seleccionados:
    origen = grafo.buscar_ciudad_por_nombre(select_obstruccion_origen.get())
    destino = grafo.buscar_ciudad_por_nombre(select_obstruccion_destino.get())

    # si existe la obstruccion:
    if (grafo.existe_obstruccion(origen.letra, destino.letra)):

        # si existe un camino entre el origen y destino seleccionados:
        if (grafo.existe_obstruccion(origen.letra, destino.letra)):
            # se elimina la ostruccion:
            grafo.eliminar_obstruccion(origen.letra, destino.letra)
            # se deja el camino tal cual como está.
            pintar_camino(origen.x, origen.y, destino.x, destino.y, "white")
            messagebox.showinfo(message="La obstrucción ha sido retirada", title="Error")


    else:
        messagebox.showinfo(message="En el momento la Ruta no presenta obstrucciones", title="Error")


def actualizar_tiempo():
    def run():
        """Este submetodo me permite iniciar una cola de ejecución con el hilo que me dirige a la función que
            deceo ejecutar en segundo plano:

        :return: Nada
        """
        # agregar a la cola de ejecución que permite el uso de thread-safe:
        try:
            cola.put(None, incrementar_tiempo())

        except:
            pass

    # se inicia el hilo
    hilo = threading.Thread(target=run)
    hilo.start()


def incrementar_tiempo():
    """Administra el tiempo de el mochilero:

    :return:Nada
    """

    global condicion_parada

    recordatorio_comida = 1
    recordatorio_dormida = 1
    while (condicion_parada):
        lbl_tiempo_disponible['text'] = f"Tiempo Restante: {mochilero.tiempo_disponible}"
        time.sleep(5)
        # se descuenta el contador de tiempo de el mochilero
        mochilero.tiempo_disponible -= 1
        # si se ha alcanzado el tiempo estipulado, muestre un anuncio, detenga el tiempo.
        verificar_tiempo()
        recordatorio_comida = recordar_alimentacion(recordatorio_comida)
        recordatorio_dormida = recordar_dormir(recordatorio_dormida)


def recordar_alimentacion(recordatorio_comida):
    """Lanza una alerta indicando a el usuario que debe alimentarse

    :param recordatorio_comida: contador que me permite verificar si ya han pasado cinco horas desde la última comida
    :return: El contador para continuar la cuenta o reiniciarla en caso de coma.
    """
    if (recordatorio_comida == 6):
        messagebox.showinfo(message="Recordatorio, es hora de comer, por favor dirígete a tu sucursal más cercano!",
                            title="Advertencia")
        return 0
    else:
        return recordatorio_comida + 1


def recordar_dormir(recordatorio_dormida):
    """Lanza una alerta indicando a el usuario debe dormir

    :param recordatorio_dormida: contador que me permite verificar si ya es hora de lanzar el mensaje
    :return: La cuenta de las horas
    """
    if (recordatorio_dormida == 18):
        messagebox.showinfo(message="Recordatorio, es hora de dormir, por favor dirígete a tu sucursal más cercano!",
                            title="Advertencia")
        return 0
    else:
        return recordatorio_dormida + 1


def verificar_tiempo():
    """Verifica si se ha agotado el tiempo que tenia asignado el viajero

    :return:
    """
    global mochilero
    if (mochilero.tiempo_disponible == 0):
        messagebox.showinfo(message="El tiempo asignado se ha agotado! ¡Es necesario ingresar tiempo adicional!",
                            title="Advertencia")
        # Cuando el presupuesto ha sido agotado se muestra una ventana indicando ingresar tiempo adicional
        mochilero.tiempo_disponible_inicial = mochilero.tiempo_disponible = integerbox(msg='Ingrese nuevo tiempo',
                                                                                       title='Tiempo', default=0,
                                                                                       lowerbound=10, upperbound=999999,
                                                                                       image=None)


def sugerir_ruta_corta():
    # se busca la ciudad de origen:
    ciudad = grafo.buscar_ciudad_por_nombre(select_origen.get())
    # se llama el recorrido primm
    ruta = grafo.recorrido_prim(ciudad.letra)
    graficar_primm(ruta)


def graficar_primm(ruta):
    """Grafica el recorrido generado por el algoritmo Primm

    :param ruta: ruta que retorna el algoritomo
    :return: Nada
    """
    # El for recorre cada una de los caminos retornados por la lista
    graficar_grafo()
    for relacion in ruta:
        # este for permite extraer los datos que vienen empaquetados en cada diccionario contenido en la lista:
        for ciudad in relacion:
            origen = grafo.buscar_ciudad(ciudad)
            destino = grafo.buscar_ciudad(relacion[ciudad])
            pintar_camino(origen.x, origen.y, destino.x, destino.y, "yellow")


def ruta_menor_costo():
    """Determina la ruta con menor costo con el presupuesto actual:

    :return:
    """
    global mochilero
    # se busca la ciudad de origen:
    ciudad = grafo.buscar_ciudad_por_nombre(select_origen.get())
    # se llama el recorrido primm
    ruta = grafo.recorrido_menor_costo(ciudad.letra, mochilero.presupuesto)
    graficar_primm(ruta)


def ruta_menor_tiempo():
    """Determina la ruta con menor tiempo con el tiempo actual:

    :return:
    """
    global mochilero
    # se busca la ciudad de origen:
    ciudad = grafo.buscar_ciudad_por_nombre(select_origen.get())
    # se llama el recorrido primm
    ruta = grafo.recorrido_menor_tiempo(ciudad.letra, mochilero.tiempo_disponible)
    graficar_primm(ruta)


def reporte_final():
    """Genera la ventana de opciones para cada ciudad:

        :param event: Evento producido al realizar doble click
        :return: Nada
        """
    global mochilero
    global condicion_parada
    global reporte
    # se genera una ventana independiente:
    ventana_opciones = Toplevel()

    # Se le da un tamaño:
    ventana_opciones.geometry("400x580")

    # Agregando un titulo a la ventana
    ventana_opciones.title("Informe")

    # En este canvas colocaremos las herramientas que nos permitan manipular el programa
    canvas_opciones = Canvas(ventana_opciones, width=400, height=580, bg="#2E065E")
    canvas_opciones.place(x=5, y=0)

    canvas_opciones.create_image(0, 0, image=img_fondo_opciones, anchor=NW)
    # Nombre de la ciudad
    etiqueta = Label(canvas_opciones, text="Estadisticas", bg="#2E065E", fg="white", font=("Arial", 11)).place(x=170, y=0)

    # ciudades_visitadas=Reporte.ciudades_visitadas

    lstInformacion = Listbox(canvas_opciones, bg="#2E065E", width=53, height=30, font=("Arial", 11),
                             fg="#ffffff")
    lstInformacion.place(x=10, y=30)

    reiniciar_valores()

    lstInformacion.insert(END, "TRABAJOS")

    for trabajo in reporte.trabajos_realizados:
        lstInformacion.insert(END, f"trabajo: {trabajo['nombre_trabajo']}")
        lstInformacion.insert(END, f"Pago: {trabajo['pago_trabajo']}")
        lstInformacion.insert(END, f"Tiempo: {trabajo['tiempo_invertido']}")
        lstInformacion.insert(END, f"ciudad: {trabajo['ciudad']}")
        lstInformacion.insert(END, " ")

    lstInformacion.insert(END, "ACTIVIDADES")

    for actividad in reporte.actividades_realizadas:
        lstInformacion.insert(END, f"Actividad: {actividad['nombre_actividad']}")
        lstInformacion.insert(END, f"Costo: {actividad['costo_actividad']}")
        lstInformacion.insert(END, f"Tiempo: {actividad['tiempo_invertido']}")
        lstInformacion.insert(END, f"ciudad: {actividad['ciudad']}")
        lstInformacion.insert(END, " ")

    lstInformacion.insert(END, "CIUDADES V.")

    for ciudades in reporte.ciudades_visitadas:
        lstInformacion.insert(END, f"Letra: {ciudades['letra']}")
        lstInformacion.insert(END, f"Nombre: {ciudades['nombre']}")
        lstInformacion.insert(END, f"Estadía_minima: {ciudades['estadía_minima']}")
        lstInformacion.insert(END, " ")

    lstInformacion.insert(END, "VIAJES")

    for costo_ciudad in reporte.costos_por_viaje:
        lstInformacion.insert(END, f"Origen: {costo_ciudad['origen']}")
        lstInformacion.insert(END, f"Destino: {costo_ciudad['destino']}")
        lstInformacion.insert(END, f"Costo: {costo_ciudad['costo']}")
        lstInformacion.insert(END, f"Tiempo: {costo_ciudad['tiempo']}")
        lstInformacion.insert(END, " ")

    lstInformacion.insert(END, " ")
    lstInformacion.insert(END, f"Total dinero gastado: {reporte.total_dinero_gastado}")
    lstInformacion.insert(END, " ")

    lstInformacion.insert(END, " ")
    lstInformacion.insert(END, f"Km recorrido: {reporte.kilometros_recorridos}")

    ventana_opciones.mainloop()


def reiniciar_valores():
    global condicion_parada
    btn_iniciar_recorrido['state'] = 'normal'
    canvas_dibujo.delete(person)
    condicion_parada = False
    txt_nombre.delete(0, END)
    txt_presupuesto.delete(0, END)
    txt_tiempo.delete(0, END)
    lbl_presupuesto["text"] = f"Saldo Actual: {0}"
    lbl_tiempo_disponible['text'] = f"Tiempo Restante: {0}"


"""--------------------------------------   --------------------Botonera---------------------------------------------------------------------------"""
# Este botón realiza la lectura de el JSON y carga el arbol:
btn_cargar_grafo = Button(canvas_principal, width=25, text="Cargar Grafo", font=("Arial", 11), fg="#ffffff",
                          command=cargar_grafo, background="#1E6F4A")
btn_cargar_grafo.place(x=50, y=50)

btn_iniciar_recorrido = Button(canvas_principal, width=25, text="Empezar", state="disabled",
                               font=("Arial", 11), fg="#ffffff", command=iniciar_recorrido,
                               background="#1E6F4A")
btn_iniciar_recorrido.place(x=50, y=270)

btn_generar_obstruccion = Button(canvas_principal, width=25, text="Obstruir", state="disabled",
                                 font=("Arial", 11), fg="#ffffff", command=generar_obstruccion,
                                 background="#1E6F4A")
btn_generar_obstruccion.place(x=50, y=400)

btn_eliminar_obstruccion = Button(canvas_principal, width=25, text="No Obstruir", state="disabled",
                                  font=("Arial", 11), fg="#ffffff", command=retirar_obstruccion,
                                  background="#1E6F4A")
btn_eliminar_obstruccion.place(x=50, y=440)

btn_generar_recorrido = Button(canvas_principal, width=25, text="MST Distancia", state="normal",
                               font=("Arial", 11), fg="#ffffff", command=sugerir_ruta_corta,
                               background="#1E6F4A")
btn_generar_recorrido.place(x=50, y=480)

btn_recorrido_menor_costo = Button(canvas_principal, width=25, text="MST Costo", state="normal",
                                   font=("Arial", 11), fg="#ffffff", command=ruta_menor_costo,
                                   background="#1E6F4A")
btn_recorrido_menor_costo.place(x=50, y=520)

btn_recorrido_menor_costo = Button(canvas_principal, width=25, text="MST Tiempo", state="normal",
                                   font=("Arial", 11), fg="#ffffff", command=ruta_menor_tiempo,
                                   background="#1E6F4A")
btn_recorrido_menor_costo.place(x=50, y=560)

btn_cerrar_ventana_principal = Button(canvas_principal, width=25, text="Terminar", font=("Arial", 11),
                                      fg="#ffffff", command=reporte_final, background="#1E6F4A")
btn_cerrar_ventana_principal.place(x=50, y=600)

btn_cerrar_ventana_principal = Button(canvas_principal, width=25, text="Salir", font=("Arial", 11),
                                      fg="#ffffff", command=lambda: ventana.destroy(), background="#1E6F4A")
btn_cerrar_ventana_principal.place(x=50, y=640)

"""----------------------------------------------------------Hilo principal de ejecución----------------------------------------------------------"""

# Hace que la ventana se mantenga persistente en pantalla
ventana.mainloop()
