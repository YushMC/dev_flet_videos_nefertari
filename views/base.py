from abc import ABC, abstractmethod
import flet as ft

class AllViews(ABC):
    @abstractmethod
    async def get_view(self) -> ft.View:
        pass