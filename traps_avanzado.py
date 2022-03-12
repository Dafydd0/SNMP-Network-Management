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


def interfaz_traps_avanzado(ip_pablo, comunidad_pablo, correo_pablo):   

    global ip, community, correo
    ip = ip_pablo
    community = comunidad_pablo
    correo = correo_pablo

    def main():
        try:   
            oid_name = "Null" # Estamos en traps_avanzado, no hay oid_name, el oid lo escribe el usuario
            valido = valida_campos() # Boolean
            if valido:
                check_var1 = var1.get() # 1 -> Checked / 0 -> Not checked
                check_var2 = var2.get()
                oid_a_monitorizar = entrada0.get()
                veces_a_monitorizar = int(entrada1.get())
                intervalo_monitorizacion = int(entrada2.get())
                if check_var1 == 1:
                    umbral_superior = int(entrada3.get())
                if check_var2 == 1:
                    umbral_inferior = int(entrada4.get())

                if var3.get() == 1:
                    sample_type = 1 # 1 -> Absoluto
                else:
                    sample_type = 2 # 2 -> Incremental
                    
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
                archivo_comunica.write(str(sample_type) + "\n")            

                print("Valores almacenados en comunica.txt")

                archivo_comunica.close()

                # Creamos un subproceso para ejecutar leer.py
                process_monitorizar = subprocess.Popen(['python', 'C:/Users/34618/Desktop/Todo/Codigos/Version_final/leer.py'])

        except:
            messagebox.showerror("Error", "Ha ocurrido un error inesperado")

        return


    def valida_campos():

        valido = False
        valido_umbrales = False
        valido_valor = False
        valido_oid = False

        # Verifica umbrales
        if (entrada1.get() == 0):
            valido_oid = False
        else:
            valido_oid = True
            if((var1.get() == 1) and (var2.get() == 1)): # Definir ambos umbrales
                if((entrada1.get() == "") or (entrada2.get() == "") or (entrada3.get() == "") or (entrada4.get() == "")):
                    valido_umbrales = False
                else:
                    valido_umbrales = True

            elif(var1.get() == 1):    # Definir umbral superior
                if((entrada1.get() == "") or (entrada2.get() == "") or (entrada3.get() == "")):
                    valido_umbrales = False
                else:
                    valido_umbrales = True

            elif(var2.get() == 1):    # Definir umbral inferior
                if((entrada1.get() == "") or (entrada2.get() == "") or (entrada4.get() == "")):
                    valido_umbrales = False
                else:
                    valido_umbrales = True

            else:   # No definir umbrales
                if((entrada1.get() == "") or (entrada2.get() == "")):
                    valido_umbrales = False
                else:
                    valido_umbrales = True


            # Verifica valores
            if((var3.get() == 1) and (var4.get() == 1)): # Definir ambos valore -> ERROR
                valido_valor = False
            elif((var3.get() == 0) and (var4.get() == 0)): # Ninguno definido -> ERROR
                valido_valor = False
            else:
                valido_valor = True

        print("Valido umbrales: " + str(valido_umbrales) + ", Valido valor: " + str(valido_valor))

        if ((valido_umbrales == False) and (valido_valor == False) and (valido_oid == False)):
            messagebox.showerror("Error", "No ha elegido ningún objeto de gestión a monitorizar, error en umbrales, error en sample type")
        
        elif ((valido_umbrales == False) and (valido_valor == False) and (valido_oid == True)):
            messagebox.showerror("Error", "Error en umbrales, error en sample type")
        
        elif ((valido_umbrales == False) and (valido_valor == True) and (valido_oid == False)):
            messagebox.showerror("Error", "No ha elegido ningún objeto de gestión a monitorizar, error en umbrales")
        
        elif ((valido_umbrales == False) and (valido_valor == True) and (valido_oid == True)):
            messagebox.showerror("Error", "Error en umbrales")
        
        elif ((valido_umbrales == True) and (valido_valor == False) and (valido_oid == False)):
            messagebox.showerror("Error", "No ha elegido ningún objeto de gestión a monitorizar, error en sample type")
        
        elif ((valido_umbrales == True) and (valido_valor == False) and (valido_oid == True)):
            messagebox.showerror("Error", "Error en sample type")
        
        elif ((valido_umbrales == True) and (valido_valor == True) and (valido_oid == False)):
            messagebox.showerror("Error", "No ha elegido ningún objeto de gestión a monitorizar")
        
        elif ((valido_umbrales == True) and (valido_valor == True) and (valido_oid == True)):
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
        var3.set(0)
        var4.set(0)
        return

    ################################################
    ################################################
    ################################################
    ################################################
    ################################################
    ################################################

    ventana = Toplevel()
    ventana.title("Interfaz de monitorización avanzada")
    ventana.geometry("600x600")
    ventana.config(bg='white')

    entrada0 = StringVar()
    entrada1 = StringVar()
    entrada2 = StringVar()
    entrada3 = StringVar()
    entrada4 = StringVar()
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()

    # Etiquetas
    # Variable a monitorizar
    etiqueta0 = Label(ventana ,text="Seleccione variable a monitorizar: ",bg='white',font=("Verdana", 15)).place(x=10,y=12)
    campo0 = Entry(ventana, textvariable=entrada0).place(x=420, y=20)

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

    # Sample type
    etiqueta5 = Label(ventana ,text="Seleccione sample type: ",bg='white',font=("Verdana", 15)).place(x=10,y=312)

    # Definir umbrales
    check_superior = Checkbutton(ventana, text="Definir umbral superior",bg='white', variable=var1, onvalue=1, offvalue=0).place(x=300, y=270)
    check_inferior = Checkbutton(ventana, text="Definir umbral inferior",bg='white', variable=var2, onvalue=1, offvalue=0).place(x=150, y=270)
    check_absoluto = Checkbutton(ventana, text="Valor absoluto",bg='white', variable=var3, onvalue=1, offvalue=0).place(x=150, y=362)
    check_incremento = Checkbutton(ventana, text="Valor incremental",bg='white', variable=var4, onvalue=1, offvalue=0).place(x=300, y=362)

    separator = Separator(ventana, orient='horizontal')
    separator.pack(fill='x')


    boton_start = Button(ventana, command=main, bg='SkyBlue2', text="Empezar").place(x=150,y=500, width=100)
    boton_limpiar = Button(ventana, command=limpiar, bg='SkyBlue2', text="Limpiar").place(x=350,y=500, width=100)


    def exit():
        ventana.destroy()

    boton_exit = Button(ventana, bg='firebrick3', fg='white', command=exit, text="Salir")
    boton_exit.pack(side=BOTTOM, ipadx=100, padx=10, pady=10)
    separator = Separator(ventana, orient='horizontal')
    separator.pack(fill='x', side=BOTTOM)



    ventana.mainloop()

#interfaz_traps_avanzado("127.0.0.1", "TrabajoGestion", "gestiontrabajo10@gmail.com")