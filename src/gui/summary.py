import flet as ft
from styles import *
import urllib.parse
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connector import Connector
from pdf_processor import extract_text_regex
from regex_func import get_summary, get_skills, get_experiences, get_education
from app import *

def get_cv_data_by_ids(detail_id: int, applicant_id: int):
    Connector.get_instance().connect()
    cv_data = Connector.get_instance().get_decrypted_cv(detail_id)
    Connector.get_instance().close()
    
    Connector.get_instance().connect()
    applicant_profile = Connector.get_instance().get_decrypted_profile(applicant_id)
    Connector.get_instance().close()
    
    if cv_data is None or applicant_profile is None:
        return None 
    
    text = extract_text_regex(cv_data)
    if text is None:
        return None

    return {
        "profile": {
            "name": applicant_profile[0] + " " + applicant_profile[1],
            "birthdate": applicant_profile[2],
            "address": applicant_profile[3],
            "phone": applicant_profile[4],
        },
        "summary": get_summary(text),
        "skills": get_skills(text),
        "job_history": get_experiences(text),
        "education": get_education(text),
        
    }

def back_function(e):
    page = e.page
    page.go("/")  # Navigate back to main search page

def create_section_container(title: str, content: ft.Control):
    """Create a styled container for each section"""
    return ft.Container(
        ft.Column([
            ft.Text(title, style=ft.TextStyle(
                size=18,
                weight=ft.FontWeight.W_600,
                color=APP_COLORS["white"]
            )),
            ft.Divider(color=APP_COLORS["white-transparent"], height=1),
            content
        ], spacing=12),
        bgcolor=APP_COLORS["glass"],
        padding=ft.padding.symmetric(horizontal=24, vertical=20),
        border_radius=16,
        border=ft.border.all(width=1, color=APP_COLORS["white-transparent"]),
        width=700
    )

def create_profile_section(profile_data: dict):
    """Create profile information section"""
    profile_text = f"""Birthdate: {profile_data['birthdate']}
Address: {profile_data['address']}
Phone: {profile_data['phone']}
Email: {profile_data['email']}"""
    
    return ft.Text(profile_text, style=BODY2_SECONDARY_STYLE)

def create_summary_section(summary_text: str):
    """Create summary section"""
    return ft.Text(summary_text, style=BODY2_SECONDARY_STYLE)

def create_skills_section(skills: list):
    """Create skills section with chips"""
    skill_chips = []
    for skill in skills:
        skill_chips.append(
            ft.Container(
                ft.Text(skill, style=ft.TextStyle(
                    size=12,
                    color=APP_COLORS["white"]
                )),
                bgcolor=APP_COLORS["primary"],
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=16
            )
        )
    
    # Arrange skills in rows
    skill_rows = []
    for i in range(0, len(skill_chips), 4):  # 4 skills per row
        skill_rows.append(
            ft.Row(
                skill_chips[i:i+4],
                spacing=8,
                wrap=True
            )
        )
    
    return ft.Column(skill_rows, spacing=8)

def create_job_history_section(job_history: list):
    """Create job history section"""
    job_entries = []
    for job in job_history:
        job_entry = ft.Column([
            ft.Text(job['position'], style=ft.TextStyle(
                size=14,
                weight=ft.FontWeight.W_600,
                color=APP_COLORS["white"]
            )),
            ft.Text(f"{job['company']} • {job['duration']}", style=ft.TextStyle(
                size=12,
                color=APP_COLORS["secondary"]
            )),
            ft.Text(job['description'], style=BODY2_SECONDARY_STYLE)
        ], spacing=4)
        
        job_entries.append(job_entry)
        if job != job_history[-1]:  # Add divider between entries
            job_entries.append(ft.Divider(color=APP_COLORS["white-transparent"], height=1))
    
    return ft.Column(job_entries, spacing=12)

def create_education_section(education: list):
    """Create education section"""
    edu_entries = []
    for edu in education:
        edu_entry = ft.Column([
            ft.Text(edu['degree'], style=ft.TextStyle(
                size=14,
                weight=ft.FontWeight.W_600,
                color=APP_COLORS["white"]
            )),
            ft.Text(f"{edu['institution']} • {edu['year']}", style=ft.TextStyle(
                size=12,
                color=APP_COLORS["secondary"]
            )),
            ft.Text(f"GPA: {edu['gpa']}", style=BODY2_SECONDARY_STYLE)
        ], spacing=4)
        
        edu_entries.append(edu_entry)
        if edu != education[-1]:  # Add divider between entries
            edu_entries.append(ft.Divider(color=APP_COLORS["white-transparent"], height=1))
    
    return ft.Column(edu_entries, spacing=12)

def create_summary_content(page: ft.Page):
    """Create summary content based on URL parameters"""
    # Parse URL parameters
    url_params = {}
    if hasattr(page, 'route') and '?' in page.route:
        query_string = page.route.split('?')[1]
        url_params = dict(urllib.parse.parse_qsl(query_string))
    
    # Get IDs from URL parameters
    detail_id = int(url_params.get('detail_id', 0))
    applicant_id = int(url_params.get('applicant_id', 0))
    
    # Fetch CV data
    cv_data = get_cv_data_by_ids(detail_id, applicant_id)
    
    # Create all sections
    sections = [
        create_section_container(
            "Profile Information",
            create_profile_section(cv_data['profile'])
        ),
        create_section_container(
            "Summary",
            create_summary_section(cv_data['summary'])
        ),
        create_section_container(
            "Skills",
            create_skills_section(cv_data['skills'])
        ),
        create_section_container(
            "Job History",
            create_job_history_section(cv_data['job_history'])
        ),
        create_section_container(
            "Education",
            create_education_section(cv_data['education'])
        )
    ]
    
    # Main content container
    summary_content = ft.Container(
        ft.Column([
            # Header with back button and title
            ft.Container(
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=APP_COLORS["white"],
                        on_click=back_function
                    ),
                    ft.Text(
                        f"CV Summary: {cv_data['name']}",
                        style=HEADING_STYLE,
                        expand=True,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(width=48)  # Spacer to center the title
                ], 
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.only(bottom=16)
            ),
            
            # All sections
            ft.Column(
                sections,
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        spacing=24,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True
        ),
        alignment=ft.alignment.top_center,
        expand=True,
        padding=ft.padding.symmetric(horizontal=20, vertical=20)
    )
    
    return summary_content