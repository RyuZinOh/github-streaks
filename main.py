from datetime import datetime
from io import BytesIO
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
import svgwrite
from fastapi.responses import StreamingResponse
from datetime import datetime
import requests
from base64 import b64encode
from theme import get_theme

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
    
    all_contributions.sort(key=lambda x: x["date"], reverse=True)
    contributions_from_2024 = [entry for entry in all_contributions if entry["date"].year >= 2024]
    
    current_streak, ongoing_streak, total_contributions = 0, 0, 0
    previous_day = None
    
    for day in contributions_from_2024:
        total_contributions += day["contributions_count"]
        if day["contributions_count"] > 0:
            if previous_day is None or (previous_day - day["date"]).days == 1:
                ongoing_streak += 1
            else:
                current_streak = max(current_streak, ongoing_streak)
                ongoing_streak = 1
        else:
            current_streak = max(current_streak, ongoing_streak)
            ongoing_streak = 0
        previous_day = day["date"]
    
    current_streak = max(current_streak, ongoing_streak)
    
    return {
        "username": username,
        "streak_days_from_2024_to_today": current_streak,
        "total_contributions": total_contributions
    }







@app.get("/streak/{username}/image")
def get_streak_image(username: str, theme: str = "midnight"):
    if username != "ryuzinoh":
        dwg = svgwrite.Drawing(profile='full', size=(600, 350))
        dwg.add(dwg.rect(insert=(0, 0), size=(600, 350), fill="none"))
        dwg.add(dwg.rect(insert=(20, 25), size=(550, 300), fill="#1e1e1e", rx=30, ry=30))
        
        sneaky_message = [
            "Bruh, thought you could sneak in?",
            "Use the provided source code and",
            "host it yourself!",
            "xD"
        ]
        
        text = dwg.text(
            "",
            insert=(50, 140),
            font_size="22px",
            fill="white",
            font_weight="bold",
            style="font-family: 'Poppins', sans-serif;",
            text_anchor="start",
            dominant_baseline="middle"
        )
        
        line_height = 30
        for i, line in enumerate(sneaky_message):
            text.add(dwg.tspan(line, x=[50], dy=[line_height if i > 0 else 0]))
        
        dwg.add(text)
        dwg.add(dwg.rect(insert=(20, 25), size=(550, 300), fill="none", stroke="#FF5555", stroke_width=5, rx=30, ry=30))
        
        svg_output = BytesIO(dwg.tostring().encode('utf-8'))
        return StreamingResponse(svg_output, media_type="image/svg+xml")
    
    try:
        # Get the selected theme
        selected_theme = get_theme(theme)
        
        streak_data = get_github_streak(username)
        current_streak = streak_data["streak_days_from_2024_to_today"]
        total_contributions = streak_data["total_contributions"]
        
        today = datetime.today()
        start_of_year = datetime(today.year, 1, 1)
        end_of_year = datetime(today.year + 1, 1, 1)
        year_progress = (today - start_of_year).days / (end_of_year - start_of_year).days
        year_progress_percentage = round(year_progress * 100, 2)
        
        dwg = svgwrite.Drawing(profile='full', size=(600, 350))
        dwg.add(dwg.rect(insert=(0, 0), size=(600, 350), fill="none"))
        dwg.add(dwg.rect(insert=(20, 25), size=(550, 300), fill=selected_theme.background_color, rx=30, ry=30))
        
        avatar_url = f"https://github.com/{username}.png"
        response = requests.get(avatar_url)
        avatar_data_url = f"data:image/png;base64,{b64encode(response.content).decode('utf-8')}" if response.status_code == 200 else "https://via.placeholder.com/60"
        
        clip_path = dwg.defs.add(dwg.clipPath(id="avatarClip"))
        clip_path.add(dwg.circle(center=(65, 65), r=30))
        dwg.add(dwg.image(avatar_data_url, insert=(35, 35), size=(60, 60), clip_path="url(#avatarClip)"))
        
        dwg.add(dwg.text(f"@{username}", insert=(110, 80), font_size="24px", font_weight="bold", fill=selected_theme.text_color, style="font-family: 'Poppins', sans-serif;"))
        dwg.add(dwg.text(today.strftime("%B %d, %Y"), insert=(50, 150), font_size="40px", font_weight="bold", fill=selected_theme.text_color, style="font-family: 'Poppins', sans-serif;"))
        dwg.add(dwg.text(f"Total Contributions: {total_contributions}", insert=(50, 220), font_size="20px", fill=selected_theme.text_color, style="font-family: 'Poppins', sans-serif;"))
        dwg.add(dwg.text(f"Current Streak: {current_streak} days", insert=(50, 250), font_size="20px", fill=selected_theme.text_color, style="font-family: 'Poppins', sans-serif;"))
        
        circle_center = (500, 150)
        circle_radius = 60
        dwg.add(dwg.circle(center=circle_center, r=circle_radius, fill=selected_theme.circle_fill_color))
        dwg.add(dwg.text(f"{current_streak}", insert=(circle_center[0] - 15, circle_center[1] + 10), font_size="30px", font_weight="bold", fill=selected_theme.circle_text_color, style="font-family: 'Poppins', sans-serif;"))
        dwg.add(dwg.text("days", insert=(circle_center[0] - 24, circle_center[1] + 40), font_size="18px", font_weight="normal", fill=selected_theme.circle_text_color, style="font-family: 'Poppins', sans-serif;"))
        
        progress_bar_width = 400
        progress_bar_height = 15
        progress_bar_x = 50
        progress_bar_y = 290
        
        dwg.add(dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(progress_bar_width, progress_bar_height), fill="#444", rx=7, ry=7))
        
        progress_filled_width = year_progress_percentage / 100 * progress_bar_width
        progress_filler = dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(0, progress_bar_height), fill=selected_theme.progress_bar_color, rx=7, ry=7)
        progress_filler.add(dwg.animate(
            attributeName="width",
            from_="0",
            to=f"{progress_filled_width}",
            dur="1.5s",
            begin="0.5s",
            fill="freeze"
        ))
        dwg.add(progress_filler)
        
        dwg.add(dwg.text(f"{year_progress_percentage}% of {today.year} completed", insert=(progress_bar_x, progress_bar_y - 10), font_size="16px", fill=selected_theme.text_color, style="font-family: 'Poppins', sans-serif;"))
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error generating streak image: {str(e)}")

    svg_output = BytesIO(dwg.tostring().encode('utf-8'))
    return StreamingResponse(svg_output, media_type="image/svg+xml")