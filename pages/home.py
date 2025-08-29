from pages.base import AllPages
from utils.class_attermpts import Response, AttemptsClass
import tkinter as tk
from PIL import Image, ImageTk
    
class MainPageWindow(AllPages):
    def __init__(self, title: str, width: int, height: int, url_icon) -> None:
        self.__window = tk.Tk()
        self.__window.title(title)
        self.__width= width
        self.__height= height
        self.__attempts= AttemptsClass().attempts
        self.__window.resizable(False, False)
        self.__init_center_position_main_window()
        self.__icon_img = ImageTk.PhotoImage(Image.open(url_icon))
        self.__window.iconphoto(True, self.__icon_img) #type: ignore
    # getters
    @property
    def instance(self):
        return self.__window
    
    @instance.setter
    def instance(self, value):
        self.__window = value
    
    @property
    def state_window(self) -> str:
        return self.__window.wm_state()
    
    #setters
    @state_window.setter
    def state_window(self, state: str):
        def __action():
            self.__window.wm_state(state)
        return self.__attempts(__action)

    #funciones 
    def start(self)-> Response:
        return self.__attempts(self.__window.mainloop)
    
    def __init_center_position_main_window(self):
        def __action():
            width_screen = self.__window.winfo_screenwidth()
            height_screen = self.__window.winfo_screenheight()
            position_x = round((width_screen /2) - (self.__width/2))
            position_y = round((height_screen /2) - (self.__height/2))
            self.__window.geometry(f"{self.__width}x{self.__height}+{position_x}+{position_y}")
        return self.__attempts(__action)
    
    def __str__(self) -> str:
        self.__window.update_idletasks() 
        return f"CreateInstanceToLoginPage(title={self.__window.title()}, geometry={self.__window.geometry()})"


