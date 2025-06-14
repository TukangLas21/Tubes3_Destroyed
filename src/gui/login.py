import flet as ft
from styles import *

# Text Fields
host_field = ft.TextField(
    label="Host", border=ft.InputBorder.NONE,
    filled=True, hint_text="Masukkan nama host Anda",
)
username_field = ft.TextField(
    label="Username", border=ft.InputBorder.NONE,
    filled=True, hint_text="Masukkan username Anda",
)
password_field = ft.TextField(
    label="Password", password=True, can_reveal_password=True, border=ft.InputBorder.NONE,
    filled=True, hint_text="Masukkan password Anda",
)
database_field = ft.TextField(
    label="Database", border=ft.InputBorder.NONE,
    filled=True, hint_text="Masukkan nama database Anda",
)


def form_submit_function(e): # nanti integrate backend disini
    print("Form submitted!")
    print(f"Host: {host_field.value}")
    print(f"Username: {username_field.value}")
    print(f"Password: {password_field.value}")
    print(f"Database: {database_field.value}")

login_container = ft.Container(
    ft.Column([
        ft.Text("Selamat datang di DestroyedCV!", style=HEADING_STYLE),
        host_field,
        username_field,
        password_field,
        database_field,

        ft.Button(
            "Masuk",
            width = 511, height = 70,
            style = BUTTON_L,
            on_click = form_submit_function
        ),
    ], horizontal_alignment = 'center'),
    width = 550, height=511, alignment=ft.alignment.center, expand=True
)
def main(page:ft.Page):
    page.title = "DestroyedCV"
    page.window.width = 1280
    page.window.height = 720
    
    page.window.min_width = 1280
    page.window.min_height = 720
    page.window.max_width = 1280
    page.window.max_height = 720

    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.bgcolor='red'

    page.fonts = {
        "SF Pro Regular": "./assets/fonts/SF-Pro-Text-Regular.otf",
        "SF Pro Medium": "./assets/fonts/SF-Pro-Text-Medium.otf",
    }
    page.theme = ft.Theme(font_family="SF Pro Regular")

    # Page BG
    bg_image = ft.Image(
        src="assets/bg.png",
        width = 1280,
        height = 720,
        fit=ft.ImageFit.COVER,
    )

    # Page setup
    page.bgcolor = ft.Colors.TRANSPARENT
    st = ft.Stack(
        [
            bg_image,
            ft.Container(
                content=login_container,
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        expand=True
    )

    page.add(st)
ft.app(main)
