from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import ttk
from tkinter import filedialog
#se normaliza las variables de respuesta
from utils.class_attermpts import Response, AttemptsClass
from PIL import Image, ImageTk

class AllPages(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @property
    @abstractmethod
    def instance(self)-> tk.Tk | tk.Toplevel:
        pass

    @abstractmethod
    def start(self) -> Response:
        pass


#TODO: CLasses de Frames



class FrameWindow:
    def __init__(self, window, width: int, height: int) -> None:
        self._frame = tk.Frame(window, width=width, height=height)
            

    @property
    def instance(self):
        return self._frame
    @instance.setter
    def instance(self, value):
        self._frame = value

class FrameWindowPlace(FrameWindow):
    def __init__(self, window, width: int, height: int, position_x, position_y, anchor) -> None:
        super().__init__(window, width, height)
        self._frame.place(relx=position_x, rely=position_y, anchor=anchor, width=width, height=height)


class FrameWindowGrid(FrameWindow):
    def __init__(self, window, width: int, height: int, anchor) -> None:
        super().__init__(window, width, height)
        self._frame.grid_propagate(False)
        self._frame.grid(sticky="nsew")
        self._frame.grid_anchor(anchor)
         
    
    def set_row_size(self, position, weight):
            self._frame.rowconfigure(position, weight=weight)
    
    def set_column_size(self,position,  weight):
        self._frame.columnconfigure(position, weight=weight)

    def amount_rows_responsives(self, amount: int):
        self._frame.rowconfigure(list(range(amount)), weight=1)
    
    def amount_columns_responsives(self, amount: int):
        self._frame.columnconfigure(list(range(amount)), weight=1)

class FrameWindowPack(FrameWindow):
    def __init__(self, window, width: int, height: int, expanded: bool, anchor) -> None:
        super().__init__(window, width, height)
        self._frame.pack(
            expand=expanded,
            anchor=anchor
        )
        self._frame.pack_propagate(False)




#TODO: CLases para imagenes



class ImageWidget:
    def __init__(self, frame, url, width:int, height: int) -> None:
        self._photo = ImageTk.PhotoImage(Image.open(url).resize((width, height)))
        self._image = tk.Label(frame, image=self._photo)

class ImageLogoPack(ImageWidget):
    def __init__(self, frame, url: str, width:int, height:int, position, expanded: bool) -> None:
        super().__init__(frame, url, width, height)
        self._image.pack(
            side=position,
            expand=expanded,
        )




#TODO: Clases para los botones




class ButtonWidget:
    def __init__(self, frame: tk.Frame, text) -> None:
        self._button= tk.Button(frame, text=text)
        self._attempts= AttemptsClass().attempts

    @property
    def instance(self):
        return self._button

    @instance.setter
    def instance(self, value):
        self._button = value
    
    
class ButtonPack(ButtonWidget):
    def __init__(self, frame: tk.Frame, text, position, expanded: bool, witdh: int, height: int, padx:int, pady:int) -> None:
        super().__init__(frame, text)
        self._button.config(width=witdh, height=height)
        self._button.pack(
            side=position,
            padx=padx,
            pady=pady,
            expand=expanded,
        )

    def __str__(self) -> str:
        return f"ButtonPack(text={self._button.cget('text')})" #type: ignore
    
class ButtonGrid(ButtonWidget):
    def __init__(self, frame: tk.Frame, text, row: int, column:int, columnspan:int, rowspan:int, span_direction: str) -> None:
        super().__init__(frame, text)
        if columnspan>0 and rowspan> 0: self._button.grid(row=row, column=column,columnspan=columnspan, rowspan=rowspan, sticky=span_direction)
        elif columnspan > 0: self._button.grid(row=row, column=column, columnspan=columnspan, sticky="we")
        elif rowspan > 0: self._button.grid(row=row, column=column, rowspan=rowspan, sticky="ns")
        else: self._button.grid(row=row, column=column, sticky=span_direction) 

class ButtonPlace(ButtonWidget):
    def __init__(self, frame: tk.Frame, text, position_x:int | float, position_y:int| float, anchor, width: int, height: int) -> None:
        super().__init__(frame, text)
        if position_x > 1: position_x= 1
        if position_y > 1: position_y=1
        self._button.place(relx=position_x, rely=position_y, anchor=anchor, width=width, height=height)




#TODO: Clases para las etiquetas




class LabelWidget:
    def __init__(self, frame: tk.Frame, text,) -> None:
        self._label= tk.Label(frame, text=text)
        self._attempts= AttemptsClass().attempts

    @property
    def instance(self):
        return self._label
    
class LabelGrid(LabelWidget):
    def __init__(self, frame: tk.Frame, text, row: int, column:int, columnspan:int, rowspan:int, span_direction: str) -> None:
        super().__init__(frame, text)
        if columnspan>0 and rowspan> 0: self._label.grid(row=row, column=column,columnspan=columnspan, rowspan=rowspan, sticky=span_direction)
        elif columnspan > 0: self._label.grid(row=row, column=column, columnspan=columnspan, sticky="we")
        elif rowspan > 0: self._label.grid(row=row, column=column, rowspan=rowspan, sticky="ns")
        else: self._label.grid(row=row, column=column, sticky=span_direction) 
    
class LabelPack(LabelWidget):
    def __init__(self, frame: tk.Frame, text,  position, expanded: bool, padx:int, pady:int) -> None:
        super().__init__(frame, text)
        self._label.pack(
            side=position,
            padx=padx,
            pady=pady,
            expand=expanded,
        )

    def __str__(self) -> str:
        return f"LabelPack(text={self._label.cget('text')})" #type: ignore}
    
class LabelPlace(LabelWidget):
    def __init__(self, frame: tk.Frame, text, position_x:int | float, position_y:int| float, anchor, width: int, height: int) -> None:
        super().__init__(frame, text)
        if position_x > 1: position_x= 1
        if position_y > 1: position_y=1
        self._label.place(relx=position_x, rely=position_y, anchor=anchor, width=width, height=height)



#TODO: Clases para las entradas de tetxto




class EntryWidget:
    def __init__(self, frame: tk.Frame) -> None:
        self._input= tk.Entry(frame)

    @property
    def instance(self):
        return self._input
    
    @instance.setter
    def instance(self, value):
        self._input = value

class EntryPack(EntryWidget):
    def __init__(self, frame: tk.Frame, position, expanded: bool, witdh: int) -> None:
        super().__init__(frame)
        self._input.config(width=witdh)
        self._input.pack(
            side=position,
            expand=expanded,
            
        )

class EntryPlace(EntryWidget):
    def __init__(self, frame: tk.Frame, position_x:int | float, position_y:int| float, anchor, width: int, height: int) -> None:
        super().__init__(frame)
        if position_x > 1: position_x= 1
        if position_y > 1: position_y=1
        self._input.place(relx=position_x, rely=position_y, anchor=anchor, width=width, height=height)

class EntryGrid(EntryWidget):
    def __init__(self, frame: tk.Frame, row: int, column:int, columnspan:int, rowspan:int, span_direction: str) -> None:
        super().__init__(frame)
        if columnspan>0 and rowspan> 0: self._input.grid(row=row, column=column,columnspan=columnspan, rowspan=rowspan, sticky=span_direction)
        elif columnspan > 0: self._input.grid(row=row, column=column, columnspan=columnspan, sticky="we")
        elif rowspan > 0: self._input.grid(row=row, column=column, rowspan=rowspan, sticky="ns")
        else: self._input.grid(row=row, column=column, sticky=span_direction) 




#FIXME: Crear clases para las listas




class ComboBoxWidget:
    def __init__(self, frame: tk.Frame) -> None:
        self._combo_box = ttk.Combobox(frame, state="readonly")

    @property
    def instance(self):
        return self._combo_box
    
    @instance.setter
    def instance(self, value):
        self._combo_box = value

class ComboBoxVideo(ComboBoxWidget):
    def __init__(self, frame: tk.Frame, videos:list) -> None:
        super().__init__(frame)
        self.__videos= videos
        self._combo_box.config(values=[item['name'] for item in self.__videos])

    def selected_item(self) -> dict:
        selected_name = self._combo_box.get()
        seleccion = next((item for item in self.__videos if item["name"] == selected_name), None)
        if seleccion: return {"success": True, "url_video": seleccion['url_video'], "name": seleccion['name']}
        else: return {"success": False}  

class ComboBoxVideoPack(ComboBoxVideo):
    def __init__(self, frame: tk.Frame, videos: list, position, expanded: bool) -> None:
        super().__init__(frame, videos)
        self._combo_box.pack(pady=20, side=position,expand=expanded)

class ComboBoxVideoGrid(ComboBoxVideo):  
    def __init__(self, frame: tk.Frame, videos: list, row: int, column:int, columnspan:int, rowspan:int, span_direction: str) -> None:
        super().__init__(frame, videos)
        if columnspan>0 and rowspan> 0: self._combo_box.grid(row=row, column=column,columnspan=columnspan, rowspan=rowspan, sticky=span_direction)
        elif columnspan > 0: self._combo_box.grid(row=row, column=column, columnspan=columnspan, sticky="we")
        elif rowspan > 0: self._combo_box.grid(row=row, column=column, rowspan=rowspan, sticky="ns")
        else: self._combo_box.grid(row=row, column=column, sticky=span_direction) 


class ComboBoxSizeVideo(ComboBoxWidget):
    def __init__(self, frame: tk.Frame, optionsList: list) -> None:
        super().__init__(frame)
        self.__options = optionsList
        self._combo_box.config(values=self.__options)
    
    def selected_item(self) -> dict:
        selected_name = self._combo_box.get()
        if selected_name: return {"success": True, "size": selected_name}
        else: return {"success": False}  

class ComboBoxSizeVideoPack(ComboBoxSizeVideo):
    def __init__(self, frame: tk.Frame, optionsList: list, position, expanded: bool) -> None:
        super().__init__(frame, optionsList)
        self._combo_box.pack(pady=20, side=position,expand=expanded)

#TODO: Clases para crear los dialogos



class MessageBoxDialogs:
    def __init__(self, window) -> None:
        self._msgbox = msgbox

    def show_message_info(self, title: str, message: str):
        self._msgbox.showinfo(title, message)

    def show_message_error(self, title: str, message: str):
        self._msgbox.showerror(title, message)

    def show_message_warning(self, title: str, message: str):
        self._msgbox.showwarning(title, message)

    def show_message_confirmation(self, title: str, message: str):
        return self._msgbox.askyesno(title, message)
    
    def show_message_continue(self, title: str, message: str):
        return self._msgbox.askokcancel(title, message)
    
    def show_message_retry(self, title: str, message: str):
        return self._msgbox.askretrycancel(title, message)



#TODO: Inputs files

class InputFilesWidget:
    def select_file(self, title_dialog):
        file = filedialog.askopenfilename(title=title_dialog)
        if file: 
            return {"success": True, "file_path": file}
        else:
            return {"success": False}

    def select_image_file(self, title_dialog):
        file= filedialog.askopenfilename(
            title=title_dialog,
            filetypes=(
                ("Archivos PNG", "*.png"),
                ("Archivos JPG", "*.jpg"),
                ("Archivos JPEG", "*.jpeg")
        ))

        if file: 
            return {"success": True, "file_path": file}
        else:
            return {"success": False}

    def select_video_file(self, title_dialog):
        file= filedialog.askopenfilename(
            title=title_dialog,
            filetypes=(
                ("Archivos MP4", "*.mp4"),
        ))

        if file: 
            return {"success": True, "file_path": file}
        else:
            return {"success": False}
    
    def select_directory(self, title_dialog):
        directory = filedialog.askdirectory(title=title_dialog)
        if directory: 
            return {"success": True, "directory_path": directory}
        else:
            return {"success": False}