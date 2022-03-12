# Imports para hilos y libreria SNMP
from io import StringIO
from pysnmp import hlapi
from quicksnmp import get
import threading, time, smtplib, os
from pysnmp.hlapi import *
from quicksnmp import construct_object_types

# Imports para la interfaz
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pysnmp import hlapi
from tkinter import messagebox
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

from datetime import date
from datetime import datetime

import subprocess


control = True
mandar_correo = False
correo = ''
ip = ''
community = ''
oid_name = ''
oid_a_monitorizar = ''

def main ():
    global correo, ip, community, oid_name, oid_a_monitorizar

    datos_leidos = leer_datos() # Leemos los datos del fichero comunica
    
    check_var1 = datos_leidos[0]
    check_var2 = datos_leidos[1]
    oid_a_monitorizar = datos_leidos[2]
    veces_a_monitorizar = datos_leidos[3]
    intervalo_monitorizacion = datos_leidos[4]
    ip = datos_leidos[5]
    community = datos_leidos[6]
    umbral_superior = datos_leidos[7]
    umbral_inferior = datos_leidos[8]
    valido = datos_leidos[9]
    oid_name = datos_leidos[10]
    correo = datos_leidos[11]

    mandar_correo = False

    print(check_var1, check_var2, oid_a_monitorizar, veces_a_monitorizar, intervalo_monitorizacion, ip, community, umbral_superior, umbral_inferior, oid_name)

    try:        
            
        i = 0
        
        archivo_log = open("log.txt", "w")  # Archivo log de los traps
        archivo_log.write("Registro de traps recibidas")

        archivo_monitorizacion = open("monitorizacion.txt", "w")    # Archivo valores monitorizados
        archivo_monitorizacion.write("Registro de la monitorizacion")


        while ((i < veces_a_monitorizar) and (control != False)): # Intervalo de monitorizacion
            
            #Fecha actual
            now = datetime.now()

            i = i + 1
            archivo_log = open("log.txt", "a")
            archivo_monitorizacion = open("monitorizacion.txt", "a") 
            
            resultado_peticion = monitorizar_columna()

            archivo_monitorizacion.write("\nEn el objeto de gestion: {}, se han obtenido los siguientes valores: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid_name, resultado_peticion, now.day, now.month, now.year, now.hour, now.minute, now.second))
            archivo_monitorizacion.close() 
        
            if((check_var1 == 1) or (check_var2 == 1)): # Si no definimos umbrales no hay que mandar el log
                if(check_var1 == 1):    # Umbral superior
                    for x in range(0, len(resultado_peticion)):
                        valor = int(resultado_peticion[x])
                        if valor > umbral_superior:
                            mandar_correo = True
                            archivo_log.write("\nEl objeto de gestion: {}, ha superado el umbral superior definido en: {}, con un valor de: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid_name, umbral_superior, valor, now.day, now.month, now.year, now.hour, now.minute, now.second))
                if(check_var2 == 1):    # Umbral inferior
                    for x in range(0, len(resultado_peticion)):
                        valor = int(resultado_peticion[x])
                        if valor < umbral_inferior:
                            mandar_correo = True
                            archivo_log.write("\nEl objeto de gestion: {}, ha superado el umbral inferior definido en: {}, con un valor de: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid_name, umbral_inferior, valor, now.day, now.month, now.year, now.hour, now.minute, now.second))
                archivo_log.close()
            print("log almacenado correctamente")
            print("i: " + str(i))
            time.sleep(intervalo_monitorizacion)    # Fin while
        
        if(mandar_correo):
            thread2 = threading.Thread(target=envia_correo())
            thread2.start() #Se crea un segundo hilo
            messagebox.showinfo("Correo enviado", "Se ha enviado un correo a {}, con el registro de traps recibidas".format(remitente))

        messagebox.showinfo("Monitorización finalizada", "La monitorización ha finalizado, revise el archivo monitorizacion.txt")

    except:
        messagebox.showerror("Error", "Ha ocurrido un error inesperado")
    return

remitente = 'gestiontrabajo10@gmail.com'
def envia_correo():
    # Iniciamos los parámetros del script
    
    destinatarios = ['gestiontrabajo10@gmail.com']
    contraseña = 'trabajogestion'
    asunto = 'Log de traps'
    cuerpo = 'Fichero con el registro de traps recibidas'
    ruta_adjunto = 'log.txt'
    nombre_adjunto = 'log.txt'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login(remitente, contraseña)

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    print("Correo con 'log.txt' enviado correctamente")

    # Cerramos la conexión
    sesion_smtp.quit()

def monitorizar_columna():
    global oid_a_monitorizar
    oid_list = [oid_a_monitorizar]

    iterator = nextCmd(SnmpEngine(),CommunityData(community),UdpTransportTarget((ip, 161)),ContextData(),*construct_object_types(oid_list),lexicographicMode=False)
    list_oid = []
    list_value = []
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:

        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break

        else:
        
            for varBind in varBinds:

                list_oid.append(str(varBind[0]))
                list_value.append(str(varBind[1].prettyPrint()))

    print("lista de values: " + str(list_value))

    return list_value

def leer_datos():
    fdatos = open("comunica.txt", "r")
    lineas = fdatos.readlines()

    res = [int(lineas[0]), int(lineas[1]), str(lineas[2].strip("\n")), int(lineas[3]), int(lineas[4]), str(lineas[5]).strip("\n"), str(lineas[6]).strip("\n"), int(lineas[7]), int(lineas[8]), str(lineas[9].strip("\n")), str(lineas[10].strip("\n")), str(lineas[11].strip("\n"))]

    return res

def plot():
    x = []
    y = []

    with open("plot.txt","r") as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(int(row[0]))
            y.append(int(row[1]))

    plt.plot(x,y)
    plt.xlabel("Iteraciones")
    plt.ylabel("Valor")
    plt.title("Gráfica de\nvalores monitorizados")
    plt.legend()
    plt.show()

    return


main()