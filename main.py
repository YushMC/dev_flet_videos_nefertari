from utils.class_files import CheckDirectories, InitPaths, DeleteFile
from utils.class_input_data import UserDataToLogin
from utils.class_fetchs import RequestToLogin, APIPaths, RequestToGetAllVideosToDownload, ReequestToDownloadVideo
from utils.class_videos import CreateVideosForAgency

import asyncio

async def getAllVideos(login_data, paths) -> bool:
    result = RequestToGetAllVideosToDownload(login_data, paths)
    if not await result.sendRequest() : raise  Exception(result.message)
    return True
    """ 
    for video in result.trips:
        print(video["key_video"])
    """

async def downloadVideo(url, paths) -> bool:
    download = ReequestToDownloadVideo(url, paths)
    if not await download.sendRequest(): raise  Exception(download.message)
    return True


async def main():
    check = CheckDirectories()
    check.checkAllDirectories()
    api_paths = APIPaths()
    files_paths = InitPaths()
    """ 
    login = RequestToLogin(UserDataToLogin(input("Ingresa tu correo electronico: \n"), input("Ingresa tu contraseña: \n")),api_paths)

    if not await login.sendRequest(): raise  Exception(login.message)
   
    await getAllVideos(login, api_paths)
     """
    if not check.checkFilesAndDirectories(files_paths.temp_video_path): await downloadVideo("https://nefertari.s3.us-east-2.amazonaws.com/videos/viaje.mp4", files_paths)

    if check.checkFilesAndDirectories(files_paths.generate_temp_video_path): DeleteFile(files_paths.generate_temp_video_path)

    final_video = CreateVideosForAgency(files_paths, "viaje_final.mp4")

    print("Video Listo") if await final_video.createVideo() else print("Ocurrio un error")

    



asyncio.run(main())