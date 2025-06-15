import flet as ft
from styles import *
import login, beranda, search, summary, cv, tentang

def main(page: ft.Page):
    ''' Page Setup '''
    page.title = "DestroyedCV"
    page.window.width = 1280
    page.window.height = 720

    # maaf ya ga ada bikin responsif responsif an awokawoka
    page.window.min_width = 1280
    page.window.min_height = 720
    page.window.max_width = 1280
    page.window.max_height = 720

    # Load fonts
    page.fonts = {
        "SF Pro Regular": "./assets/fonts/SF-Pro-Text-Regular.otf",
        "SF Pro Medium": "./assets/fonts/SF-Pro-Text-Medium.otf",
    }
    page.theme = ft.Theme(font_family="SF Pro Regular")

    # page.vertical_alignment = ft.MainAxisAlignment.CENTER,
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER,

    # # Load BG Image
    # page.bgcolor = ft.Colors.TRANSPARENT
    # page.decoration = bg_image

    # Load navbar with routing function
    main_navbar = create_navbar(page)
    
    ''' Page Navigation '''
    def route_change(route: ft.RouteChangeEvent):
        # Clear current stack of page view
        page.views.clear()
        
        # Append first page, homepage as index page
        page.views.append(
            ft.View(
                route = "/",
                controls = [
                    # ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    # ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                    login.login_menu(page)
                ],
                # *** VIEW SETUP ***
                vertical_alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                # Load BG Image
                bgcolor = ft.Colors.TRANSPARENT,
                decoration = bg_image,
            )
        )

        # ''' PLACEHOLDER '''
        # if page.route == "/store":
        #     page.views.append(
        #         ft.View(
        #             route = "/store",
        #             controls = [
        #                 ft.AppBar(title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
        #                 ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        #             ],
        #         )
        #     )

        ''' Beranda '''
        if page.route == "/beranda":
            page.views.append(
                ft.View(
                    route = "/beranda",
                    controls = [
                        beranda.beranda_menu(page)
                    ],
                    # *** VIEW SETUP ***
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    appbar = main_navbar,
                    # Load BG Image
                    bgcolor = ft.Colors.TRANSPARENT,
                    decoration = bg_image,
                )
           )
           
        ''' Search '''
        if page.route == "/search":
            page.views.append(
                ft.View(
                    route = "/search",
                    controls = [
                        search.search_and_result
                    ],
                    # *** VIEW SETUP ***
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    appbar = main_navbar,
                    # Load BG Image
                    bgcolor = ft.Colors.TRANSPARENT,
                    decoration = bg_image,
                )
           )
           
        ''' Summary '''
        if page.route == "/summary":
            page.views.append(
                ft.View(
                    route = "/summary",
                    controls = [
                        summary.summary_content
                    ],
                    # *** VIEW SETUP ***
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    appbar = main_navbar,
                    # Load BG Image
                    bgcolor = ft.Colors.TRANSPARENT,
                    decoration = bg_image,
                )
           )

        ''' CV '''
        if page.route == "/cv":
            page.views.append(
                ft.View(
                    route = "/cv",
                    controls = [
                        cv.cv_content
                    ],
                    # *** VIEW SETUP ***
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    appbar = main_navbar,
                    # Load BG Image
                    bgcolor = ft.Colors.TRANSPARENT,
                    decoration = bg_image,
                )
            )

        ''' Tentang '''
        if page.route == "/tentang":
            page.views.append(
                ft.View(
                    route = "/tentang",
                    controls = [
                        tentang.tentang_content
                    ],
                    # *** VIEW SETUP ***
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    appbar = main_navbar,
                    # Load BG Image
                    bgcolor = ft.Colors.TRANSPARENT,
                    decoration = bg_image,
                )
            )

        page.update()

    def view_pop(view):
        ''' Go back function, popping the stack of page view and nampilin page terakhir '''
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            # 1 view left
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main, view=ft.AppView.WEB_BROWSER)