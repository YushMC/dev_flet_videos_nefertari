from utils.class_files import CheckDirectories, InitPaths, DeleteFile, MoveFIles, ShowFiles
import os, sys
file_paths= InitPaths()
#os.makedirs(os.path.dirname(file_paths.logs), exist_ok=True)
#sys.stdout = open(file_paths.logs, "a")
#sys.stderr = open(file_paths.logs, "a")

from utils.class_fetchs import RequestToGetAllVideosToDownload, APIPaths, RequestToLogin
from utils.class_check_init_files import ConfigFileValues
from utils.class_input_data import UserDataToLogin
from home import HomePage
from login import LoginPage
from download import DownloadPage
from file_selected import FileSelectedPage
from select_directory_output import DirectorySelectedPage
from pages.base import  MessageBoxDialogs
import asyncio
import tkinter as tk
import shutil

 
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
config_file_data= ConfigFileValues(file_paths, check_files)
token_user = ""
trips= []
# Función de utilidad
def get_root():
    return tk.Tk()

# Inicio de tu aplicación
root = get_root()

checkInit(file_paths, check_files)
config_file_data.loadFile()

main_window = HomePage(root,"Editor de Videos Nefertari", file_paths)


async def getVideos():
    global trips
    response_to_videos = await RequestToGetAllVideosToDownload(config_file_data.token, api_paths).sendRequest()
    if response_to_videos["success"]: trips = response_to_videos["trips"]

asyncio.run(getVideos())
def check_conditions():
    global trips
    
    if len(trips) == 0: 
        main_window.hide()
        MessageBoxDialogs(main_window.instance).show_message_warning(
            "Advertencia",
            "No ha iniciado sesión, será redirigido a la ventana de inicio de sesión"
        )
        login_page = LoginPage(main_window.instance)
        login_page.show()

        async def request():
            global trips
            user_data.email = login_page.email_input.get()
            user_data.password = login_page.password_input.get()
            response = await RequestToLogin(user_data, api_paths).sendRequest()
            if response["success"]:
                config_file_data.token = response["token"]
                config_file_data.saveConfigData()
                response2 = await RequestToGetAllVideosToDownload(response["token"], api_paths).sendRequest()
                if response2["success"]:
                    trips = response2["trips"]
                    login_page.delete()
                    MessageBoxDialogs(main_window.instance).show_message_info("Correcto", response["message"])
                    main_window.show()
                    # 🔄 Vuelve a comprobar después de loguear
                    check_conditions()
                else:
                    MessageBoxDialogs(main_window.instance).show_message_error("Error", response["message"])
                    main_window.delete()
            else:
                MessageBoxDialogs(login_page.instance).show_message_error("Error", response["message"])
                main_window.delete()

        def callback():
            asyncio.run(request())

        login_page.button_login.configure(command=callback)

    elif not checkFilesVideos(file_paths, check_files):
        main_window.hide()
        MessageBoxDialogs(main_window.instance).show_message_warning(
            "Advertencia",
            "No se han detectado archivos importantes, será redirigido a la ventana de carga de archivos"
        )
        files_page = FileSelectedPage(main_window.instance)
        files_page.show()

        def move_all_files():
            if (files_page.video_intro_input.get() != '' 
                and files_page.video_outro_input.get() != '' 
                and files_page.logo_input.get() != ''):
                
                move_files.moveMp4(files_page.video_intro_input.get(), file_paths.intro_video_path)
                move_files.moveMp4(files_page.video_outro_input.get(), file_paths.outro_video_path)
                move_files.moveImg(files_page.logo_input.get())
                
                MessageBoxDialogs(files_page.instance).show_message_info("Correcto", "Los archivos se han cargado correctamente")
                files_page.delete()
                main_window.show()
                
                # 🔄 Vuelve a comprobar después de cargar archivos
                check_conditions()
            else:
                MessageBoxDialogs(files_page.instance).show_message_warning("Advertencia", "No se han detectado ubicaciones de archivos")

        files_page.button_check.configure(command=move_all_files)

    elif check_files.checkFilesAndDirectories(file_paths.output_path) and config_file_data.output_path == '':
        main_window.hide()
        response = MessageBoxDialogs(main_window.instance).show_message_confirmation(
            "Importante",
            "Se ha detectado una carpeta de salida de antiguas versiones, ¿Deseas cambiar de ubicación?"
        )
        if not response:
            config_file_data.output_path = file_paths.output_path
            config_file_data.saveConfigData()
            MessageBoxDialogs(main_window.instance).show_message_info("Correcto", "Se utilizará la ubicación por defecto.")
            main_window.show()
        else:
            directory_page = DirectorySelectedPage(main_window.instance, file_paths.output_path)
            directory_page.show()

            def move_all_files():
                route_dir = directory_page.directory_path.get()
                if route_dir != '':
                    os.makedirs(directory_page.directory_path.get(), exist_ok=True)
                    shutil.move(file_paths.output_path, directory_page.directory_path.get())
                    config_file_data.output_path = os.path.join(directory_page.directory_path.get(), "output")
                    config_file_data.saveConfigData()
                    directory_page.delete()
                    main_window.show()
                    MessageBoxDialogs(main_window.instance).show_message_info(
                        "Correcto",
                        "Se ha cambiado la ubicación y los archivos se han trasladado correctamente."
                    )
                else:
                    MessageBoxDialogs(main_window.instance).show_message_error(
                        "Error",
                        "No se ha seleccionado una carpeta de salida"
                    )
                # 🔄 Vuelve a comprobar después de mover directorio
            directory_page.button_check.configure(command=move_all_files)

    elif config_file_data.output_path == '':
        main_window.hide()
        MessageBoxDialogs(main_window.instance).show_message_info(
            "Importante",
            "Seleccione una carpeta de salida, se colocará una ruta por defecto"
        )
        directory_page = DirectorySelectedPage(main_window.instance, file_paths.output_path)
        directory_page.show()

        def move_all_files():
            route_dir = directory_page.directory_path.get()
            if route_dir != '':
                os.makedirs(os.path.join(directory_page.directory_path.get(), "output"), exist_ok=True)
                config_file_data.output_path = os.path.join(directory_page.directory_path.get(), "output")
                config_file_data.saveConfigData()
                directory_page.delete()
                main_window.show()
                MessageBoxDialogs(main_window.instance).show_message_info(
                    "Correcto",
                    "Se ha cambiado la ubicación y los archivos se han trasladado correctamente."
                )
            else:
                MessageBoxDialogs(main_window.instance).show_message_error(
                    "Error",
                    "No se ha seleccionado una carpeta de salida"
                )
            
            # 🔄 Vuelve a comprobar después de mover directorio

        directory_page.button_check.configure(command=move_all_files)

        
check_conditions()


def create_video():
    main_window.hide()
    download_page = DownloadPage(main_window.instance, trips, file_paths, config_file_data.output_path)
    def back_to_main():
        download_page.hide()
        main_window.show()
    download_page.button_back_to_main.configure(command=back_to_main)


def open_carpeta():
    respuesta= ShowFiles().showFile(config_file_data.output_path)
    if not respuesta.success: print(respuesta.message)

def change():
    main_window.hide
    directory_page = DirectorySelectedPage(main_window.instance, "")
    directory_page.instance.protocol("WM_DELETE_WINDOW", directory_page.instance.destroy)
    def move_all_files():
        os.makedirs(os.path.dirname(directory_page.directory_path.get()), exist_ok=True)
        shutil.move(config_file_data.output_path, directory_page.directory_path.get())
        config_file_data.output_path = os.path.join(directory_page.directory_path.get(),"output")
        config_file_data.saveConfigData()
        directory_page.delete()
        main_window.show()
        MessageBoxDialogs(main_window.instance).show_message_info("Correcto", "Archivos movidos correctamente.")
    directory_page.button_check.configure(command=move_all_files)
    def back_to_main():
        directory_page.hide()
        main_window.show()
    directory_page.button_back.configure(command=back_to_main)

main_window.button_crear_video.config(command=create_video)
main_window.button_abrir_carpeta.configure(command=open_carpeta)
main_window.button_cambiar_carpeta.instance.configure(command=change)


main_window.start()


