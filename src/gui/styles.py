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
    color = APP_COLORS["white"],
    letter_spacing = -2,
    height = 1  # height is 1x font size
)

CAPTION_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=24,
    color = APP_COLORS["grey"],
    letter_spacing = -1
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

    shape = ft.RoundedRectangleBorder(radius=24),
    padding=ft.padding.symmetric(horizontal=44, vertical=24),
    side=ft.BorderSide(width=1, color=APP_COLORS["stroke"]),
)

BUTTON_S = ft.ButtonStyle(
    bgcolor = APP_COLORS["black-transparent"],
    color = APP_COLORS["white"],
    overlay_color=ft.Colors.TRANSPARENT,

    shape = ft.RoundedRectangleBorder(radius=24),
    padding=ft.padding.symmetric(horizontal=24, vertical=12),
    side=ft.BorderSide(width=1, color=APP_COLORS["stroke"]),
)

# Sejujurnya ini dibikin untuk option button yang bentuk button, bukan untuk segmented (yg skrg)
# Semoga ada waktu untuk edit tapi kalo ngga ya gapapa sih kayaknya UI ga segede itu penilaiannya oakwaowoakw
BUTTON_OPTION_DEFAULT = ft.ButtonStyle(
    bgcolor = APP_COLORS["white-transparent"],
    color = APP_COLORS["grey"],
    overlay_color=ft.Colors.TRANSPARENT,

    shape = ft.RoundedRectangleBorder(radius=24),
    padding=ft.padding.symmetric(horizontal=24, vertical=20),
)

BUTTON_OPTION_SELECTED = ft.ButtonStyle(
    bgcolor = APP_COLORS["black-transparent"],
    color = APP_COLORS["white"],
    overlay_color=ft.Colors.TRANSPARENT,

    shape = ft.RoundedRectangleBorder(radius=24),
    padding=ft.padding.symmetric(horizontal=24, vertical=21),
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

# Components - Navbar
navbar_container = ft.Container(
    content=ft.Row(
        controls=[
            ft.Text("Beranda", style=MENU_STYLE),
            ft.Text("Search and Match", style=MENU_STYLE),
            ft.Text("Tentang Kami", style=MENU_STYLE),
            ft.Text("Keluar", style=MENU_STYLE),
        ],
        spacing=44
    ),
    width=540,
    padding=ft.padding.symmetric(horizontal=32, vertical=16),
    bgcolor=APP_COLORS["black-transparent"],
    border=ft.border.all(width=1, color=APP_COLORS["stroke"]),
    border_radius=ft.border_radius.all(32)
)

navbar = ft.AppBar(
        title=navbar_container,
        center_title=True,
        bgcolor=ft.Colors.TRANSPARENT,
        elevation=0,
        toolbar_height=112 # Set the height to be (60px gap + ~52px nav bar height) from the top
)