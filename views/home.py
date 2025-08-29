import flet as ft
from utils.class_fetchs import RequestToLogin, APIPaths
from utils.class_input_data import *
from views.dowloadVideoView import DownloadVideoView
from abc import ABC, abstractmethod
from views.base import AllViews

class HomeView(AllViews):
    def __init__(self, page: ft.Page):
        self.__page= page
        self.__username = ft.TextField(label="Usuario", width=300)
        self.__password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        self.__token= ""

    async def __login(self)-> dict:
        login = RequestToLogin(UserDataToLogin(self.__username.value,  self.__password.value), APIPaths())
        return { "success" : True, "message" : login.message, "token": login.token}  if await login.sendRequest() else { "success" : False, "message" : login.message}
    
    async def __getVideos(self):
        videos_to_download_page = DownloadVideoView(self.__page, self.__token)
        self.__page.views.clear()
        await videos_to_download_page.getAllVideos(APIPaths())
        self.__page.views.append(await videos_to_download_page.get_view())
        self.__page.go("/get-videos")

    async def get_view(self):
        dlg = ft.AlertDialog(
            title=ft.Text(""),
            alignment=ft.alignment.center,
            on_dismiss=None,
            title_padding=ft.padding.all(25),
            icon=ft.Icon()
        )

        async def login_click(e):
            response = await self.__login()
            if response["success"]:
                self.__token = response["token"]
                await self.__getVideos()
            else:
                self.__page.update()
                dlg.title = ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=50)
                self.__page.open(dlg)

        container=  ft.Container(
            content=ft.Column(
                [
                    ft.Text("Iniciar Sesión", size=25, weight="bold"), #type: ignore
                    self.__username,
                    self.__password,
                    ft.ElevatedButton("Ingresar", on_click=login_click),#type: ignore
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                
            ),
            expand=True,
            alignment=ft.alignment.center,
            width=None
        )

        return ft.View(
            '/home',
            [container]
        )
    
