from dataclasses import dataclass

@dataclass
class Response:
    success: bool
    message: str

class AttemptsClass:
    #setter para las respuestas
    def __set_response(self, success, message):
        #para los tipos
        return Response(success, message)
    #funcion general para todos
    def attempts(self, action):
        try:
            action()
        except Exception as e:
            success, message = False, str(e)
        else:
            success, message = True, "La operación fue realizada con éxito"
        return self.__set_response(success,message)