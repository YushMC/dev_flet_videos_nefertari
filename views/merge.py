import flet as ft
from utils.class_fetchs import APIPaths
from utils.class_videos import CreateVideosForAgency
from views.base import AllViews
import sys
import asyncio
import subprocess

class MergeView(AllViews):
    def __init__(self, page: ft.Page, files_paths, name):
        self.__page= page
        self.__files_paths= files_paths
        self.__final_name= name
        self.__progress_bar= ft.ProgressBar(width=300, value=0)

    async def __create(self)-> dict:
        final_video = CreateVideosForAgency(self.__files_paths, f"video_{self.__final_name}.mp4")
        response = await self.__actualizar_progress_bar(final_video.createVideo())
        if response["route"]:
            return {"success": response["success"], "message": response["message"],"route": response["route"]}
        else:
            return {"success": response["success"], "message": response["message"]}
    
    def __getVideos(self):
        self.__page.update()
        self.__page.go("/get-videos")
        self.__page.update()

    def __abrir_carpeta(self, route):
        if sys.platform.startswith("darwin"):  # macOS
            subprocess.run(["open", route])
        elif sys.platform.startswith("win"):  # Windows
            subprocess.run(["start", "", route], shell=True)
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.run(["xdg-open", route])
        else:
            raise OSError("Sistema operativo no soportado")
        
    async def __actualizar_progress_bar(self, create_video):
        progreso = 0
        task = asyncio.create_task(create_video)

        while not task.done():
            # Incrementamos la barra lentamente hasta 99%
            if progreso < 0.59:
                progreso += 0.001
            elif progreso < 0.90:
                progreso += 0.0001
            else:
                progreso = 0.90
            self.__progress_bar.value = progreso
            self.__page.update()
            await asyncio.sleep(0.1)  # refresco cada 50ms

        # Cuando termine createVideo()
        result = await task
        self.__progress_bar.value = 1
        self.__page.update()
        if result["route"]:
            return {"success": result["success"], "message": result["message"],"route": result["route"]}
        else:
            return {"success": result["success"], "message": result["message"]}

    async def get_view(self):

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(""),
            content=ft.Text(""),
            alignment=ft.alignment.center,
            on_dismiss=None,
            title_padding=ft.padding.all(25),
            icon=ft.Icon()
        )

        async def create_click(e):
            self.__page.update()
            dlg.title= ft.Text("Creando video final")
            dlg.content=ft.Column(
                [
                    ft.Text("Por favor espere..."),
                    self.__progress_bar
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            self.__page.open(dlg)
            response = await self.__create()
            if response["success"]:
                self.__page.update()
                self.__page.close(dlg)
                dlg.modal = False
                dlg.title = ft.Text("Correcto")
                dlg.content = ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN, size=50)
                dlg.on_dismiss=self.__abrir_carpeta(response["route"])   #await self.__getVideos(response["token"])
                dlg.actions = [ft.TextButton("Aceptar", on_click=lambda e: (self.__page.close(dlg) , self.__getVideos()))]
                dlg.actions_alignment = ft.MainAxisAlignment.END
                self.__page.open(dlg)
                self.__page.update()
            else:
                self.__page.update()
                self.__page.close(dlg)
                dlg.modal= False
                dlg.title = ft.Text("Ocurrio un error")
                dlg.content = ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=50)
                dlg.actions = [ft.TextButton("Aceptar", on_click=lambda e: self.__page.close(dlg))]
                dlg.actions_alignment = ft.MainAxisAlignment.END
                self.__page.open(dlg)
                self.__page.update()

        container=  ft.Container(
            content=ft.Column(
                [
                    ft.Text("Crear Video", size=25, weight="bold"), #type: ignore
                    ft.ElevatedButton("Crear", on_click=create_click),#type: ignore
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
            '/final',
            [container]
        )
    
