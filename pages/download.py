#importacion de tkinter
from utils.class_fetchs import RequestToLogin
import asyncio 
import tkinter as tk
from utils.class_attermpts import Response, AttemptsClass
from pages.base import  AllPages

class DownloadPageWindow(AllPages):
    def __init__(self, window_father: tk.Tk, title: str) -> None:
        self.__window = tk.Toplevel(window_father)
        self.__window.title(title)
        self.__attempts= AttemptsClass().attempts
        self.__window.resizable(False, False)
        #positions of father
        self.__x= window_father.winfo_x()
        self.__y= window_father.winfo_y()
        #sizes of father
        self.__w= window_father.winfo_width()
        self.__h= window_father.winfo_height()
        self.__window.geometry(f"{self.__w}x{self.__h}+{self.__x}+{self.__y}")
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
    
    def __str__(self) -> str:
        self.__window.update_idletasks() 
        return f"CreateInstanceToLoginPage(title={self.__window.title()}, geometry={self.__window.geometry()})"
    

