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
def get_streak_image(username: str):
    if username != "ryuzinoh":
        dwg = svgwrite.Drawing(profile='full', size=(600, 350))
        dwg.add(dwg.text("Bruh, thought you could sneak in?\nUse the provided source code and\nhost it yourself!\nxD",
                         insert=(40, 140), font_size="22px", fill="black"))
        
        svg_output = BytesIO(dwg.tostring().encode('utf-8'))
        return StreamingResponse(svg_output, media_type="image/svg+xml")
    
    try:
        streak_data = get_github_streak(username)
        current_streak = streak_data["streak_days_from_2024_to_today"]
        total_contributions = streak_data["total_contributions"]
        
        today = datetime.today()
        start_of_year = datetime(today.year, 1, 1)
        end_of_year = datetime(today.year + 1, 1, 1)
        year_progress = (today - start_of_year).days / (end_of_year - start_of_year).days
        year_progress_percentage = round(year_progress * 100, 2)
        
        dwg = svgwrite.Drawing(profile='full', size=(600, 350))
        
        dwg.add(dwg.rect(insert=(0, 0), size=(600, 350), fill="black"))
        dwg.add(dwg.rect(insert=(40, 40), size=(520, 270), fill="black", rx=25, ry=25))
        
        avatar_url = f"https://github.com/{username}.png"
        response = requests.get(avatar_url)
        if response.status_code == 200:
            avatar_base64 = b64encode(response.content).decode("utf-8")
            avatar_data_url = f"data:image/png;base64,{avatar_base64}"
        else:
            avatar_data_url = "https://via.placeholder.com/60"
        
        clip_path = dwg.defs.add(dwg.clipPath(id="avatarClip"))
        clip_path.add(dwg.circle(center=(65, 65), r=30))
        
        dwg.add(dwg.image(avatar_data_url, insert=(35, 35), size=(60, 60), clip_path="url(#avatarClip)"))
        
        username_label = dwg.text(f"@{username}", insert=(110, 80), font_size="24px", font_weight="bold", fill="white", style="font-family: 'Poppins', sans-serif;")
        username_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0s", fill="freeze"))
        dwg.add(username_label)
        
        current_date_text = today.strftime("%B %d, %Y")
        current_date_label = dwg.text(current_date_text, insert=(50, 180), font_size="28px", font_weight="bold", fill="white", style="font-family: 'Poppins', sans-serif;")
        current_date_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.25s", fill="freeze"))
        dwg.add(current_date_label)
        
        contributions_text = f"Total Contributions: {total_contributions}"
        contributions_label = dwg.text(contributions_text, insert=(50, 220), font_size="20px", fill="white", style="font-family: 'Poppins', sans-serif;")
        contributions_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.5s", fill="freeze"))
        dwg.add(contributions_label)
        
        streak_info_text = f"Current Streak: {current_streak} days"
        streak_info_label = dwg.text(streak_info_text, insert=(50, 250), font_size="20px", fill="white", style="font-family: 'Poppins', sans-serif;")
        streak_info_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.75s", fill="freeze"))
        dwg.add(streak_info_label)
        
        circle_center = (500, 150)
        circle_radius = 60
        dwg.add(dwg.circle(center=circle_center, r=circle_radius, fill="white"))

        streak_text = f"{current_streak}"
        streak_text_element = dwg.text(streak_text, insert=(circle_center[0] - 15, circle_center[1] + 10), font_size="30px", font_weight="bold", fill="black", style="font-family: 'Poppins', sans-serif;")
        streak_text_element.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0s", fill="freeze"))
        streak_text_element.add(dwg.animate(attributeName="y", from_="{circle_center[1] + 50}", to_="{circle_center[1] + 10}", dur="1s", begin="0s", fill="freeze"))
        dwg.add(streak_text_element)

        days_text_element = dwg.text("days", insert=(circle_center[0] - 24, circle_center[1] + 40), font_size="18px", font_weight="normal", fill="black", style="font-family: 'Poppins', sans-serif;")
        days_text_element.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.5s", fill="freeze"))
        dwg.add(days_text_element)
        
        progress_bar_width = 400
        progress_bar_height = 15
        progress_bar_x = 50
        progress_bar_y = 320
        
        dwg.add(dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(progress_bar_width, progress_bar_height), fill="#444", rx=7, ry=7))
        
        progress_filled_width = (year_progress_percentage / 100) * progress_bar_width
        progress_filler = dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(0, progress_bar_height), fill="#00FF00", rx=7, ry=7)
        
        progress_filler.add(dwg.animate(attributeName="width", from_="0", to=f"{progress_filled_width}", dur="1.5s", begin="1s", fill="freeze"))
        dwg.add(progress_filler)
        
        progress_text = f"{year_progress_percentage}% of {today.year} completed"
        progress_text_element = dwg.text(progress_text, insert=(progress_bar_x, progress_bar_y - 10), font_size="16px", fill="white", style="font-family: 'Poppins', sans-serif;")
        progress_text_element.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="1s", fill="freeze"))
        dwg.add(progress_text_element)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error generating streak image: {str(e)}")

    svg_output = BytesIO(dwg.tostring().encode('utf-8'))
    return StreamingResponse(svg_output, media_type="image/svg+xml")
