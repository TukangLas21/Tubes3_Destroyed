import flet as ft
from styles import *

#Text Fields
keyword_field = create_textfield(
    label= "Kata Kunci",
    hint_text="Contoh: React, NextJS, Java"
)

top_matches_field = create_textfield(
    label = "Top Matches",
    hint_text = "Contoh: 5",
    input_filter=ft.NumbersOnlyInputFilter(),
    # width = 140
)

def handle_change(e):
    print("on_change data : " + str(e.data))

algoritma_option = ft.Column(
    [
        ft.Text("Algoritma", style=SH2_STYLE),
        ft.SegmentedButton(
            on_change=handle_change,
            style = BUTTON_OPTION_DEFAULT,
            show_selected_icon = True,
            selected={"KMP"}, # ini buat nunjukin contoh keselect aja
            segments = [
                ft.Segment(value="KMP", label=ft.Text("KMP", width=100, style=BODY1_PRIMARY_STYLE, text_align = 'center')),
                ft.Segment(value="BM", label=ft.Text("BM", width=100, style=BODY1_PRIMARY_STYLE, text_align = 'center')),
                ft.Segment(value="Aho-Cor", label=ft.Text("Aho-Cor", width=100, style=BODY1_PRIMARY_STYLE, text_align = 'center')),
            ]
        )
    ]
)

# Sesuaikan fungsinya mas backend
def search_submit_function(e):
    print("Search submitted!")
    print(f"Kata Kunci: {keyword_field.controls[1].value}")
    print(f"Jumlah Top Matches: {top_matches_field.controls[1].value}")
    print(f"Algoritma: {algoritma_option.controls[1].selected}")


    
search_container = ft.Container(
    ft.Column([
        ft.Text("Cari CV Sesuai Keinginanmu", style=HEADING_STYLE),
        # Container to set less spacing between input field
        ft.Column([
            keyword_field,
            top_matches_field,
            algoritma_option], 
            spacing=12
        ),

        ft.Row([
            ft.FilledButton(
                content=ft.Text("Buat Pencarian", style=SH2_STYLE),
                style = BUTTON_L,
                expand=True,
                on_click = search_submit_function
            )]
        ),
    ],
    spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    ),
    margin = ft.margin.only(bottom=56),  # Shift up by half the navbar height (from container) #might be refactored
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
    page.decoration = bg_image
    page.appbar = navbar
    page.add(search_container)
    page.update()
ft.app(main)