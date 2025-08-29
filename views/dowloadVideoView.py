from utils.class_fetchs import RequestToGetAllVideosToDownload,ReequestToDownloadVideo
from utils.class_files import InitPaths
import flet as ft
from views.base import AllViews
from views.merge import MergeView
import base64
import asyncio
import secrets

class DownloadVideoView(AllViews):
    def __init__(self, page: ft.Page, token):
        self.__page= page
        self.__videos= []
        self.__token = token

    async def getAllVideos(self, paths):
        result = RequestToGetAllVideosToDownload(self.__token,paths)
        if not await result.sendRequest() : raise  Exception(result.message)
        self.__videos= result.trips
        
    def get_options(self):
        options = []
        for video in self.__videos:
            options.append(
                ft.DropdownOption(
                    key= video["url_video"], #video["name"], # cambiar esta key por el que será final
                    content=ft.Text(
                        value=video["name"],
                    ),
                )
            )
        return options
    
    async def __joinVideos(self, name):
        videos_to_download_page = MergeView(self.__page,InitPaths(),name)
        self.__page.views.append(await videos_to_download_page.get_view())
        self.__page.update()
        self.__page.go("/final")

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

        def get_selected_label() -> str:
            raw = secrets.token_bytes(16)  
            encoded = base64.b64encode(raw).decode("utf-8")
            return encoded[:10]
        
        def click_to_download_wrapper(e):
            self.__page.run_task(click_to_download, e)

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
            #self.__page.dialog = dlg
            dlg.open = True
            video_to_download= ReequestToDownloadVideo(self.__dd.value, InitPaths())
            response = await video_to_download.sendRequest()
            
            if response["success"]:
                dlg.open = False
                self.__page.update()
                await self.__joinVideos(get_selected_label())
            else:
                self.__page.close(dlg)
                self.__page.update()
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
                    ft.ElevatedButton("Continuar", on_click=click_to_download_wrapper), #type: ignore
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