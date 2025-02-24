from datetime import datetime
from io import BytesIO
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
import svgwrite
from datetime import datetime
from fastapi.responses import StreamingResponse

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
        
        # Black background color
        dwg.add(dwg.rect(insert=(0, 0), size=(600, 350), fill="black"))
        
        # Adding a rounded card without any border
        dwg.add(dwg.rect(insert=(40, 40), size=(520, 270), fill="black", rx=25, ry=25))
        
        # Adding profile picture (circular) inside the card
        clip_path = dwg.defs.add(dwg.clipPath(id="avatarClip"))
        clip_path.add(dwg.circle(center=(65, 65), r=30))
        
        # Add the image with the clipPath applied
        dwg.add(dwg.image("https://github.com/ryuzinoh.png", insert=(35, 35), size=(60, 60), clip_path="url(#avatarClip)"))
        
        # Add username label with fade-in animation
        username_label = dwg.text(f"@{username}", insert=(110, 80), font_size="24px", font_weight="bold", fill="white", style="font-family: 'Poppins', sans-serif;")
        username_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0s", fill="freeze"))
        dwg.add(username_label)
        
        # Add current elapsed date in big text above total contributions
        current_date_text = today.strftime("%B %d, %Y")  # Format: February 24, 2024
        current_date_label = dwg.text(current_date_text, insert=(50, 180), font_size="28px", font_weight="bold", fill="white", style="font-family: 'Poppins', sans-serif;")
        current_date_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.25s", fill="freeze"))
        dwg.add(current_date_label)
        
        # Add total contributions information below the current date
        contributions_text = f"Total Contributions: {total_contributions}"
        contributions_label = dwg.text(contributions_text, insert=(50, 220), font_size="20px", fill="white", style="font-family: 'Poppins', sans-serif;")
        contributions_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.5s", fill="freeze"))
        dwg.add(contributions_label)
        
        # Add current streak information below total contributions
        streak_info_text = f"Current Streak: {current_streak} days"
        streak_info_label = dwg.text(streak_info_text, insert=(50, 250), font_size="20px", fill="white", style="font-family: 'Poppins', sans-serif;")
        streak_info_label.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.75s", fill="freeze"))
        dwg.add(streak_info_label)
        
        # Add a larger circle showing streak in bold, positioned perfectly
        circle_center = (500, 150)
        circle_radius = 60
        dwg.add(dwg.circle(center=circle_center, r=circle_radius, fill="white"))  # Larger white circle

        # Text for streak days centered in the circle with fade-in and slide-up animation
        streak_text = f"{current_streak}"
        streak_text_element = dwg.text(streak_text, insert=(circle_center[0] - 15, circle_center[1] + 10), font_size="30px", font_weight="bold", fill="black", style="font-family: 'Poppins', sans-serif;")
        streak_text_element.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0s", fill="freeze"))
        streak_text_element.add(dwg.animate(attributeName="y", from_="{circle_center[1] + 50}", to_="{circle_center[1] + 10}", dur="1s", begin="0s", fill="freeze"))
        dwg.add(streak_text_element)

        # Text for "days" centered below the number with fade-in animation
        days_text_element = dwg.text("days", insert=(circle_center[0] - 24, circle_center[1] + 40), font_size="18px", font_weight="normal", fill="black", style="font-family: 'Poppins', sans-serif;")
        days_text_element.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="0.5s", fill="freeze"))
        dwg.add(days_text_element)
        
        # Add progress bar for contributions in perspective to this year
        progress_bar_width = 400
        progress_bar_height = 15
        progress_bar_x = 50
        progress_bar_y = 320
        
        # Background of the progress bar
        dwg.add(dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(progress_bar_width, progress_bar_height), fill="#444", rx=7, ry=7))
        
        # Foreground of the progress bar (percentage filled)
        progress_filled_width = (year_progress_percentage / 100) * progress_bar_width
        progress_filler = dwg.rect(insert=(progress_bar_x, progress_bar_y), size=(0, progress_bar_height), fill="#00FF00", rx=7, ry=7)
        
        # Animate the green filler to grow from left to right
        progress_filler.add(dwg.animate(attributeName="width", from_="0", to=f"{progress_filled_width}", dur="1.5s", begin="1s", fill="freeze"))
        dwg.add(progress_filler)
        
        # Add text showing the percentage and current year
        progress_text = f"{year_progress_percentage}% of {today.year} completed"
        progress_text_element = dwg.text(progress_text, insert=(progress_bar_x, progress_bar_y - 10), font_size="16px", fill="white", style="font-family: 'Poppins', sans-serif;")
        progress_text_element.add(dwg.animate(attributeName="opacity", from_="0", to="1", dur="1s", begin="1s", fill="freeze"))
        dwg.add(progress_text_element)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error generating streak image: {str(e)}")

    svg_output = BytesIO(dwg.tostring().encode('utf-8'))
    return StreamingResponse(svg_output, media_type="image/svg+xml")