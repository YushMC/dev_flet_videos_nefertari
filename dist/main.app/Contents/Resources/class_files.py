import os, sys
import subprocess
from utils.class_attermpts import AttemptsClass
import platform
from PIL import Image

def resource_path(relative_path: str) -> str:
    """Devuelve la ruta correcta tanto en dev como en ejecutable"""
    if getattr(sys, "_MEIPASS", None):
        # Cuando corres el .exe/.app
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class InitPaths:
    def __init__(self):
        base = os.path.abspath(".")  # por defecto
        if hasattr(sys, "_MEIPASS"):
            base = sys._MEIPASS  # en ejecutable PyInstaller

        self.__base_path = base
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

class MakeDierctory:
    def make(self, path):
        os.mkdir(path)

class CheckDirectories(InitPaths, MakeDierctory):
    def __init__(self):
        InitPaths.__init__(self)
    
    def createDirectories(self, route):
        if not os.path.exists(route) : MakeDierctory.make(self, route)
    
    def checkAllDirectories(self):
        for route in self.allpaths:
            self.createDirectories(route)
               
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
        