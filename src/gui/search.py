import flet as ft
import os
import sys
from styles import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connector import Connector
from app import *

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
                ft.Segment(value="AC", label=ft.Text("Aho-Cor", width=100, style=BODY1_PRIMARY_STYLE, text_align = 'center')),
            ]
        )
    ]
)

# Sesuaikan fungsinya mas backend
def search_submit_function(e):
    page = e.page
    
    print("Search submitted!")
    keywords = keyword_field.controls[1].value
    print(f"Kata Kunci: {keyword_field.controls[1].value}")
    top_matches = top_matches_field.controls[1].value
    print(f"Jumlah Top Matches: {top_matches_field.controls[1].value}")
    algoritma = algoritma_option.controls[1].selected
    print(f"Algoritma: {algoritma_option.controls[1].selected}")
    
    if not keyword_field.controls[1].value or not top_matches_field.controls[1].value:
        print("Please fill in all fields.")
        return
    
    page.splash = ft.ProgressBar()
    page.update()
    
    results, exact_search_result, fuzzy_search_result = start_search(
        keywords=keywords,
        algorithm=algoritma,
        number_of_results=int(top_matches)
    )
    
    status_text_exact.value = f"Exact Match: {len(results)} CV ditemukan dalam {exact_search_result:.4f} detik."
    if fuzzy_search_result == 0:
        status_text_fuzzy.value = "Fuzzy Match tidak dijalankan."
    else:
        status_text_fuzzy.value = f"Fuzzy Match dijalankan dalam {fuzzy_search_result:.4f} detik."
    
    cards_area.controls.clear()
    
    top_results = results[:int(top_matches)]
    if not top_results:
        cards_area.controls.append(ft.Text("Tidak ada hasil yang ditemukan.", style=BODY1_SECONDARY_STYLE))
    else:
        row_of_cards = ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER)
        for i, res in enumerate(top_results):
            if i > 0 and i % 3 == 0:
                cards_area.controls.append(row_of_cards)
                row_of_cards = ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER)
            row_of_cards.controls.append(create_result_card(res))
        cards_area.controls.append(row_of_cards)
        
    result_container.visible = True
    page.splash = None
    page.update()   
    

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
    detail_id = e.control.data['detail_id']
    applicant_id = e.control.data['applicant_id']
    cv_path = e.control.data['cv_path']
    page = e.page
    page.go("/summary")

def cv_function(e):
    cv_path = e.control.data['cv_path']
    page = e.page
    page.go("/cv")

# Result cards
def create_result_card(result_data: dict):
    keywords_column = ft.Column(spacing=2, scroll=ft.ScrollMode.HIDDEN)
    keywords_column.controls.append(ft.Text("Matched keywords:", style=BODY2_SECONDARY_STYLE))
    
    for keyword, (count, match_type) in result_data['keywords_matches'].items():
        keywords_column.controls.append(
            ft.Text(f"{keyword}: {count} occurence{'s' if count > 1 else ''} ({match_type})", 
                    style=BODY2_SECONDARY_STYLE)
        )
        
    card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(result_data['profile']['first_name'] + " " + result_data['profile']['last_name'], style=BODY1_PRIMARY_STYLE),
                ft.Text(f"{result_data['accuracy_score']} Matches", style=BODY2_SECONDARY_STYLE)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=keywords_column, height=100, padding=ft.padding.only(top=5)
            ),
            ft.Row([
                ft.FilledButton(
                    content=ft.Text("Summary", style=BODY1_PRIMARY_STYLE),
                    style=BUTTON_S,
                    on_click=summary_function
                ),
                ft.FilledButton(
                    content=ft.Text("Lihat CV", style=BODY1_PRIMARY_STYLE),
                    style=BUTTON_S,
                    on_click=cv_function
                ),
            ]),
        ]),
        bgcolor=APP_COLORS["glass"],
        padding=ft.padding.symmetric(horizontal=32, vertical=32),
        border_radius=24, 
        border=ft.border.all(width=1, color=APP_COLORS["white-transparent"])
    )
    return card

# Result Container
status_text_exact = ft.Text("Menunggu pencarian...", style=BODY1_SECONDARY_STYLE)
status_text_fuzzy = ft.Text("", style=BODY1_SECONDARY_STYLE)
cards_area = ft.Column(
    wrap=True,
    run_spacing=16,
    spacing=16,
    alignment=ft.MainAxisAlignment.CENTER
)

result_container = ft.Container(
    ft.Column([
        ft.Text("Hasil Pencarian", style=HEADING_STYLE),
        status_text_exact,
        status_text_fuzzy,
    ],spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER, 
    ),
    alignment=ft.alignment.top_center,
    expand=True,
    visible=False,  # Initially hidden
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