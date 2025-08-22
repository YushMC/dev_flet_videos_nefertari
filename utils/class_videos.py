
from moviepy import  * #type: ignore
import asyncio
import threading
from abc import ABC, abstractmethod


class CreateVideos:
    @abstractmethod
    async def start(self) -> bool:
        pass

class CreateFinalVideo(CreateVideos):
    def __init__(self, paths, name):
        self.__intro = VideoFileClip(paths.intro_video_path)
        self.__outro = VideoFileClip(paths.outro_video_path)
        self.__temp= VideoFileClip(paths.generate_temp_video_path)
        self.__output = paths.output_path
        self.__name= name
        self.__final_clip = ""
        self.__message= ""

    def __concatenate(self):
        self.__intro = self.__intro.subclipped(0, self.__intro.duration - 0.01)
        self.__outro = self.__outro.subclipped(0, self.__outro.duration - 0.01)
        self.__temp = self.__temp.subclipped(0, self.__temp.duration - 0.01)
        self.__final_clip = concatenate_videoclips([self.__intro, self.__temp, self.__outro], method="compose") # type: ignore

    async def start(self):
        self.__concatenate()
        try:
            await asyncio.to_thread(self.__final_clip.write_videofile, f"{self.__output}/{self.__name}") #type: ignore
            self.__message = f"Video Guardado en: {self.__name}"
            self.__intro.close()
            self.__temp.close()
            self.__outro.close()
            self.__final_clip.close()#type: ignore
            return True
        except Exception as e:
            self.__message = f"Ourrio un error: {e}"
            return False
        
    @property
    def message(self):
        return self.__message


class AddLogoToVideo(CreateVideos):
    def __init__(self, paths):
        self.__video = paths.temp_video_path
        self.__logo = paths.logo_path
        self.__temp= paths.generate_temp_video_path
        self.__message= ""
        self.__background= ""
        self.__logo_create= ""
        self.__final_clip = ""

    async def start(self):
        try:
            await asyncio.to_thread(self.__final_clip.write_videofile, self.__temp) #type: ignore
            self.__message = f"Video Guardado en: {self.__temp}"
            self.__background.close() #type: ignore
            self.__logo_create.close() #type: ignore
            self.__final_clip.close() #type: ignore
            return True
        except Exception as e:
            self.__message = f"Ocurrio un error {e}"
            return False

    def create(self):
        self.__background = VideoFileClip(self.__video).subclipped(0,10)
        self.__logo_create = ImageClip(self.__logo, duration=self.__background.duration).resized(height=100)
        top= (self.__background.h - self.__logo_create.h)/2 # type: ignore
        self.__logo_create = self.__logo_create.with_position(lambda t: ("right","top")) # type: ignore
        self.__final_clip = CompositeVideoClip([self.__background, self.__logo_create])

    @property
    def message(self):
        return self.__message
    
class CreateVideosForAgency():
    def __init__(self, files_paths, name):
        self.__paths = files_paths
        self.__name_video= name
    
    async def __createVideWithLogo(self) -> bool:
        logo = AddLogoToVideo(self.__paths)
        logo.create()
        if not await logo.start(): raise  Exception(logo.message)
        return True

    async def __joinVideos(self)-> bool:
        video = CreateFinalVideo(self.__paths, self.__name_video)
        if not await video.start() : raise Exception(video.message)
        return True

    async def createVideo(self) -> bool:
        isReadyVideoWithLogo = await self.__createVideWithLogo()
        isReadyVideoFinal = await self.__joinVideos()
        return True if isReadyVideoWithLogo and isReadyVideoFinal else False