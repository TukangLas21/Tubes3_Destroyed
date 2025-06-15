import flet as ft
import os
import sys
from urllib.parse import urlencode
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

def search_submit_function(e):
    page = e.page
    
    print("Search submitted!")
    
    # Get values with proper error handling
    try:
        keywords = keyword_field.controls[1].value
        top_matches = top_matches_field.controls[1].value
        algoritma = list(algoritma_option.controls[1].selected)[0] if algoritma_option.controls[1].selected else "KMP"
        
        print(f"Kata Kunci: {keywords}")
        print(f"Jumlah Top Matches: {top_matches}")
        print(f"Algoritma: {algoritma}")
        
        # Validation
        if not keywords or not keywords.strip():
            print("Keywords cannot be empty.")
            status_text_exact.value = "Error: Kata kunci tidak boleh kosong."
            status_text_fuzzy.value = ""
            page.update()
            return
            
        if not top_matches or not top_matches.strip():
            print("Top matches cannot be empty.")
            status_text_exact.value = "Error: Jumlah top matches tidak boleh kosong."
            status_text_fuzzy.value = ""
            page.update()
            return
        
        # Convert top_matches to int
        try:
            top_matches_int = int(top_matches)
            if top_matches_int <= 0:
                raise ValueError("Top matches must be positive")
        except ValueError:
            print("Invalid top matches value.")
            status_text_exact.value = "Error: Jumlah top matches harus berupa angka positif."
            status_text_fuzzy.value = ""
            page.update()
            return
        
        # Show loading
        page.splash = ft.ProgressBar()
        status_text_exact.value = "Sedang mencari..."
        status_text_fuzzy.value = ""
        result_container.visible = True
        cards_area.controls.clear()
        page.update()
        
        # Perform search
        try:
            search_result = start_search(
                keywords=keywords,
                algorithm=algoritma,
                number_of_results=top_matches_int
            )
            
            # Debug: Print the type and structure of search_result
            print(f"Search result type: {type(search_result)}")
            print(f"Search result: {search_result}")
            
            # Handle different return formats from start_search
            if isinstance(search_result, tuple):
                if len(search_result) == 3:
                    results, exact_search_result, fuzzy_search_result = search_result
                else:
                    # Handle unexpected tuple length
                    print(f"Unexpected tuple length: {len(search_result)}")
                    results = search_result[0] if search_result else []
                    exact_search_result = search_result[1] if len(search_result) > 1 else 0
                    fuzzy_search_result = search_result[2] if len(search_result) > 2 else 0
            else:
                # If start_search returns only results
                results = search_result
                exact_search_result = 0
                fuzzy_search_result = 0
            
            # Ensure results is a list
            if not isinstance(results, list):
                print(f"Warning: results is not a list, it's {type(results)}")
                results = []
            
            print(f"Results type: {type(results)}")
            print(f"Results length: {len(results) if isinstance(results, list) else 'N/A'}")
            
            Connector.get_instance().connect()
            total_CVs = len(Connector.get_instance().get_paths_id())
            Connector.get_instance().close()
            # Update status texts
            status_text_exact.value = f"Exact Match: {total_CVs} diproses dalam {exact_search_result:.4f} detik."
            if fuzzy_search_result == 0:
                status_text_fuzzy.value = "Fuzzy Match tidak dijalankan."
            else:
                status_text_fuzzy.value = f"Fuzzy Match dijalankan dalam {fuzzy_search_result:.4f} detik."
            
            # Clear previous results
            cards_area.controls.clear()
            
            # Display results with better error handling
            if not results or len(results) == 0:
                cards_area.controls.append(
                    ft.Container(
                        content=ft.Text("Tidak ada hasil yang ditemukan.", style=BODY1_SECONDARY_STYLE),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20)
                    )
                )
            else:
                # Get top results safely
                top_results = results[:top_matches_int] if len(results) >= top_matches_int else results
                
                print(f"Top results length: {len(top_results)}")
                
                # Create cards in rows of 3
                current_row = ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER, wrap=True)
                
                for index, result in enumerate(top_results):
                    print(f"Processing result {index}: {type(result)}")
                    
                    # Add card to current row
                    if index > 0 and index % 3 == 0:
                        cards_area.controls.append(current_row)
                        current_row = ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER, wrap=True)
                    
                    # Create card with proper data
                    try:
                        card = create_result_card(result)
                        # Set data for buttons safely
                        if (hasattr(card, 'content') and 
                            hasattr(card.content, 'controls') and 
                            len(card.content.controls) > 2 and
                            hasattr(card.content.controls[2], 'controls') and
                            len(card.content.controls[2].controls) > 1):
                            
                            card.content.controls[2].controls[0].data = {
                                'detail_id': result.get('detail_id'),
                                'applicant_id': result.get('applicant_id'),
                                'cv_path': result.get('cv_path')
                            }
                            card.content.controls[2].controls[1].data = {
                                'detail_id': result.get('detail_id'),  # Added detail_id for CV page
                                'cv_path': result.get('cv_path')
                            }
                        
                        current_row.controls.append(card)
                        
                    except Exception as card_error:
                        print(f"Error creating card for result {index}: {card_error}")
                        # Skip this result and continue
                        continue
                
                # Add the last row if it has cards
                if current_row.controls:
                    cards_area.controls.append(current_row)
            
            # Make result container visible and remove loading
            result_container.visible = True
            page.splash = None
            page.update()
            
        except Exception as search_error:
            print(f"Search error: {search_error}")
            import traceback
            traceback.print_exc()  # This will print the full stack trace
            
            status_text_exact.value = f"Error: Terjadi kesalahan saat pencarian - {str(search_error)}"
            status_text_fuzzy.value = ""
            cards_area.controls.clear()
            cards_area.controls.append(
                ft.Container(
                    content=ft.Text("Terjadi kesalahan saat pencarian. Silakan coba lagi.", style=BODY1_SECONDARY_STYLE),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
            )
            page.splash = None
            page.update()
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()  # This will print the full stack trace
        
        status_text_exact.value = f"Error: Terjadi kesalahan tak terduga - {str(e)}"
        status_text_fuzzy.value = ""
        page.splash = None
        page.update()

# Search Container
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
    margin = ft.margin.only(bottom=56),
    width = 510
)

''' RESULT  '''
def summary_function(e):
    try:
        detail_id = e.control.data['detail_id']
        applicant_id = e.control.data['applicant_id']
        page = e.page
        
        params = {
            'detail_id': str(detail_id),
            'applicant_id': str(applicant_id)
        }
        url_params = urlencode(params)
        
        print(f"Summary clicked for: {detail_id}, {applicant_id}")
        print(f"Navigating to summary with params: /summary?{url_params}")
        page.go(f"/summary?{url_params}")
    except Exception as ex:
        print(f"Summary function error: {ex}")

def cv_function(e):
    try:
        detail_id = e.control.data['detail_id']
        page = e.page
        params = {
            'detail_id': str(detail_id)
        }
        url_params = urlencode(params)
        print(f"CV clicked for: {detail_id}")
        page.go(f"/cv?{url_params}")
    except Exception as ex:
        print(f"CV function error: {ex}")


def create_result_card(result_data: dict):
    keywords_column = ft.Column(spacing=2, scroll=ft.ScrollMode.HIDDEN)
    keywords_column.controls.append(ft.Text("Matched keywords:", style=BODY2_SECONDARY_STYLE))
    
    # Handle keywords_matches safely
    keywords_matches = result_data.get('keywords_matches', {})
    if keywords_matches:
        for keyword, match_info in keywords_matches.items():
            try:
                # Handle both list and tuple formats
                if isinstance(match_info, (list, tuple)) and len(match_info) >= 2:
                    count, match_type = match_info[0], match_info[1]
                elif isinstance(match_info, (list, tuple)) and len(match_info) == 1:
                    count, match_type = match_info[0], "exact"
                elif isinstance(match_info, (int, float)):
                    count, match_type = match_info, "exact"
                else:
                    # Fallback for unexpected formats
                    count, match_type = str(match_info), "unknown"
                
                # Ensure count is a number for display
                if isinstance(count, (int, float)):
                    count_text = str(int(count))
                else:
                    count_text = str(count)
                
                # Create the display text
                occurrence_text = "occurrence" if int(count) == 1 else "occurrences"
                keywords_column.controls.append(
                    ft.Text(f"{keyword}: {count_text} {occurrence_text} ({match_type})", 
                            style=BODY2_SECONDARY_STYLE)
                )
                
            except Exception as e:
                print(f"Error processing keyword {keyword} with match_info {match_info}: {e}")
                # Add a fallback display
                keywords_column.controls.append(
                    ft.Text(f"{keyword}: {str(match_info)}", 
                            style=BODY2_SECONDARY_STYLE)
                )
    else:
        keywords_column.controls.append(
            ft.Text("No keyword matches found", style=BODY2_SECONDARY_STYLE)
        )
    
    # Handle profile data safely
    profile = result_data.get('profile', {})
    first_name = profile.get('first_name', 'Unknown')
    last_name = profile.get('last_name', 'Unknown')
    accuracy_score = result_data.get('accuracy_score', 0)
    
    # Ensure accuracy_score is displayable
    try:
        accuracy_score_text = str(int(accuracy_score)) if isinstance(accuracy_score, (int, float)) else str(accuracy_score)
    except:
        accuracy_score_text = "0"
    
    card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"{first_name} {last_name}", style=BODY1_PRIMARY_STYLE),
                ft.Text(f"{accuracy_score_text} Matches", style=BODY2_SECONDARY_STYLE)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=keywords_column, 
                height=100, 
                padding=ft.padding.only(top=5)
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
        border=ft.border.all(width=1, color=APP_COLORS["white-transparent"]),
        width=300  # Fixed width for consistent layout
    )
    return card

# Result Container - Fixed
status_text_exact = ft.Text("Menunggu pencarian...", style=BODY1_SECONDARY_STYLE)
status_text_fuzzy = ft.Text("", style=BODY1_SECONDARY_STYLE)
cards_area = ft.Column(
    spacing=16,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)

result_container = ft.Container(
    ft.Column([
        ft.Text("Hasil Pencarian", style=HEADING_STYLE),
        status_text_exact,
        status_text_fuzzy,
        cards_area,  # Added cards_area to the result container
    ],
    spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER, 
    ),
    alignment=ft.alignment.top_center,
    expand=True,
    visible=False,  # Initially hidden
)

''' SEARCH + RESULT (Result di bawah Search) '''
search_and_result = ft.Container(
    ft.Column([
        search_container,
        result_container,
    ],
    spacing = 24,
    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    scroll = ft.ScrollMode.AUTO,  # Changed to AUTO for better scrolling
    expand = True,
    ),
    width = 1000,
    alignment = ft.alignment.top_center, 
    expand = True,
)