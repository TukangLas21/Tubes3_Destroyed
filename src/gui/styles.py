import flet as ft

# Colors
APP_COLORS = {
    "black": "#0B0E16",
    "stroke": "#272C38",
    "grey": "#B9BFC8",
    "white": "#FEFDFF",

    "black-transparent": "#0B0E1680", #50% opacity
    "white-transparent": "#FEFDFF80" #50% opacity
}

gradient = ft.LinearGradient(
    colors = ["#DB222E", "886AFF"],
    stops = [0,1],
    begin = "ft.Alignment.center_left",
    end = "ft.Alignment.center_right"
)

# Text Styla

DISPLAY_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=72,
    height=72,
    weight=ft.FontWeight.BOLD
)

CAPTION_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=24,
    height=32,
    weight=ft.FontWeight.NORMAL
)

HEADING_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=32,
    height=52,
    weight=ft.FontWeight.BOLD
)

SH1_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=24,
    height=32,
    weight=ft.FontWeight.BOLD
)

SH2_STYLE = ft.TextStyle(
    font_family="SF Pro Medium",
    size=20,
    height=28,
    weight=ft.FontWeight.BOLD
)

BODY_STYLE = ft.TextStyle(
    font_family="SF Pro Regular",
    size=16,
    height=20,
    weight=ft.FontWeight.NORMAL
)