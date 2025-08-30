from utils.class_files import CheckDirectories, InitPaths, DeleteFile, MoveFIles, ShowFiles
import os, sys
file_paths= InitPaths()
#os.makedirs(os.path.dirname(file_paths.logs), exist_ok=True)
#sys.stdout = open(file_paths.logs, "a")
#sys.stderr = open(file_paths.logs, "a")

from utils.class_fetchs import RequestToGetAllVideosToDownload, APIPaths, RequestToLogin
from utils.class_input_data import UserDataToLogin
from home import HomePage
from login import LoginPage
from download import DownloadPage
from file_selected import FileSelectedPage
from pages.base import  MessageBoxDialogs
import asyncio
import tkinter as tk

 
def checkInit(files_paths, check):
    #if not check.checkFilesAndDirectories(files_paths.temp_video_path): await downloadVideo("https://nefertari.s3.us-east-2.amazonaws.com/videos/viaje.mp4", files_paths)
    if check.checkFilesAndDirectories(files_paths.temp_video_to_generate_path): DeleteFile(files_paths.temp_video_to_generate_path)
    if check.checkFilesAndDirectories(files_paths.temp_video_path): DeleteFile(files_paths.temp_video_path)

def checkFilesVideos(files_paths: InitPaths, check:CheckDirectories):
    return True if check.checkFilesAndDirectories(files_paths.intro_video_path) and check.checkFilesAndDirectories(files_paths.outro_video_path) and  check.checkFilesAndDirectories(files_paths.logo_path) else False
api_paths = APIPaths()
user_data = UserDataToLogin("","")
check_files = CheckDirectories()
move_files= MoveFIles()
token_user = ""
trips= []
# Función de utilidad
def get_root():
    return tk.Tk()

# Inicio de tu aplicación
root = get_root()
#checkInit(file_paths, check_files)
main_window = HomePage(root,"Editor de Videos Nefertari", token_user, file_paths)

def login():
    if len(trips)==0: 
        
        MessageBoxDialogs(main_window.instance).show_message_warning("Advertencia", "No ha iniciado sesión, será redirigido a la ventana de incio de sesión")
        main_window.hide()
        login_page = LoginPage(main_window.instance)
        async def request():
            global trips
            user_data.email = login_page.email_input.get()
            user_data.password = login_page.password_input.get()
            response = await RequestToLogin(user_data, api_paths).sendRequest()

            if response["success"]:
                response2 = await RequestToGetAllVideosToDownload(response["token"], api_paths).sendRequest()
                if response2["success"]:
                    trips = response2["trips"]
                    login_page.delete()
                    main_window.show()
                    MessageBoxDialogs(main_window.instance).show_message_info("Correcto", response["message"])
                else:
                    MessageBoxDialogs(main_window.instance).show_message_error("Error", response["message"])
            else:
                MessageBoxDialogs(login_page.instance).show_message_error("Error", response["message"])

        def callback():
            asyncio.run(request())
        login_page.button_login.configure(command=callback)


    #FIXME: Continuar con la ventana de descarga
    elif not checkFilesVideos(file_paths, check_files):
        MessageBoxDialogs(main_window.instance).show_message_warning("Advertencia", "No se han detectado archivos importantes, será redirigido a la ventana de carga de archvivos")
        main_window.hide()
        files_page = FileSelectedPage(main_window.instance)

        def move_all_files():
            if files_page.video_intro_input.get() !='' and files_page.video_outro_input.get() !='' and files_page.logo_input.get() != '':
                move_files.moveMp4(files_page.video_intro_input.get(),file_paths.intro_video_path)
                move_files.moveMp4(files_page.video_outro_input.get(),file_paths.outro_video_path)
                move_files.moveImg(files_page.logo_input.get())
                MessageBoxDialogs(files_page.instance).show_message_info("Correcto", "los archivos se han cargado correctamente")
                main_window.show()
                files_page.delete()
            else:
                MessageBoxDialogs(files_page.instance).show_message_warning("Advertencia", "No se han detectado ubicaciones de archivos")

        files_page.button_check.configure(command=move_all_files)
        
    else:
        main_window.hide()
        download_page = DownloadPage(main_window.instance, trips, file_paths)
        def back_to_main():
            download_page.hide()
            main_window.show()
        download_page.button_back_to_main.configure(command=back_to_main)


def open_carpeta():
    respuesta= ShowFiles().showFile(file_paths.base_write_path)
    if not respuesta.success: print(respuesta.message)

main_window.button_crear_video.config(command=login)
main_window.button_abrir_carpeta.configure(command=open_carpeta)
main_window.start()


