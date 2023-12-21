import flet as ft

from .ui import AppUI
from .constants import TITLE, WIDTH, HEIGHT, PADDING


class EnergyAuditApp:
    @staticmethod
    def config(page: ft.Page) -> None:
        page.title = TITLE
        page.window_width = WIDTH
        page.window_height = HEIGHT
        page.window_min_width = WIDTH
        page.window_min_height = HEIGHT
        page.padding = PADDING
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.LIGHT
        page.scroll = ft.ScrollMode.AUTO
        page.update()
        app = AppUI(page)
        page.add(app)

    def start(self) -> None:
        ft.app(target=self.config)
