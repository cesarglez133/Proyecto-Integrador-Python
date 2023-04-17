import datetime


class Tiempo:
    
    def __init__(self):
        self.__activo =True
    
    def obtener_fecha(self):
        fecha_actual = datetime.date.today()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
        return fecha_formateada
