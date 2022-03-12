# Imports para hilos y libreria SNMP
#from io import StringIO
#from pysnmp import hlapi
#from quicksnmp import get
#import threading, time, smtplib, os

# Imports para la interfaz
#import tkinter as tk
from tkinter import *
from tkinter import ttk
#from pysnmp import hlapi
from tkinter import messagebox
from tkinter.ttk import Separator
from traps_avanzado import interfaz_traps_avanzado
import sys

# Imports para mandar correo con log.txt
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

# Imports para plotear los valores monitorizdos
import matplotlib.pyplot as plt
import csv

import subprocess

# Control = True  -> Sigue
# Control = False -> Para
control = True
mandar_correo = False

ip = ""
community = ""
correo = ""


def interfaz_traps_Interface(ip_pablo, comunidad_pablo, correo_pablo):   
 
    global ip, community, correo
    ip = ip_pablo
    community = comunidad_pablo
    correo = correo_pablo

    def main():
        try:    
            valido = valida_campos() # Boolean
            if valido:
                check_var1 = var1.get() # 1 -> Checked / 0 -> Not checked
                check_var2 = var2.get()
                oid_name = lista_desplegable.get()

                # Asocia el oid con el nombre del objeto de gestión
                for i in range(0,len(opciones)):
                    if (oid_name == opciones[i]):
                        print("i: " + str(i))
                        oid_a_monitorizar = lista_oids[i]

                veces_a_monitorizar = int(entrada1.get())
                intervalo_monitorizacion = int(entrada2.get())
                if check_var1 == 1:
                    umbral_superior = int(entrada3.get())
                if check_var2 == 1:
                    umbral_inferior = int(entrada4.get())

                print("ip: " + str(ip) + " correo: "+str(correo)+" community: "+str(community))

                archivo_comunica = open("comunica.txt", "w")  # Archivo para pasarle los parametros al programa que monitorizará

                # Pasamos los valores al fichero
                archivo_comunica.write(str(check_var1) + "\n")
                archivo_comunica.write(str(check_var2) + "\n")
                archivo_comunica.write(str(oid_a_monitorizar) + "\n")
                archivo_comunica.write(str(veces_a_monitorizar) + "\n")
                archivo_comunica.write(str(intervalo_monitorizacion) + "\n")
                archivo_comunica.write(str(ip) + "\n")
                archivo_comunica.write(str(community) + "\n")
                if(check_var1 == 1):
                    archivo_comunica.write(str(umbral_superior) + "\n")
                else:
                    archivo_comunica.write(str(0) + "\n")
                if(check_var2 == 1):
                    archivo_comunica.write(str(umbral_inferior) + "\n")
                else:
                    archivo_comunica.write(str(0) + "\n")
                archivo_comunica.write(str(valido) + "\n")
                archivo_comunica.write(str(oid_name) + "\n")
                archivo_comunica.write(str(correo) + "\n")
                
                print("Valores almacenados en comunica.txt")

                archivo_comunica.close()

                # Creamos un subproceso para ejecutar leer.py
                process_monitorizar = subprocess.Popen(['python', 'C:/Users/34618/Desktop/Todo/Codigos/Version_final/leer_Interface.py'])

        except:
            messagebox.showerror("Error", "Ha ocurrido un error inesperado")

            return


    def valida_campos():
        valido = False
        if((var1.get() == 1) and (var2.get() == 1)): # Definir ambos umbrales
            if((lista_desplegable.get() == "") or (entrada1.get() == "") or (entrada2.get() == "") or (entrada3.get() == "") or (entrada4.get() == "")):
                messagebox.showerror("Campo incorrecto", "Algún campo es incorrecto")
                valido = False
            else:
                valido = True

        elif(var1.get() == 1):    # Definir umbral superior
            if((lista_desplegable.get() == "") or (entrada1.get() == "") or (entrada2.get() == "") or (entrada3.get() == "")):
                messagebox.showerror("Campo incorrecto", "Algún campo es incorrecto")
                valido = False
            else:
                valido = True

        elif(var2.get() == 1):    # Definir umbral inferior
            if((lista_desplegable.get() == "") or (entrada1.get() == "") or (entrada2.get() == "") or (entrada4.get() == "")):
                messagebox.showerror("Campo incorrecto", "Algún campo es incorrecto")
                valido = False
            else:
                valido = True

        else:   # No definir umbrales
            if((lista_desplegable.get() == "") or (entrada1.get() == "") or (entrada2.get() == "")):
                print("Algún campo no es válido")
                messagebox.showerror("Campo incorrecto", "Algún campo es incorrecto")
                valido = False
            else:
                valido = True

        return valido
        

    def limpiar():
        entrada0.set("")
        entrada1.set("")
        entrada2.set("")
        entrada3.set("")
        entrada4.set("")
        var1.set(0)
        var2.set(0)
        return


    ################################################
    ################################################
    ################################################
    ################################################
    ################################################
    ################################################

    ventana = Toplevel()
    ventana.title("Interfaz de monitorización del grupo Interface")
    ventana.geometry("600x600")
    ventana.config(bg='white')

    entrada0 = StringVar()
    entrada1 = StringVar()
    entrada2 = StringVar()
    entrada3 = StringVar()
    entrada4 = StringVar()
    var1 = IntVar()
    var2 = IntVar()


    lista_desplegable = ttk.Combobox(ventana, width=17, state="readonly")
    lista_desplegable.place(x=420, y=20)
    opciones = ["ifSpeed", "ifInOctets", "ifInDiscards", "ifInErrors", "ifInUnknownProtos", "ifOutOctets", "ifOutDiscards", "ifOutErrors"]
    lista_oids = ['1.3.6.1.2.1.2.2.1.5', '1.3.6.1.2.1.2.2.1.10', '1.3.6.1.2.1.2.2.1.13', '1.3.6.1.2.1.2.2.1.14', '1.3.6.1.2.1.2.2.1.15', '1.3.6.1.2.1.2.2.1.16', '1.3.6.1.2.1.2.2.1.19', '1.3.6.1.2.1.2.2.1.20']
    lista_desplegable["values"] = opciones

    # Etiquetas
    # Variable a monitorizar
    etiqueta0 = Label(ventana, text="Seleccione columna a monitorizar: ",bg='white',font=("Verdana", 15)).place(x=0,y=12)


    # Intervalo
    etiqueta1 = Label(ventana ,text="Introduzca veces a monitorizar: ",bg='white',font=("Verdana", 15)).place(x=10,y=62)
    campo1 = Entry(ventana, bg='gray95', textvariable=entrada1).place(x=420, y=70)

    # Tiempo
    etiqueta2 = Label(ventana ,text="Introduzca intervalo de monitorización: ",bg='white',font=("Verdana", 15)).place(x=10,y=112)
    campo2 = Entry(ventana, bg='gray95', textvariable=entrada2).place(x=420, y=120)

    # Umbral superior
    etiqueta3 = Label(ventana ,text="Introduzca umbral superior: ",bg='white',font=("Verdana", 15)).place(x=10,y=162)
    campo3 = Entry(ventana, bg='gray95', textvariable=entrada3).place(x=420, y=170)

    # Umbral inferior
    etiqueta4 = Label(ventana ,text="Introduzca umbral inferior: ",bg='white',font=("Verdana", 15)).place(x=10,y=212)
    campo4 = Entry(ventana, bg='gray95', textvariable=entrada4).place(x=420, y=220)

    # Definir umbrales
    check_superior = Checkbutton(ventana, text="Definir umbral superior",bg='white', variable=var1, onvalue=1, offvalue=0).place(x=300, y=270)
    check_inferior = Checkbutton(ventana, text="Definir umbral inferior",bg='white', variable=var2, onvalue=1, offvalue=0).place(x=150, y=270)

    separator = Separator(ventana, orient='horizontal')
    separator.pack(fill='x')

    boton_start = Button(ventana, command=main, bg='SkyBlue2', text="Empezar").place(x=120,y=500, width=100)
    boton_limpiar = Button(ventana, command=limpiar, bg='SkyBlue2', text="Limpiar").place(x=250,y=500, width=100)

    def avanzado(ip,community,correo):
        interfaz_traps_avanzado(ip,community,correo)
    boton_limpiar = Button(ventana, command=lambda: avanzado(ip, community,correo), bg='SkyBlue2', text="Monitorizar otros objetos").place(x=380, y=500)

    def exit():
        ventana.destroy()
    
    boton_exit = Button(ventana, bg='firebrick3', fg='white', command=exit, text="Salir")
    boton_exit.pack(side=BOTTOM, ipadx=100, padx=10, pady=10)
    separator = Separator(ventana, orient='horizontal')
    separator.pack(fill='x', side=BOTTOM)

    ventana.mainloop()

#interfaz_traps_Interface("127.0.0.1", "TrabajoGestion", "gestiontrabajo10@gmail.com")