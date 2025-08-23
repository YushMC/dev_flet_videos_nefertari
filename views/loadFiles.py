from utils.class_files import InitPaths, MoveFIles, CheckDirectories
import flet as ft
from views.home import HomeView
from views.base import AllViews

class LoadFiles(AllViews):
    def __init__(self, page: ft.Page):
        self.__page= page
       
        self.__file_picker_1 = ft.FilePicker(on_result=self.on_file_selected)
        self.__file_picker_2 = ft.FilePicker(on_result=self.on_file_selected)
        self.__file_picker_3 = ft.FilePicker(on_result=self.on_file_selected)

        print("FilePickers inicializados en la vista:", self.__file_picker_1, self.__file_picker_2, self.__file_picker_3)
        """ 
        self.__file_picker_1.dialog_title = "intro"
        self.__file_picker_2.dialog_title = "outro"
        self.__file_picker_3.dialog_title = "logo"

        self.__file_picker_1.on_result = self.on_file_selected
        self.__file_picker_2.on_result = self.on_file_selected
        self.__file_picker_3.on_result = self.on_file_selected
        print("FilePickers configurados:", self.__file_picker_1, self.__file_picker_2, self.__file_picker_3)
        self.__intro_video = ft.TextField(label="Video de introduccción", width=600)
        self.__outro_video = ft.TextField(label="Video de despedida", width=600)
        self.__agency_logo = ft.TextField(label="Logo de la agencia", width=600)
        """

        self.__page.overlay.append(self.__file_picker_1)
        self.__page.overlay.append(self.__file_picker_2)
        self.__page.overlay.append(self.__file_picker_3)
        print("Pagina en la vista:", self.__page)
        self.__intro_video = ft.TextField(label="Video de introduccción", width=600)
        self.__outro_video = ft.TextField(label="Video de despedida", width=600)
        self.__agency_logo = ft.TextField(label="Logo de la agencia", width=600)

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        print(f"on_file_selected llamado desde: {e.control.dialog_title}")
        if e.files:
            file_path = e.files[0].path
            print(f"Archivo seleccionado: {file_path}")

            if e.control.dialog_title == "intro":
                self.__intro_video.value = file_path
            elif e.control.dialog_title == "outro":
                self.__outro_video.value = file_path
            elif e.control.dialog_title == "logo":
                self.__agency_logo.value = file_path

            self.__page.update()

    def __moveFiles(self):
        check= CheckDirectories()
        files_paths = InitPaths()
        if not self.__agency_logo.value == '' and not self.__intro_video.value == '' and not self.__outro_video.value == '':
            if not check.checkFilesAndDirectories(files_paths.intro_video_path): 
                response = MoveFIles().moveMp4(self.__intro_video.value, files_paths.intro_video_path)
                print(response["message"])

            if not check.checkFilesAndDirectories(files_paths.outro_video_path): 
                response = MoveFIles().moveMp4(self.__outro_video.value, files_paths.outro_video_path)
                print(response["message"])

            if not check.checkFilesAndDirectories(files_paths.logo_path): 
                response = MoveFIles().moveImg(self.__agency_logo.value)
                print(response["message"])

            if check.checkFilesAndDirectories(files_paths.intro_video_path) and check.checkFilesAndDirectories(files_paths.outro_video_path) and  check.checkFilesAndDirectories(files_paths.logo_path): 
                return { "success": True, "message": "Archivos cargados correctamente"}
            else:
                return { "success": False, "message": "Ocurrio un error"}
        else:
            return { "success": False, "message": "Alguno de los campos estan vacios"}
        

    async def get_view(self):
        dlg = ft.AlertDialog(
            title=ft.Text(""),
            content=ft.Text(""),
            alignment=ft.alignment.center,
            on_dismiss=None,
            title_padding=ft.padding.all(25),
            icon=ft.Icon()
        )

        async def startToMoveFiles(e):
            response =  self.__moveFiles()
            if response["success"]:
                self.__page.update()
                dlg.title = ft.Text("Correcto")
                dlg.content= ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN, size=50)
                self.__page.open(dlg)
                home_page = HomeView(self.__page)
                self.__page.views.clear()
                self.__page.views.append(await home_page.get_view())
                self.__page.go("/home")
            else:
                self.__page.update()
                dlg.title = ft.Text("Error")
                dlg.content = ft.Text(response["message"])
                dlg.icon = ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=50)
                self.__page.open(dlg)

        container=  ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cargar archivos", size=25, weight="bold"), #type: ignore
                    ft.Row([self.__intro_video, ft.ElevatedButton("Seleccionar archivo", on_click=lambda _:(print("Botón Intro presionado"), self.__file_picker_1.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.VIDEO)))]),
                    ft.Row([self.__outro_video, ft.ElevatedButton("Seleccionar archivo", on_click=lambda _: (print("Botón Outro presionado"), self.__file_picker_2.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.VIDEO)))]),
                    ft.Row([self.__agency_logo, ft.ElevatedButton("Seleccionar archivo", on_click=lambda _: (print("Botón Logo presionado"), self.__file_picker_3.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)))]),
                    ft.ElevatedButton("Continuar", on_click=startToMoveFiles),#type: ignore
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
            '/files',
            [container]
        )
    