import flet as ft
from styles import *

''' SEARCH  '''
# Input Fields
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

# Search Containernya
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

''' RESULT  '''
def summary_function(e):
    page = e.page
    page.go("/summary")

def cv_function(e):
    page = e.page
    page.go("/cv")

# Result cards
def create_result_card(name: str, matches: int,):
    return ft.Container(
    ft.Column([
        # Bagian atas
        ft.Column([
            # Judul dan Matches
            ft.Row([
                ft.Text(name, style = SH1_STYLE),
                ft.Text(f"{matches} {'Matches' if (matches > 1) else 'Match'}", 
                        style = BODY1_SECONDARY_STYLE),
            ],
            spacing = 16,
            ),

            # Matches keywords
            ft.Column([
                ft.Text("Matched keywords:", style = BODY2_SECONDARY_STYLE),
                ft.Text("React: 1 occurence (ini diappend nanti)", style = BODY2_SECONDARY_STYLE),
                ft.Text("Express: 1 occurence", style = BODY2_SECONDARY_STYLE),
                ft.Text("HTML: 1 occurence", style = BODY2_SECONDARY_STYLE),
                ft.Text("HTML: 1 occurence", style = BODY2_SECONDARY_STYLE),
                ft.Text("HTML: 1 occurence", style = BODY2_SECONDARY_STYLE),
            ],
            spacing = 0,
            height = 100,
            scroll = ft.ScrollMode.HIDDEN, # scroll jika keywordnya banyak
            )
        ],
        # Pengaturan Column
        spacing = 12,
        ),

        # Bagian Bawah
        ft.Row([
            ft.FilledButton(
                content = ft.Text("Summary", style = BODY1_PRIMARY_STYLE),
                style = BUTTON_S,
                on_click = summary_function
            ),
            ft.FilledButton(
                content = ft.Text("Lihat CV", style = BODY1_PRIMARY_STYLE),
                style = BUTTON_S,
                on_click = cv_function
            ),
        ],
        expand = True,
        ),

    ],
    # Pengaturan Column
    spacing = 44,
    width = 230,
    ),
    # Pengaturan column container (glass style)
    bgcolor = APP_COLORS["glass"],
    padding = ft.padding.symmetric(horizontal = 32, vertical = 32),
    border_radius = 24, border = ft.border.all(width = 1, color = APP_COLORS["white-transparent"])
)

# Result Container
result_container = ft.Container(
    ft.Column([
        # Title
        ft.Column([
            ft.Text("Hasil Pencarian", style = HEADING_STYLE),
            ft.Text("Exact Match: 100 CVs di-scan dalam 100 ms.", style = BODY1_SECONDARY_STYLE),
            ft.Text("Fuzzy Match: 100 CVs di-scan dalam 100 ms.", style = BODY1_SECONDARY_STYLE)
        ],
        spacing = 0,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        ),

        # Result Cards, 3 cards per row
        ft.Column([
            # 1st Row of Cards
            ft.Row([
                create_result_card(name="Lucas", matches=4),
                create_result_card(name="Nicoa", matches=1),
                create_result_card(name="Lucas", matches=4),
            ],
            spacing = 16),

            # 2nd Row of Cards
            ft.Row([
                create_result_card(name="Lucas", matches=4),
                create_result_card(name="Nicoa", matches=1),
                create_result_card(name="Lucas", matches=4),
            ],
            spacing = 16),
        ],
        spacing = 16)

    ],
    spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    ),
    alignment = ft.alignment.top_center, expand = True
)

''' SEARCH + RESULT (Result di bawah Search) '''
search_and_result = ft.Container(
    ft.Column([
        # berlapis yak tapi ini biar bisa onclick
        search_container,
        result_container,
    ],
    spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    scroll = ft.ScrollMode.HIDDEN,
    expand = True,

    ),
width = 1000,
alignment = ft.alignment.top_center, expand = True,
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
#     page.add(search_and_result)
#     page.update()
# ft.app(main)