from pages.base import  FrameWindowPack, FrameWindowGrid , ButtonGrid, ImageLogoPack
from utils.class_files import InitPaths
from pages.home import MainPageWindow

class HomePage:
    def __init__(self, root, titulo, token, paths) -> None:
        self.__paths= paths
        self.__main_window = MainPageWindow(root,titulo, 500, 400, self.__paths.logo_file)
        self.__frame_for_image = FrameWindowPack(self.__main_window.instance,400, 300, False, "center")
        self.__image_logo = ImageLogoPack(self.__frame_for_image.instance, self.__paths.logo_file,300 ,200,"top", True)

        self.__frame_bottom = FrameWindowPack(self.__main_window.instance, 0,0, True, "center")

        self.__frame_for_buttons= FrameWindowGrid(self.__frame_bottom.instance, 400, 100, "center")
        self.__button_crear_video = ButtonGrid(self.__frame_for_buttons.instance, "Crear Video",0,0, 0,0,"we")
        self.__button_abrir_carpeta = ButtonGrid(self.__frame_for_buttons.instance, "Abrir Carpeta",0,1, 0,0,"we")
        self.__frame_for_buttons.amount_columns_responsives(2)
        self.__frame_for_buttons.amount_rows_responsives(1)
        self.__token= token

    @property
    def instance(self):
        return self.__main_window.instance
    
    @instance.setter
    def instance(self, value):
        self.__main_window.instance = value

    @property
    def button_crear_video(self):
        return self.__button_crear_video.instance

    @button_crear_video.setter
    def button_crear_video(self, value):
        self.__button_crear_video.instance = value

    @property
    def button_abrir_carpeta(self):
        return self.__button_abrir_carpeta.instance
    
    @button_abrir_carpeta.setter
    def button_abrir_carpeta(self, value):
        self.__button_abrir_carpeta.instance = value

    def start(self):
        self.__main_window.start()

    def hide(self):
        self.__main_window.instance.withdraw()

    def show(self):
        self.__main_window.instance.deiconify()

    def delete(self):
        self.__main_window.instance.destroy()
