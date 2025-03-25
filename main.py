from datetime import datetime
from io import BytesIO
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
import svgwrite
from fastapi.responses import StreamingResponse
import requests
from base64 import b64encode
from datetime import datetime, timedelta
from theme import get_theme
import json
from translation import translation_service

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

@app.get("/")
def home():
    return {"message": "GitHub Streak API is running!"}

def fetch_github_data(username: str):
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GitHub Token is missing!")
    
    query = """
    {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """ % username

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query}, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from GitHub")
    
    return response.json()

@app.get("/streak/{username}")
def get_github_streak(username: str):
    data = fetch_github_data(username)
    
    if "errors" in data:
        raise HTTPException(status_code=404, detail="GitHub user not found")
    
    weeks_data = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    all_contributions = []
    
    for week in weeks_data:
        for day in week["contributionDays"]:
            day_date = datetime.strptime(day["date"], "%Y-%m-%d")
            all_contributions.append({"date": day_date, "contributions_count": day["contributionCount"]})
    
    all_contributions.sort(key=lambda x: x["date"])
    
    max_streak = 0
    ongoing_streak = 0
    previous_day_contributions = 0
    
    now = datetime.now()
    today = now.date()
    end_of_today = datetime.combine(today, datetime.max.time())
    
    for day in all_contributions:
        day_date = day["date"]
        contributions_count = day["contributions_count"]
        
        is_current_day = day_date.date() == today
        is_day_ongoing = is_current_day and now < end_of_today
        
        if contributions_count > 0:
            if previous_day_contributions == 0:
                ongoing_streak = 1
            else:
                ongoing_streak += 1
            max_streak = max(max_streak, ongoing_streak)
        else:
            if not is_day_ongoing:
                ongoing_streak = 0
        
        previous_day_contributions = contributions_count
    
    return {
        "username": username,
        "max_streak": max_streak,
        "ongoing_streak": ongoing_streak,
        "total_contributions": sum(day["contributions_count"] for day in all_contributions)
    }

# read allowed.json
with open("allowed.json", "r") as file:
    allowed_usernames = json.load(file)

allowed_usernames = [username.lower() for username in allowed_usernames]    

CROWN_SVG_PATH = "assets/crown.svg"


@app.get("/streak/{username}/image")
def get_streak_image(
    username: str, 
    theme: str = "goldenshade",  
    lang: str = "en"           
):
    # Validate language
    if lang not in translation_service.get_supported_languages():
        lang = "en"
    
    # Validate theme (fallback to midnight if invalid)
    selected_theme = get_theme(theme.lower())
    
    # Check if the username is in the allowed list
    if username.lower() not in allowed_usernames:
        dwg = svgwrite.Drawing(size=("550px", "300px"), viewBox="0 0 550 300")
        dwg.add(dwg.rect(insert=(0, 0), size=(550, 300), fill="#1e1e1e", rx=30, ry=30))
        
        access_denied_message = translation_service.get_language_config(lang).strings["access_denied"]
        
        text = dwg.text(
            "",
            insert=(30, 120),
            font_size="22px",
            fill="white",
            font_weight="bold",
            style=translation_service.get_font_style(lang),
            text_anchor="start",
            dominant_baseline="middle"
        )
        
        line_height = 30
        for i, line in enumerate(access_denied_message):
            text.add(dwg.tspan(line, x=[30], dy=[line_height if i > 0 else 0]))
        
        dwg.add(text)
        dwg.add(dwg.rect(insert=(0, 0), size=(550, 300), fill="none", stroke="#FF5555", stroke_width=5, rx=30, ry=30))
        
        svg_output = BytesIO(dwg.tostring().encode('utf-8'))
        return StreamingResponse(svg_output, media_type="image/svg+xml")
    
    try:
        streak_data = get_github_streak(username)
        max_streak = streak_data["max_streak"]
        ongoing_streak = streak_data["ongoing_streak"]
        total_contributions = streak_data["total_contributions"]
        
        today = datetime.today()
        start_of_year = datetime(today.year, 1, 1)
        end_of_year = datetime(today.year + 1, 1, 1)
        year_progress = (today - start_of_year).days / (end_of_year - start_of_year).days
        year_progress_percentage = round(year_progress * 100, 2)
        
        dwg = svgwrite.Drawing(size=("550px", "300px"), viewBox="0 0 550 300")
        dwg.add(dwg.rect(insert=(0, 0), size=(550, 300), fill=selected_theme.background_color, rx=30, ry=30))
        
        # Fetch and add avatar
        avatar_url = f"https://github.com/{username}.png"
        response = requests.get(avatar_url, timeout=5)
        avatar_data_url = f"data:image/png;base64,{b64encode(response.content).decode('utf-8')}" if response.status_code == 200 else "https://via.placeholder.com/60"
        
        clip_path = dwg.defs.add(dwg.clipPath(id="avatarClip"))
        clip_path.add(dwg.circle(center=(45, 40), r=30))
        dwg.add(dwg.image(avatar_data_url, insert=(15, 10), size=(60, 60), clip_path="url(#avatarClip)"))
        
        # Username
        dwg.add(dwg.text(f"@{username}", insert=(90, 55), font_size="24px", font_weight="bold", 
                        fill=selected_theme.text_color, style=translation_service.get_font_style(lang)))
        
        # Localized date with numerals
        month_name = translation_service.get_month_name(today.month, lang)
        localized_day = translation_service.convert_to_local_numeral(today.day, lang)
        localized_year = translation_service.convert_to_local_numeral(today.year, lang)
        localized_date = f"{month_name} {localized_day}, {localized_year}"
        dwg.add(dwg.text(localized_date, insert=(30, 125), font_size="40px", font_weight="bold", 
                        fill=selected_theme.text_color, style=translation_service.get_font_style(lang)))
        
        # Convert numbers to local numerals if needed
        total_contributions_text = f"{translation_service.get_translation('total_contributions', lang)}: {translation_service.convert_to_local_numeral(total_contributions, lang)}"
        ongoing_streak_text = f"{translation_service.get_translation('ongoing_streak', lang)}: {translation_service.convert_to_local_numeral(ongoing_streak, lang)} {translation_service.get_translation('days', lang).lower()}"
        
        dwg.add(dwg.text(total_contributions_text, insert=(30, 195), font_size="20px", 
                        fill=selected_theme.text_color, style=translation_service.get_font_style(lang)))
        dwg.add(dwg.text(ongoing_streak_text, insert=(30, 225), font_size="20px", 
                        fill=selected_theme.text_color, style=translation_service.get_font_style(lang)))
        
        # Max streak circle with numerals
        circle_center = (480, 125)
        circle_radius = 60
        dwg.add(dwg.circle(center=circle_center, r=circle_radius, fill=selected_theme.circle_fill_color))
        
        max_streak_text = translation_service.convert_to_local_numeral(max_streak, lang)
        dwg.add(dwg.text(max_streak_text, insert=(circle_center[0] - 25, circle_center[1] + 5), 
                        font_size="45px", font_weight="bold", fill=selected_theme.circle_text_color, 
                        style=translation_service.get_font_style(lang)))
        dwg.add(dwg.text(translation_service.get_translation("days", lang), insert=(circle_center[0] - 23, circle_center[1] + 25), 
                        font_size="18px", font_weight="bold", fill=selected_theme.circle_text_color, 
                        style=translation_service.get_font_style(lang)))
        
        # Add crown SVG
        if os.path.exists(CROWN_SVG_PATH):
            with open(CROWN_SVG_PATH, "r", encoding='utf-8') as crown_file:
                crown_svg = crown_file.read()
                crown_svg = crown_svg.replace('fill="currentColor"', f'fill="{selected_theme.crown_theme_color}"')
                dwg.add(dwg.image(href=f"data:image/svg+xml;base64,{b64encode(crown_svg.encode('utf-8')).decode('utf-8')}", 
                              insert=(circle_center[0] - 33, circle_center[1] - 122), size=(69, 69)))
        
        # Year progress bar with numerals
        progress_bar_width = 400
        progress_bar_height = 15
        progress_bar_x = 30
        progress_bar_y = 265
        
        dwg.add(dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(progress_bar_width, progress_bar_height), 
                        fill="#444", rx=7, ry=7))
        
        progress_filled_width = year_progress_percentage / 100 * progress_bar_width
        progress_filler = dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(0, progress_bar_height), 
                                fill=selected_theme.progress_bar_color, rx=7, ry=7)
        progress_filler.add(dwg.animate(
            attributeName="width",
            from_="0",
            to=f"{progress_filled_width}",
            dur="1.5s",
            begin="0.5s",
            fill="freeze"
        ))
        dwg.add(progress_filler)
        
        # Localized year progress text with numerals
        year_progress_str = f"{year_progress_percentage:.2f}"
        year_progress_localized = translation_service.convert_to_local_numeral(year_progress_str, lang)
        localized_year_num = translation_service.convert_to_local_numeral(today.year, lang)
        year_progress_text = translation_service.get_translation("year_progress", lang).format(
            year_progress_localized, 
            localized_year_num
        )
        dwg.add(dwg.text(year_progress_text, insert=(progress_bar_x, progress_bar_y - 10), 
                        font_size="16px", fill=selected_theme.text_color, 
                        style=translation_service.get_font_style(lang)))
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching external resources: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating streak image: {str(e)}")

    svg_output = BytesIO(dwg.tostring().encode('utf-8'))
    return StreamingResponse(svg_output, media_type="image/svg+xml")