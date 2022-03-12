from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
from tkinter import messagebox

from pysnmp import hlapi
from quicksnmp import get
from quicksnmp import set
import os
from tablas import tablas
from traps_IP import interfaz_traps_IP
from traps_ICMP import interfaz_traps_ICMP
from traps_TCP import interfaz_traps_TCP
from traps_UDP import interfaz_traps_UDP
from traps_Interface import interfaz_traps_Interface


# Funcion que muestra la ventana para la gestion de objetos escalares
# Parametros:
#   -Lista de IP's de la red
def escalares(ip, nombre):
    gestion = Tk()
    gestion.focus()
    gestion.geometry('1650x800')
    gestion.title("Gestion de objetos")

    intro1 = Label(gestion, text="Seleccione una ip", font=("Arial", 18))
    intro1.pack(pady=10)
    combo_ip = Combobox(gestion, width=30)
    valores=['Selecione una ip','']
    for i in range(len(ip)):
        valores.append(ip[i]+nombre[i])

    combo_ip['values'] = valores
    combo_ip.current(1)
    combo_ip.pack(pady=10)

    intro2 = Label(gestion, text="Seleccione una comunidad", font=("Arial", 18))
    intro2.pack(pady=10)
    comunidad_entry = Entry(gestion, width=30)
    comunidad_entry.insert(0, "TrabajoGestion")
    comunidad_entry.pack(pady=10)

    intro3 = Label(gestion, text = "Seleccione un grupo de objetos predeterminados", font=("Arial",18))
    intro3.pack(pady=10)
    combo_grupos = Combobox(gestion)
    combo_grupos['values'] = ['Seleccione un grupo', 'system', 'ip e interfaces','icmp, tcp y udp' ,'host-resources']
    combo_grupos.current(0)
    combo_grupos.pack(pady=10)
    boton_grupos = Button(gestion, text="Ver objetos del grupo", command=lambda: objPredeterminados(combo_grupos.get(), combo_ip.get(), comunidad_entry.get()))
    boton_grupos.pack(pady=10)
    intro4 = Label(gestion, text="Seleccionar un objeto", font=("Arial", 18))
    intro4.pack(pady=10)
    boton_get = Button(gestion, text="Peticion GET", command=lambda: get_objeto(combo_ip.get(), comunidad_entry.get()))
    boton_get.pack(pady=10)
    boton_set = Button(gestion, text="Peticion SET", command=lambda: set_objeto(combo_ip.get(), comunidad_entry.get()))
    boton_set.pack(pady=10)

    def salir():
        gestion.destroy()

    boton_volver = Button(gestion, text="Volver al menu", command=salir)
    boton_volver.pack(pady=10)

# Funcion que muestra el menu de acceso a las tablas
# Parametros
#   - ip seleccionada
#   - comunidad seleccionada
#   - grupo de tablas seleccinado
def get_tablas(ip,comunidad,grupo):
    tablas(ip,comunidad,grupo)

#Funcion que muestra la ventana de los objetos predeterminados segun el grupo
#Parametros:
#   -Grupo de objetos predeterminados
#   -ip a la que se manda la peticion
#   -comunidad SNMP
def objPredeterminados(grupo,ip, comunidad,correo):
    ip=ip[:13]
    ip=ip.replace(" ", "")

    def salir():
        system.destroy()

    if (grupo == 'system'):
        system = Tk()
        system.geometry('1650x800')
        system.title("Grupo System")
        system.config(bg='white')
        intro = Label(system, text="Grupo System", font=("Arial Bold", 25))
        intro.pack(ipady=30)
        intro.config(bg='white')

        boton_salir = Button(system, text="Salir", bg='firebrick3', fg='white', command=salir)
        boton_salir.pack(side=BOTTOM, ipadx=100, padx=10, pady=10)
        separator = Separator(system, orient='horizontal')
        separator.pack(fill='x', side=BOTTOM)

        frameTitulos = Frame(system)
        frameTitulos.pack(side=TOP, padx=50, pady=15)
        frameTitulos.pack(fill="x")
        frameTitulos.config(bg='white')

        frameGetSet = Frame(system)
        frameGetSet.pack(side=RIGHT, ipadx=250, anchor=N)
        frameGetSet.config(bg='white')

        framePantalla = Frame(system)
        framePantalla.pack(side=RIGHT, anchor=N)
        framePantalla.config(bg='white')

        frameBotones = Frame(system)
        frameBotones.pack(side=RIGHT, anchor=N, padx=10)
        frameBotones.config(bg='white')

        intro3 = Label(frameTitulos, text="Objetos predeterminados", font=("Arial Bold", 20))
        intro3.pack(side=LEFT, ipadx=100)
        intro3.config(bg='white')
        intro4 = Label(frameTitulos, text="Seleccionar un objeto", font=("Arial Bold", 20))
        intro4.pack(side=RIGHT, ipadx=100)
        intro4.config(bg='white')

        pantalla = Text(framePantalla, state="disabled", width=60, height=4, font=("Helvetica", 15), bg='gray95')
        boton1 = Button(frameBotones, text="Nombre del equipo", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.1.5.0',
                                                           pantalla))
        boton1.pack(side=TOP, ipadx=21)
        boton2 = Button(frameBotones, text="Descripcion", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.1.1.0',
                                                           pantalla))
        boton2.pack(side=TOP, ipadx=40)
        boton3 = Button(frameBotones, text="Nombre de contacto", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.1.4.0',
                                                           pantalla))
        boton3.pack(side=TOP, ipadx=17)
        boton4 = Button(frameBotones, text="Localizacion del equipo", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.1.6.0',
                                                           pantalla))
        boton4.pack(side=TOP, ipadx=10)
        boton5 = Button(frameBotones, text="Tiempo encendido (ms)", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.1.3.0',
                                                           pantalla))
        boton5.pack(side=TOP, ipadx=10)
        pantalla.pack(padx=15, pady=20)

        boton_limpia = Button(framePantalla, text="Limpiar pantalla", bg='gainsboro', command=lambda: limpiarPantalla(pantalla))
        boton_limpia.pack(pady=10)

        boton_get = Button(frameGetSet, text="Peticion GET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: get_objeto(ip, comunidad))
        boton_get.pack(pady=10)
        boton_set = Button(frameGetSet, text="Peticion SET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: set_objeto(ip, comunidad))
        boton_set.pack(pady=10)

    if (grupo == 'ip e interfaces'):
        system = Tk()
        system.geometry('1650x800')
        system.config(bg='white')
        system.title("Grupo IP e Interfaces")
        intro = Label(system, text="Grupo IP e Interfaces", font=("Arial Bold", 25))
        intro.pack(ipady=25)
        intro.config(bg='white')
        intro0 = Label(system, text="Objetos Escalares", font=("Arial Bold", 20))
        intro0.pack(ipady=10)
        intro0.config(bg='white')

        boton_salir = Button(system, text="Salir", bg='firebrick3', fg='white', command=salir)
        boton_salir.pack(side=BOTTOM, ipadx=100, padx=10, pady=15)
        separator = Separator(system, orient='horizontal')
        separator.pack(fill='x', side=BOTTOM)

        boton_if = Button(system, text="ifTable", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 'if'))
        boton_if.pack(side=BOTTOM, ipadx=28, pady=5)
        boton_ip = Button(system, text="ipAddrTable", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 'ip1'))
        boton_ip.pack(side=BOTTOM, ipadx=5)
        boton_ip2 = Button(system, text="ipRouteTable", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 'ip2'))
        boton_ip2.pack(side=BOTTOM, pady=5)
        intro5 = Label(system, text="Tablas", font=("Arial Bold", 20))
        intro5.pack(ipady=15, side=BOTTOM)
        intro5.config(bg='white')

        boton_mon1 = Button(system, text="Monitorizar grupo IP",bg='SkyBlue2', font=("Arial", 15),
                           command=lambda: interfaz_traps_IP(ip, comunidad, correo))
        boton_mon1.pack(pady=20, ipadx=34, side=BOTTOM)
        boton_mon2 = Button(system, text="Monitorizar grupo Interfaces", bg='SkyBlue2', font=("Arial", 15),
                           command=lambda: interfaz_traps_Interface(ip, comunidad, correo))
        boton_mon2.pack(pady=7, side=BOTTOM)
        intro6 = Label(system, text="Monitorización", font=("Arial Bold", 20))
        intro6.pack(ipady=10, side=BOTTOM)
        intro6.config(bg='white')

        frameTitulos = Frame(system)
        frameTitulos.pack(side=TOP, padx=50, pady=15)
        frameTitulos.pack(fill="x")
        frameTitulos.config(bg='white')

        frameGetSet = Frame(system)
        frameGetSet.pack(side=RIGHT, ipadx=225, anchor=N)
        frameGetSet.config(bg='white')

        framePantalla = Frame(system)
        framePantalla.pack(side=RIGHT, anchor=N)
        framePantalla.config(bg='white')

        frameBotones = Frame(system)
        frameBotones.pack(side=RIGHT, anchor=N, padx=10)
        frameBotones.config(bg='white')

        intro3 = Label(frameTitulos, text="Objetos predeterminados", font=("Arial Bold", 20))
        intro3.pack(side=LEFT, ipadx=100)
        intro3.config(bg='white')
        intro4 = Label(frameTitulos, text="Seleccionar un objeto", font=("Arial Bold", 20))
        intro4.pack(side=RIGHT, ipadx=100)
        intro4.config(bg='white')

        pantalla = Text(framePantalla, state="disabled", width=60, height=4, font=("Helvetica", 15), bg='gray95')
        boton1 = Button(frameBotones, text="Valor del campo TTL", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.4.2.0',
                                                           pantalla))
        boton1.pack(side=TOP, ipadx=50, padx=5)
        boton2 = Button(frameBotones, text="Numero de datagramas recibidos", bg='SkyBlue2' ,
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.4.3.0',
                                                           pantalla))
        boton2.pack(side=TOP, ipadx=15, padx=5)
        boton3 = Button(frameBotones, text="Numero de datagramas recibidos\n con cabecera erronea", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.4.4.0',
                                                           pantalla))
        boton3.pack(side=TOP, ipadx=15, padx=5)
        boton4 = Button(frameBotones, text="Numero de datagramas recibidos\n con direccion IP erronea", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.4.5.0',
                                                           pantalla))
        boton4.pack(side=TOP, ipadx=15, padx=5)
        boton5 = Button(frameBotones, text="Numero de interfaces", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.2.1.0',
                                                           pantalla))
        boton5.pack(side=TOP, ipadx=45, padx=5)
        pantalla.pack(padx=15,pady=15)

        boton_limpia = Button(framePantalla, text="Limpiar pantalla", bg='gainsboro', command=lambda: limpiarPantalla(pantalla))
        boton_limpia.pack(pady=10)

        boton_get = Button(frameGetSet, text="Peticion GET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: get_objeto(ip, comunidad))
        boton_get.pack(pady=10)
        boton_set = Button(frameGetSet, text="Peticion SET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: set_objeto(ip, comunidad))
        boton_set.pack(pady=10)

    if (grupo == 'icmp, tcp y udp'):
        system = Tk()
        system.geometry('1650x800')
        system.config(bg='white')
        system.title("Grupos ICMP, TCP y UDP")
        intro = Label(system, text="Grupo ICMP, TCP y UDP", font=("Arial Bold", 25))
        intro.pack(ipady=20)
        intro.config(bg='white')
        intro0 = Label(system, text="Objetos Escalares", font=("Arial Bold", 20))
        intro0.pack(ipady=7)
        intro0.config(bg='white')

        boton_salir = Button(system, text="Salir", bg='firebrick3', fg='white', command=salir)
        boton_salir.pack(side=BOTTOM, ipadx=100, padx=10, pady=15)
        separator = Separator(system, orient='horizontal')
        separator.pack(fill='x', side=BOTTOM)

        boton_if = Button(system, text="Tabla de TCP", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 't'))
        boton_if.pack(side=BOTTOM, pady=15)
        boton_ip = Button(system, text="Tabla de UDP", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 'u'))
        boton_ip.pack(side=BOTTOM)
        intro5 = Label(system, text="Tablas", font=("Arial Bold", 20))
        intro5.pack(ipady=10, side=BOTTOM)
        intro5.config(bg='white')

        boton_mon1 = Button(system, text="Monitorizar grupo TCP", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: interfaz_traps_TCP(ip, comunidad, correo))
        boton_mon1.pack(pady=5, side=BOTTOM)
        boton_mon2 = Button(system, text="Monitorizar grupo UDP", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: interfaz_traps_UDP(ip, comunidad, correo))
        boton_mon2.pack(pady=5, side=BOTTOM)
        boton_mon3 = Button(system, text="Monitorizar grupo ICMP", font=("Arial", 15), bg='SkyBlue2',
                            command=lambda: interfaz_traps_ICMP(ip, comunidad, correo))
        boton_mon3.pack(pady=5, side=BOTTOM)
        intro6 = Label(system, text="Monitorización", font=("Arial Bold", 20))
        intro6.pack(ipady=7, side=BOTTOM)
        intro6.config(bg='white')

        frameTitulos = Frame(system)
        frameTitulos.pack(side=TOP, padx=50, pady=15)
        frameTitulos.pack(fill="x")
        frameTitulos.config(bg='white')

        frameGetSet = Frame(system)
        frameGetSet.pack(side=RIGHT, ipadx=225, anchor=N)
        frameGetSet.config(bg='white')

        framePantalla = Frame(system)
        framePantalla.pack(side=RIGHT, anchor=N)
        framePantalla.config(bg='white')

        frameBotones = Frame(system)
        frameBotones.pack(side=RIGHT, anchor=N, padx=10)
        frameBotones.config(bg='white')

        intro3 = Label(frameTitulos, text="Objetos predeterminados", font=("Arial Bold", 20))
        intro3.pack(side=LEFT, ipadx=100)
        intro3.config(bg='white')
        intro4 = Label(frameTitulos, text="Seleccionar un objeto", font=("Arial Bold", 20))
        intro4.pack(side=RIGHT, ipadx=100)
        intro4.config(bg='white')

        pantalla = Text(framePantalla, state="disabled", width=60, height=4, bg='gray95', font=("Helvetica", 15))
        boton1 = Button(frameBotones, text="Numero de mensajes ICMP recibidos", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.5.1.0',
                                                           pantalla))
        boton1.pack(side=TOP, ipadx=10, padx=5)
        boton2 = Button(frameBotones, text="Numero de mensajes ICMP recibidos\n con error", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.5.2.0',
                                                           pantalla))
        boton2.pack(side=TOP, ipadx=10, padx=5)
        boton3 = Button(frameBotones, text="Numero de conexiones TCP", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.6.9.0',
                                                           pantalla))
        boton3.pack(side=TOP, ipadx=34, padx=5)
        boton4 = Button(frameBotones, text="Numero de segmentos TCP recibidos", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.6.10.0',
                                                           pantalla))
        boton4.pack(side=TOP, ipadx=10, padx=5)
        boton5 = Button(frameBotones, text="Numero de datagramas UDP recibidos", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.7.1.0',
                                                           pantalla))
        boton5.pack(side=TOP, ipadx=7, padx=5)
        pantalla.pack(padx=15,pady=15)

        boton_limpia = Button(framePantalla, text="Limpiar pantalla", bg='gainsboro', command=lambda: limpiarPantalla(pantalla))
        boton_limpia.pack(pady=10)

        boton_get = Button(frameGetSet, text="Peticion GET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: get_objeto(ip, comunidad))
        boton_get.pack(pady=10)
        boton_set = Button(frameGetSet, text="Peticion SET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: set_objeto(ip, comunidad))
        boton_set.pack(pady=10)

    if (grupo == 'host-resources'):
        system = Tk()
        system.geometry('1650x800')
        system.config(bg='white')
        system.title("Grupos Host-Resources")
        intro = Label(system, text="Grupo Host-Resources", font=("Arial Bold", 25))
        intro.pack(ipady=30)
        intro.config(bg='white')
        intro0 = Label(system, text="Objetos Escalares", font=("Arial Bold", 20))
        intro0.pack(ipady=20)
        intro0.config(bg='white')

        boton_salir = Button(system, text="Salir", bg='firebrick3', fg='white', command=salir)
        boton_salir.pack(side=BOTTOM, ipadx=100, padx=10, pady=15)
        separator = Separator(system, orient='horizontal')
        separator.pack(fill='x', side=BOTTOM)

        boton_hr1 = Button(system, text="hrDevicesTable", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 'h2'))
        boton_hr1.pack(side=BOTTOM, pady=15)
        boton_hr2 = Button(system, text="hrSWRunTable", font=("Arial", 15), bg='SkyBlue2', command=lambda: get_tablas(ip, comunidad, 'h1'))
        boton_hr2.pack(side=BOTTOM, pady=15)
        intro5 = Label(system, text="Tablas", font=("Arial Bold", 20))
        intro5.pack(ipady=15, side=BOTTOM)
        intro5.config(bg='white')

        frameTitulos = Frame(system)
        frameTitulos.pack(side=TOP, padx=50, pady=15)
        frameTitulos.pack(fill="x")
        frameTitulos.config(bg='white')

        frameGetSet = Frame(system)
        frameGetSet.pack(side=RIGHT, ipadx=225, anchor=N)
        frameGetSet.config(bg='white')

        framePantalla = Frame(system)
        framePantalla.pack(side=RIGHT, anchor=N)
        framePantalla.config(bg='white')

        frameBotones = Frame(system)
        frameBotones.pack(side=RIGHT, anchor=N, padx=10)
        frameBotones.config(bg='white')

        intro3 = Label(frameTitulos, text="Objetos predeterminados", font=("Arial Bold", 20))
        intro3.pack(side=LEFT, ipadx=100)
        intro3.config(bg='white')
        intro4 = Label(frameTitulos, text="Seleccionar un objeto", font=("Arial Bold", 20))
        intro4.pack(side=RIGHT, ipadx=100)
        intro4.config(bg='white')

        pantalla = Text(framePantalla, state="disabled", width=60, height=4, bg='gray95', font=("Helvetica", 15))
        boton2 = Button(frameBotones, text="Numero de sesiones en el equipo", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.25.1.5.0',
                                                           pantalla))
        boton2.pack(side=TOP, ipadx=12, padx=5)
        boton3 = Button(frameBotones, text="Numero de procesos en el equipo", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.25.1.6.0',
                                                           pantalla))
        boton3.pack(side=TOP, ipadx=10, padx=5)
        boton4 = Button(frameBotones, text="Cantidad de memoria fisica del\n equipo (KBytes)", bg='SkyBlue2',
                        command=lambda: get_predeterminado(ip, comunidad, '1.3.6.1.2.1.25.2.2.0',
                                                           pantalla))
        boton4.pack(side=TOP, ipadx=17, padx=5)
        pantalla.pack(padx=15,pady=15)

        boton_limpia = Button(framePantalla, text="Limpiar pantalla", command=lambda: limpiarPantalla(pantalla))
        boton_limpia.pack(pady=10)

        boton_get = Button(frameGetSet, text="Peticion GET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: get_objeto(ip, comunidad))
        boton_get.pack(pady=10)
        boton_set = Button(frameGetSet, text="Peticion SET", font=("Arial", 15), bg='SkyBlue2',
                           command=lambda: set_objeto(ip, comunidad))
        boton_set.pack(pady=10)

# Funcion para limpiar la pantalla
# Parametros:
#   - pantalla a limpiar
def limpiarPantalla(pantalla):
    pantalla.configure(state="normal")
    pantalla.delete("1.0", END)
    pantalla.configure(state="disabled")

# Funcion que genera la peticion GET para el objeto hostname
# Paramentros:
#   - ip a la que se manda la peticion
#   - community SNMP
def get_predeterminado(ip,community,oid,pantalla):
    valor = get(ip, [oid], hlapi.CommunityData(community))
    for key, value in valor.items():
        a = (key, value)
    oid = a[0]
    value = a[1]
    #messagebox.showerror('Error', 'No se ha podido obtener el objeto')

    msg = 'El objeto con oid: '+oid+' es: '+str(value)
    limpiarPantalla(pantalla)
    pantalla.configure(state="normal")
    pantalla.insert(END, msg)
    pantalla.configure(state="disabled")

# Funcion para generar la peticion GET para un objeto que introduzca el usuario
# Paramentros:
#   - ip a la que se manda la peticion
#   - community SNMP
def get_objeto(ip,community):
    ip = ip[:13]
    ip.replace(" ", "")
    get_win = Tk()
    get_win.geometry('600x300')
    get_win.config(bg='white')
    get_win.title("Peticion GET")
    peticion = Label(get_win, text="Inroduzca el oid del objeto", font=("Arial", 14))
    peticion.pack()
    peticion.config(bg='white')
    peticion_entry = Entry(get_win, width=30, bg='gray95')
    peticion_entry.pack()
    try:
        boton_get = Button(get_win, text="GET", bg='SkyBlue2', command=lambda: get_objeto_aux(peticion_entry.get(), ip, community))
    except:
        messagebox.showerror('Error', 'No se han introducido el oid del objeto')
    boton_get.pack(pady=10, ipadx=20)
    pantalla = Text(get_win, state="disabled", width=50, height=3, bg='gray95', font=("Helvetica", 15))
    pantalla.pack()

    def salir():
        get_win.destroy()

    boton_limpia = Button(get_win, text="Limpiar", bg='gainsboro', command=lambda: limpiarPantalla(pantalla))
    boton_limpia.pack(pady=10, ipadx=7)
    separator = Separator(get_win, orient='horizontal')
    separator.pack(fill='x')
    boton_salir = Button(get_win, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(side=BOTTOM, ipadx=100, padx=10, pady=10)
    def get_objeto_aux(oid,ip,community):
        limpiarPantalla(pantalla)
        try:
            valor = get(ip, [oid], hlapi.CommunityData(community))
            for key, value in valor.items():
                a = (key, value)
                oid = a[0]
                value = a[1]
        except:
            messagebox.showerror('Error', 'No se ha podido obtener el objeto')
        msg = 'El objeto con oid: '+oid+', tiene el valor: \n'+str(value)
        pantalla.configure(state="normal")
        pantalla.insert(END, msg)
        pantalla.configure(state="disabled")

# Funcion para generar la peticion SET para un objeto que introduzca el usuario
# Paramentros:
#   - ip a la que se manda la peticion
#   - community SNMP
def set_objeto(ip, community):
    ip = ip[:13]
    ip.replace(" ", "")
    set_win = Tk()
    set_win.geometry('600x300')
    set_win.config(bg='white')
    set_win.title("Peticion SET")
    peticion = Label(set_win, text="Inroduzca el oid del objeto", font=("Arial", 14))
    peticion.pack()
    peticion.config(bg='white')
    peticion_entry = Entry(set_win, width=30, bg='gray95')
    peticion_entry.pack()
    valor = Label(set_win, text="Inroduzca el valor deseado", font=("Arial", 14))
    valor.pack()
    valor.config(bg='white')
    valor_entry = Entry(set_win, width=30, bg='gray95')
    valor_entry.pack()
    boton_set = Button(set_win, text="SET", bg='SkyBlue2', command=lambda: set_objeto_aux(peticion_entry.get(), valor_entry.get(),  ip, community))
    boton_set.pack(pady=10, ipadx=20)
    def set_objeto_aux(oid, valor, ip, community):
        try:
            set(ip, {oid: valor}, hlapi.CommunityData(community))
            msg = 'El objeto con oid: '+oid+', ha pasado a tener el valor: '+valor
            messagebox.showinfo(oid, msg)
            set_win.destroy()
        except:
            messagebox.showerror('Error', 'No se ha podido realizar el set')

    def salir():
        set_win.destroy()

    separator = Separator(set_win, orient='horizontal')
    separator.pack(fill='x')
    boton_salir = Button(set_win, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(side=BOTTOM, ipadx=100, padx=10, pady=10)



