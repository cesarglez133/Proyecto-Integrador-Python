
#Se importan librerias de trabajo
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox
#Para las interfaces de registro e inicio Sesion
from Validaciones import *
from FuncionesBD import *

from Usuario import *
from Tiempo import *

#Se crea clase principal (tk.Tk), la cual es la encargada de manejar los Frames
class APP(tk.Tk):
    #OJO: Notar que pasamos "*args" y "**kwargs", porque podrian ser necesarios (recordar pasarlos a inicializacion de tk.Tk)
    def __init__(self,*args,**kwargs):
        #Se inicializa ademas, con la herencia de tk.Tk, para tener todas estas disponibilidades en "self"
        super().__init__(*args,**kwargs)

        #Se agrega fondo a ventana principal (la que va a contener el contenedor y a su vez, los frames)
        self.configure(bg = "black")

        #Cambiar "font" por defecto a todo (ojo con forma de importar libreria arriba)
        font.nametofont("TkDefaultFont").configure(size = 12, underline = True)

        #Se aprovecha que "self" ya es la ventana principal y se agrega titulo respectivo
        self.title("Bets Play Simulator")
        
        #un atributo sera un objeto tipo usuario para poder persistir la sesion entre las interfaces
        #self.usuarioActivo = Usuario("5","micorreo@gmail.com","abcd1234","Chiapaneco69","Bet 365","5000")
        self.usuarioActivo = Usuario()
        
        #Se busca que Ventana se mantenga central y correcta independiente del tamanno y expansiones realizadas:
        self.columnconfigure( 0, weight = 1 )
        self.rowconfigure(0, weight = 1)


        #OJO: Se crea el "CONTENEDOR PRINCIPAL", el cual es un Frame en donde se llamaran a los otros Frames de las otras clases...
        #...esto nos permitira tener el efecto de multiples ventanas segun la que se necesita (osea el frame respectivo)
        contenedor_principal = tk.Frame( self ,bg = "gray")
        contenedor_principal.grid( padx = 5, pady = 5 , sticky = "nsew")

        #IMPORTANTISIMO (CREACION DE DICCIONARIO CON FRAMES A UTILIZAR EN APP --> TODAS LAS FRAMES QUE SE TENGAN):
        #Recordar que este diccionario, almacena los frames y juega un papel esencial en indicar cual de todos mostrar.
        #Ademas, se vuelve util con metodo especial para acceder a otros frames (ver mas abajo)
        self.todos_los_frames = dict()

        #PARTE INDISPENSABLE DE TRABAJO CON MULTIPAGINAS (MULTIPLES FRAMES):
        #Se debe crear cada una de las clases de los frames (TODAS), de tal forma que se agregen al diccionario de estas...
        #...esto es fundamental, porque asi identificaremos a cual frame ir, segun algo interactivo para el usuario
        #OJO: se pasan TODAS las clases asociadas a las paginas con las que trabajaremos, y se agregan correctamente...
        #RECORDERIS: Se recorre tupla, de todas las clases (forma de ahorrar lineas de codigo)
        for F in (InicioS, Registro,Individuales,Historial):
            #Se ejecuta la labor de llamar a todas las clases asociadas a Frames_N (una a una)
            #NOTA: ver que se almacenan momentaneamente en frame, para simplificar labor
            #OJO: NECESARIO: Parametro "self", como encargado de ser el "controller", la razon es porque...
            #... desde TODAS las otras clases (Frames), se debe poder acceder a metododo "show_frame", y si...
            #...NO se pasa esta, implica que NO habra acceso a los metodos de la APP principal. Por esto se pasa self.
            frame = F( contenedor_principal , self)
            #Se agrega a diccionario de todos los frames la llave y su respectivo correspondiente:
            #LLAVE = "F"    ---> Cada llave es cada clase de Frame_1, Frame_2, etc...
            #OBJETO = frame, que es :"F(contenedor_principal)"   ---> Cada objeto es Frame_1(contenedor_principal), etc...
            self.todos_los_frames[F] = frame
            #Ahora, se agrega correctamente cada una de las Frames recorridas en la tupla de frames
            #NOTA: FUNDAMENTAL crear frames con sticky = "nsew", para que no aparezcan cosas de otros frames indeseadas
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        #OJO: luego se debe llamar al metodo "show_frame", creado por nosotros, para mostrar un frame deseado...
        #...en esencia, permite traer al primer plano, un frame del vector "self.todos+los_frames"
        self.show_frame( InicioS )


    #METODO PARA MOSTRAR UNICAMENTE FRAME DESEADO (controller = Clase que queremos obtener de diccionario de frames)
    def show_frame(self,contenedor_llamado):
        #Se selecciona el frame requerido por el controller, desde el diccionario de frames ya creado anteriormente
        #Recordemos que el controller, es simplemente el valor por defecto de la clase asociada a cada Frame...
        #...estos keys se crearon arriba al recorrer tupla de los frames de la app
        frame = self.todos_los_frames[contenedor_llamado]

        #llamamos al metodo que setea la informacion de sesion en esta interfaz
        if(frame.titulo == "Apuestas"):
            frame.setInfoSesion()
        #llamamos al metodo que setea la informacion de sesion en esta interfaz
        if(frame.titulo == "Historial"):
            frame.setInfoUltimaApuesta()
        
        self.title(frame.titulo)
        
        #Ahora se llama a funcion de tkinter heredada desde clase APP, la cual permite traer frame indicada a primer plano
        frame.tkraise()
    def setInfoUsuarioActivo(self,Usuario):
        for Dato in Usuario:
            self.usuarioActivo.set_IDusuario(Dato[0])
            self.usuarioActivo.set_correo(Dato[1])
            self.usuarioActivo.set_password(Dato[2])
            self.usuarioActivo.set_nickname(Dato[3])
            self.usuarioActivo.set_nombreCasa(Dato[4])
            self.usuarioActivo.set_dineroInicial(Dato[5])
#Interfaz inicio de sesion

#OJO( CREACION DE FRAMES):
#Se crean como clases con herencia de tk.Frame (para acceder inmediatamente a las clases Frames respectivas)
#NOTA: Si bien creamos Frames, recordemos que hace falta "llamarlos", de lo contrario, no se crea ni se hacen efectivos
class InicioS(tk.Frame):
    #Se inicializan, recibiendo de parametro self, parent y controller.
    #self es para manejo de clase interna
    #container es para indicar el frame o root, en donde se ubicara el frame (en este caso en APP principal)
    #controller es indicador interno para manejo correcto de cambio de frames 
    # (es decir, podra acceder a app principal y a sus metodos, de tal forma que se permita cambio)
    #Recordemos que este container sera entonces un parametro que debemos incluir, al llamar a clase.
    #Se pueden incluir los *args y **kwargs, como parametros extra disponibles
    def __init__(self, container, controller,*args, **kwargs):
        #Para inicializar Frame y que se entienda la clase como un Frame, tambien se inicializa desde la herencia:
        #NOTA: NO olvidar pasar el parametro tambien, de lo contrario, no se comprende donde localizar el Frame creado
        #Luego de hacer esto, recordar que "self" es equivalente a decir el Frame_1, que es en donde agregaremos widgets
        super().__init__(container, *args, **kwargs)
        self.configure(bg = "black")
        #guardamos como atributo el controlador
        self.controller = controller 
        self.titulo = "Inicio sesion"
        # Crear etiqueta "Bienvenido a BetsPlay Simulator"
        self.etiqueta_bienvenida = tk.Label(self, text="Bienvenido a BetsPlay Simulator", font=("Arial", 24), fg="white", bg="black")
        self.etiqueta_bienvenida.grid(row=0, column=0, pady=40, padx=200)

        # Crear cuadro de entrada de correo electrónico
        self.cuadro_correo = tk.Entry(self, font=("Arial", 12), width=30)
        self.cuadro_correo.grid(row=1, column=0, padx=250)
         
       # Crear etiqueta "Correo"
        self.etiqueta_correo = tk.Label(self, text="Correo", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_correo.grid(row=2, column=0, pady=10)

        # Crear cuadro de entrada de contraseña
        self.cuadro_contrasena = tk.Entry(self, font=("Arial", 12), width=30, show="*")
        self.cuadro_contrasena.grid(row=3, column=0, padx=250)

        # Crear etiqueta "Contraseña"
        self.etiqueta_contrasena = tk.Label(self, text="Contraseña", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_contrasena.grid(row=4, column=0, pady=10)  
        
        # Crear botón "Iniciar sesión"
        self.boton_inicio_sesion = tk.Button(self, text="Iniciar sesión", font=("Arial", 12), bg="#008CBA", fg="white", width=20,command=self.ingresaSistema)
        self.boton_inicio_sesion.grid(row=5, column=0, pady=20, padx=250)

        # Crear etiqueta "¿No tienes una cuenta?"
        self.etiqueta_registro = tk.Label(self, text="¿No tienes una cuenta?", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_registro.grid(row=6, column=0, pady=20)

        # Crear botón "Regístrate aquí"
        self.boton_registro = tk.Button(self, text="Regístrate aquí", font=("Arial", 12), bg="#008CBA", fg="white", width=15,command = lambda:controller.show_frame( Registro ) )
        self.boton_registro.grid(row=7, column=0, pady=10, padx=250)

    #Metodos de la clase
    def ingresaSistema(self):
        Correo = self.cuadro_correo.get()
        Password = self.cuadro_contrasena.get()
        #Instanciamos validaciones y funciones de la base datos
        myFuncionesBD = FuncionesBD()
        myValidaciones = Validaciones()
        #Validamos que los campos no esten vacios
        if(myValidaciones.validaCamposInicioSesion(Correo,Password)):
            if(myFuncionesBD.verificarUsuario(Correo,Password)):
                messagebox.showinfo("Usuario encontrado","Ingresando al sistema...")
                #establecemos la nformacion el atributo del usuario activo para simular la sesion
                self.controller.setInfoUsuarioActivo(myFuncionesBD.getInfoSesion(Correo,Password))
                #mostramos la interfaz de las apuestas individuales
                self.controller.show_frame( Individuales )
            else:
                messagebox.showwarning("Datos erroneos","Correo y/o Contrasenia incorrectos")    
        else:
            messagebox.showinfo("Campos no validos","Completa todos los campos")              
        
#interfaz de registro

#Se crea Frame_2 (similar a primera, pero con idioma ingles)
class Registro(tk.Frame):
    #Se inicializan, recibiendo de parametro self, parent y controller.
    #self es para manejo de clase interna
    #parent es para indicar el frame o root, en donde se ubicara el frame (en este caso en APP principal)
    #controller es indicador interno para manejo correcto de cambio entre frames.
    # (es decir, podra acceder a app principal y a sus metodos, de tal forma que se permita cambio)
    def __init__(self, container,controller,*args, **kwargs):
        #Para inicializar Frame y que se entienda la clase como un Frame, tambien se inicializa desde la herencia:
        #NOTA: NO olvidar pasar el parametro tambien, de lo contrario, no se comprende donde localizar el Frame creado
        #Luego de hacer esto, recordar que "self" es equivalente a decir el Frame_1, que es en donde agregaremos widgets
        super().__init__(container, *args, **kwargs)
        self.configure(bg = "black")
        
        self.titulo = "Registro"
        
        # Crear etiqueta "Bienvenido a BetsPlay Simulator"
        self.etiqueta_bienvenida = tk.Label(self, text="Bienvenido a BetsPlay Simulator", font=("Arial", 20), fg="white", bg="black")
        self.etiqueta_bienvenida.grid(row=0, column=0, pady=15, padx=200)

        # Crear etiqueta "Registro"
        self.etiqueta_registro = tk.Label(self, text="Registro", font=("Arial", 18), fg="white", bg="black")
        self.etiqueta_registro.grid(row=1, column=0, pady=20)

        # Crear etiqueta "Correo"
        self.etiqueta_correo = tk.Label(self, text="Correo", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_correo.grid(row=3, column=0, pady=10)

        # Crear cuadro de entrada de correo electrónico
        self.cuadro_correo = tk.Entry(self, font=("Arial", 12), width=30)
        self.cuadro_correo.grid(row=4, column=0, padx=250)

        # Crear etiqueta "Contraseña"
        self.etiqueta_contrasena = tk.Label(self, text="Contraseña", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_contrasena.grid(row=5, column=0, pady=8)

        # Crear cuadro de entrada de contraseña
        self.cuadro_contrasena = tk.Entry(self, font=("Arial", 12), width=30, show="*")
        self.cuadro_contrasena.grid(row=6, column=0, padx=250)

        # Crear etiqueta "Nickname"
        self.etiqueta_nickname = tk.Label(self, text="Nickname", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_nickname.grid(row=7, column=0, pady=8)

        # Crear cuadro de entrada de nickname
        self.cuadro_nickname = tk.Entry(self, font=("Arial", 12), width=30)
        self.cuadro_nickname.grid(row=8, column=0, padx=250)

        self.var = tk.StringVar(self)
        self.var.set("Caliente.mx")

        self.etiqueta_casa = tk.Label(self, text="Selecciona una casa de apuestas", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_casa.grid(row=9, column=0, pady=8)

        self.opciones = ["Caliente.mx"]
        self.menu_desplegable = tk.OptionMenu(self, self.var, *self.opciones)
        self.menu_desplegable.grid(row=10, column=0, pady=8)


        self.etiqueta_dinero = tk.Label(self, text="Ingresa la cantidad de dinero con la que vas a iniciar", font=("Arial", 12), fg="white", bg="black")
        self.etiqueta_dinero.grid(row=11, column=0, pady=8)

        self.cuadro_dinero = tk.Entry(self, font=("Arial", 12), width=30)
        self.cuadro_dinero.grid(row=12, column=0, padx=250)

        # Crear botón "Registrarme"
        self.boton_registro = tk.Button(self, text="Registrarme", font=("Arial", 12), bg="#008CBA", fg="white", width=20,command=self.registraUser)
        self.boton_registro.grid(row=13, column=0, pady=20, padx=250)

        # Crear etiqueta "Ya tengo una cuenta" y botón "Iniciar sesión"
        self.etiqueta_inicio_sesion = tk.Label(self, text="Ya tengo una cuenta", font=("Arial", 10), fg="white", bg="black")
        self.etiqueta_inicio_sesion.grid(row=14, column=0, pady=15)

        self.boton_inicio_sesion = tk.Button(self, text="Iniciar sesión", font=("Arial", 10), bg="#008CBA", fg="white", width=15,command = lambda:controller.show_frame( InicioS ))
        self.boton_inicio_sesion.grid(row=15, column=0, padx=200)

        #metodos de la clase
    def registraUser(self):
        #Instanciamos las validaciones
        myValidaciones = Validaciones()
        #instanciamos funciones de la base datos
        myFuncionesBD = FuncionesBD()
        # Obtener los datos del formulario
        correo = self.cuadro_correo.get()
        contrasena = self.cuadro_contrasena.get()
        nickname = self.cuadro_nickname.get()
        casa = self.var.get()
        dinero = self.cuadro_dinero.get()
        if(myValidaciones.validaCamposRegistro(correo,contrasena,nickname,casa,dinero)):
            myFuncionesBD.insertaUsuario(correo,contrasena,nickname,casa,dinero)
        else:
            messagebox.showinfo("Campos no validos","Completa todos los campos")    
        
#interfaz de individuales

#Se crea Frame_3 (donde van las apuestas individuales)
class Individuales(tk.Frame):
    #Se inicializan, recibiendo de parametro self, parent y controller.
    #self es para manejo de clase interna
    #parent es para indicar el frame o root, en donde se ubicara el frame (en este caso en APP principal)
    #controller es indicador interno para manejo correcto de cambio entre frames.
    # (es decir, podra acceder a app principal y a sus metodos, de tal forma que se permita cambio)
    def __init__(self, container,controller,*args, **kwargs):
        #Para inicializar Frame y que se entienda la clase como un Frame, tambien se inicializa desde la herencia:
        #NOTA: NO olvidar pasar el parametro tambien, de lo contrario, no se comprende donde localizar el Frame creado
        #Luego de hacer esto, recordar que "self" es equivalente a decir el Frame_1, que es en donde agregaremos widgets
        super().__init__(container, *args, **kwargs)
        self.configure(bg = "#222222")
        self.titulo = "Apuestas"
        self.font = ('Arial', 10)
        
        self.controller = controller 
        
        #Componentes de la interfaz
        
        # Crear botones para cambiar de pestaña
        self.individuales_button = tk.Button(self, text="Apuestas individuales", font=self.font, bg='#222222', fg='white')
        self.individuales_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.historial_button = tk.Button(self, text="Historial", font=self.font, bg='#222222', fg='white',command=lambda:controller.show_frame( Historial ))
        self.historial_button.grid(row=0, column=3, padx=10, pady=10, sticky='n')
        # Crear elementos de la pestaña Apuestas individuales
        self.dinero_label = tk.Label(self, text="Dinero disponible", font=self.font, bg='#222222', fg='white')
        self.dinero_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.completa_info_label = tk.Label(self, text="Completa toda la info.", font=self.font, bg='#222222', fg='white')
        self.completa_info_label.grid(row=1, column=2, padx=10, pady=10, sticky='n')

        self.cerrar_sesion_button = tk.Button(self, text="Cerrar sesión", font=self.font, bg='#222222', fg='white',command=self.cerrarSesion)
        self.cerrar_sesion_button.grid(row=1, column=3, padx=10, pady=10, sticky='n')

        self.equipos_label = tk.Label(self, text="Nombres de los equipos:", font=self.font, bg='#222222', fg='white')
        self.equipos_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.equipo1_entry = tk.Entry(self, font=self.font)
        self.equipo1_entry.grid(row=2, column=1, padx=10, pady=10)

        self.empate_label = tk.Label(self, text="Empate", font=self.font, bg='#222222', fg='white')
        self.empate_label.grid(row=2, column=2, padx=10, pady=10, sticky='n')

        self.equipo2_entry = tk.Entry(self, font=self.font)
        self.equipo2_entry.grid(row=2, column=3, padx=10, pady=10)

        self.momios_label = tk.Label(self, text="Ingresa los momios de los equipos y el empate", font=self.font, bg='#222222', fg='white')
        self.momios_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        self.momios1_entry = tk.Entry(self, font=self.font)
        self.momios1_entry.grid(row=3, column=1, padx=10, pady=10)

        self.momios_empate_entry = tk.Entry(self, font=self.font)
        self.momios_empate_entry.grid(row=3, column=2, padx=10, pady=10)

        self.momios2_entry = tk.Entry(self, font=self.font)
        self.momios2_entry.grid(row=3, column=3, padx=10, pady=10)

        self.seleccion_label = tk.Label(self, text="Selecciona tu apuesta", font=self.font, bg='#222222', fg='white')
        self.seleccion_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')

        self.equipoApostado= StringVar()
        self.equipoApostado.set("Equipo_1")
        
        self.equipo1_radiobutton = Radiobutton(self,text="Equipo 1",variable=self.equipoApostado,value="Equipo_1",font=self.font, bg='#222222', fg='lime')
        self.equipo1_radiobutton.grid(row=4, column=1, padx=10, pady=10)

        self.empate_radiobutton = Radiobutton(self,text="Empate",variable=self.equipoApostado,value="Empate",font=self.font, bg='#222222', fg='lime')
        self.empate_radiobutton.grid(row=4, column=2, padx=10, pady=10)

        self.equipo2_radiobutton = Radiobutton(self,text="Equipo 2",variable=self.equipoApostado,value="Equipo_2",font=self.font, bg='#222222', fg='lime')
        self.equipo2_radiobutton.grid(row=4, column=3, padx=10, pady=10)

        self.apuesta_label = tk.Label(self, text="Ingresa la cantidad de dinero a apostar", font=self.font, bg='#222222', fg='white')
        self.apuesta_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')

        self.apuesta_entry = tk.Entry(self, font=self.font)
        self.apuesta_entry.grid(row=5, column=1, padx=10, pady=10)

        self.calcular_button = tk.Button(self, text="Calcular", font=self.font, bg='#222222', fg='white', command=self.calcular_ganancia)
        self.calcular_button.grid(row=5, column=2, padx=10, pady=10)

        self.guardar_button = tk.Button(self, text="Guardar", font=self.font, bg='#222222', fg='white',command=self.guardaApuesta)
        self.guardar_button.grid(row=5, column=3, padx=10, pady=10)

        self.ganar_label = tk.Label(self, text="Si aciertas esta apuesta, podrás ganar:", font=self.font, bg='#222222', fg='white')
        self.ganar_label.grid(row=6, column=0, padx=10, pady=10, sticky='e')

        self.historial_label = tk.Label(self, text='Ve al apartado "Historial" para controlar y seleccionar si acertaste esta apuesta', font=self.font, bg='#222222', fg='white')
        self.historial_label.grid(row=6, column=2, padx=10, pady=10, sticky='w')

        # Crear etiqueta para mostrar la ganancia
        self.ganancia_label = tk.Label(self, text="Si aciertas esta apuesta, podrás ganar: $0.00", font=self.font, bg='#222222', fg='white')
        self.ganancia_label.grid(row=6, column=0, padx=10, pady=10, sticky='e')
    
    #metodos de la clase    
    def obtenEquipoApostado(self):
        equipoSeleccionado=''    
        #en caso de que se seleccione el equipo 1
        if(self.equipoApostado.get()=="Equipo_1"):
            equipoSeleccionado = self.equipo1_entry.get()
        #en caso de que se seleccione el equipo 2    
        if(self.equipoApostado.get()=="Equipo_2"):
            equipoSeleccionado = self.equipo2_entry.get()
        #en caso de que se seleccione empate
        if(self.equipoApostado.get()=="Empate"):
            equipoSeleccionado = self.equipoApostado.get()
        return equipoSeleccionado 
    
    def getMomioSeleccionado(self):
        momioSeleccionado=''    
        #en caso de que se seleccione el equipo 1
        if(self.equipoApostado.get()=="Equipo_1"):
            momioSeleccionado = self.momios1_entry.get()
        #en caso de que se seleccione el equipo 2    
        if(self.equipoApostado.get()=="Equipo_2"):
            momioSeleccionado = self.momios2_entry.get()
        #en caso de que se seleccione empate
        if(self.equipoApostado.get()=="Empate"):
            momioSeleccionado = self.momios_empate_entry.get()
            
        momioSeleccionado = float(int(momioSeleccionado)/100)
        return momioSeleccionado
           
    def calcular_ganancia(self):
        myValidaciones = Validaciones()
        if(myValidaciones.validaCamposIndividualesCalc(self.equipo1_entry.get(),self.equipo2_entry.get(),self.momios1_entry.get(),self.momios2_entry.get(),self.momios_empate_entry.get(),self.apuesta_entry.get())):    
            dineroApostado = int(self.apuesta_entry.get())
            ganancia = ((self.getMomioSeleccionado() * dineroApostado) + dineroApostado)
            self.ganancia_label.config(text="Si aciertas esta apuesta, podrás ganar: $"+str(ganancia))
        else:
            messagebox.showinfo("Campos no validos","Completa todos los campos")
            
    def guardaApuesta(self):
        #instanciamos las validaciones
        myValidaciones = Validaciones()
        myFunciones = FuncionesBD()
        #nombres equipos
        Equipo1 = self.equipo1_entry.get()
        Equipo2 = self.equipo2_entry.get()
        #momios
        MomioE1 = self.momios1_entry.get()
        MomioE2 = self.momios2_entry.get()
        MomioEmpate = self.momios_empate_entry.get()
        #selecciones
        EquipoSelec = self.obtenEquipoApostado()
        #monetariamente
        DineroApos = self.apuesta_entry.get()
        DineroGanar = self.ganancia_label.cget("text")
        DineroGanar = DineroGanar[41:]
        IdUsuario = self.controller.usuarioActivo.get_IDusuario()
        IdHistorial = self.controller.usuarioActivo.get_IDusuario()
        Datos=[Equipo1,Equipo2,MomioE1,MomioE2,MomioEmpate,EquipoSelec,DineroApos,DineroGanar,IdUsuario,IdHistorial]        
        if(myValidaciones.validaCamposIndividualesGuard(Datos)):
            #procedemos a realizar las inserciones
            #si la insercion es correcta entonces procedemos a guardar el id de la apuesta
            if(myFunciones.guardaApuesta(Datos)==True):
                IDUltimaApuest = myFunciones.getIdApuestaIns(Datos)
                #Guardamos en sesion el id de esta ultima apuesta
                self.controller.usuarioActivo.set_IDLastApuesta(IDUltimaApuest)  
                #Guardamos el monto que se calculo
                self.controller.usuarioActivo.set_MontoEnJuego(DineroGanar)   
        else:   
            messagebox.showinfo("Campos no validos","Completa todos los campos") 
        
    def setInfoSesion(self):      
        self.dinero_label.config(text="Dinero disponible:"+str(self.controller.usuarioActivo.get_dineroInicial()))
        
    def cerrarSesion(self):
        Confirmacion = messagebox.askyesno("Confirmacion","Cerrar sesion?")
        if(Confirmacion):
            #limpiamos valores de la sesion
            self.controller.usuarioActivo.limpiaValores()
            #redirigimos a la interfaz de inicio de sesion
            self.controller.show_frame( InicioS )
        
#Se crea Frame_4 (donde va el historial)
class Historial(tk.Frame):
    #Se inicializan, recibiendo de parametro self, parent y controller.
    #self es para manejo de clase interna
    #parent es para indicar el frame o root, en donde se ubicara el frame (en este caso en APP principal)
    #controller es indicador interno para manejo correcto de cambio entre frames.
    # (es decir, podra acceder a app principal y a sus metodos, de tal forma que se permita cambio)
    def __init__(self, container,controller,*args, **kwargs):
        #Para inicializar Frame y que se entienda la clase como un Frame, tambien se inicializa desde la herencia:
        #NOTA: NO olvidar pasar el parametro tambien, de lo contrario, no se comprende donde localizar el Frame creado
        #Luego de hacer esto, recordar que "self" es equivalente a decir el Frame_1, que es en donde agregaremos widgets
        super().__init__(container, *args, **kwargs)
        self.configure(bg = "#222222")
        self.titulo = "Historial"
        self.font = ('Arial', 10)
        
        self.controller = controller 
        
        #componentes de la interfaz
        # Crear botones de pestañas
        self.apuestas_button = tk.Button(self, text="Individuales", font=self.font,command=lambda:controller.show_frame( Individuales ))
        self.apuestas_button.grid(row=0, column=1, pady=10, sticky='n')

        self.historial_button = tk.Button(self, text="Historial", font=self.font)
        self.historial_button.grid(row=0, column=3, pady=10, sticky='n')

        # Crear widgets para ingreso de dinero
        self.ingreso_label = tk.Label(self, text="Ingresar dinero:", font=self.font, bg='#222222', fg='white')
        self.ingreso_label.grid(row=1, column=0, padx=10, pady=10, sticky='n')

        self.ingreso_entry = tk.Entry(self, font=self.font)
        self.ingreso_entry.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        self.aceptar_ingreso_button = tk.Button(self, text="Aceptar", font=self.font, bg='#222222', fg='white')
        self.aceptar_ingreso_button.grid(row=1, column=2, padx=10, pady=10, sticky='n')

        #cambiar_casa_button = tk.Button(ventana, text="Cambiar casa de apuesta", font=font, bg='#222222', fg='white')
        #cambiar_casa_button.grid(row=1, column=3, padx=10, pady=10, sticky='n')

        self.cerrar_sesion_button = tk.Button(self, text="Cerrar sesión", font=self.font, bg='#222222', fg='white', command=self.cerrarSesion)
        self.cerrar_sesion_button.grid(row=1, column=4, padx=10, pady=10, sticky='n')

        # Crear widgets para retirar dinero
        self.retiro_label = tk.Label(self, text="Retirar dinero", font=self.font, bg='#222222', fg='white')
        self.retiro_label.grid(row=2, column=0, padx=10, pady=10, sticky='n')

        self.retiro_entry = tk.Entry(self, font=self.font)
        self.retiro_entry.grid(row=2, column=1, padx=10, pady=10, sticky='n')

        self.aceptar_retiro_button = tk.Button(self, text="Aceptar", font=self.font, bg='#222222', fg='white')
        self.aceptar_retiro_button.grid(row=2, column=2, padx=10, pady=10, sticky='n')

        # Crear widgets para mostrar dinero disponible
        self.dinero_inicial_label = tk.Label(self, text="Dinero inicial:", font=self.font, bg='#222222', fg='white')
        self.dinero_inicial_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.dinero_disponible_label = tk.Label(self, text="Dinero disponible:", font=self.font, bg='#222222', fg='white')
        self.dinero_disponible_label.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.dinero_perdido_label = tk.Label(self, text="Dinero perdido:", font=self.font, bg='#222222', fg='white')
        self.dinero_perdido_label.grid(row=3, column=2, padx=10, pady=10, sticky='w')

        self.dinero_ganado_label = tk.Label(self, text="Dinero ganado:", font=self.font, bg='#222222', fg='white')
        self.dinero_ganado_label.grid(row=3, column=3, padx=10, pady=10, sticky='w')

        # Crear widgets para identificador de apuesta
        self.id_label = tk.Label(self, text="Identificador de apuesta:", font=self.font, bg='#222222', fg='white')
        self.id_label.grid(row=4, column=0, padx=10, pady=10, sticky='n')

        # Crear widgets para equipos
        self.equipos_label = tk.Label(self, text="Equipos:", font=self.font, bg='#222222', fg='white')
        self.equipos_label.grid(row=5, column=0, padx=10, pady=10, sticky='n')

        # Crear widgets para momios
        self.momios_label = tk.Label(self, text="Momios:", font=self.font, bg='#222222', fg='white')
        self.momios_label.grid(row=6, column=0, padx=10, pady=10, sticky='n')

        # Crear widgets para seleccionar apuesta
        self.apuesta_label = tk.Label(self, text="En esta apuesta, seleccionaste a:", font=self.font, bg='#222222', fg='white')
        self.apuesta_label.grid(row=7, column=0, padx=10, pady=10, sticky='n')

        # Crear widgets para dinero ganado
        self.ganado_label = tk.Label(self, text="Dinero ganado en esta apuesta:", font=self.font, bg='#222222', fg='white')
        self.ganado_label.grid(row=8, column=0, padx=10, pady=10, sticky='n')

        # Crear widgets para dinero perdido
        self.perdido_label = tk.Label(self, text="Dinero perdido en esta apuesta:", font=self.font, bg='#222222', fg='white')
        self.perdido_label.grid(row=9, column=0, padx=10, pady=10, sticky='n')

        # Crear widgets para seleccionar si ganaste la apuesta
        self.ganaste_label = tk.Label(self, text="¿Ganaste la apuesta?", font=self.font, bg='#222222', fg='white')
        self.ganaste_label.grid(row=9, column=3, padx=10, pady=10, sticky='n')

        self.varGanado = StringVar()
        self.varGanado.set("Si")
        #radio button por si se gano
        self.si_button = Radiobutton(self,text="Si",variable=self.varGanado,value="Si",font=self.font, bg='#222222', fg='lime')
        self.si_button.grid(row=10, column=3, padx=10, pady=10, sticky='n')
        #radio button por si no se gano
        self.no_button = Radiobutton(self,text="No",variable=self.varGanado,value="No",font=self.font, bg='#222222', fg='lime')
        self.no_button.grid(row=10, column=4, padx=10, pady=10, sticky='n')
        
        self.confirma = Button(self,text="Aceptar",font=self.font, bg='#222222', fg='white',command=self.guadarHistorial)
        self.confirma.grid(row=10, column=5, padx=10, pady=10, sticky='n')
        # Crear widget para fecha de realización
        self.fecha_label = tk.Label(self, text="Fecha de realización:", font=self.font, bg='#222222', fg='white')
        self.fecha_label.grid(row=10, column=0, padx=10, pady=10, sticky='n')
    #metodos de la clase
    def guadarHistorial(self):
        myFunciones = FuncionesBD()
        idApuesta = int(self.controller.usuarioActivo.get_IDLastApuesta())
        MontoJuego = float(self.controller.usuarioActivo.get_MontoEnJuego())
        if(self.varGanado.get()=="Si"):
           myFunciones.insertaApuestaGanada(idApuesta,MontoJuego,self.varGanado.get())
           self.setDineroGP(self.varGanado.get(),MontoJuego)
        else:
            myFunciones.insertaApuestaPerdida(idApuesta,MontoJuego,self.varGanado.get())
            self.setDineroGP(self.varGanado.get(),MontoJuego)
    
    def cerrarSesion(self):
        Confirmacion = messagebox.askyesno("Confirmacion","Cerrar sesion?")
        if(Confirmacion):
            #limpiamos valores de la sesion
            self.controller.usuarioActivo.limpiaValores()
            #redirigimos a la interfaz de inicio de sesion
            self.controller.show_frame( InicioS )   
    def cleanLabels(self):
        self.equipos_label.config(text='')
        self.momios_label.config(text='')
        self.apuesta_label.config(text='')
        self.fecha_label.config(text='')
    def setDineroGP(self,Gano_Perdio,Monto):
        if(Gano_Perdio == "Si"):
            self.ganado_label.config(text=(f"Dinero ganado en esta apuesta:{Monto}"))
            self.perdido_label.config(text=(f"Dinero perdido en esta apuesta: 0"))
        else:    
            self.perdido_label.config(text=(f"Dinero ganado en esta apuesta:{Monto}"))
            self.ganado_label.config(text=(f"Dinero perdido en esta apuesta: 0"))  
            
                
    def setInfoUltimaApuesta(self):
        #mostramos en la interfaz el id de la ultima apuesta
        IdUltimaApuesta = self.controller.usuarioActivo.get_IDLastApuesta()
        self.id_label.config(text=(f"Identificador de apuesta: {IdUltimaApuesta}"))    
        #instanciamos nuestras funciones
        myFunciones = FuncionesBD()
        myTiempo = Tiempo()
        
        DatosApuesta = myFunciones.getDataApuesta(IdUltimaApuesta)
        if(len(DatosApuesta)<1):
            messagebox.showerror("ERROR FATAL","SE HAN ENCONTRADO 17 ROOTKITS!\nTOMAR ACCION AHORA!")
            return
        #self.cleanLabels()    
        for DatosAp in DatosApuesta:
            #mostramos los equipos involucrados en las apuestas
            self.equipos_label.config(text=(f"Equipos:  {DatosAp[1]} | Empate | {DatosAp[2]}"))
            self.momios_label.config(text=(f"Momios: {DatosAp[3]} | {DatosAp[4]} | {DatosAp[5]}"))
            self.apuesta_label.config(text=(f"En esta apuesta, seleccionaste a: {DatosAp[6]}"))
        #seteamos la fecha en la etquita
        self.fecha_label.config(text=(f"Fecha de realización: {myTiempo.obtener_fecha()}"))    

#Se crea APP como tal (aprovechandonos de la clase creada)
root = APP()

#Se ejecuta la ventana principal, creada a traves de POO con las clases respectivas
root.mainloop()