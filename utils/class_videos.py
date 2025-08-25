
from moviepy import  * #type: ignore
import asyncio
from abc import ABC, abstractmethod


class CreateVideos:
    @abstractmethod
    async def start(self) -> dict:
        pass

class CreateFinalVideo(CreateVideos):
    def __init__(self, paths, name):
        self.__intro = VideoFileClip(paths.intro_video_path)
        self.__outro = VideoFileClip(paths.outro_video_path)
        self.__temp= VideoFileClip(paths.generate_temp_video_path)
        self.__output = paths.output_path
        self.__name= name
        self.__final_clip = ""

    def __concatenate(self):
        self.__intro = self.__intro.subclipped(0, self.__intro.duration - 0.01)
        self.__outro = self.__outro.subclipped(0, self.__outro.duration - 0.01)
        self.__temp = self.__temp.subclipped(0, self.__temp.duration - 0.01)
        self.__final_clip = concatenate_videoclips([self.__intro, self.__temp, self.__outro], method="compose") # type: ignore

    async def start(self)-> dict:
        self.__concatenate()
        try:
            await asyncio.to_thread(self.__final_clip.write_videofile, f"{self.__output}/{self.__name}") #type: ignore
            self.__intro.close()
            self.__temp.close()
            self.__outro.close()
            self.__final_clip.close()#type: ignore
            return {"success": True, "message": f"Video Guardado en: {self.__name}"}
        except Exception as e:
            return {"success": False, "message":  f"Ourrio un error: {e}"} 


class AddLogoToVideo(CreateVideos):
    def __init__(self, paths):
        self.__video = paths.temp_video_path
        self.__logo = paths.logo_path
        self.__temp= paths.generate_temp_video_path
        self.__background= ""
        self.__logo_create= ""
        self.__final_clip = ""

    async def start(self)-> dict:
        try:
            await asyncio.to_thread(self.__final_clip.write_videofile, self.__temp) #type: ignore
            self.__background.close() #type: ignore
            self.__logo_create.close() #type: ignore
            self.__final_clip.close() #type: ignore
            return {"success": True , "message": f"Video Guardado en: {self.__temp}" }
        except Exception as e:
            return {"success": False , "message": f"Ocurrio un error {e}"}

    def create(self):
        self.__background = VideoFileClip(self.__video)
        self.__logo_create = ImageClip(self.__logo, duration=self.__background.duration).resized(height=100)
        top= (self.__background.h - self.__logo_create.h)/2 # type: ignore
        self.__logo_create = self.__logo_create.with_position(lambda t: ("right","top")) # type: ignore
        self.__final_clip = CompositeVideoClip([self.__background, self.__logo_create])
    
class CreateVideosForAgency():
    def __init__(self, files_paths, name):
        self.__paths = files_paths
        self.__name_video= name
    
    async def __createVideWithLogo(self) -> dict:
        logo = AddLogoToVideo(self.__paths)
        logo.create()
        response = await logo.start()
        return {"success": response["success"], "message": response["message"]}

    async def __joinVideos(self)-> dict:
        video = CreateFinalVideo(self.__paths, self.__name_video)
        response= await video.start()
        return {"success": response["success"], "message": response["message"]}

    async def createVideo(self) -> dict:
        isReadyVideoWithLogo = await self.__createVideWithLogo()
        isReadyVideoFinal = await self.__joinVideos()

        if isReadyVideoWithLogo["success"] and isReadyVideoFinal["success"]:
            return {"success": True, "message": "Video generado correctamente", "route": f"{self.__paths.output_path}"}
        else:
            return {"success": True, "message": "Video generado correctamente" }