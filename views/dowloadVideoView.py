from utils.class_fetchs import RequestToGetAllVideosToDownload,ReequestToDownloadVideo
from utils.class_files import InitPaths
import flet as ft
from views.base import AllViews

class DownloadVideoView(AllViews):
    def __init__(self, page: ft.Page,):
        self.__page= page
        self.__videos= []

    async def getAllVideos(self,  login_data, paths):
        result = RequestToGetAllVideosToDownload(login_data,paths)
        if not await result.sendRequest() : raise  Exception(result.message)
        self.__videos= result.trips
        
    def get_options(self):
        options = []
        for video in self.__videos:
            options.append(
                ft.DropdownOption(
                    key= "https://nefertari.s3.us-east-2.amazonaws.com/videos/viaje.mp4", #video["name"], # cambiar esta key por el que será final
                    content=ft.Text(
                        value=video["name"],
                    ),
                )
            )
        return options

    async def get_view(self) -> ft.View:
        self.__dd = ft.Dropdown(editable=True,label="Video",options=self.get_options(), width=300)
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(""),
            content=ft.Text(""),
            alignment=ft.alignment.center,
            on_dismiss=None,
            title_padding=ft.padding.all(25),
            icon=ft.Icon()
        )

        async def click_to_download(e):
            self.__page.update()
            dlg.title= ft.Text("Descargando archivo")
            dlg.content=ft.Column(
                [
                    ft.ProgressRing(),
                    ft.Text("Por favor espera..."),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            self.__page.open(dlg)
            video_to_download= ReequestToDownloadVideo(self.__dd.value, InitPaths())
            response = await video_to_download.sendRequest()
            if response["success"]:
                self.__page.update()
                self.__page.close(dlg)
                dlg.title = ft.Text("Correcto")
                dlg.content = ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN, size=50)
                dlg.actions = [ft.TextButton("Aceptar", on_click=lambda e: self.__page.close(dlg))]
                dlg.actions_alignment = ft.MainAxisAlignment.END
                #dlg.on_dismiss= await self.__getVideos(response["token"])
                self.__page.open(dlg)
            else:
                self.__page.update()
                self.__page.close(dlg)
                dlg.title = ft.Text("Ocurrio un error")
                dlg.content = ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=50)
                dlg.actions = [ft.TextButton("Aceptar", on_click=lambda e: self.__page.close(dlg))]
                dlg.actions_alignment = ft.MainAxisAlignment.END
                self.__page.open(dlg)

        container=  ft.Container(
            content=ft.Column(
                [
                    ft.Text("Selecciona un video", size=25, weight="bold"), #type: ignore
                    self.__dd,
                    ft.ElevatedButton("Continuar", on_click=click_to_download), #type: ignore
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
            '/get-videos',
            [container]
        )