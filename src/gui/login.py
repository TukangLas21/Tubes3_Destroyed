import flet as ft
import os
import sys
from styles import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connector import Connector
from test_connector import test_connector

# Text Fields

host_field = create_textfield(
    label= "Host",
    hint_text="Masukkan nama host Anda"
)

username_field = create_textfield(
    label= "Username",
    hint_text="Masukkan username Anda"
)

password_field = create_textfield(
    label= "Password",
    hint_text="Masukkan password Anda",
    password=True,
    can_reveal_password=True
)

database_field = create_textfield(
    label= "Database",
    hint_text="Masukkan nama database Anda",
)

key_field = create_textfield(
    label= "Encyption Key",
    hint_text="Masukkan encryption key Anda",
    password=True,
    can_reveal_password=True
)

def form_submit_function(e):
    print("Form submitted!")
    print(f"Host: {host_field.controls[1].value}")
    print(f"Username: {username_field.controls[1].value}")
    print(f"Password: {password_field.controls[1].value}")
    print(f"Database: {database_field.controls[1].value}")
    print(f"Key: {key_field.controls[1].value}")

    connector = test_connector(
        host=host_field.controls[1].value,
        user=username_field.controls[1].value,
        password=password_field.controls[1].value,
        database=database_field.controls[1].value,
        encryption_key=key_field.controls[1].value
        )
    
    if connector is None:
        print("Connection failed. Please check your credentials.")
        return
    
    page = e.page
    page.go("/beranda")

def login_menu(page: ft.Page):
    login_container = ft.Container(
        ft.Column([
            ft.Text("Selamat datang di DestroyedCV!", style=HEADING_STYLE),
            
            # Container to set less spacing between text field
            ft.Column([
                host_field,
                username_field,
                password_field,
                database_field,
                key_field],
                spacing=8,
            ),

            ft.Row(
                controls=[
                ft.FilledButton(
                    content=ft.Text("Masuk", style=SH2_STYLE),
                    style = BUTTON_L,
                    expand=True,
                    on_click = form_submit_function
                )]
            ),
        ], horizontal_alignment = 'center', spacing=16),
        width = 510
    )

    return login_container

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
#     page.add(login_menu(page))
#     page.update()
# ft.app(main)
