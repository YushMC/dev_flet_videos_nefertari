import tkinter as tk
from pages.base import ButtonPlace, ComboBoxVideoPack, FrameWindowPlace, LabelPack, MessageBoxDialogs
from pages.download import DownloadPageWindow
from pages.loading import SpinnerPage
from pages.progress_videos import Process1Logo, Process2Final
from utils.class_fetchs import ReequestToDownloadVideo
from utils.class_files import InitPaths, ShowFiles
from utils.class_videos import CreateVideosForAgency
import asyncio, threading
import random


class DownloadPage:
    def __init__(self, window, trips: list) -> None:
        self.__download_page = DownloadPageWindow(window,"Descargar Video")
        self.__button_back = ButtonPlace(self.__download_page.instance, "Regresar", 0.1, 0.05, "center", 100, 30)#type: ignore
        self.__frame_container = FrameWindowPlace(self.__download_page.instance, 400, 200, 0.5, 0.5, "center")
        self.__instruction_label = LabelPack(self.__frame_container.instance, "Selecciona un video de la lista", "top", False, 5, 5)
        self.__combo_box = ComboBoxVideoPack(self.__frame_container.instance, trips, "top", True)
        self.__combo_box.instance.pack_configure(fill="x")
        self.__button_download = ButtonPlace(self.__frame_container.instance, "Descargar", 0.5, 0.8, "center", 100, 30)
        self.__button_download.instance.configure(command=self.get_url)
        self.__download_page.instance.protocol("WM_DELETE_WINDOW", window.destroy)

    def get_url(self):
        """Ejecuta todo el proceso en orden dentro de un hilo para no bloquear Tkinter"""
        response = self.__combo_box.selected_item()
        if not response["success"]:
            MessageBoxDialogs(self.__download_page.instance).show_message_error("Error", "No se seleccionó ningún video")
            return

        threading.Thread(target=self.__process_video, args=(response["url_video"],response["name"]), daemon=True).start()

    def __process_video(self, video_url, name):
        """Hilo que ejecuta todo el flujo asincrónicamente"""
        asyncio.run(self.__wrapper(video_url, name))

    async def __wrapper(self, video_url, name):
        # 1️⃣ Spinner mientras se descarga el video
        self.__download_page.instance.attributes("-alpha", 0.9)
        loading_download = SpinnerPage(self.__download_page.instance)
        await self.__download_video(video_url)
        self.__download_page.instance.after(0, loading_download.delete)

        # 2️⃣ Spinner para crear logo
        loading_logo = Process1Logo(self.__download_page.instance)
        await self.__create_video_logo()
        self.__download_page.instance.after(0, loading_logo.delete)

        # 3️⃣ Spinner para generar video final
        loading_final = Process2Final(self.__download_page.instance)
        resp_final = await self.__create_video_final(name)
        self.__download_page.instance.after(0, loading_final.delete)
        MessageBoxDialogs(self.__download_page.instance).show_message_info("Final", resp_final["message"])
        respuesta= ShowFiles().showFile(resp_final["ubication"])
        if not respuesta.success: print(respuesta.message)
        self.__download_page.instance.attributes("-alpha", 1)

    async def __download_video(self, url):
        response = await ReequestToDownloadVideo(url, InitPaths()).sendRequest()
        return response["message"]

    async def __create_video_logo(self):
        response = await CreateVideosForAgency(InitPaths()).createVideWithLogo()
        return {"success": response["success"], "message": response["message"]}

    async def __create_video_final(self, name):
        texto_base4 = ''.join(str(random.randint(0, 9)) for _ in range(4))
        str_name = f'video_{name}_{texto_base4}.mp4'
        response = await CreateVideosForAgency(InitPaths()).joinVideos(str_name)
        return {"success": response["success"], "message": response["message"], "ubication": f"{InitPaths().output_path}/{str_name}"}

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
