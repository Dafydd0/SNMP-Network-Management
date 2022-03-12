# Imports para hilos y libreria SNMP
from io import StringIO
from pysnmp import hlapi
from quicksnmp import get
import threading, time, smtplib, os

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

control = True
mandar_correo = False
correo = ''

def main ():
    global correo

    valor_anterior = 0
    valor_incremental = 0
    valor_incremental_anterior = 0
    suficientes = False # Indica si se puede hacer o no la comparación por incremento

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
    sample_type = datos_leidos[12]

    mandar_correo = False

    try:        
            
        i = 0

        archivo_log = open("log.txt", "w")  # Archivo log de los traps
        archivo_log.write("Registro de traps recibidas")

        archivo_monitorizacion = open("monitorizacion.txt", "w")    # Archivo valores monitorizados
        archivo_monitorizacion.write("Registro de la monitorizacion")

        archivo_plot = open("plot.txt", "w")    # Archivo valores para plotearlos


        while ((i < veces_a_monitorizar) and (control != False)): # Intervalo de monitorizacion

            #Fecha actual
            now = datetime.now()
            segundo_ini = now.second

            archivo_log = open("log.txt", "a")
            archivo_monitorizacion = open("monitorizacion.txt", "a")
            archivo_plot = open("plot.txt", "a")


            resultado_peticion = get(ip, [oid_a_monitorizar], hlapi.CommunityData(community)) #Peticion de variable a monitorizar

            for key, value in resultado_peticion.items(): # Pasamos de diccionario a tupla
                a = (key, value)
            
            oid = a[0]  # Obtenemos valores independientes de la tupla
            if(i != 0):
                valor_anterior = valor
            valor = a[1]
            print("valor anterior: " + str(valor_anterior) + ", valor: " + str(valor))

            if((i != 0) and (i != 1)):
                valor_incremental_anterior = valor_incremental
                suficientes = True

            valor_incremental = valor - valor_anterior

            print("valor incremental anterior: " + str(valor_incremental_anterior) + ", valor incremental: " + str(valor_incremental))



            print("Estamos monitorizando la variable oid: {} ,cada {} segundos, durante {} veces, IP: {}".format(oid_a_monitorizar, intervalo_monitorizacion, veces_a_monitorizar, ip))
            print("Valor de la variable con oid {} : {}".format(oid_a_monitorizar, valor))
        
            if sample_type == 1:
                archivo_monitorizacion.write("\nLa variable cuyo oid es: {}, tiene el valor: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid, valor, now.day, now.month, now.year, now.hour, now.minute, now.second))
                archivo_monitorizacion.close()   

                if((check_var1 == 1) or (check_var2 == 1)): # Si no definimos umbrales no hay que mandar el log
                    if(check_var1 == 1):    # Umbral superior
                        if((type(valor) == int) and (valor > umbral_superior)):
                            mandar_correo = True
                            archivo_log.write("\nLa variable cuyo oid es: {}, ha superado el umbral superior definido en: {}, con un valor de: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid, umbral_superior, valor, now.day, now.month, now.year, now.hour, now.minute, now.second))
                            archivo_log.close()
                            print("log almacenado correctamente")
                    if(check_var2 == 1):    # Umbral inferior
                        if((type(valor) == int) and (valor < umbral_inferior)):
                            mandar_correo = True
                            archivo_log.write("\nLa variable cuyo oid es: {}, ha superado el umbral inferior definido en: {}, con un valor de: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid, umbral_inferior, valor, now.day, now.month, now.year, now.hour, now.minute, now.second))
                            archivo_log.close()
                            print("log almacenado correctamente")
                archivo_plot.write("{},{}\n".format(i*intervalo_monitorizacion, valor))  # Añadimos los valores al fichero paro poder dibujar la gráfica posteriormente
            
            else: # Sample type = 2

                if suficientes:
                    incremento = valor_incremental - valor_incremental_anterior
                    print("incremento: " + str(incremento))
                    archivo_monitorizacion.write("\nLa variable cuyo oid es: {}, ha tenido un incremento de: {}. Fecha actual: {}-{}-{} {}:{}:{}".format(oid, incremento, now.day, now.month, now.year, now.hour, now.minute, now.second))
                    archivo_monitorizacion.close() 
                    
                    if((check_var1 == 1) or (check_var2 == 1)):
                        if(check_var1 == 1):    # Umbral superior
                            if (incremento > umbral_superior):
                                mandar_correo = True
                                archivo_log.write("\nLa variable cuyo oid es: {}, ha superado el umbral incremental superior definido en: {}, con un valor de: {}, ya que se ha elegido un Sample Type incremental. Fecha actual: {}-{}-{} {}:{}:{}".format(oid, umbral_superior, incremento, now.day, now.month, now.year, now.hour, now.minute, now.second))
                                archivo_log.close()
                                print("log almacenado correctamente")
                        if(check_var2 == 1):    # Umbral inferior
                            if (incremento < umbral_inferior):
                                mandar_correo = True
                                archivo_log.write("\nLa variable cuyo oid es: {}, ha superado el umbral incremental inferior definido en: {}, con un valor de: {}, ya que se ha elegido un Sample Type incremental. Fecha actual: {}-{}-{} {}:{}:{}".format(oid, umbral_inferior, incremento, now.day, now.month, now.year, now.hour, now.minute, now.second))
                                archivo_log.close()
                                print("log almacenado correctamente")
                    archivo_plot.write("{},{}\n".format(i*intervalo_monitorizacion, incremento))  # Añadimos los valores al fichero paro poder dibujar la gráfica posteriormente

            
            archivo_plot.close()

            i = i + 1
            time.sleep(intervalo_monitorizacion)    # Fin while
        
        if(mandar_correo):
            thread2 = threading.Thread(target=envia_correo())
            thread2.start() #Se crea un segundo hilo
            messagebox.showinfo("Correo enviado", "Se ha enviado un correo a {}, con el registro de traps recibidas".format(remitente))

        resul = messagebox.askyesno("Monitorización finalizada", "¿Desea representar gráficamente los valores monitorizados?")
        if resul:
            plot()
    except:
        messagebox.showerror("Error", "Ha ocurrido un error inesperado")
    return

remitente = 'gestiontrabajo10@gmail.com'
def envia_correo():
    # Iniciamos los parámetros del script
    
    destinatarios = [correo]
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



def leer_datos():
    fdatos = open("comunica.txt", "r")
    lineas = fdatos.readlines()

    res = [int(lineas[0]), int(lineas[1]), str(lineas[2].strip("\n")), int(lineas[3]), int(lineas[4]), str(lineas[5]).strip("\n"), str(lineas[6]).strip("\n"), int(lineas[7]), int(lineas[8]), str(lineas[9].strip("\n")), str(lineas[10].strip("\n")), str(lineas[11].strip("\n")), int(lineas[12])]

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
    plt.xlabel("Segundos")
    plt.ylabel("Valor")
    plt.title("Gráfica de\nvalores monitorizados")
    plt.legend()
    plt.show()

    return


main()