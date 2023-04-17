import sqlite3
from tkinter import messagebox
from Tiempo import *

class FuncionesBD:
    def __init__(self):
        self.__BaseDatos = "prueba final.db"
        
    def __conectaBD(self):
        try:
            Conexion = sqlite3.connect(self.__BaseDatos) 
            print("Conexion exitosa")
            return Conexion 
        except sqlite3.OperationalError:
            Conexion.close()
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN EL SERVIDOR!")
           
    def insertaUsuario(self,Correo,Password,Nickname,CasaAp,Dinero):       
        Conexion = self.__conectaBD()
        Cursor = Conexion.cursor()
        try:
            Datos = [Correo,Password,Nickname,CasaAp,Dinero]
            SQL = "INSERT INTO Usuarios (correo, password, nickname, nombreCasa, dineroInicial) VALUES (?, ?, ?, ?, ?)"
            Resultado = Cursor.execute(SQL,Datos)
            Conexion.commit()
            Conexion.close()
            messagebox.showinfo("Exito","Se inserto correctamente")
            messagebox.showinfo("Exito","Ya puedes iniciar sesion")
        except sqlite3.OperationalError:   
            Conexion.close()  
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA INSERCCION!")
            
    def verificarUsuario(self,Correo,Password):
        Conexion = self.__conectaBD()   
        Cursor = Conexion.cursor()
        try:   
            Datos = [Correo,Password]
            SQL = "SELECT idUsuario FROM Usuarios WHERE correo = ? AND password = ?"
            Cursor.execute(SQL,Datos)
            Resultado = Cursor.fetchall()
            Conexion.close()
            if(len(Resultado) < 1):
                return False
            else:
                return True
        except sqlite3.OperationalError:  
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA SELECCION DE USUARIO!")
           
    def getInfoSesion(self,Correo,Password):       
        Conexion = self.__conectaBD()   
        Cursor = Conexion.cursor()
        try:   
            Datos = [Correo,Password]
            SQL = "SELECT * FROM Usuarios WHERE correo = ? AND password = ?"
            Cursor.execute(SQL,Datos)
            Resultado = Cursor.fetchall()
            Conexion.close()
            return Resultado
        except sqlite3.OperationalError: 
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA SELECCION DE USUARIO!")  
                 
    def guardaApuesta(self,Datos): #recibe una lista con los datos
        Conexion = self.__conectaBD() 
        Cursor = Conexion.cursor()
        try:     
            #Se realiza la insercion en la tabla de individuales
            SQL = "INSERT INTO Individuales(nombreEq1,nombreEq2,momioEq1,momioEq2,momioEmpate,eqSeleccionado,dineroApostado,dineroAGanar,idUsuario,idHistorial)VALUES(?,?,?,?,?,?,?,?,?,?)"
            Cursor.execute(SQL,Datos)
            Conexion.commit()
            Conexion.close()
            
            #insertamos en el historial
            self.insertaHistorial(Datos)
            messagebox.showinfo("Exito","Se guardo correctamente")
            return True
        except sqlite3.OperationalError as e:           
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA INSERCION DE DATOS!:"+str(e))
            return False
            
    def getIdApuestaIns(self,Datos):
        Conexion = self.__conectaBD() 
        Cursor = Conexion.cursor()
        try:
            SQL = "SELECT idApuesta FROM Individuales WHERE nombreEq1 = ? AND nombreEq2 = ? AND momioEq1 = ? AND momioEq2 = ? AND momioEmpate = ? AND eqSeleccionado = ? AND dineroApostado = ? AND dineroAGanar = ? AND idUsuario = ? AND idHistorial = ?"
            
            Cursor.execute(SQL,Datos)  
            Resultado = Cursor.fetchone()
            Conexion.close() 
            #regresamos el ID de apuesta insertado
            idApuesta= Resultado[len(Resultado)-1]
            return idApuesta   
        except sqlite3.OperationalError as e:    
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA SELECCION DE DATOS! getIdApuesta"+str(e))      
                  
                  
    def insertaHistorial(self,Datos):
        Conexion = self.__conectaBD()
        Cursor = Conexion.cursor()
        try:
            #se realiza la insercion en la tabla de historial
            DatosH = [Datos[9],self.getIdApuestaIns(Datos),Datos[8]]            
            print("Datos historial:",DatosH)
            SQL2 = "INSERT INTO Historial(idHistorial,idApuesta,idUsuario)VALUES(?,?,?)"
            Cursor.execute(SQL2,DatosH)
            Conexion.commit()
            Conexion.close()
        except sqlite3.OperationalError as e:   
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA SELECCION DE DATOS! getIdApuesta:"+str(e))   
            
    def getDataApuesta(self,IdApuesta):
        Conexion = self.__conectaBD()
        Cursor = Conexion.cursor()
        try:
          SQL = f"SELECT * FROM Individuales WHERE idApuesta = {IdApuesta}"
          Cursor.execute(SQL)
          Resultado = Cursor.fetchall()
          Conexion.close()
          return Resultado      
        except sqlite3.OperationalError as e:   
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA SELECCION DE DATOS! getIdApuesta:"+str(e))  
            print("Id de apuesta:",IdApuesta)    
            
    def insertaApuestaGanada(self,idApuesta,dineroGanado,seGano):
        Conexion = self.__conectaBD()
        Cursor = Conexion.cursor()
        myFecha = Tiempo()
        dineroPerdido = 0
        fecha = myFecha.obtener_fecha()
        try:
            Datos = [dineroGanado,dineroPerdido,fecha,seGano,idApuesta]
            SQL = "UPDATE  Historial SET dineroGanado = ?,dineroPerdido = ?,fecha = ?,seGano = ? WHERE idApuesta = ?"
            Cursor.execute(SQL,Datos)
            Conexion.commit()
            Conexion.close()   
            messagebox.showinfo("Todo correcto","Se guardo correctamente")
        except sqlite3.OperationalError as e:   
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA INSERCION DE DATOS! getIdApuesta:"+str(e))    
    
    
    def insertaApuestaPerdida(self,idApuesta,dineroPerdido,seGano):
        Conexion = self.__conectaBD()
        Cursor = Conexion.cursor()
        myFecha = Tiempo()
        dineroGanado = 0
        fecha = myFecha.obtener_fecha()       
        
        try:
            Datos = [dineroGanado,dineroPerdido,fecha,seGano,idApuesta]
            SQL = "UPDATE  Historial SET dineroGanado = ?,dineroPerdido = ?,fecha = ?,seGano = ? WHERE idApuesta = ?"
            Cursor.execute(SQL,Datos)
            Conexion.commit()
            Conexion.close()   
            messagebox.showinfo("Todo correcto","Se guardo correctamente")
        except sqlite3.OperationalError as e:
            Conexion.close()      
            messagebox.showinfo("ERROR","HA OCURRIDO UN ERROR EN LA INSERCION DE DATOS! getIdApuesta:"+str(e))              