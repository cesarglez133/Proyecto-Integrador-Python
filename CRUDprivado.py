#Esta ventana es privada y solo será visible para los administradores. El usuario final no tiene ecceso a esta. Aqui se controlara a los usuarios registrados.
from tkinter import *
from tkinter import ttk
import tkinter as tk
from controladorBD import * #Le presentamos la clase a la ventana

#Crear una instancia de tipo controlador
controlador = controladorBD()

#Procede a guardar usando el metodo del objeto controlador
def ejecutaInsert():
    controlador.guardarUsuario(varNick.get(), varCor.get(), varCon.get(), varCasa.get(), varDinero.get())

#Funcion para buscar usuario    
def ejecutaSelecU():
    rsUsuario=controlador.consultaUsuario(varBus.get())
    for usu in rsUsuario:
        cadena=str(usu[0])+" "+usu[1]+" "+str(usu[2])+" "+str(usu[3] )+" "+str(usu[4])+" "+str(usu[5])
       
    #Colocamos el usuario en el textBus    
    if(rsUsuario):
        textBus=tk.Text(pestana2, height=5, width=52)
        textBus.pack()
        textBus.insert(INSERT, cadena)
    else:
        messagebox.showinfo("No encontrado", "No se encontró el usuario")
        print("No se encontró el usuario")
        
def activaCamposAct():
    #hace que los campos de la pestania actualizacion sean editables
    txtNickNue.config(state="normal")
    txtCorNue.config(state="normal")
    txtConNue.config(state="normal")
    txtDinNue.config(state="normal")
    btnGuardarCambios.config(state="normal")
    
def desactivaBusActu():
    #desactiva el campo de id a modificar para que no se pueda alterar y sea util al momento de actualizar
    txtIDAct.config(state="disabled")
    BtnBuscaIDAct.config(state="disabled")
    
def muestraInfoActu():
    ID = varID.get()
    if(ID == ""):
        messagebox.showwarning("Aviso!","Por favor ingresa un id")
        return
    #consulta la informacion del id para mostrarla
    Resultado = controlador.consultaUsuario(ID)
    #si la longitud es 0, quiere decir que no hay concidencias
    if(len(Resultado) < 1):
         messagebox.showinfo("No encontrado", "No se encontró el usuario")
         return
     
    activaCamposAct() 
    for usuario in Resultado:
        txtNickNue.insert(0,usuario[3]) 
        txtCorNue.insert(0,usuario[1]) 
        #txtConNue.insert(0,usuario[1]) 
        txtDinNue.insert(0,usuario[5]) 
    #Deshabilitamos el campo del ID para que no edite y se pueda ejecutar la edicion
    desactivaBusActu() 

def restableceCampActu():
    #eliminamos la informacion de los campos
    txtNickNue.delete(0,END)
    txtCorNue.delete(0,END)
    txtConNue.delete(0,END)
    txtDinNue.delete(0,END)
    #deshabilitamos campos de la info
    txtNickNue.config(state="disabled")
    txtCorNue.config(state="disabled")
    txtConNue.config(state="disabled")
    txtDinNue.config(state="disabled")
    btnGuardarCambios.config(state="disabled")     
    #habilitamos campos de busqueda
    txtIDAct.config(state="normal")
    BtnBuscaIDAct.config(state="normal")   
        
def guardarCambios():
    # Obtener los valores de los campos de entrada
    id = varID.get()
    nick = varNickNue.get()
    cor = varCorNue.get()
    con = varConNue.get()
    dinero = varDinNue.get()
    
    controlador.actualizaUsuarioV2(id, nick, cor, con, dinero)   

    
#Función para mostrar todos los usuarios en la tabla
def mostrarUsuarios():
    #Obtener todos los usuarios de la base de datos
    usuarios = controlador.consultaTodos()
    
    #Limpiar la tabla
    for i in tablaUsuarios.get_children():
        tablaUsuarios.delete(i)
    
    #Llenar la tabla con los datos obtenidos
    for usu in usuarios:
        tablaUsuarios.insert("", END, values=(usu[0], usu[1], usu[2], usu[3], usu[4], usu[5]))
        
def actualizarTabla():
    tablaUsuarios.delete(*tablaUsuarios.get_children())
    usuarios = controlador.consultaTodos()
    for usu in usuarios:
        tablaUsuarios.insert("", END, values=(usu[0], usu[1], usu[2], usu[3]))
        
#habilita los campos de la eliminacion para que se pueda poner la informacion        
def habilitaCampDel():
    txtNickDel.config(state="normal")
    txtCorDel.config(state="normal")
    txtCADel.config(state="normal")
    txtDinDel.config(state="normal")
#deshabilita los campos para que no se puedan editar    

def deshabilitaCampDel():
    txtNickDel.config(state="disabled")
    txtCorDel.config(state="disabled")
    txtCADel.config(state="disabled")
    txtDinDel.config(state="disabled")
    
#muestra la informacion relacionada a un id a eliminar
def buscaEliminacion():
    ID = varIdEliminar.get()
    if(ID == ""):
        messagebox.showwarning("Aviso!","Por favor ingresa un id")
        return
    #consulta la informacion del id para mostrarla
    Resultado = controlador.consultaUsuario(ID)
    #si la longitud es 0, quiere decir que no hay concidencias
    if(len(Resultado) < 1):
         messagebox.showinfo("No encontrado", "No se encontró el usuario")
         return     
    #habilita los campos para ingresar la info  
    habilitaCampDel()
    for Usuario in Resultado:
        txtNickDel.insert(0,Usuario[3]) 
        txtCorDel.insert(0,Usuario[1]) 
        txtCADel.insert(0,Usuario[4]) 
        txtDinDel.insert(0,Usuario[5]) 
    #deshabilita los campos para que no se pueda editar la infor    
    deshabilitaCampDel()
    #activamos el boton para que pueda ejecutar la eliminacion
    btnEliminar.config(state="normal")
    #deshabilitamos la entrada de texto del id y el boton de busqueda
    txtIdEliminar.config(state="disabled")
    btnBuscaDel.config(state="disabled")
    #habilitamos el boton para cambiar ID
    estadoBtnCambiaDel()

#restablece los campos para cambiar el id
def cambiaIDDel():
    #eliminamos la info de los campos
    habilitaCampDel()
    txtNickDel.delete(0,END)
    txtCorDel.delete(0,END)
    txtCADel.delete(0,END)
    txtDinDel.delete(0,END)   
    deshabilitaCampDel()
    #deshabilitamos el boton de eliminacion
    habilitaDesBtnDel() 
    #habilitamos la entrada de texto del id y el boton de busqueda
    txtIdEliminar.config(state="normal")
    btnBuscaDel.config(state="normal")
    estadoBtnCambiaDel()
    
     
def habilitaDesBtnDel():
    if(btnEliminar.cget("state")== "disabled"):
        btnEliminar.config(state="normal")
    elif(btnEliminar.cget("state")== "normal"):    
        btnEliminar.config(state="disabled")
        
def estadoBtnCambiaDel():
    if(btnCambiaDel.cget("state")== "disabled"):
        btnCambiaDel.config(state="normal")
    elif(btnCambiaDel.cget("state")== "normal"):    
        btnCambiaDel.config(state="disabled")    
    
# Función para eliminar usuario
def eliminarUsuario():
    id = varIdEliminar.get()
    
    # Verificar que el ID no esté vacío
    if id == "":
        messagebox.showwarning("Advertencia", "Ingresa un ID, no puede estar vacío")
    else:
        # Verificar que el ID existe en la base de datos
        usuario = controlador.consultaUsuario(id)
        if usuario:
            # Mostrar mensaje de confirmación antes de eliminar el usuario
            respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro que quieres eliminar este usuario?")
            if respuesta == True:
                # Eliminar el usuario
                eliminado = controlador.eliminarUsuario(id)
                if eliminado:
                    messagebox.showinfo("Eliminación exitosa", "Usuario borrado con éxito")
                    # Limpiar el campo de entrada
                    varIdEliminar.set("")
                    # Actualizar la tabla
                    actualizarTabla()
                else:
                    messagebox.showwarning("Advertencia", "No se pudo eliminar el usuario")
        else:
            messagebox.showwarning("Advertencia", "Usuario no válido")


#funcion que ejecuta la eliminacion
def elimnaUser():
    ID = varIdEliminar.get()
    Resultado = controlador.eliminaUsuarioV2(ID)
    #Si la eliminacion se realizo correctamente actualizamos la tabla
    if(Resultado==1):
        actualizarTabla()
        cambiaIDDel()

Ventana = Tk()
Ventana.title("CRUD de Usuarios BETSPLAY SIMULATOR")
Ventana.geometry("500x350")
Ventana.configure(bg="black")
# Crea un objeto ttk.Style y establece el color de fondo del área de pestañas
estilo_pestana = ttk.Style()
estilo_pestana.configure("TNotebook", background="black")

# Crea un nuevo estilo que herede de estilo_pestana y establece el color de fondo del contenido de las pestañas
estilo_contenido = ttk.Style()
estilo_contenido.configure("MiEstilo.TFrame", background="white", foreground="black", font=("Arial", 12))



panel=ttk.Notebook(Ventana)
panel.pack(fill="both",expand="yes")

pestana1=ttk.Frame(panel)
pestana2=ttk.Frame(panel)
pestana3=ttk.Frame(panel)
pestana4=ttk.Frame(panel)
pestana5=ttk.Frame(panel)



#Pestana1: Formulario de usuarios
titulo=Label(pestana1,text="Registro de usuarios", fg="blue", font=("Modern",18)).pack()

varCor=tk.StringVar()
lblCor=Label(pestana1, text="Correo: ").pack()
txtCor=Entry(pestana1, textvariable=varCor).pack()

varNick=tk.StringVar()
lblNick=Label(pestana1, text="Nickname: ").pack()
txtNick=Entry(pestana1, textvariable=varNick).pack()

varCon=tk.StringVar()
lblCon=Label(pestana1, text="Contrasena: ").pack()
txtCon=Entry(pestana1, textvariable=varCon,show="*").pack()

varCasa=tk.StringVar()
CasasAp = ["Caliente MX"]
lblCasa=Label(pestana1, text="Casa de apuestas: ").pack()
varCasa.set(CasasAp[0])
#txtCasa=Entry(pestana1, textvariable=varCasa).pack()
txtCasa = ttk.Combobox(pestana1,textvariable=varCasa,values=CasasAp)
txtCasa.pack()

varDinero=tk.StringVar()
lblDinero=Label(pestana1, text="Dinero inicial: ").pack()
txtDinero=Entry(pestana1, textvariable=varDinero).pack()

btnGuardar=Button(pestana1, text="Guardar usuario", command=ejecutaInsert).pack()


#Comienza pestaña 2. Buscar usuario

titulo2=Label(pestana2,text="Buscar usuario", fg="green", font=("Modern",18)).pack()

varBus=tk.StringVar()
lblid=Label(pestana2, text="Identificador de usuario: ").pack()
txtid=Entry(pestana2, textvariable=varBus).pack()

btnBusqueda=Button(pestana2, text="Buscar", command=ejecutaSelecU).pack()

subBus=Label(pestana2,text="Registrado", fg="blue", font=("Modern",15)).pack()
textBus=tk.Text(pestana2, height=5, width=52).pack()



#Pestaña 3. Consultar usuarios
titulo3=Label(pestana3,text="Consultar usuarios", fg="blue", font=("Modern",18)).pack()

#Creación de la tabla
tablaUsuarios = ttk.Treeview(pestana3, columns=("ID", "Correo", "Contraseña", "Nickname", "Casa", "Dinero Inicial"), show='headings')
tablaUsuarios.heading("ID", text="ID")
tablaUsuarios.heading("Correo", text="Correo")
tablaUsuarios.heading("Contraseña", text="Contraseña")
tablaUsuarios.heading("Nickname", text="Nickname")
tablaUsuarios.heading("Casa", text="Casa")
tablaUsuarios.heading("Dinero Inicial", text="Dinero Inicial")
tablaUsuarios.pack()

#Botón para mostrar usuarios
btnMostrar=Button(pestana3, text="Mostrar usuarios", command=mostrarUsuarios).pack()



#Pestaña 4. Actualizar usuario
titulo4 = Label(pestana4, text="Actualizar usuario", fg="brown", font=("Modern", 18)).pack()

# Texto para ingresar ID del usuario a modificar
varID = tk.StringVar()
lblIDAct = Label(pestana4, text="ID de usuario a modificar: ")
lblIDAct.pack()
txtIDAct = Entry(pestana4, textvariable=varID)
txtIDAct.pack()

BtnBuscaIDAct = Button(pestana4,text="Buscar",command=muestraInfoActu)
BtnBuscaIDAct.pack()

#Boton que restablece campos en caso de querer cambiar ID
BtnCambiaID = Button(pestana4,text="Cambiar ID actualizar",command=restableceCampActu)
BtnCambiaID.pack()

# Campos de entrada para los datos actualizados
varNickNue = tk.StringVar()
lblNickNue = Label(pestana4, text="Nickname nuevo: ")
lblNickNue.pack()
txtNickNue = Entry(pestana4, textvariable=varNickNue)
txtNickNue.config(state="disabled")
txtNickNue.pack()

varCorNue = tk.StringVar()
lblCorNue = Label(pestana4, text="Correo nuevo: ")
lblCorNue.pack()
txtCorNue = Entry(pestana4, textvariable=varCorNue)
txtCorNue.config(state="disabled")
txtCorNue.pack()

varConNue = tk.StringVar()
lblConNue = Label(pestana4, text="Contraseña nueva: ")
lblConNue.pack()
txtConNue = Entry(pestana4, textvariable=varConNue, show='*')
txtConNue.config(state="disabled")
txtConNue.pack()

varDinNue = tk.StringVar()
lblDinNue = Label(pestana4, text="Dinero actualizado: ")
lblDinNue.pack()
txtDinNue = Entry(pestana4, textvariable=varDinNue)
txtDinNue.config(state="disabled")
txtDinNue.pack()

# Botón para guardar los cambios
btnGuardarCambios = Button(pestana4, text="Guardar cambios", command=guardarCambios)
btnGuardarCambios.config(state="disabled")
btnGuardarCambios.pack()




# Pestaña 5. Eliminar usuario
titulo5 = Label(pestana5, text="Eliminar usuario", fg="red", font=("Modern", 18)).pack()

varIdEliminar = tk.StringVar()
lblIdEliminar = Label(pestana5, text="ID de usuario a eliminar: ")
lblIdEliminar.pack()
txtIdEliminar = Entry(pestana5, textvariable=varIdEliminar)
txtIdEliminar.pack()
#boton para buscar la informacion relacionada con el id
btnBuscaDel = Button(pestana5,text="Buscar",command=buscaEliminacion)
btnBuscaDel.pack()
#boton para cambiar el ID a eliminar
btnCambiaDel = Button(pestana5,text="Cambiar Id",command=cambiaIDDel)
btnCambiaDel.config(state="disabled")
btnCambiaDel.pack()


#campos para mostrar la informacion relacionada
lblNickDel = Label(pestana5,text="Nickname:")
lblNickDel.pack()
txtNickDel = Entry(pestana5)
#deshabilitamos el campo para que no se pueda modificar la info
txtNickDel.config(state="disabled")
txtNickDel.pack()

lblCorDel = Label(pestana5,text="Correo:")
lblCorDel.pack()
txtCorDel = Entry(pestana5)
#deshabilitamos el campo para que no se pueda modificar la info
txtCorDel.config(state="disabled")
txtCorDel.pack()

lblCADel = Label(pestana5,text="Casa apuestas:")
lblCADel.pack()
txtCADel = Entry(pestana5)
#deshabilitamos el campo para que no se pueda modificar la info
txtCADel.config(state="disabled")
txtCADel.pack()

lblDinDel = Label(pestana5,text="Dinero:")
lblDinDel.pack()
txtDinDel = Entry(pestana5)
#deshabilitamos el campo para que no se pueda modificar la info
txtDinDel.config(state="disabled")
txtDinDel.pack()

# Botón para eliminar usuario
btnEliminar = Button(pestana5, text="Eliminar usuario", command=elimnaUser)
#deshabilitamos el boton para que se pueda usar hasta que se busca un id
btnEliminar.config(state="disabled")
btnEliminar.pack()



panel.add(pestana1, text="Formulario de usuarios")
panel.add(pestana2, text="Buscar usuario")
panel.add(pestana3, text="Consultar usuario")
panel.add(pestana4, text="Actualizar usuario")
panel.add(pestana5, text="Eliminar usuario")

Ventana.mainloop()
