from pages.base import  FrameWindowPlace, LabelPack , EntryGrid, ButtonPack, FrameWindowGrid, ButtonGrid, FrameWindowPack, InputFilesWidget
from pages.select_files import SelectFilePageWindow
import tkinter as tk

class FileSelectedPage:
    def __init__(self, window) -> None:
        self.__file_page = SelectFilePageWindow(window,"Cargar archivos")
        self.__inputs_dialogs = InputFilesWidget()
        self.__frame_container= FrameWindowPlace(self.__file_page.instance,350, 300, 0.5, 0.5,"center")

        self.__email_label = LabelPack(self.__frame_container.instance, "Video introductorio", "top", False, 5, 5)
        #input intro
        self.__father_container_intro = FrameWindowPack(self.__frame_container.instance, 0, 0,False, "center")
        self.__frame_intro_container= FrameWindowGrid(self.__father_container_intro.instance, 350, 50,"center")
        self.__frame_intro_container.set_row_size(0, 2)
        self.__frame_intro_container.set_row_size(1, 1)
        self.__frame_intro_container.set_column_size(0, 1)
        self.__video_intro_input = EntryGrid(self.__frame_intro_container.instance, 0,0 , 0, 0, "ew")
        self.__button_open_file_intro=  ButtonGrid(self.__frame_intro_container.instance, "Abrir",0,1, 0,0,"we")
        self.__button_open_file_intro.instance.configure(command=lambda: self.set_path_input(1))

        self.__password_label = LabelPack(self.__frame_container.instance, "Video de cierre", "top", False, 5, 5)

        self.__father_container_outro = FrameWindowPack(self.__frame_container.instance, 0, 0,False, "center")
        self.__frame_outro_container= FrameWindowGrid(self.__father_container_outro.instance, 350, 50,"center")
        self.__frame_outro_container.set_row_size(0, 2)
        self.__frame_outro_container.set_row_size(1, 1)
        self.__frame_outro_container.set_column_size(0, 1)
        self.__video_outro_input = EntryGrid(self.__frame_outro_container.instance, 0,0 , 0, 0, "ew")
        self.__button_open_file_outro=  ButtonGrid(self.__frame_outro_container.instance, "Abrir",0,1, 0,0,"we")
        self.__button_open_file_outro.instance.configure(command=lambda: self.set_path_input(2))

        self.__agency_label = LabelPack(self.__frame_container.instance, "Logo de la agencia", "top", False, 5, 5)

        self.__father_container_logo = FrameWindowPack(self.__frame_container.instance, 0, 0,False, "center")
        self.__frame_logo_container= FrameWindowGrid(self.__father_container_logo.instance, 350, 50,"center")
        self.__frame_logo_container.set_row_size(0, 2)
        self.__frame_logo_container.set_row_size(1, 1)
        self.__frame_logo_container.set_column_size(0, 1)
        self.__logoo_input = EntryGrid(self.__frame_logo_container.instance, 0,0 , 0, 0, "ew")
        self.__button_open_file_logo=  ButtonGrid(self.__frame_logo_container.instance, "Abrir",0,1, 0,0,"we")
        self.__button_open_file_logo.instance.configure(command=lambda: self.set_path_input(3))

        self.__button_check= ButtonPack(self.__frame_container.instance, "Continuar", "top", False, 0 ,1, 0,0)
        self.__file_page.instance.protocol("WM_DELETE_WINDOW", lambda: None)

    def set_path_input(self, opcion):
        match opcion:
            case 1:
                self.__video_intro_input.instance.delete(0, tk.END)
                file_path = self.__inputs_dialogs.select_video_file("Selecciona un video")
                file_path_value = file_path.get("file_path", "")
                if not isinstance(file_path_value, str):
                    file_path_value = str(file_path_value)
                self.__video_intro_input.instance.insert(0, file_path_value)
            case 2:
                self.__video_outro_input.instance.delete(0, tk.END)
                file_path = self.__inputs_dialogs.select_video_file("Selecciona un video")
                file_path_value = file_path.get("file_path", "")
                if not isinstance(file_path_value, str):
                    file_path_value = str(file_path_value)
                self.__video_outro_input.instance.insert(0, file_path_value)
            case 3:
                self.__logoo_input.instance.delete(0, tk.END)
                file_path = self.__inputs_dialogs.select_image_file("Selecciona una imagen")
                file_path_value = file_path.get("file_path", "")
                if not isinstance(file_path_value, str):
                    file_path_value = str(file_path_value)
                self.__logoo_input.instance.insert(0, file_path_value)



    @property
    def instance(self):
        return self.__file_page.instance
    
    @instance.setter
    def instance(self, value):
        self.__file_page.instance = value

    @property
    def video_intro_input(self):
        return self.__video_intro_input.instance
    
    @video_intro_input.setter
    def video_intro_input(self, value):
        self.__video_intro_input.instance = value

    @property
    def video_outro_input(self):
        return self.__video_outro_input.instance
    
    @video_outro_input.setter
    def video_outro_input(self, value):
        self.__video_outro_input.instance = value

    @property
    def logo_input(self):
        return self.__logoo_input.instance
    
    @logo_input.setter
    def logo_input(self, value):
        self.__logoo_input.instance= value

    @property
    def button_check(self):
        return self.__button_check.instance
    
    @button_check.setter
    def button_check(self, value):
        self.__button_check.instance = value

    def hide(self):
        self.__file_page.instance.withdraw()

    def show(self):
        self.__file_page.instance.deiconify()

    def delete(self):
        self.__file_page.instance.destroy()
