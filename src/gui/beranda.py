import flet as ft
from styles import *
def beranda_menu(page: ft.Page):
    beranda_content = ft.Container(
        ft.Column(
            controls=[
                ft.Text(
                    "Rekrutmen Lebih Cerdas,\nSaring Para Vibecoders.",
                    style=DISPLAY_STYLE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Tinggali input data manual, biarkanlah DestroyedCV bekerja untuk Anda.",
                    style=CAPTION_STYLE,
                    text_align=ft.TextAlign.CENTER
                ),

                ft.FilledButton(
                    content=ft.Row(
                        [
                            ft.Text("Mulai Sekarang", style=SH1_STYLE),
                            ft.Icon(ft.Icons.ARROW_FORWARD)
                        ],
                        tight=True # Makes the row take minimum space
                    ),
                    style=BUTTON_M,
                    on_click=lambda _: page.go("/search")
                ),
            ],
            spacing=24,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(bottom=56)  # Shift up by half the navbar height (from container) #might be refactored
        )
    return beranda_content

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
#     page.add(beranda_menu(page))
#     page.update()
# ft.app(main)