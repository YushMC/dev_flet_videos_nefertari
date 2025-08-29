from utils.class_files import CheckDirectories, InitPaths, DeleteFile
from utils.class_fetchs import RequestToGetAllVideosToDownload, ReequestToDownloadVideo, APIPaths, RequestToLogin
from utils.class_videos import CreateVideosForAgency
from utils.class_input_data import UserDataToLogin
from home import HomePage
from login import LoginPage
from pages.login import LoginPageWindow
from pages.base import  FrameWindowPlace, MessageBoxDialogs, LabelPack, EntryPack
import asyncio

async def getAllVideos(login_data, paths) -> bool:
    result = RequestToGetAllVideosToDownload(login_data, paths)
    if not await result.sendRequest() : raise  Exception(result.message)
    return True

async def downloadVideo(url, paths) -> bool:
    download = ReequestToDownloadVideo(url, paths)
    if not await download.sendRequest(): raise  Exception(download.message)
    return True

 
async def crearVideos(files_paths):
    final_video = CreateVideosForAgency(files_paths, "viaje_final.mp4")
    print("Video Listo") if await final_video.createVideo() else print("Ocurrio un error")

async def checkInit(files_paths, check):
    #if not check.checkFilesAndDirectories(files_paths.temp_video_path): await downloadVideo("https://nefertari.s3.us-east-2.amazonaws.com/videos/viaje.mp4", files_paths)
    if check.checkFilesAndDirectories(files_paths.generate_temp_video_path): DeleteFile(files_paths.generate_temp_video_path)
    if check.checkFilesAndDirectories(files_paths.temp_video_path): DeleteFile(files_paths.temp_video_path)

api_paths = APIPaths()
user_data = UserDataToLogin("","")
#response = RequestToLogin(user_data, api_paths)
token_user = ""
main_window = HomePage("Nefertari Videos", token_user)

def login():
    if token_user == '': 
        main_window.instance.withdraw()
        login_page = LoginPage(main_window.instance)
        async def request():
            global token_user
            user_data.email = login_page.email_input.get()
            user_data.password = login_page.password_input.get()
            response = await RequestToLogin(user_data, api_paths).sendRequest()

            if response["success"]:
                token_user = response["token"]
                login_page.instance.destroy()
                main_window.instance.deiconify()
                MessageBoxDialogs(main_window.instance).show_message_info("Correcto", response["message"])
            else:
                MessageBoxDialogs(login_page.instance).show_message_error("Error", response["message"])

        def callback():
            asyncio.run(request())
        
        login_page.button_login.configure(command=callback)
    else: MessageBoxDialogs(main_window.instance).show_message_info("Bienvenido", "Esto es una prueba")




main_window.button_crear_video.config(command=login)
main_window.start()






""" 
if __name__ == "__main__":
    asyncio.run(run_app())

"""