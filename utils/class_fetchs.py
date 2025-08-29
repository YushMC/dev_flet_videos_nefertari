import aiohttp
from utils.class_files import DeleteFile, CheckDirectories
from abc import ABC, abstractmethod
import ssl


class APIPathsInterface(ABC):
    @abstractmethod
    def endpoint(self, name: str) -> str:
        raise NotImplementedError
    
class APIPaths(APIPathsInterface):
    def __init__(self):
        self._base_url = "https://api.salonnefertaritravel.com/api/client/"
        self._endpoints = {
            "videos": "trip/list",
            "login": "login"
        }
    
    def endpoint(self, name: str):
        if name in self._endpoints:
            return f"{self._base_url}{self._endpoints[name]}"
        raise ValueError(f"Endpoint '{name}' no definido")

########################## no tocar ###################################################

class Requests(ABC):
    def __init__(self):
       self._ssl_context = ssl.create_default_context()
       self._ssl_context.check_hostname = False
       self._ssl_context.verify_mode = ssl.CERT_NONE
       
    @abstractmethod
    async def sendRequest(self)-> bool | dict:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class RequestToLogin(Requests):
    def __init__(self, user_data_to_login, api_path):
        super().__init__()
        self.__end_point_api = api_path.endpoint("login")
        self.__user_data =  {"user":user_data_to_login.email, "password": user_data_to_login.password}
        self.__response = {}

    async def sendRequest(self) :
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.__end_point_api, json=self.__user_data, ssl=self._ssl_context) as response:
                    if response.status == 200:
                        self.__response= await response.json()
                        return {"success": True, "message": self.__response["message"], "token": self.__response["token"]}
                    else:
                        message_response = await response.json()
                        return {"success": False, "message": f"Error: {message_response['message']}"}
            except Exception as e:
                return {"success": False, "message": f"Error: {e}"}
    
    @property
    def token(self):
        return self.__response["token"]
    
    def __str__(self) -> str:
        return f"RequestToLogin(end_point_api= {self.__end_point_api}, user_data= {self.__user_data}, response= {self.__response})"

class DataUser:
    @property
    def getToken(self) -> str:
        return str(RequestToLogin.token)

class ReequestToDownloadVideo(Requests):
    def __init__(self, url, init_paths):
        super().__init__()
        self.__url_video = url
        self.__path_to_save= init_paths.temp_video_path
        self.__message = ""

    async def sendRequest(self) -> dict:
        if CheckDirectories().checkFilesAndDirectories(self.__url_video): DeleteFile(self.__url_video)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.__url_video, ssl=self._ssl_context) as response:
                    if response.status == 200:
                        with open(self.__path_to_save, "wb") as f:
                            while True:
                                chunk = await response.content.read(1024*1024)  # 1 MB por chunk
                                if not chunk:
                                    break
                                f.write(chunk)
                            
                            return {"success": True, "message": f"Descarga completada"}
                    else:
                        return { "success" : False, "message": f"Error {response.status} al descargar el video"}
            except Exception as e:
                return {"success": False, "message":  f"ocurrio un error: {e}"}
            
    @property
    def message(self):
        return self.__message
    
    def __str__(self) -> str:
        return f"RequestToLogin(url_video= {self.__url_video}, path_to_save= {self.__path_to_save}, message= {self.__message})"

class RequestToGetAllVideosToDownload(Requests):
    def __init__(self, user_info, api_path):
        super().__init__()
        self.__api_path= api_path.endpoint("videos")
        self.__token= user_info
        self.__data_from_nefertari = {}
        self.__message = ""
        self.__trips= []

    async def sendRequest(self):
        headers = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.__api_path, headers=headers, ssl=self._ssl_context) as response:
                    if response.status == 200:
                        self.__data_from_nefertari = await response.json()
                        self.__message= self.__data_from_nefertari["message"]
                        self.__trips= self.__data_from_nefertari["trips"]
                        return True
                    else:
                        self.__message = f"Error {response.status}: {await response.text()}"
                        return False
            except Exception as e:
                self.__message = f"ocurrio un error: {e}"
                return False

    @property
    def message(self):
        return self.__message
    
    @property
    def trips(self):
        return self.__trips

    def __str__(self) -> str:
        return f"RequestToLogin(end_point_api= {self.__api_path}, user_data= {self.__token}, response= {self.__data_from_nefertari}, message= {self.__message})"
    

