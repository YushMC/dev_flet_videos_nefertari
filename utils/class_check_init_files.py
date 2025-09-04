from utils.class_files import ConfigFile
from utils.class_attermpts import AttemptsClass, Response

import os

class ConfigFileValues:
    def __init__(self, paths, check) -> None:
        self.__paths= paths
        self.__check= check
        self.token= ""
        self.exist_token= False
        self.output_path= ""
        self.__config_file = ConfigFile(paths)

    def loadFile(self):
        if self.__check.checkFilesAndDirectories(self.__paths.config_file):
            self.__config_file.loadConfigFile()
            if self.__config_file.token != '': self.exist_token = True
            self.token = self.__config_file.token
            self.output_path= self.__config_file.output_dir

        else: 
            self.saveConfigData()

    def saveConfigData(self) -> Response:
        def __action():
            self.__config_file.token = self.token
            self.__config_file.output_dir = self.output_path
            self.__config_file.saveConfigFile()
        return AttemptsClass().attempts(__action)

    






