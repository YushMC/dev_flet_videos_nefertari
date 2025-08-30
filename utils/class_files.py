import os, sys
import subprocess
from utils.class_attermpts import AttemptsClass
import platform
from PIL import Image

# Función para recursos empaquetados
def resource_path(relative_path):
    """
    Devuelve la ruta absoluta de un recurso, ya sea ejecutable PyInstaller o script normal
    """
    try:
        base_path = sys._MEIPASS  # Bundle PyInstaller
    except AttributeError:
        base_path = os.getcwd()    # Script normal
    return os.path.join(base_path, relative_path)

class InitPaths:
    def __init__(self):
        sistema = platform.system()
        # Carpeta base de escritura (input/output/temp) fuera del bundle
        if sistema == "Windows":
            # Carpeta base de usuario en Windows
            self.base_write_path = os.path.join(os.environ["USERPROFILE"], "NefertariVideos")
        else:
            # macOS / Linux
            self.base_write_path = os.path.join(os.path.expanduser("~"), "NefertariVideos")
        self.input_path = os.path.join(self.base_write_path, "input")
        self.output_path = os.path.join(self.base_write_path, "output")
        self.temp_path = os.path.join(self.base_write_path, "temp")
        self.logs = os.path.join(self.base_write_path, "log.txt")

        # Crear carpetas si no existen
        for path in [self.input_path, self.output_path, self.temp_path]:
            os.makedirs(path, exist_ok=True)

        # Rutas de archivos temporales
        self.temp_video_path = os.path.join(self.temp_path, "viaje.mp4")
        self.temp_video_to_generate_path = os.path.join(self.temp_path, "temp_video.mp4")
        self.audio_temp_video_logo = os.path.join(self.temp_path, "temp_audio.mp3")
        self.audio_final_video_logo = os.path.join(self.temp_path, "temp_final_audio.mp3")

        # Rutas de archivos de entrada (escritura/lectura del usuario)
        self.intro_video_path = os.path.join(self.input_path, "intro.mp4")
        self.outro_video_path = os.path.join(self.input_path, "outro.mp4")
        self.logo_path = os.path.join(self.input_path, "logo.webp")

        # Recursos empaquetados (solo lectura dentro del bundle)
        self.logo_file = resource_path("images/logo.png")

    def __str__(self):
        return (f"InitPaths(base_write_path={self.base_write_path}, "
                f"input={self.input_path}, output={self.output_path}, temp={self.temp_path})")



""" 
class InitPaths:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            # Path dentro del bundle de PyInstaller
            self.__base_path = sys._MEIPASS
        else:
            self.__base_path = os.getcwd() # en ejecutable PyInstaller
        self.allpaths= [f"{self.__base_path}/output", f"{self.__base_path}/input",  f"{self.__base_path}/temp"]
        self.__output_path= f"{self.__base_path}/output"
        self.__input_path= f"{self.__base_path}/input"
        self.__temp_path= f"{self.__base_path}/temp"
        self.__temp_video_path= f"{self.__base_path}/temp/viaje.mp4"
        self.__temp_video_to_generate_path= f"{self.__base_path}/temp/temp_video.mp4"
        self.__input_intro= f"{self.__base_path}/input/intro.mp4"
        self.__input_outro= f"{self.__base_path}/input/outro.mp4"
        self.__input_logo= f"{self.__base_path}/input/logo.webp"

    @property
    def base_path(self):
        return self.__base_path
    
    @property
    def output_path(self):
        return self.__output_path
    
    @property
    def input_path(self):
        return self.__input_path
    
    @property
    def temp_path(self):
        return self.__temp_path
    
    @property
    def generate_temp_video_path(self):
        return  self.__temp_video_to_generate_path
    
    @property
    def temp_video_path(self):
        return  self.__temp_video_path
    
    @property
    def intro_video_path(self):
        return  self.__input_intro
    
    @property
    def outro_video_path(self):
        return  self.__input_outro
    
    @property
    def logo_path(self):
        return  self.__input_logo
    
    def __str__(self) -> str:
        return f"InitPaths(base_path= {self.base_path}, temp_path= {self.temp_path}, output_path= {self.output_path}, input_path= {self.input_path})"

"""
class MakeDierctory:
    def make(self, path):
        os.mkdir(path)

class CheckDirectories(InitPaths, MakeDierctory):
    def __init__(self):
        InitPaths.__init__(self)
    
    def createDirectories(self, route):
        if not os.path.exists(route) : MakeDierctory.make(self, route)
    
    def checkAllDirectories(self):
        pass
               
    def checkFilesAndDirectories(self, route):
        return os.path.exists(route)

class FileNames:
    def __init__(self):
        self.__output_file_name= ""
        self.__input_file_name= ""
        self.__logo_file_name= ""
        self.__intro_file_name= ""
    
    @property
    def output_file_name(self):
        return self.__output_file_name
    
    @output_file_name.setter
    def output_file_name(self, value):
        self.__output_file_name = value

    @property
    def input_file_name(self):
        return self.__input_file_name
    
    @input_file_name.setter
    def input_file_name(self, value):
        self.__input_file_name = value

    @property
    def logo_file_name(self):
        return self.__logo_file_name
    
    @logo_file_name.setter
    def logo_file_name(self, value):
        self.__logo_file_name = value

    @property
    def intro_file_name(self):
        return self.__intro_file_name
    
    @intro_file_name.setter
    def intro_file_name(self, value):
        self.__intro_file_name = value

class DeleteFile:
    def __init__(self, file):
        os.remove(file)

class MoveFIles:
    def moveMp4(self, route, destination):
        try:
            if not CheckDirectories().checkFilesAndDirectories(InitPaths().input_path): os.mkdir(InitPaths().input_path)
            os.remove(destination) if os.path.exists(destination) else os.rename(route, destination)
            return {"success": True, "message": f"El archvio fue movido correctamente"}
        except Exception as e:
            return {"success": False, "message": e}

    def moveImg(self, route):
        try:
            img = Image.open(route)
            img.save(InitPaths().logo_path, "WEBP")
            return {"success": True, "message": f"El archvio fue convertido y movido correctamente"}
        except Exception as e:
            return {"success": False, "message": e}
        
class ShowFiles:
    def __init__(self) -> None:
        self.__system_name = sistema = platform.system()
        self.__atempts = AttemptsClass().attempts

    def __openFiles(self, file):
        if self.__system_name == "Windows":
            os.system(f'start "" "{file}"')
        else:  # MacOS
            subprocess.run(["open", file])

    def showInputFiles(self):
        return self.__atempts(self.__openFiles(InitPaths().input_path))
        
    def showOutputFiles(self):
        return self.__atempts(self.__openFiles(InitPaths().output_path))
        
    def showFile(self, file):
        return self.__atempts(self.__openFiles(file))
        