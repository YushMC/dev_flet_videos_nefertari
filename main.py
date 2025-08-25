from utils.class_files import CheckDirectories, InitPaths, DeleteFile
from utils.class_fetchs import RequestToGetAllVideosToDownload, ReequestToDownloadVideo
from utils.class_videos import CreateVideosForAgency
from views.home import HomeView
from views.loadFiles import LoadFiles
import flet as ft
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

async def main(page: ft.Page):
    check = CheckDirectories()
    check.checkAllDirectories()
    files_paths = InitPaths()
    await checkInit(files_paths, check)
    ##configurations
    page.title= "Nefertari Editor de Videos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # FilePickers como atributos de clase
    #file_picker_1 = ft.FilePicker()
    #file_picker_2 = ft.FilePicker()
    #file_picker_3 = ft.FilePicker()
    
    # IMPORTANTE: agregar FilePickers a la page principal

    #page.overlay.extend([file_picker_1, file_picker_2, file_picker_3])
    #page.update()
    #init views
    if check.checkFilesAndDirectories(files_paths.intro_video_path) and check.checkFilesAndDirectories(files_paths.outro_video_path) and check.checkFilesAndDirectories(files_paths.logo_path):
        home_page = HomeView(page)
        page.views.append(await home_page.get_view())
        page.go("/home")
    else:
        files_page = LoadFiles(page)
        page.views.append(await files_page.get_view())
        page.go("/files")
    
async def run_app():
    await ft.app_async(main)

if __name__ == "__main__":
    asyncio.run(run_app())