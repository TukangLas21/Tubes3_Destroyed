import flet as ft

def main(page: ft.Page):
    page.title = "DestroyedCV"
    page.window.width = 1280
    page.window.height = 720

    # maaf ya ga ada bikin responsif responsif an awokawoka
    page.window.min_width = 1280
    page.window.min_height = 720
    page.window.max_width = 1280
    page.window.max_height = 720

    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    
    # Asset setup
    page.fonts = {
        "SF Pro Regular": "./gui/assets/fonts/SF-Pro-Text-Regular.otf",
        "SF Pro Medium": "./gui/assets/fonts/SF-Pro-Text-Medium.otf"
    }
    page.theme = ft.Theme(font_family="SF Pro Regular") # Default app font

    page.decoration = ft.BoxDecoration (
        image = ft.DecorationImage(
        src= 'gui/assets/bg.png',
        fit= ft.ImageFit.COVER
        )
    )

    # Page setup
    page.bgcolor = ft.Colors.TRANSPARENT
    page.add(
        ft.Text("Halo! First version", font_family="SF Pro Medium", size=44),
        ft.Text("Ditunggu update-update selanjutnya very soon :D")
    )
    
ft.app(target=main)