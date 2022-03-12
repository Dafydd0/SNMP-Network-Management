from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
from tkinter import messagebox
from pysnmp import hlapi
from quicksnmp import get
import nmap
import socket
from datetime import datetime
from escalares import objPredeterminados


# Clase Red para guardad la lista de IP's y MAC's
class Red:
    ip = []
    mac = []
    nombre = []
class Correo:
    correo = ''

# FUNCIONES:

# Funion que escanea las direcciones IPv4 y mac de la red
# Parametros:
#   - direccion ip/mascara de la red que queremos escanear
def scan(red, win, combo_ip):
    mac_aux=[]
    ip_aux=[]
    nombre_aux=[]
    pb = Progressbar(win, orient=HORIZONTAL, length=100, mode='determinate')
    pb.pack()
    win.update_idletasks()
    pb['value'] = 0
    nm = nmap.PortScanner()
    nm.scan(hosts=red, arguments='-sn')

    total=len(nm.all_hosts())
    i=1
    for host in nm.all_hosts():
        ip_aux.append(nm[host]['addresses']['ipv4'])
        win.update_idletasks()
        pb['value'] += 100*(i/total)/2
        nombre_aux.append('')

    total = len(ip_aux)
    i = 1
    for i in range(len(ip_aux)):
        win.update_idletasks()
        pb['value'] += 100*(i/total)/2
        ip=ip_aux[i]
        value=''
        try:
            valor = get(ip, ['1.3.6.1.2.1.1.5.0'], hlapi.CommunityData('TrabajoGestion'))
            for key, value in valor.items():
                a = (key, value)
            oid = a[0]
            value = a[1]
        except Exception:
            pass
        if value!='':
            print('equipo con snmp'+value)
            nombre_aux[i]=' (' + value + ')'
        else:
            print('equipo no valido')
            nombre_aux[i]=''

    Red.ip = ip_aux
    Red.mac = mac_aux
    Red.nombre = nombre_aux

    valores = ['Selecione una ip', '']
    for i in range(len(Red.ip)):
        if(Red.nombre[i]!=''):
            valores.append(Red.ip[i] + Red.nombre[i])
    combo_ip['values'] = valores
    combo_ip.current(1)

    if Red.ip:
        messagebox.showinfo('Informacion', 'Escaneo completado')
        win.destroy()
    else:
        messagebox.showerror('Error de escaneo', 'No se ha podido realizar el escaneo, revise que ha introducido una red correcta')

# Funcion que muestra una ventana para indicar que red queremos escanear
# Parametros:
#   - lista desplegable de las ip
def red(combo_ip):
    #ip=[]
    #mac=[]
    red = Tk()
    red.geometry('600x200')
    red.title("Escanear la red")
    red.config(bg='white')
    intro = Label(red, text='Introduzca la red a escanear (formato: ip/red):')
    intro.pack(ipady=10)
    intro.config(bg='white')
    red_entry = Entry(red, width=30, bg='gray95')
    red_entry.pack(pady=5)
    boton = Button(red, text="Escanear", bg='SkyBlue2', command=lambda: scan(red_entry.get(), red, combo_ip))
    boton.pack(pady=5)
    def salir():
        red.destroy()

    boton_salir = Button(red, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(ipadx=100, padx=10, pady=15, side=BOTTOM)
    separator = Separator(red, orient='horizontal')
    separator.pack(fill='x', side=BOTTOM)


# Funcion que muestra una ventana para añadir un usuario al sistema
# Sin parametros
def add_user():
    def write(cadena):
        error=0
        try:
            file = open("contraseñas.txt", "a")
            file.write(cadena+"\n")
        except:
            error = 1
        if error:
            messagebox.showerror('Error de escaneo', 'Ha ocurrido un error al introducir un usuario')
        else:
            messagebox.showinfo('Informacion', 'Usuario añadido correctamente')
            win.destroy()
        file.close()

    win = Tk()
    win.geometry('600x250')
    win.title("Añadir usuario")
    win.config(bg='white')
    intro = Label(win, text='Introduzca los datos del nuevo usuario (formato: usuario->contraseña; correo):')
    intro.pack(ipady=10)
    intro.config(bg='white')
    user_entry = Entry(win, bg='gray95', width=30)
    user_entry.pack(pady=5)

    boton = Button(win, text="Añadir",width=15, bg='SkyBlue2', command=lambda: write(user_entry.get()))
    boton.pack(pady=5)

    def salir():
        win.destroy()

    separator = Separator(win, orient='horizontal')
    separator.pack(fill='x')
    boton_salir = Button(win, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(ipadx=100, padx=10, pady=20)

# Funcion que muestra una ventana para eliminar un usuario al sistema
# Sin parametros
def remove_user():
    def delete(usuario,lista):
        error=0
        try:
            file2 = open("contraseñas.txt", "w")
            for line in lista:
                if line.strip("\n") != usuario.strip("\n"):
                    file2.write(line)
        except:
            error = 1
        if error:
            messagebox.showerror('Error de escaneo', 'Ha ocurrido un error al eliminar el usuario')
        else:
            messagebox.showinfo('Informacion', 'Usuario eliminado correctamente')
            win.destroy()
        file.close()

    file = open("contraseñas.txt", "r")
    lines = file.readlines()
    file.close()
    win = Tk()
    win.geometry('600x250')
    win.title("Eliminar usuario")
    win.config(bg='white')
    intro = Label(win, text='Seleccione el usuario que quiere eliminar')
    intro.pack(ipady=10)
    intro.config(bg='white')
    combo_us = Combobox(win, width=50)
    valores = ['Selecione un usuario', '']
    for i in range(len(lines)):
        valores.append(lines[i])
    combo_us['values'] = valores
    combo_us.current(1)
    combo_us.pack(pady=10)
    boton = Button(win, text="Eliminar usuario", bg='SkyBlue2', command=lambda: delete(combo_us.get(),lines))
    boton.pack(pady=5)

    def salir():
        win.destroy()

    separator = Separator(win, orient='horizontal')
    separator.pack(fill='x')
    boton_salir = Button(win, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(ipadx=100, padx=10, pady=20)

# Funcion que muestra una ventana para gestionar los usuarios del sistema
# Sin parametros
def ges_us():
    win = Tk()
    win.geometry('600x250')
    win.title("Añadir usuario")
    win.config(bg='white')
    intro = Label(win, text='Añadir un usuario',font=("Arial Bold", 15))
    intro.pack(ipady=10)
    intro.config(bg='white')
    boton = Button(win, text="Añadir usuario", bg='SkyBlue2', command=add_user)
    boton.pack(pady=5)
    intro = Label(win, text='Eliminar un usuario',font=("Arial Bold", 15))
    intro.pack(ipady=10)
    intro.config(bg='white')
    boton = Button(win, text="Eliminar usuario", bg='SkyBlue2', command=remove_user)
    boton.pack(pady=5)

    def salir():
        win.destroy()

    separator = Separator(win, orient='horizontal')
    separator.pack(fill='x')

    boton_salir = Button(win, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(ipadx=100, padx=10, pady=15)

# Funcion que muestra la ventana para el menu principal
# Parametros:
#   - correo electronico del administrador, al que se mandarán los logs de los traps
def menu(correo=Correo.correo):
    print(correo)
    Correo.correo = correo
    menu = Tk()
    menu.geometry('1650x800')
    menu.title("Gestor de red local")
    menu.config(bg='white')
    intro = Label(menu, text="Seleccionar una Comunidad ", font=("Arial Bold", 25))
    intro.pack(ipady=30)
    intro.config(bg='white')
    comunidad_entry = Entry(menu, width=30,bg='gray90')
    comunidad_entry.insert(0, "TrabajoGestion")
    comunidad_entry.pack(pady=10)
    intro = Label(menu, text="Seleccionar una IP ", font=("Arial Bold", 25))
    intro.pack(ipady=30)
    intro.config(bg='white')
    boton0 = Button(menu, text="Escanear la red", font=("Arial", 15), command=lambda: red(combo_ip))
    boton0.pack(pady=10, ipadx=27)
    boton0.config(bg='SkyBlue2')
    combo_ip = Combobox(menu, width=30)
    valores = ['Selecione una ip', '']
    for i in range(len(Red.ip)):
        valores.append(Red.ip[i] + Red.nombre[i])

    combo_ip['values'] = valores
    combo_ip.current(1)
    combo_ip.pack(pady=10)
    intro = Label(menu, text="Seleccionar un grupo de objetos", font=("Arial Bold", 25))
    intro.pack(ipady=30)
    intro.config(bg='white')
    boton1 = Button(menu, text="Grupo System", font=("Arial", 15), bg='SkyBlue2', command=lambda: objPredeterminados('system',combo_ip.get(), comunidad_entry.get(), correo))
    boton1.pack(pady=10, ipadx=65)
    boton2 = Button(menu, text="Grupo IP e Interfaces", font=("Arial", 15), bg='SkyBlue2', command=lambda: objPredeterminados('ip e interfaces',combo_ip.get(), comunidad_entry.get(), correo))
    boton2.pack(pady=10, ipadx=32)
    boton3 = Button(menu, text="Grupo ICMP, TCP y UDP", font=("Arial", 15), bg='SkyBlue2', command=lambda: objPredeterminados('icmp, tcp y udp',combo_ip.get(), comunidad_entry.get(), correo))
    boton3.pack(pady=10, ipadx=15)
    boton4 = Button(menu, text="Grupo HostResources", font=("Arial", 15), bg='SkyBlue2', command=lambda: objPredeterminados('host-resources',combo_ip.get(), comunidad_entry.get(), correo))
    boton4.pack(pady=10, ipadx=30)

    def salir():
        menu.destroy()

    separator = Separator(menu, orient='horizontal')
    separator.pack(fill='x')
    frame = Frame(menu)
    frame.pack(side=TOP)
    frame.config(bg='white')

    boton_salir = Button(menu, text="Salir", bg='firebrick3', fg='white', command=salir)
    boton_salir.pack(in_=frame, side=LEFT, ipadx=100, padx=10)
    boton_us = Button(menu, text="Gestionar usuarios del sistema", bg='gainsboro', command=ges_us)
    boton_us.pack(in_=frame, side=LEFT, ipadx=50, padx=10, pady=20)

    menu.mainloop()

sesion = Tk()
sesion.geometry('650x400')
sesion.title("Gestor de red local")

intro = Label(sesion, text="Bienvenido al gestor de red", font=("Arial Bold", 25))
intro.pack()

#Formulario de inicio de sesión
usuario = Label(sesion, text="Inroduzca su usuario", font=("Arial", 14))
usuario.pack(pady=10)
usuario_entry = Entry(sesion,width=30)
usuario_entry.pack(pady=10)
contraseña = Label(sesion, text="Inroduzca su contraseña", font=("Arial", 14))
contraseña.pack(pady=10)
contraseña_entry = Entry(sesion, show="*", width=30)
contraseña_entry.pack(pady=10)
correo = Label(sesion, text="Inroduzca su correo electronico", font=("Arial", 14))
correo.pack(pady=10)
correo_entry = Entry(sesion,width=30)
correo_entry.pack()

def inicio_sesion():
    contraseñas = []
    file_pass = open("contraseñas.txt", "r")
    contraseñas = file_pass.readlines()
    file_pass.close()
    user = usuario_entry.get()
    mail = correo_entry.get()
    input = user + '->' + contraseña_entry.get() + '; ' + mail
    autenticado = 0
    for i in range(len(contraseñas)):
        comp=contraseñas[i].strip("\n")
        if (input == comp):
            sesion.destroy()
            autenticado = 1
            file_us = open("log-usuarios.txt", "a")
            fecha = datetime.now()
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
            file_us.write('Ha iniciado sesion el usuario: ' + user + ', con correo: ' + mail + ' (' + fecha + ') \n')
            file_us.close()


    if (autenticado == 0):
        messagebox.showerror('Error autenticacion', 'Los datos introducidos no son correctos')
    else:
        menu(mail)


boton = Button(sesion, text="Iniciar sesion", bg='gainsboro', command=inicio_sesion)
boton.pack(pady=10)


def salir():
    sesion.destroy()
separator = Separator(sesion, orient='horizontal')
separator.pack(fill='x')
boton_salir = Button(sesion, text="Salir", bg='firebrick3', fg='white', command=salir)
boton_salir.pack(ipadx=100, padx=10, pady=15)
sesion.mainloop()

