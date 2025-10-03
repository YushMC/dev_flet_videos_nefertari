import tkinter as tk
from pages.base import ButtonPlace, ComboBoxVideoPack, FrameWindowPlace, LabelPack, MessageBoxDialogs, ButtonPack, ComboBoxSizeVideoPack
from pages.download import DownloadPageWindow
from pages.loading import SpinnerPage
from utils.class_fetchs import ReequestToDownloadVideo
from utils.class_files import ShowFiles
from utils.class_videos import CreateVideosForAgency
import asyncio, threading
import random
import os


class DownloadPage:
    def __init__(self, window, trips: list,optionsList: list, paths, output_dir) -> None:
        self.__paths = paths
        self.output_dir= output_dir
        self._spinner = None
        self.__create_videos_for_agency = CreateVideosForAgency(self.__paths, self.output_dir)
        self.__download_page = DownloadPageWindow(window,"Descargar Video")
        self.__button_back = ButtonPlace(self.__download_page.instance, "Regresar", 0.1, 0.05, "center", 100, 30)#type: ignore
        self.__frame_container = FrameWindowPlace(self.__download_page.instance, 400, 300, 0.5, 0.5, "center")
        self.__instruction_label = LabelPack(self.__frame_container.instance, "Selecciona un video de la lista", "top", False, 5, 5)
        self.__combo_box = ComboBoxVideoPack(self.__frame_container.instance, trips, "top", True)
        self.__combo_box.instance.pack_configure(fill="x")
        self.__instruction_label = LabelPack(self.__frame_container.instance, "Selecciona el tamaño del video final", "top", False, 5, 5)
        self.__combo_box_size = ComboBoxSizeVideoPack(self.__frame_container.instance, optionsList, "top", True)
        self.__combo_box_size.instance.pack_configure(fill="x")
        self.__button_download = ButtonPack(self.__frame_container.instance, "Descargar", "top", False, 0 ,1, 0,0)
        self.__button_download.instance.configure(command=self.get_url)
        self.__download_page.instance.protocol("WM_DELETE_WINDOW", window.destroy)
        self.size_selected = ""

    def get_url(self):
        """Ejecuta todo el proceso en orden dentro de un hilo para no bloquear Tkinter"""
        self.hide()

        responseSize = self.__combo_box_size.selected_item()
        if not responseSize["success"]:
            MessageBoxDialogs(self.__download_page.instance).show_message_error("Error", "No se seleccionó ningún tamaño de video")
            self.show()
            return

        response = self.__combo_box.selected_item()
        if not response["success"]:
            MessageBoxDialogs(self.__download_page.instance).show_message_error("Error", "No se seleccionó ningún video")
            self.show()
            return
        
        self.size_selected = responseSize["size"]

        # Ejecutar la corrutina en el loop principal de asyncio, no en un nuevo hilo
        threading.Thread(target=lambda: asyncio.run(self.__process_video(response["url_video"], response["name"])),daemon=True).start()

    async def __process_video(self, video_url, name):
        """Hilo que ejecuta todo el flujo asincrónicamente"""
        await self.__wrapper(video_url, name)

    async def __wrapper(self, video_url, name):
        # 1️⃣ Spinner mientras se descarga el video
        
        # Usar un solo spinner
        if self._spinner is None or not self._spinner.instance.winfo_exists():
           self._spinner = SpinnerPage(self.__download_page.instance, name)
        else:
            self._spinner.instance.lift()
        await self.__download_video(video_url)

        # 2️⃣ Spinner para crear logo
        self.__download_page.instance.after(0, lambda: self._spinner.message_spinner.configure(text="Estado: Agregando logo"))#type: ignore
        await self.__create_video_logo()
        

        # 3️⃣ Spinner para generar video final
        self.__download_page.instance.after(0, lambda: self._spinner.message_spinner.configure(text="Estado: Generando Video"))#type: ignore
        resp_final = await self.__create_video_final(name)
        #self.__download_page.instance.after(0, self._spinner.delete)
        
        
        def restore_ui():
            self._spinner.detener_timer()#type:ignore
            self._spinner.delete()#type: ignore
            self.show()
            MessageBoxDialogs(self.__download_page.instance).show_message_info("Final", resp_final["message"])
            respuesta= ShowFiles().showFile(resp_final["ubication"])
            if not respuesta.success: print(respuesta.message)
        
        self.__download_page.instance.after(0, restore_ui)

    async def __download_video(self, url):
        response = await ReequestToDownloadVideo(url,self.__paths).sendRequest()
        return response["message"]

    async def __create_video_logo(self):
        response = await self.__create_videos_for_agency.createVideWithLogo()
        return {"success": response["success"], "message": response["message"]}

    async def __create_video_final(self, name):
        texto_base4 = ''.join(str(random.randint(0, 9)) for _ in range(5))
        str_name = f'video_{name}_{texto_base4}.mp4'
        response = await self.__create_videos_for_agency.joinVideos(str_name, self.size_selected)
        return {"success": response["success"], "message": response["message"], "ubication": f"{os.path.join(self.output_dir, str_name)}"}

    @property 
    def instance(self): 
        return self.__download_page.instance
        
    @instance.setter 
    def instance(self, value): 
        self.__download_page.instance = value 
        
    @property 
    def select(self): 
        return self.__combo_box.instance 
    
    @select.setter 
    def email_input(self, value): 
        self.__combo_box.instance = value 
        
    @property 
    def button_back_to_main(self): 
        return self.__button_back.instance 
    
    @button_back_to_main.setter 
    def button_back_to_main(self, value): 
        self.__button_back.instance = value 
        
    @property 
    def button_download(self): 
        return self.__button_download.instance 
    
    @button_download.setter 
    def button_download(self, value): 
        self.__button_download.instance = value 
        
    def hide(self): self.__download_page.instance.withdraw() 
        
    def show(self): self.__download_page.instance.deiconify() 
    
    def delete(self): self.__download_page.instance.destroy()
