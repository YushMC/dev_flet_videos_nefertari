import tkinter as tk
from tkinter import ttk

class SpinnerPage:
    def __init__(self, window_father) -> None:
        self.__spinner = tk.Toplevel(window_father)
        self.__spinner.title("Procesando...")
        self.__spinner.transient(window_father)  # Siempre encima de root
        self.__spinner.grab_set()       # Bloquea interacción con root

        self.__spinner.resizable(False, False)
        #positions of father
        self.__x= window_father.winfo_x()
        self.__y= window_father.winfo_y()
        #sizes of father
        self.__w= window_father.winfo_width()
        self.__h= window_father.winfo_height()
        self.__spinner.overrideredirect(True) 
        self.__spinner.focus_set()
        self.__spinner.focus_force()
        x = self.__x + (self.__w // 2) - (300 // 2)
        y = self.__y + (self.__h // 2) - (200 // 2)
        self.__spinner.geometry(f"300x200+{x}+{y}")
        self.__spinner.protocol("WM_DELETE_WINDOW", lambda: None)

        self.__message = tk.Label(self.__spinner, text="Descargando video...")
        self.__message.pack(pady=10)

        # Barra de progreso tipo spinner
        progress = ttk.Progressbar(self.__spinner, mode="indeterminate")
        progress.pack(pady=10, fill="x", padx=20)
        progress.start(10)  # velocidad de animación

    def delete(self):
        self.__spinner.destroy()

    @property
    def instance(self):
        return self.__spinner
    
    @instance.setter
    def instance(self, value):
        self.__spinner = value

    @property
    def message_spinner(self):
        return self.__message
    
    @message_spinner.setter
    def message_spinner(self, value):
        self.__message = value