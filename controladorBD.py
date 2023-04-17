from tkinter import messagebox
import sqlite3
import bcrypt

class controladorBD:
    
    def __init__(self):
       self.varAux = ''

    def conexionBD(self):
        #Preparamos la conexión para usarla cuando sea necesario
        try:
            conexion = sqlite3.connect("C:/Users/cesar/OneDrive/Escritorio/PI(refactor)/prueba final.db")
            print("Conexión exitosa")
            return conexion
        
        except sqlite3.OperationalError:
            print("No se pudo conectar a la base de datos")
            
            
            
    def guardarUsuario(self, nick, cor, con, casa, dinero):
        #Llamar a la conexión
        conx = self.conexionBD()
        
        #Revisar que los parametros no estén vacíos
        if(nick == "" or cor == "" or con == "" or casa == "" or dinero == ""):    
            messagebox.showwarning("Advertencia", "Revisa tu formuladio, no puedes dejar campos vacíos")
            conx.close()
        else:
            #Preparamos datos y el querySQL
            cursor=conx.cursor()
            conH = self.encriptarCon(con)
            datos = (cor, conH, nick, casa, dinero)
            qrInsert = "INSERT INTO Usuarios (correo, password, nickname, nombreCasa, dineroInicial) values (?, ?, ?, ?, ?)"
            
            #Procede a insertar los datos y cerramos la conexión
            cursor.execute(qrInsert, datos)
            conx.commit()
            conx.close()
            messagebox.showinfo("Registro exitoso", "Se ha registrado exitosamente")
            
        
            
    def encriptarCon(self, con):
        conPlana = con
        conPlana = conPlana.encode() #Codifica la contraseña en bytes
        salt = bcrypt.gensalt() #Genera el salt
        conHash = bcrypt.hashpw(conPlana, salt) #Genera el hash
        print(conHash)
        return conHash
    
    
    
    def consultaUsuario(self,id):
        #Llamar a la conexión
        conx = self.conexionBD()
        
        #Verificar que el id no esté vacío
        if(id == ""):
            messagebox.showwarning("Advertencia", "Revisa tu formuladio, no puedes dejar campos vacíos")
            conx.close()
        else:
            #Proceder a buscar el usuario
            try:
                #Preparamos lo necesario para el select
                cursor=conx.cursor()
                sqlSelect = "SELECT * FROM Usuarios WHERE idUsuario ="+ id
                
                #5. Ejecucion y guardado de la consulta
                cursor.execute(sqlSelect)
                RSusuario = cursor.fetchall()
                conx.close()
                
                return RSusuario
                
            except sqlite3.OperationalError:
                print("Error de consulta")
                
                

    def consultaTodos(self):
        #Llamar a la conexión
        conx = self.conexionBD()
        
        #Proceder a buscar todos los usuarios
        try:
            #Preparamos lo necesario para el select
            cursor=conx.cursor()
            sqlSelect = "SELECT idUsuario, correo, password, nickname, nombreCasa, dineroInicial FROM Usuarios"
            
            #Ejecucion y guardado de la consulta
            cursor.execute(sqlSelect)
            RSusuarios = cursor.fetchall()
            conx.close()
            
            return RSusuarios
            
        except sqlite3.OperationalError:
            print("Error de consulta")
            
    def actualizaUsuarioV2(self, id, nick, cor, con, dinero):   
        #comprobamos que los campos no esten vacios    
        if(id == "" or nick == "" or cor =="" or con=="" or dinero==""):
            messagebox.showwarning("Advertencia", "Por favor completa los campos para actualizar")
            return
        
        Conexion = self.conexionBD()
        try:
            Cursor = Conexion.cursor()
            #recopilamos los datos
            Datos = [nick,cor,self.encriptarCon(con),dinero,id]
            #construimos la sentencia SQL
            SQL = "UPDATE Usuarios SET nickname = ?, correo = ?, password = ?, dineroInicial = ? WHERE idUsuario = ?"
            #pedimos intervencion del usuario para confirmar la operacion
            Confirmacion = messagebox.askyesno("Confirmacion","¿Seguro de realizar los cambios?")
            if(Confirmacion):
                Cursor.execute(SQL,Datos)
                Conexion.commit()
                Conexion.close()
                messagebox.showinfo("Exitoso!","La actualizacion se realizo correctamente")
            else:
                Conexion.close()    
        except sqlite3.OperationalError:   
            print("Error al realizar la actualizacion")
    
    def eliminaUsuarioV2(self,ID):
        if(ID == ""):
            messagebox.showerror("Aviso!","Ingresa un ID")
            return
        try:
            #abrimos conexion
            Conexion = self.conexionBD()
            Cursor = Conexion.cursor()
            SQL = "DELETE FROM Usuarios WHERE idUsuario=?"
            #pedimos confirmacion del usuario
            Confirmacion = messagebox.askyesno("Confirmacion","¿Seguro de eliminar este usuario?")
            if(Confirmacion):
                Cursor.execute(SQL,(ID,))
                Conexion.commit()
                Conexion.close()
                messagebox.showinfo("Exitoso!","La eliminacion se realizo correctamente")
                return 1
            else:
                Conexion.close()
        except sqlite3.OperationalError:
            print("Error de eliminacion :/")    
    
            
    def eliminarUsuario(self, id):
        try:
            # Obtener una nueva conexión
            conexion = self.conexionBD()
            
            # Verificar que el usuario exista en la base de datos
            usuario = self.consultaUsuario(id)
            if usuario:
                # Eliminar el usuario de la base de datos
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Usuarios WHERE idUsuario=?", (id,))
                conexion.commit()
                conexion.close()
                return True
            else:
                conexion.close()
                return False
        except:
            return False