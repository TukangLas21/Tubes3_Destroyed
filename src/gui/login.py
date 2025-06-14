import flet as ft
from styles import *

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
    hint_text="Masukkan nama database Anda"
)

def form_submit_function(e):
    print("Form submitted!")
    # The text field values will be accessible here because they are in the same scope
    print(f"Host: {host_field.controls[1].value}")
    print(f"Username: {username_field.controls[1].value}")
    print(f"Password: {password_field.controls[1].value}")
    print(f"Database: {database_field.controls[1].value}")

login_container = ft.Container(
    ft.Column([
        ft.Text("Selamat datang di DestroyedCV!", style=HEADING_STYLE),
        
        # Container to set less spacing between text field
        ft.Column([
            host_field,
            username_field,
            password_field,
            database_field],
            spacing=12,
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
    ], horizontal_alignment = 'center', spacing=24),
    width = 510
)
def main(page:ft.Page):
    page.title = "DestroyedCV"
    page.window.width = 1280
    page.window.height = 720
    
    page.window.min_width = 1280
    page.window.min_height = 720
    page.window.max_width = 1280
    page.window.max_height = 720

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor=ft.Colors.TRANSPARENT

    page.fonts = {
        "SF Pro Regular": "./assets/fonts/SF-Pro-Text-Regular.otf",
        "SF Pro Medium": "./assets/fonts/SF-Pro-Text-Medium.otf",
    }
    page.theme = ft.Theme(font_family="SF Pro Regular")

    # Page setup
    page.bgcolor = ft.Colors.TRANSPARENT
    page.decoration = ft.BoxDecoration (
        image = ft.DecorationImage(
            src= 'assets/bg.png',
            fit= ft.ImageFit.COVER
        )
    )
    page.add(login_container)
    page.update()
ft.app(main)
