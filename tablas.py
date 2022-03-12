from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from tkinter.ttk import Separator

from quicksnmp import construct_object_types, cast
from pysnmp.hlapi import *
from pysnmp import hlapi
class Tablas():
    def __init__(self, ip, community, tabla):
        # Función para validar datos y calcular importe a pagar
        error_dato = False
        total = 0
        try:
            self.ip_u = str(ip)
            tabla = str(tabla)
            self.community_u = str(community)
        except:
            error_dato = True
        if not error_dato:
            if tabla == 't':
                self.gest_tcp()
            if tabla == 'u':
                self.gest_udp()
            if tabla == 'ip1':
                self.gest_ip()
            if tabla == 'h1':
                self.gest_host()
            if tabla == 'ip2':
                self.gest_ip2()
            if tabla == 'if':
                self.gest_if()
            if tabla == "h2":
                self.gest_host2()
        else:
            print("Error en los datos introducidos")

    def gest_tcp(self):
        self.window1 = Toplevel()
        self.window1.geometry('1500x700')
        self.window1.title("Tablas del grupo tcp")
        self.window1.col = ['1.3.6.1.2.1.6.13.1.1', '1.3.6.1.2.1.6.13.1.2', '1.3.6.1.2.1.6.13.1.3',
               '1.3.6.1.2.1.6.13.1.4', '1.3.6.1.2.1.6.13.1.5']
        self.window1.col_nomb = ['TcpConnState', 'TcpConnLocalAddress', 'TcpConnLocalPort', 'TcpConnRemAddress',
                                 'TcpConnRemPort']
        self.window1.col1 = BooleanVar()
        self.window1.col2 = BooleanVar()
        self.window1.col3 = BooleanVar()
        self.window1.col4 = BooleanVar()
        self.window1.col5 = BooleanVar()
        self.window1.etq1 = ttk.Label(self.window1, text="Seleccione las columnas que desea ver:")
        self.window1.state = ttk.Checkbutton(self.window1, text='TcpConnState',
                                      variable=self.window1.col1,
                                      onvalue=True, offvalue=False)
        self.window1.localaddress = ttk.Checkbutton(self.window1, text='TcpConnLocalAddress',
                                      variable=self.window1.col2,
                                      onvalue=True, offvalue=False)
        self.window1.localport = ttk.Checkbutton(self.window1, text='TcpConnLocalPort',
                                      variable=self.window1.col3,
                                      onvalue=True, offvalue=False)
        self.window1.remoteaddress = ttk.Checkbutton(self.window1, text='TcpConnRemAddress',
                                      variable=self.window1.col4,
                                      onvalue=True, offvalue=False)
        self.window1.remoteport = ttk.Checkbutton(self.window1, text='TcpConnRemPort',
                                      variable=self.window1.col5,
                                      onvalue=True, offvalue=False)
        self.window1.separ1 = ttk.Separator(self.window1, orient=HORIZONTAL)

        self.window1.button1 = Button(self.window1, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_tcp)
        self.window1.button2 = Button(self.window1, text="Salir", bg='firebrick3', fg='white',
                              command=self.window1.destroy)
        self.window1.etq1.pack(side=TOP, fill=BOTH, expand=False,
                        padx=10, pady=5)
        self.window1.state.pack(side=TOP, fill=BOTH, expand=False,
                       padx=10, pady=5)
        self.window1.localaddress.pack(side=TOP, fill=BOTH, expand=False,
                       padx=10, pady=5)
        self.window1.localport.pack(side=TOP, fill=BOTH, expand=False,
                       padx=10, pady=5)
        self.window1.remoteaddress.pack(side=TOP, fill=BOTH, expand=False,
                       padx=10, pady=5)
        self.window1.remoteport.pack(side=TOP, fill=BOTH, expand=False,
                       padx=10, pady=5)
        self.window1.separ1.pack(side=TOP, fill=BOTH, expand=True,
                         padx=5, pady=5)
        self.window1.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.window1.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        #self.window1.grab_set()
        #self.raiz.wait_window(self.window1)

        self.window1.mainloop()

    def fun_tcp(self):
        error_dato = False
        if self.window1.col1.get() == False and self.window1.col2.get() == False and self.window1.col3.get() == False and self.window1.col4.get() == False and self.window1.col5.get() == False:
            error_dato = True
        if not error_dato:
            list_col = []
            lista_col_nomb = []
            if (self.window1.col1.get() == True):
                list_col.append(self.window1.col[0])
                lista_col_nomb.append(self.window1.col_nomb[0])
            if (self.window1.col2.get() == True):
                list_col.append(self.window1.col[1])
                lista_col_nomb.append(self.window1.col_nomb[1])
            if (self.window1.col3.get() == True):
                list_col.append(self.window1.col[2])
                lista_col_nomb.append(self.window1.col_nomb[2])
            if (self.window1.col4.get() == True):
                list_col.append(self.window1.col[3])
                lista_col_nomb.append(self.window1.col_nomb[3])
            if (self.window1.col5.get() == True):
                list_col.append(self.window1.col[4])
                lista_col_nomb.append(self.window1.col_nomb[4])
            self.obtenertabla(self.ip_u, list_col,self.community_u, lista_col_nomb)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")

    def gest_udp(self):
        self.window2 = Toplevel()
        self.window2.geometry('1500x700')
        self.window2.title("Tablas del grupo udp")
        self.window2.col = ['1.3.6.1.2.1.7.5.1.1', '1.3.6.1.2.1.7.5.1.2']
        self.window2.col_nomb = ['udpLocalAddress', 'udpLocalPort']
        self.window2.col1 = BooleanVar()
        self.window2.col2 = BooleanVar()
        self.window2.etq1 = ttk.Label(self.window2, text="Seleccione las columnas que desea ver:")
        self.window2.localaddress = ttk.Checkbutton(self.window2, text='udpLocalAddress',
                                             variable=self.window2.col1,
                                             onvalue=True, offvalue=False)
        self.window2.localport = ttk.Checkbutton(self.window2, text='udpLocalPort',
                                                    variable=self.window2.col2,
                                                    onvalue=True, offvalue=False)
        self.window2.separ1 = ttk.Separator(self.window2, orient=HORIZONTAL)

        self.window2.button1 = Button(self.window2, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_udp)
        self.window2.button2 = Button(self.window2, text="Salir", bg='firebrick3', fg='white',
                                      command=self.window2.destroy)
        self.window2.etq1.pack(side=TOP, fill=X, expand=False,
                               padx=10, pady=5)
        self.window2.localaddress.pack(side=TOP, fill=X, expand=False,
                                padx=10, pady=5)
        self.window2.localport.pack(side=TOP, fill=X, expand=False,
                                       padx=10, pady=5)
        self.window2.separ1.pack(side=TOP, fill=BOTH, expand=True,
                                 padx=5, pady=5)
        self.window2.button1.pack(side=LEFT, fill=X, expand=True, padx=10, pady=10)
        self.window2.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        #self.window2.grab_set()
        #self.raiz.wait_window(self.window2)
        self.window2.mainloop()
    def fun_udp(self):
        error_dato = False
        if self.window2.col1.get() == False and self.window2.col2.get() == False:
            error_dato = True
        if not error_dato:
            list_col = []
            lista_col_nomb = []
            if (self.window2.col1.get() == True):
                list_col.append(self.window2.col[0])
                lista_col_nomb.append(self.window2.col_nomb[0])
            if (self.window2.col2.get() == True):
                list_col.append(self.window2.col[1])
                lista_col_nomb.append(self.window2.col_nomb[1])
            self.obtenertabla(self.ip_u, list_col, self.community_u, lista_col_nomb)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")

    def gest_ip(self):
        self.window3 = Toplevel()
        self.window3.geometry('1500x700')
        self.window3.title("Tabla ipAddrTable del grupo ip")

        self.window3.col1 = BooleanVar()
        self.window3.col2 = BooleanVar()
        self.window3.col3 = BooleanVar()
        self.window3.col4 = BooleanVar()
        self.window3.col5 = BooleanVar()
        self.window3.col = ['1.3.6.1.2.1.4.20.1.1', '1.3.6.1.2.1.4.20.1.2', '1.3.6.1.2.1.4.20.1.3',
                            '1.3.6.1.2.1.4.20.1.4', '1.3.6.1.2.1.4.20.1.5']
        self.window3.col_nomb = ['ipAdEntAddr', 'ipAdEntIfIndex', 'ipAdEntNetMask', 'ipAdEntBcastAddr',
                                 'ipAdEntReasmMaxSize']
        self.window3.etq1 = ttk.Label(self.window3, text="Seleccione las columnas que desea ver:")
        self.window3.entaddr = ttk.Checkbutton(self.window3, text='ipAdEntAddr',
                                             variable=self.window3.col1,
                                             onvalue=True, offvalue=False)
        self.window3.index = ttk.Checkbutton(self.window3, text='ipAdEntIfIndex',
                                                    variable=self.window3.col2,
                                                    onvalue=True, offvalue=False)
        self.window3.netmask = ttk.Checkbutton(self.window3, text='ipAdEntNetMask',
                                                 variable=self.window3.col3,
                                                 onvalue=True, offvalue=False)
        self.window3.bcastaddr = ttk.Checkbutton(self.window3, text='ipAdEntBcastAddr',
                                                     variable=self.window3.col4,
                                                     onvalue=True, offvalue=False)
        self.window3.reasmmaxsize = ttk.Checkbutton(self.window3, text='ipAdEntReasmMaxSize',
                                                  variable=self.window3.col5,
                                                  onvalue=True, offvalue=False)
        self.window3.separ1 = ttk.Separator(self.window3, orient=HORIZONTAL)

        self.window3.button1 = Button(self.window3, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_ip)
        self.window3.button2 = Button(self.window3, text="Salir", bg='firebrick3', fg='white',
                                      command=self.window3.destroy)
        self.window3.etq1.pack(side=TOP, fill=BOTH, expand=False,
                               padx=10, pady=5)
        self.window3.entaddr.pack(side=TOP, fill=BOTH, expand=False,
                                padx=10, pady=5)
        self.window3.index.pack(side=TOP, fill=BOTH, expand=False,
                                       padx=10, pady=5)
        self.window3.netmask.pack(side=TOP, fill=BOTH, expand=False,
                                    padx=10, pady=5)
        self.window3.bcastaddr.pack(side=TOP, fill=BOTH, expand=False,
                                        padx=10, pady=5)
        self.window3.reasmmaxsize.pack(side=TOP, fill=BOTH, expand=False,
                                     padx=10, pady=5)

        self.window3.separ1.pack(side=TOP, fill=BOTH, expand=True,
                                 padx=5, pady=5)
        self.window3.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.window3.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        #self.window3.grab_set()
        #self.raiz.wait_window(self.window3)
        self.window3.mainloop()

    def fun_ip(self):
        error_dato = False
        if self.window3.col1.get() == False and self.window3.col2.get() == False and self.window3.col3.get() == False and self.window3.col4.get() == False and self.window3.col5.get() == False:
            error_dato = True
        if not error_dato:
            list_col = []
            lista_col_nomb = []
            if (self.window3.col1.get() == True):
                list_col.append(self.window3.col[0])
                lista_col_nomb.append(self.window3.col_nomb[0])
            if (self.window3.col2.get() == True):
                list_col.append(self.window3.col[1])
                lista_col_nomb.append(self.window3.col_nomb[1])
            if (self.window3.col3.get() == True):
                list_col.append(self.window3.col[2])
                lista_col_nomb.append(self.window3.col_nomb[2])
            if (self.window3.col4.get() == True):
                list_col.append(self.window3.col[3])
                lista_col_nomb.append(self.window3.col_nomb[3])
            if (self.window3.col5.get() == True):
                list_col.append(self.window3.col[4])
                lista_col_nomb.append(self.window3.col_nomb[4])
            self.obtenertabla(self.ip_u, list_col, self.community_u, lista_col_nomb)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")

    def gest_if(self):
        self.window4 = Toplevel()
        self.window4.geometry('1500x700')
        self.window4.title("Tablas del grupo interfaces")
        self.window4.col = ['1.3.6.1.2.1.2.2.1.1', '1.3.6.1.2.1.2.2.1.2', '1.3.6.1.2.1.2.2.1.3',
                            '1.3.6.1.2.1.2.2.1.4', '1.3.6.1.2.1.2.2.1.5', '1.3.6.1.2.1.2.2.1.6',
                            '1.3.6.1.2.1.2.2.1.7', '1.3.6.1.2.1.2.2.1.8', '1.3.6.1.2.1.2.2.1.9',
                            '1.3.6.1.2.1.2.2.1.10', '1.3.6.1.2.1.2.2.1.11', '1.3.6.1.2.1.2.2.1.12',
                            '1.3.6.1.2.1.2.2.1.13', '1.3.6.1.2.1.2.2.1.14', '1.3.6.1.2.1.2.2.1.15',
                            '1.3.6.1.2.1.2.2.1.16', '1.3.6.1.2.1.2.2.1.17', '1.3.6.1.2.1.2.2.1.18',
                            '1.3.6.1.2.1.2.2.1.19', '1.3.6.1.2.1.2.2.1.20', '1.3.6.1.2.1.2.2.1.21',
                            '1.3.6.1.2.1.2.2.1.22']
        self.window4.lista = []
        self.window4.agregadas = StringVar()
        self.window4.col1 = BooleanVar()
        self.window4.etq1 = ttk.Label(self.window4, text="Agregue las columnas que desea ver:")
        self.window4.combo = ttk.Combobox(self.window4, state="readonly")
        self.window4.todas = ["ifIndex", "ifDescr", "ifType", "ifMtu", "ifSpeed", "ifPhysAddress",
                                        "ifAdminStatus", "ifOperStatus", "ifLastChange", "ifInOctets",
                                        "ifInUcastPkts", "ifInNUcastPkts", "ifInDiscards", "ifInErrors",
                                        "ifInUnknownProtos", "ifOutOctets", "ifOutUcastPkts", "ifOutNUcastPkts",
                                        "ifOutDiscards", "ifOutErrors", "ifOutQLen", "ifSpecific"]
        self.window4.combo["values"] = ["ifIndex", "ifDescr", "ifType", "ifMtu", "ifSpeed", "ifPhysAddress",
                                        "ifAdminStatus", "ifOperStatus", "ifLastChange", "ifInOctets",
                                        "ifInUcastPkts", "ifInNUcastPkts", "ifInDiscards", "ifInErrors",
                                        "ifInUnknownProtos", "ifOutOctets", "ifOutUcastPkts", "ifOutNUcastPkts",
                                        "ifOutDiscards", "ifOutErrors", "ifOutQLen", "ifSpecific", "Todas"]
        self.window4.button3 = Button(self.window4, text="Agregar columna señalada", bg='SkyBlue2', command=self.agregar)
        self.window4.text_box = ttk.Label(self.window4, textvariable=self.window4.agregadas,
                               foreground="black", background="white",
                               borderwidth=5)
        self.window4.separ1 = ttk.Separator(self.window4, orient=HORIZONTAL)

        self.window4.button1 = Button(self.window4, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_if)
        self.window4.button2 = Button(self.window4, text="Salir", bg='firebrick3', fg='white',
                                      command=self.window4.destroy)
        self.window4.etq1.pack(side=TOP, expand=False,
                               padx=10, pady=5)
        self.window4.combo.pack(side=TOP,expand=False,
                                padx=10, pady=5)
        self.window4.button3.pack(side=TOP, fill=Y, expand=False, padx=10, pady=10)
        self.window4.text_box.pack(side=TOP, expand=False,
                        padx=20, pady=5)
        self.window4.separ1.pack(side=TOP, fill=BOTH, expand=True,
                                 padx=5, pady=5)
        self.window4.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.window4.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        #self.window4.grab_set()
        #self.raiz.wait_window(self.window4)

        self.window4.mainloop()


    def agregar(self):
        new_element = self.window4.combo.get()
        if new_element == "Todas":
            self.window4.lista = self.window4.todas
        else:
            if ((new_element in self.window4.lista) == False):
                self.window4.lista.append(new_element)
        cadena = "["
        for i in self.window4.lista:
            cadena += i
            if i != self.window4.lista[len(self.window4.lista)-1]:
                cadena += ', '

        cadena += "]"
        self.window4.agregadas.set(cadena)
    def fun_if(self):
        error_dato = False
        if len(self.window4.lista) == 0:
            error_dato = True
        if not error_dato:
            list_col = []
            ind = 0
            for i in self.window4.lista:
                ind = self.window4.todas.index(i)
                list_col.append(self.window4.col[ind])
            self.obtenertabla(self.ip_u, list_col, self.community_u, self.window4.lista)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")

    def gest_ip2(self):
        self.window5 = Toplevel()
        self.window5.geometry('1500x700')
        self.window5.title("Tabla del grupo ip")
        self.window5.col = ['1.3.6.1.2.1.4.21.1.1', '1.3.6.1.2.1.4.21.1.2', '1.3.6.1.2.1.4.21.1.3', '1.3.6.1.2.1.4.21.1.4',
                            '1.3.6.1.2.1.4.21.1.5', '1.3.6.1.2.1.4.21.1.6', '1.3.6.1.2.1.4.21.1.7', '1.3.6.1.2.1.4.21.1.8',
                            '1.3.6.1.2.1.4.21.1.9', '1.3.6.1.2.1.4.21.1.10', '1.3.6.1.2.1.4.21.1.11', '1.3.6.1.2.1.4.21.1.12',
                            '1.3.6.1.2.1.4.21.1.13']
        self.window5.lista = []
        self.window5.agregadas = StringVar()
        self.window5.etq1 = ttk.Label(self.window5, text="Agregue las columnas que desea ver:")
        self.window5.combo = ttk.Combobox(self.window5, state="readonly")
        self.window5.todas = ["ipRouteDest", "ipRouteIfIndex", "ipRouteMetric1", "ipRouteMetric2",
                              "	ipRouteMetric3", "	ipRouteMetric4", "ipRouteNextHop", "ipRouteType",
                              "ipRouteProto", "	ipRouteAge", "ipRouteMask", "ipRouteMetric5", "ipRouteInfo"]
        self.window5.combo["values"] = ["ipRouteDest", "ipRouteIfIndex", "ipRouteMetric1", "ipRouteMetric2",
                              "	ipRouteMetric3", "	ipRouteMetric4", "ipRouteNextHop", "ipRouteType",
                              "ipRouteProto", "	ipRouteAge", "ipRouteMask", "ipRouteMetric5", "ipRouteInfo", "Todas"]
        self.window5.button3 = Button(self.window5, text="Agregar columna señalada", bg='SkyBlue2',
                                      command=self.agregar2)
        self.window5.text_box = ttk.Label(self.window5, textvariable=self.window5.agregadas,
                                          foreground="black", background="white",
                                          borderwidth=5, anchor="e")
        self.window5.separ1 = ttk.Separator(self.window5, orient=HORIZONTAL)

        self.window5.button1 = Button(self.window5, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_ip2)
        self.window5.button2 = Button(self.window5, text="Salir", bg='firebrick3', fg='white',
                                      command=self.window5.destroy)
        self.window5.etq1.pack(side=TOP, expand=False,
                               padx=10, pady=5)
        self.window5.combo.pack(side=TOP, expand=False,
                                padx=10, pady=5)
        self.window5.button3.pack(side=TOP, fill=Y, expand=False, padx=10, pady=10)
        self.window5.text_box.pack(side=TOP, expand=False,
                                   padx=20, pady=5)
        self.window5.separ1.pack(side=TOP, fill=BOTH, expand=True,
                                 padx=5, pady=5)
        self.window5.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.window5.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        #self.window5.grab_set()
        #self.raiz.wait_window(self.window5)
        self.window5.mainloop()
    def agregar2(self):
        new_element = self.window5.combo.get()
        if new_element == "Todas":
            self.window5.lista = self.window5.todas
        else:
            if ((new_element in self.window5.lista) == False):
                self.window5.lista.append(new_element)
        cadena = "["
        for i in self.window5.lista:
            cadena += i
            if i != self.window5.lista[len(self.window5.lista)-1]:
                cadena += ', '

        cadena += "]"
        self.window5.agregadas.set(cadena)

    def fun_ip2(self):
        error_dato = False
        if len(self.window5.lista) == 0:
            error_dato = True
        if not error_dato:
            list_col = []
            ind = 0
            for i in self.window5.lista:
                ind = self.window5.todas.index(i)
                list_col.append(self.window5.col[ind])

            self.obtenertabla(self.ip_u, list_col, self.community_u, self.window5.lista)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")
    def gest_host(self):
        self.window6 = Toplevel()
        self.window6.geometry('1500x700')
        self.window6.title("Tabla del grupo host")
        self.window6.col = ['1.3.6.1.2.1.25.4.2.1.1', '1.3.6.1.2.1.25.4.2.1.2', '1.3.6.1.2.1.25.4.2.1.3', '1.3.6.1.2.1.25.4.2.1.4',
                            '1.3.6.1.2.1.25.4.2.1.5', '1.3.6.1.2.1.25.4.2.1.6', '1.3.6.1.2.1.25.4.2.1.7', '1.3.6.1.2.1.25.4.2.1.100']
        self.window6.lista = []
        self.window6.agregadas = StringVar()
        self.window6.etq1 = ttk.Label(self.window6, text="Agregue las columnas que desea ver:")
        self.window6.combo = ttk.Combobox(self.window6, state="readonly")
        self.window6.todas = ["hrSWRunIndex", "hrSWRunName", "hrSWRunID", "hrSWRunPath", "hrSWRunParameters", "hrSWRunType",
                                        "hrSWRunStatus", "hrSWRunPriority"]
        self.window6.combo["values"] = ["hrSWRunIndex", "hrSWRunName", "hrSWRunID", "hrSWRunPath", "hrSWRunParameters", "hrSWRunType",
                                        "hrSWRunStatus", "hrSWRunPriority", "Todas"]
        self.window6.button3 = Button(self.window6, text="Agregar columna señalada", bg='SkyBlue2',
                                      command=self.agregar1)
        self.window6.text_box = ttk.Label(self.window6, textvariable=self.window6.agregadas,
                                          foreground="black", background="white",
                                          borderwidth=5, anchor="e")
        self.window6.separ1 = ttk.Separator(self.window6, orient=HORIZONTAL)

        self.window6.button1 = Button(self.window6, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_host)
        self.window6.button2 = Button(self.window6, text="Salir", bg='firebrick3', fg='white',
                                      command=self.window6.destroy)
        self.window6.etq1.pack(side=TOP, expand=False,
                               padx=10, pady=5)
        self.window6.combo.pack(side=TOP, expand=False,
                                padx=10, pady=5)
        self.window6.button3.pack(side=TOP, fill=Y, expand=False, padx=10, pady=10)
        self.window6.text_box.pack(side=TOP, expand=False,
                                   padx=20, pady=5)
        self.window6.separ1.pack(side=TOP, fill=BOTH, expand=True,
                                 padx=5, pady=5)
        self.window6.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.window6.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        #self.window6.grab_set()
        #self.raiz.wait_window(self.window6)
        self.window6.mainloop()
    def agregar1(self):
        new_element = self.window6.combo.get()
        if new_element == "Todas":
            self.window6.lista = self.window6.todas
        else:
            if ((new_element in self.window6.lista) == False):
                self.window6.lista.append(new_element)
        cadena = "["
        for i in self.window6.lista:
            cadena += i
            if i != self.window6.lista[len(self.window6.lista)-1]:
                cadena += ', '

        cadena += "]"
        self.window6.agregadas.set(cadena)

    def fun_host(self):
        error_dato = False
        if len(self.window6.lista) == 0:
            error_dato = True
        if not error_dato:
            list_col = []
            ind = 0
            for i in self.window6.lista:
                ind = self.window6.todas.index(i)
                list_col.append(self.window6.col[ind])

            self.obtenertabla(self.ip_u, list_col, self.community_u, self.window6.lista)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")

    def gest_host2(self):
        self.window7 = Toplevel()
        self.window7.geometry('1500x700')
        self.window7.title("Tablas del grupo host")
        self.window7.col = ['1.3.6.1.2.1.25.3.2.1.1', '1.3.6.1.2.1.25.3.2.1.2', '1.3.6.1.2.1.25.3.2.1.3',
                            '1.3.6.1.2.1.25.3.2.1.4', '1.3.6.1.2.1.25.3.2.1.5', '1.3.6.1.2.1.25.3.2.1.6']
        self.window7.lista = []
        self.window7.agregadas = StringVar()
        self.window7.col1 = BooleanVar()
        self.window7.etq1 = ttk.Label(self.window7, text="Agregue las columnas que desea ver:")
        self.window7.combo = ttk.Combobox(self.window7, state="readonly")
        self.window7.todas = ["hrDeviceIndex", "hrDeviceType", "hrDeviceDescr", "hrDeviceID", "hrDeviceStatus", "hrDeviceErrors"]

        self.window7.combo["values"] = ["hrDeviceIndex", "hrDeviceType", "hrDeviceDescr", "hrDeviceID", "hrDeviceStatus", "hrDeviceErrors", "Todas"]
        self.window7.button3 = Button(self.window7, text="Agregar columna señalada", bg='SkyBlue2', command=self.agregar3)
        self.window7.text_box = ttk.Label(self.window7, textvariable=self.window7.agregadas,
                               foreground="black", background="white",
                               borderwidth=5)
        self.window7.separ1 = ttk.Separator(self.window7, orient=HORIZONTAL)

        self.window7.button1 = Button(self.window7, text="Mostrar tabla", bg='snow4', fg='white', command=self.fun_host2)
        self.window7.button2 = Button(self.window7, text="Salir", bg='firebrick3', fg='white',
                                      command=self.window7.destroy)
        self.window7.etq1.pack(side=TOP, expand=False,
                               padx=10, pady=5)
        self.window7.combo.pack(side=TOP,expand=False,
                                padx=10, pady=5)
        self.window7.button3.pack(side=TOP, fill=Y, expand=False, padx=10, pady=10)
        self.window7.text_box.pack(side=TOP, expand=False,
                        padx=20, pady=5)
        self.window7.separ1.pack(side=TOP, fill=BOTH, expand=True,
                                 padx=5, pady=5)
        self.window7.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.window7.button2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        #self.window7.grab_set()
        #self.raiz.wait_window(self.window7)
        self.window7.mainloop()
    def agregar3(self):
        new_element = self.window7.combo.get()
        self.window7.lista.append(new_element)
        if new_element == "Todas":
            self.window7.lista = self.window7.todas
        cadena = "["
        for i in self.window7.lista:
            cadena += i
            if i != self.window7.lista[len(self.window7.lista) - 1]:
                cadena += ', '

        cadena += "]"
        self.window7.agregadas.set(cadena)
        print(cadena)

    def fun_host2(self):
        error_dato = False
        if len(self.window7.lista) == 0:
            error_dato = True
        if not error_dato:
            list_col = []
            ind = 0
            for i in self.window7.lista:
                ind = self.window7.todas.index(i)
                list_col.append(self.window7.col[ind])
            self.obtenertabla(self.ip_u, list_col, self.community_u, self.window7.lista)
        else:
            print("Error en los datos introducidos o no seleccionada ninguna columna")

    def obtenertabla(self, ip, columnas, community, col_nomb):

        iterator = nextCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((ip, 161)),
            ContextData(),
            *construct_object_types(columnas),
            lexicographicMode=False)
        list_oid = []
        list_value = []
        for errorIndication, errorStatus, errorIndex, varBinds in iterator:

            if errorIndication:
                print(errorIndication)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break

            else:
                if "ifDescr" in col_nomb:
                    i = 0
                    index = col_nomb.index("ifDescr")
                    for varBind in varBinds:
                        if (i == index):
                            list_oid.append(str(varBind[0]))
                            list_value.append(cast(varBind[1]))
                        else:
                            list_oid.append(str(varBind[0]))
                            list_value.append(str(varBind[1].prettyPrint()))
                        if (((i+1) % len(col_nomb)) == 0):
                            i = 0
                        else:
                            i = i + 1
                else:
                    for varBind in varBinds:
                        list_oid.append(str(varBind[0]))
                        list_value.append(str(varBind[1].prettyPrint()))

        list_col = tuple(col_nomb)
        j = 1
        lista1 = []
        lista_filas = []
        for element in list_value:
            lista1.append(element)
            if ((j % len(list_col)) == 0):
                lista_filas.append(tuple(lista1))
                lista1.clear()
            j = j + 1
        tupla_filas = tuple(lista_filas)
        tam = len(tupla_filas)
        self.tablas = Tk()
        self.tablas.geometry('1500x700')
        self.tablas.title("Tabla")
        self.tablas.configure(bg="#E8C8CD")
        self.title = ttk.Label(self.tablas, text="Valores de la tabla seleccionada", background="#ECCCCE", font=("Helvetica", 16))
        self.title.pack(side=TOP, padx=20, pady=20)
        self.buttonset = ttk.Button(self.tablas, command= self.tablas.destroy, text="Salir", width = 30)

        self.buttonset.pack(side=BOTTOM, padx=20, pady=20)



        tree = Table(self.tablas, headers=list_col, height=tam+1)
        tree.pack()

        for row in tupla_filas:
            tree.add_row(row)

        #self.tablas.grab_set()
        #self.raiz.wait_window(self.tablas)
        self.tablas.mainloop()

class Table(ttk.Frame):
    def __init__(self, parent=None, headers=[], height=10, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self._headers = headers
        self._tree = ttk.Treeview(self,
                                  height=height,
                                  columns=self._headers,
                                  show="headings")

        # Agregamos dos scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self._tree.xview)
        hsb.pack(side='bottom', fill='x')

        self._tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        self._tree.pack(side="top")
        for header in self._headers:
            self._tree.heading(header, text=header.title())
            self._tree.column(header, stretch=True,
                              width=tkFont.Font().measure(header.title()))
    def add_row(self, row):
        self._tree.insert('', 'end', values=row)
        for i, item in enumerate(row):
            col_width = tkFont.Font().measure(item)
            if self._tree.column(self._headers[i], width=None) < col_width:
                self._tree.column(self._headers[i], width=col_width)

def tablas(ip, community, table):
    Tablas(ip, community, table)

