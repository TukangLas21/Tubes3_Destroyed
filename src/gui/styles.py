import flet as ft

# Colors
APP_COLORS = {
    "black": "#0B0E16",
    "stroke": "#272C38",
    "grey": "#B9BFC8",
    "white": "#FEFDFF",

    "black-transparent": ft.Colors.with_opacity(0.5, '#0B0E16'),
    "white-transparent": ft.Colors.with_opacity(0.1, "#FEFDFF")
}

gradient = ft.LinearGradient(
    colors = ["#DB222E", "#886AFF"],
    stops = [0,1],
    begin = "ft.Alignment.center_left",
    end = "ft.Alignment.center_right"
)

# Text Styles
DISPLAY_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=72,
    color = APP_COLORS["white"]
)

CAPTION_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=24,
    color = APP_COLORS["grey"]
)

HEADING_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=32,
    color = APP_COLORS["white"]
)

SH1_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=24,
    color = APP_COLORS["white"]
)

SH2_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=20,
    color = APP_COLORS["white"]
)

MENU_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=20,
    color = APP_COLORS["white"]
)

BODY1_PRIMARY_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=16,
    color = APP_COLORS["white"]
)

BODY1_SECONDARY_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=16,
    color = APP_COLORS["grey"]
)

BODY2_PRIMARY_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=14,
    color = APP_COLORS["white"]
)

BODY2_SECONDARY_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=14,
    color = APP_COLORS["grey"]
)

#Components - Buttons
BUTTON_L = ft.ButtonStyle(
    bgcolor = APP_COLORS["black-transparent"],
    color = APP_COLORS["white"],
    overlay_color=ft.Colors.TRANSPARENT,

    shape = ft.RoundedRectangleBorder(radius=32),
    padding=ft.padding.symmetric(horizontal=44, vertical=24),
    side=ft.BorderSide(width=1, color=APP_COLORS["stroke"]),

)

BUTTON_M = ft.ButtonStyle(
    bgcolor = APP_COLORS["black-transparent"],
    color = APP_COLORS["white"],
    overlay_color=ft.Colors.TRANSPARENT,

    shape = ft.RoundedRectangleBorder(radius=32),
    padding=ft.padding.symmetric(horizontal=44, vertical=12),
    side=ft.BorderSide(width=1, color=APP_COLORS["stroke"]),

)

# Components - Text Field
def create_textfield(label: str, hint_text: str, **kwargs):
# kwargs adalah tambahan atribut untuk styling, misal mau dibikin password atau counter!
    return ft.Column(
        spacing=8,
        controls=[
            ft.Text(label, style=SH2_STYLE),

            ft.TextField(
                hint_text=hint_text,
                hint_style=BODY1_SECONDARY_STYLE, # placeholder text
                text_style=BODY1_PRIMARY_STYLE, # input text

                filled=True,
                bgcolor=APP_COLORS["white-transparent"],
                
                border=ft.InputBorder.OUTLINE,
                border_width=0,
                border_radius=24,
                focused_border_width=1,
                focused_border_color=APP_COLORS["white-transparent"],
                
                content_padding=ft.padding.symmetric(vertical=12, horizontal=24),

                # kwargs akan unpack semua argument yang dimasukkan disini
                **kwargs    
            )
        ]
    )

bg_image = ft.BoxDecoration (
        image = ft.DecorationImage(
            src= 'assets/bg.png',
            fit= ft.ImageFit.COVER
        )
    )

# PAGE STYLING!!
def setup_page(page):
    
    page.title = "DestroyedCV"
    page.window.width = 1280
    page.window.height = 720
    
    # maaf ya ga ada bikin responsif responsif an awokawoka
    page.window_min_width = 1280
    page.window_min_height = 720
    page.window_max_width = 1280
    page.window_max_height = 720
    
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    
    # Fonts setup
    page.fonts = {
        "SF Pro Regular": "./gui/assets/fonts/SF-Pro-Text-Regular.otf",
        "SF Pro Medium": "./gui/assets/fonts/SF-Pro-Text-Medium.otf"
    }
    page.theme = ft.Theme(font_family="SF Pro Regular") # Default app font
        
    # Stack: background image at bottom, content above
    content_container = ft.Container(
        expand=True,
        content=ft.Stack([
            # Background image
            ft.Image(
                src="gui/assets/images/bg.png",
                fit=ft.ImageFit.COVER,
            ),
            # Pages will include their main content here
            ft.Container(
                expand=True,
                content=ft.Column([], alignment=ft.MainAxisAlignment.CENTER)
            )
        ])
    )
    
    page.add(content_container)
    
    # Return the content container where specific pages can add their elements by appending the stack
    return content_container.content.controls[1].content