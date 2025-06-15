import flet as ft
from urllib.parse import parse_qs, urlparse
from styles import *
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connector import Connector
from pdf_processor import extract_text_regex
from app import *

def back_function(e):
    page = e.page
    page.go("/")  # Navigate back to main search page

def get_cv_text_by_detail_id(detail_id: int) -> str:
    # Cari CV path
    Connector.get_instance().connect()
    cv_path = Connector.get_instance().get_decrypted_cv(detail_id)
    Connector.get_instance().close()
    
    # get text
    if cv_path is None:
        return "CV tidak ditemukan."
    
    if not os.path.exists(cv_path):
        return "CV tidak ditemukan di path yang diberikan."
    
    cv_text = extract_text_regex(cv_path)
    if cv_text is None:
        return "Gagal memuat CV. Pastikan file PDF valid."
    
    return cv_text.strip() if cv_text else "CV tidak ditemukan atau kosong."

def get_cv_owner_name(detail_id: int) -> str:
    """
    Replace this function with your actual function to get CV owner name
    This should return the name of the CV owner based on detail_id
    """
    Connector.get_instance().connect()
    cv_owner_name = Connector.get_instance().get_decrypted_name(detail_id)
    Connector.get_instance().close()
    
    if cv_owner_name is None:
        return "CV Owner tidak ditemukan."

    if not cv_owner_name.strip():
        return "CV Owner tidak ditemukan atau kosong."
    
    return cv_owner_name.strip()

def create_cv_content(page_route: str = ""):
    """
    Create CV content based on URL parameters
    """
    detail_id = None
    cv_owner_name = "Unknown"
    cv_text = "CV tidak ditemukan."
    
    try:
        # Parse URL to get detail_id parameter
        if "?" in page_route:
            query_string = page_route.split("?")[1]
            params = parse_qs(query_string)
            
            if 'detail_id' in params and params['detail_id']:
                detail_id = int(params['detail_id'][0])
                print(f"CV page loaded with detail_id: {detail_id}")
                
                # Get CV text using your function
                cv_text = get_cv_text_by_detail_id(detail_id)
                cv_owner_name = get_cv_owner_name(detail_id)
                
                print(f"CV loaded for: {cv_owner_name}")
            else:
                cv_text = "Error: detail_id tidak ditemukan dalam URL."
                print("Error: No detail_id found in URL parameters")
        else:
            cv_text = "Error: Tidak ada parameter yang ditemukan dalam URL."
            print("Error: No URL parameters found")
            
    except ValueError as ve:
        cv_text = f"Error: detail_id tidak valid - {str(ve)}"
        print(f"Error parsing detail_id: {ve}")
    except Exception as e:
        cv_text = f"Error: Terjadi kesalahan saat memuat CV - {str(e)}"
        print(f"Error loading CV: {e}")
    
    # Create the CV content container
    cv_content = ft.Container(
        ft.Column([
            # Back button and header
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.ARROW_BACK, color=APP_COLORS["white"]),
                    ft.Text(
                        f"Menunjukkan CV: {cv_owner_name}",
                        style=HEADING_STYLE,
                        text_align=ft.TextAlign.CENTER
                    ),
                ], 
                tight=True
                ),
                on_click=back_function
            ),
            # CV content area
            ft.Container(
                ft.Column([
                    ft.Text(
                        cv_text, 
                        style=BODY2_SECONDARY_STYLE,
                        selectable=True,  # Allow text selection for copying
                        no_wrap=False,    # Allow text wrapping
                    ),
                ],
                spacing=8,
                width=650,
                scroll=ft.ScrollMode.AUTO,  # Allow scrolling if content is long
                ),
                bgcolor=APP_COLORS["glass"],
                padding=ft.padding.symmetric(horizontal=32, vertical=32),
                border_radius=24, 
                border=ft.border.all(width=1, color=APP_COLORS["white-transparent"]),
                expand=True,  # Allow container to expand
            ),
        ],
        spacing=24,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        ),
        alignment=ft.alignment.top_center, 
        expand=True,
    )

    return cv_content

# For backwards compatibility, keep the original cv_content for static display
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