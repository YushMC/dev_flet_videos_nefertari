from pages.base import  FrameWindowPlace, LabelPack , EntryGrid, ButtonPack, FrameWindowGrid, ButtonGrid, FrameWindowPack, InputFilesWidget
from pages.select_files import SelectFilePageWindow
import tkinter as tk

class DirectorySelectedPage:
    def __init__(self, window, output_default) -> None:
        self.__file_page = SelectFilePageWindow(window,"Seleccionar carpeta de salida")
        self.__inputs_dialogs = InputFilesWidget()
        self.__frame_container= FrameWindowPlace(self.__file_page.instance,440, 300, 0.5, 0.5,"center")
        self.__email_label = LabelPack(self.__frame_container.instance, "Directorio de salida", "top", False, 5, 5)
        #input intro
        self._output_default =  output_default
        self.__father_container_intro = FrameWindowPack(self.__frame_container.instance, 0, 0,False, "center")
        self.__frame_intro_container= FrameWindowGrid(self.__father_container_intro.instance, 440, 50,"center")
        self.__frame_intro_container.set_row_size(0, 2)
        self.__frame_intro_container.set_row_size(1, 1)
        self.__frame_intro_container.set_column_size(0, 1)
        self.__video_intro_input = EntryGrid(self.__frame_intro_container.instance, 0,0 , 0, 0, "ew")
        self.__video_intro_input.instance.insert(0, self._output_default)
        self.__button_open_file_intro=  ButtonGrid(self.__frame_intro_container.instance, "Seleccionar carpeta",0,1, 0,0,"we")
        self.__button_open_file_intro.instance.configure(command= self.set_path_input)

        self.__button_check= ButtonPack(self.__frame_container.instance, "Continuar", "top", False, 0 ,1, 0,0)
        self.__file_page.instance.protocol("WM_DELETE_WINDOW", lambda: None)

    def set_path_input(self):
        self.__video_intro_input.instance.delete(0, tk.END)
        file_path = self.__inputs_dialogs.select_directory("Selecciona una carpeta de salida")
        file_path_value = file_path.get("directory_path", "")
        if not isinstance(file_path_value, str):
            file_path_value = str(file_path_value)

        if file_path_value != '':
            self.__video_intro_input.instance.insert(0, file_path_value)
        else:
            self.__video_intro_input.instance.insert(0, self._output_default)
            


    @property
    def instance(self):
        return self.__file_page.instance
    
    @instance.setter
    def instance(self, value):
        self.__file_page.instance = value

    @property
    def directory_path(self):
        return self.__video_intro_input.instance
    
    @directory_path.setter
    def directory_path(self, value):
        self.__video_intro_input.instance = value

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
