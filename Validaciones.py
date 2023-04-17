from tkinter import messagebox
class Validaciones:
    
    def __init__(self):
        self.__activo = True
        
    def validaCamposRegistro(self,Correo,Password,Nickname,CasaAp,Dinero):
        if(Correo == "" or Password == "" or Nickname == "" or CasaAp== "" or Dinero==""):
           return False     
        return True 
    
    def validaCamposInicioSesion(self,Correo,Password):
        if(Correo == "" or Password == ""):
           return False     
        return True 
    
    def validaCamposIndividualesCalc(self,Equipo1,Equipo2,MomioE1,MomioE2,MomioEmpate,DineroApostado):
        if(Equipo1 == "" or Equipo2=="" or MomioE1=="" or MomioE2 =="" or MomioEmpate=="" or DineroApostado==""):
            return False
        return True   
    
    #recibe 7 datos en un arreglo y comprueba que ninguno este vacio
    def validaCamposIndividualesGuard(self,Datos):
        for Dato in Datos:
            if(Dato == ""):
                return False
        return True    