import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # evita pygame windows
os.environ["DISPLAY"] = ""               # en mac/linux, evita usar X11

from moviepy import  * #type: ignore
import asyncio
from abc import ABC, abstractmethod


class CreateVideos:
    @abstractmethod
    async def start(self) -> dict:
        pass

class CreateFinalVideo(CreateVideos):
    def __init__(self, paths, name, output_dir):
        self.__intro = VideoFileClip(paths.intro_video_path)
        self.__outro = VideoFileClip(paths.outro_video_path)
        self.__temp= VideoFileClip(paths.temp_video_to_generate_path)
        self.__output = output_dir
        self.__audio_temp= paths.audio_final_video_logo
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
            await asyncio.to_thread(self.__final_clip.write_videofile, f"{self.__output}/{self.__name}",temp_audiofile=self.__audio_temp, audio_codec="mp3", logger=None) #type: ignore
            self.__intro.close()
            self.__temp.close()
            self.__outro.close()
            self.__final_clip.close()#type: ignore
            return {"success": True, "message": f"Video Guardado en: {os.path.join(self.__output, self.__name)}"}
        except Exception as e:
            return {"success": False, "message":  f"Ourrio un error: {e}"} 


class AddLogoToVideo(CreateVideos):
    def __init__(self, paths):
        self.__video = paths.temp_video_path
        self.__audio_temp= paths.audio_temp_video_logo
        self.__logo = paths.logo_path
        self.__temp= paths.temp_video_to_generate_path
        self.__background= ""
        self.__logo_create= ""
        self.__final_clip = ""

    async def start(self)-> dict:
        try:
            await asyncio.to_thread(self.__final_clip.write_videofile, self.__temp, temp_audiofile=self.__audio_temp, audio_codec="mp3", logger=None) #type: ignore
            self.__background.close() #type: ignore
            self.__logo_create.close() #type: ignore
            self.__final_clip.close() #type: ignore
            return {"success": True , "message": f"Video Guardado en: {self.__temp}" }
        except Exception as e:
            return {"success": False , "message": f"Ocurrio un error {e}"}

    def create(self):
        self.__background = VideoFileClip(self.__video)#### cambiar esto
        self.__logo_create = ImageClip(self.__logo, duration=self.__background.duration).resized(height=100)
        top= (self.__background.h - self.__logo_create.h)/2 # type: ignore
        self.__logo_create = self.__logo_create.with_position(lambda t: ("right","top")) # type: ignore
        self.__final_clip = CompositeVideoClip([self.__background, self.__logo_create])
    
class CreateVideosForAgency():
    def __init__(self, files_paths, output_dir):
        self.__paths = files_paths
        self.__output_dir= output_dir
    
    async def createVideWithLogo(self) -> dict:
        logo = AddLogoToVideo(self.__paths)
        logo.create()
        response = await logo.start()
        return {"success": response["success"], "message": response["message"]}

    async def joinVideos(self, name)-> dict:
        video = CreateFinalVideo(self.__paths, name, self.__output_dir)
        response= await video.start()
        return {"success": response["success"], "message": response["message"]}

    async def createVideo(self, name) -> dict:
        isReadyVideoWithLogo = await self.createVideWithLogo()
        isReadyVideoFinal = await self.joinVideos(name)

        if isReadyVideoWithLogo["success"] and isReadyVideoFinal["success"]:
            return {"success": True, "message": "Video generado correctamente", "route": f"{self.__paths.output_path}"}
        else:
            return {"success": False, "message": "Ocurrio un error" }
        
