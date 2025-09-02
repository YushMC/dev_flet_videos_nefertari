import tkinter as tk
from tkinter import ttk
import time

class SpinnerPage:
    def __init__(self, window_father, name) -> None:
        self.__spinner = tk.Toplevel(window_father)
        self.__spinner.title("Generando video")

        self.__spinner.resizable(False, False)
        #positions of father
        self.__x= window_father.winfo_x()
        self.__y= window_father.winfo_y()
        #sizes of father
        self.__w= window_father.winfo_width()
        self.__h= window_father.winfo_height()
        x = self.__x + (self.__w // 2) - (300 // 2)
        y = self.__y + (self.__h // 2) - (200 // 2)
        self.__spinner.geometry(f"300x200+{x}+{y}")
        self.__spinner.protocol("WM_DELETE_WINDOW", lambda: None)
        self.__spinner.attributes("-topmost", True)
        self.__message_video_name = tk.Label(self.__spinner, text=f"Video: {name}")
        self.__message_video_name.pack(pady=10)
        self.__message = tk.Label(self.__spinner, text="Estado: Descargando")
        self.__message.pack(pady=10)
        
        # Barra de progreso tipo spinner
        progress = ttk.Progressbar(self.__spinner, mode="indeterminate")
        progress.pack(pady=10, fill="x", padx=20)
        progress.start(10)  # velocidad de animación
        self.label_time = tk.Label(self.__spinner, text="Tiempo transcurrido:")
        self.label_time.pack(pady=10)
        self.label_timer = tk.Label(self.__spinner, text="00:00:00", font=("Helvetica", 20))
        self.label_timer.pack(pady=10)

        self.inicio = None
        self.en_ejecucion = False
        self.tiempo_transcurrido = 0
        self.start_timer()

    def start_timer(self):
        if not self.en_ejecucion:
            self.inicio = time.time() - self.tiempo_transcurrido
            self.en_ejecucion = True
            self.actualizar()


    def actualizar(self):
        if self.en_ejecucion:
            ahora = time.time()
            self.tiempo_transcurrido = ahora - self.inicio #type: ignore
            horas, resto = divmod(int(self.tiempo_transcurrido), 3600)
            minutos, segundos = divmod(resto, 60)
            self.label_timer.config(text=f"{horas:02}:{minutos:02}:{segundos:02}")
            self.__spinner.after(1000, self.actualizar)  # repetir cada segundo

    def detener_timer(self):
        self.en_ejecucion = False

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