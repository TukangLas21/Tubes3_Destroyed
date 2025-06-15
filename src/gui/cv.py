import flet as ft
from styles import *

# nanti ganti ya mas BE
def back_function(e):
    page = e.page
    page.on_view_pop

cv_content = ft.Container(
    ft.Column([
        # berlapis yak tapi ini biar bisa onclick
        ft.Container(
            ft.Row([
                ft.Icon(ft.Icons.ARROW_BACK, color=APP_COLORS["white"]),
                ft.Text(
                    "Menunjukkan CV: Lucas", # jangan lupa ganti ini sesuai pemilik CV
                    style = HEADING_STYLE,
                    text_align = ft.TextAlign.CENTER
                ),
            ], 
            tight=True
            ),
            on_click = back_function
        ),
        ft.Container(
            ft.Column(
                spacing = 8,
                controls = [
                    ft.Text("Lucas", style = BODY1_PRIMARY_STYLE),
                    ft.Text("Birthdate: 10-06-2025\nAddress: R.9009 ITB\nPhone: 0912 3456 7890", 
                            style = BODY2_SECONDARY_STYLE),

                    ft.Text("Skills", style = BODY1_PRIMARY_STYLE),
                    ft.Text("React, Express, NextJS", 
                            style = BODY2_SECONDARY_STYLE),

                    ft.Text("Job History", style = BODY1_PRIMARY_STYLE),
                    ft.Text("UI/UX Designer (2025-2050)\nLeading the organization for UX Research and Design", 
                            style = BODY2_SECONDARY_STYLE),
                    ft.Text("Graphic Designer (2020-2020)\nFreelance graphic designer for top clients like Danantara", 
                            style = BODY2_SECONDARY_STYLE),

                    ft.Text("Education", style = BODY1_PRIMARY_STYLE),
                    ft.Text("Informatics Engineering (Institut Teknologi Bandung)\n2023-2027", 
                            style = BODY2_SECONDARY_STYLE),

                    ft.Text("Education", style = BODY1_PRIMARY_STYLE),
                    ft.Text("Informatics Engineering (Institut Teknologi Bandung)\n2023-2027", 
                            style = BODY2_SECONDARY_STYLE),
                ],
                width = 650,
            ),
            bgcolor = APP_COLORS["glass"],
            padding = ft.padding.symmetric(horizontal = 32, vertical = 32),
            border_radius = 24, border = ft.border.all(width = 1, color = APP_COLORS["white-transparent"])
        ),
    ],
    spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    scroll = ft.ScrollMode.HIDDEN,
    expand = True,

    ),
alignment = ft.alignment.top_center, expand = True,
# margin=ft.margin.only(bottom=56),
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
#     page.add(summary_content)
#     page.update()
# ft.app(main)