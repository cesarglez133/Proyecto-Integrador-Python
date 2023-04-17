from tkinter import * 
#from tkinter import ttk as ttk
class Usuario: 

    def __init__(self,IDusuario=None,correo=None,password=None,nickname=None,nombreCasa=None,dineroInicial=None):
        self.__IDusuario = IDusuario
        self.__correo = correo
        self.__password = password
        self.__nickname = nickname
        self.__nombreCasa = nombreCasa
        self.__dineroInicial = dineroInicial
        self.__IDLastApuesta = None
        self.__MontoEnJuego = None
        
    #metodos SETTER y GETTER de la clase    
    def get_IDusuario(self):
        return self.__IDusuario

    def set_IDusuario(self, IDusuario):
        self.__IDusuario = IDusuario

    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        self.__correo = correo

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_nickname(self):
        return self.__nickname

    def set_nickname(self, nickname):
        self.__nickname = nickname

    def get_nombreCasa(self):
        return self.__nombreCasa

    def set_nombreCasa(self, nombreCasa):
        self.__nombreCasa = nombreCasa

    def get_dineroInicial(self):
        return self.__dineroInicial

    def set_dineroInicial(self, dineroInicial):
        self.__dineroInicial = dineroInicial   
    
    def set_IDLastApuesta(self,IDLastApuesta):
        self.__IDLastApuesta = IDLastApuesta
    
    def get_IDLastApuesta(self):
        return self.__IDLastApuesta   
    
    def set_MontoEnJuego(self,MontoEnJuego):
         self.__MontoEnJuego = MontoEnJuego
    
    def get_MontoEnJuego(self):
        return self.__MontoEnJuego     
        
    def limpiaValores(self):
        self.__IDusuario = None
        self.__correo = None
        self.__password = None
        self.__nickname = None
        self.__nombreCasa = None
        self.__dineroInicial = None 