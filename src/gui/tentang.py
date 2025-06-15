import flet as ft
from styles import *

tentang_content = ft.Container(
    ft.Column(
        controls=[
            ft.Text(
                "Kelompok 11 - Destroyed",
                style=DISPLAY_STYLE,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Column([
                ft.Text(
                    "1. Nicholas Andhika Lucas (13523014)",
                    style=CAPTION_STYLE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "2. Aria Judhistira (13523112)",
                    style=CAPTION_STYLE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "3. Ignacio Kevin Alberiann (15223090)",
                    style=CAPTION_STYLE,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),

        ],
        spacing=24,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    margin=ft.margin.only(bottom=56)  # Shift up by half the navbar height (from container) #might be refactored
    )

''' Individual Page Testing :D '''
# def main(page:ft.Page):
#     page.title = "DestroyedCV"
#     page.window.width = 1280
#     page.window.height = 720
    
#     page.window.min_width = 1280
#     page.window.min_height = 720
#     page.window.max_width = 1280
#     page.window.max_height = 720

#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.bgcolor=ft.Colors.TRANSPARENT

#     page.fonts = {
#         "SF Pro Regular": "./assets/fonts/SF-Pro-Text-Regular.otf",
#         "SF Pro Medium": "./assets/fonts/SF-Pro-Text-Medium.otf",
#     }
#     page.theme = ft.Theme(font_family="SF Pro Regular")

#     # Page setup
#     page.bgcolor = ft.Colors.TRANSPARENT
#     page.decoration = bg_image
#     page.appbar = navbar
#     page.add(tentang_content)
#     page.update()
# ft.app(main)