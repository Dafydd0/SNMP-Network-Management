from tkinter import Tk,Text,Button,END,re
from pysnmp import hlapi
import sys,smtplib

email = input(str("Introduzca correo: "))
password = input(str("Introduzca contraseña: "))

message = "Mensaje de prueba por correo"
subject = "Prueba de correo"

message = "Subject: {}\n\n{}".format(subject, message)

class Interfaz:
    def __init__(self, ventana):
        #Inicializar la ventana con un título
        self.ventana=ventana
        self.ventana.title("Interfaz")

        #Agregar una caja de texto para que sea la pantalla de la calculadora
        self.pantalla=Text(self.ventana, state="disabled", width=100, height=3, background="blue", foreground="white", font=("Helvetica",15))

        #Ubicar la pantalla en la ventana
        self.pantalla.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        #Inicializar la operación mostrada en pantalla como string vacío
        self.operacion=""

        #Crear los botones de la calculadora
        boton1=self.crearBoton("Puertos activos", escribir=False)
        boton2=self.crearBoton("Paquetes recibidos", escribir=False)
        boton3=self.crearBoton("Octetos recibidos", escribir=False)
        boton4=self.crearBoton("Limpiar salida", escribir=False)
        boton5=self.crearBoton("Enviar correo", escribir=False)
        boton6=self.crearBoton("Añadir2", escribir=False)
        boton7=self.crearBoton("Añadir3", escribir=False)
        boton8=self.crearBoton("Añadir4", escribir=False)
        boton9=self.crearBoton("Añadir5", escribir=False)
        boton10=self.crearBoton("Añadir6", escribir=False)
        boton11=self.crearBoton("Añadir7", escribir=False)
        boton12=self.crearBoton("Salir", escribir=False)
        

        #Ubicar los botones con el gestor grid
        botones=[boton1, boton2, boton3, boton4, boton5, boton6, boton7, boton8, boton9, boton10, boton11, boton12]
        contador=0
        for fila in range(1,4):
            for columna in range(4):
                botones[contador].grid(row=fila,column=columna)
                contador+=1
        #Ubicar el último botón al final
        #botones[17].grid(row=5,column=0,columnspan=4)
        
        return


    #Crea un botón mostrando el valor pasado por parámetro
    def crearBoton(self, valor, escribir=True, ancho=25, alto=1):
        return Button(self.ventana, text=valor, width=ancho, height=alto, font=("Helvetica",15), command=lambda:self.click(valor,escribir))

    
    #Controla el evento disparado al hacer click en un botón
    def click(self, texto, escribir):
        #Si el parámetro 'escribir' es True, entonces el parámetro texto debe mostrarse en pantalla. Si es False, no.
        if not escribir:

            if texto == "Salir":    #Salir del programa
                sys.exit()
                
            elif texto == "Puertos activos":
                self.limpiarPantalla()
                self.mostrarEnPantalla(texto)

            elif texto == "Paquetes recibidos":
                self.limpiarPantalla()
                self.mostrarEnPantalla(texto)

            elif texto == "Octetos recibidos":
                self.limpiarPantalla()
                self.mostrarEnPantalla(texto)

            elif texto == "Enviar correo":
                self.limpiarPantalla()
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(email, password)

                print("Login success")

                server.sendmail(email, email, message)

                print("Email enviado a: ", email)

                server.quit()

                self.mostrarEnPantalla("Correo enviado")

            elif texto == "Limpiar salida":
                self.limpiarPantalla()

            else:
                self.limpiarPantalla()
                self.mostrarEnPantalla(texto)
        #Mostrar texto
        else:
            self.operacion+=str(texto)
            self.mostrarEnPantalla(texto)
        return
    

    #Borra el contenido de la pantalla de la calculadora
    def limpiarPantalla(self):
        self.pantalla.configure(state="normal")
        self.pantalla.delete("1.0", END)
        self.pantalla.configure(state="disabled")
        return
    

    #Muestra en la pantalla de la calculadora el contenido de las operaciones y los resultados
    def mostrarEnPantalla(self, valor):
        self.pantalla.configure(state="normal")
        self.pantalla.insert(END, valor)
        self.pantalla.configure(state="disabled")
        return

    #############################################################
    #############################################################
    #############################################################
    #############################################################
    #############################################################
    ##############       Métodos SNMP          ##################
    #############################################################
    #############################################################
    #############################################################
    #############################################################
    #############################################################
    

    def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *construct_object_types(oids)
        )
        return fetch(handler, 1)[0]


    def construct_object_types(list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types

    def fetch(handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
            except StopIteration:
                break
        return result

    def cast(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    def set(target, value_pairs, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.setCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *construct_value_pairs(value_pairs)
        )
        return fetch(handler, 1)[0]


    # Simply converts our input dictionary in a format PySNMP will like
    def construct_value_pairs(list_of_pairs): 
        pairs = []
        for key, value in list_of_pairs.items():
            pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
        return pairs




ventana_principal=Tk()
calculadora=Interfaz(ventana_principal)
ventana_principal.mainloop()