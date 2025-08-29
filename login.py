from pages.base import  FrameWindowPlace, LabelPack , EntryPack, ButtonPack
from pages.login import LoginPageWindow
import tkinter as tk

class LoginPage:
    def __init__(self, window) -> None:
        self.__login_page = LoginPageWindow(window,"Iniciar Sesión")
        self.__frame_container= FrameWindowPlace(self.__login_page.instance,300, 200, 0.5, 0.5,"center")
        self.__email_label = LabelPack(self.__frame_container.instance, "Correo Electónico", "top", False, 5, 5)
        self.__email_input = EntryPack(self.__frame_container.instance, "top", False, 300)
        self.__password_label = LabelPack(self.__frame_container.instance, "Contraseña", "top", False, 5, 5)
        self.__password_input = EntryPack(self.__frame_container.instance, "top", False, 300)
        self.__button_login= ButtonPack(self.__frame_container.instance, "Entrar", "top", False, 0 ,1, 0,0)
        self.__login_page.instance.protocol("WM_DELETE_WINDOW", window.destroy)

    @property
    def instance(self):
        return self.__login_page.instance
    
    @instance.setter
    def instance(self, value):
        self.__login_page.instance = value

    @property
    def email_input(self):
        return self.__email_input.instance
    
    @email_input.setter
    def email_input(self, value):
        self.__email_input.instance = value

    @property
    def password_input(self):
        return self.__password_input.instance
    
    @password_input.setter
    def password_input(self, value):
        self.__password_input.instance = value

    @property
    def button_login(self):
        return self.__button_login.instance
    
    @button_login.setter
    def button_login(self, value):
        self.__button_login.instance = value

    def hide(self):
        self.__login_page.instance.withdraw()

    def show(self):
        self.__login_page.instance.deiconify()

    def delete(self):
        self.__login_page.instance.destroy()
