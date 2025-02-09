from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
APE_KEY = os.getenv("APE_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
MONKEYTYPE_URL = "https://api.monkeytype.com/users/streak"

def load_font(size: int, bold=False):
    font_path = "assets/Poppins-Bold.ttf" if bold else "assets/Poppins-Regular.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

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



def make_avatar_circular(avatar_img):
    size = min(avatar_img.size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    mask = mask.resize(avatar_img.size, Image.Resampling.LANCZOS)
    avatar_img.putalpha(mask)
    return avatar_img

def fetch_github_avatar(username: str):
    url = f"https://github.com/{username}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub user not found")
    return Image.open(BytesIO(response.content))

@app.get("/streak/{username}/image")
def get_streak_image(username: str):
    if username != "ryuzinoh":
        background_img = Image.new("RGBA", (900, 550), (255, 255, 255))  # Reduced height
        draw = ImageDraw.Draw(background_img)
        font_small = load_font(22)
        message = "Bruh, thought you could sneak in? \n Use the provided source code and \nhost it yourself! \n xD"
        draw.text((40, 240), message, font=font_small, fill="#000000")
        img_io = BytesIO()
        background_img.save(img_io, "PNG")
        img_io.seek(0)
        return StreamingResponse(img_io, media_type="image/png")
    
    try:
        streak_data = get_github_streak(username)
        current_streak = streak_data["streak_days_from_2024_to_today"]
        total_contributions = streak_data["total_contributions"]
        
        background_img = Image.new("RGBA", (900, 475), (255, 255, 255))  # Reduced height
        draw = ImageDraw.Draw(background_img)
        
        title_color = "#000000"
        streak_color = "#000000"
        text_color = "#000000"
        year_color = "#000000"
        
        font_big = load_font(40, bold=True)
        font_small = load_font(28)
        font_streak = load_font(60, bold=True)
        font_year = load_font(70, bold=True)
        font_year_maxxr = load_font(120, bold=True)

        draw.text((10, 0), f"{username}'s GitHub Streak", font=font_big, fill=title_color)
        
        draw.rectangle([40, 80, 220, 300], outline=streak_color, width=3)
        draw.text((90, 120), f"{current_streak}", font=font_streak, fill=streak_color)
        draw.text((90, 190), "days", font=font_small, fill=text_color)
        draw.text((40, 430), f"Total Contributions: {total_contributions}", font=font_small, fill=text_color)
        
        streak_percentage = (current_streak / 365) * 100
        draw.rectangle([(40, 320), (840, 350)], outline=streak_color, width=3)
        for i in range(int(800 * streak_percentage / 100)):
            draw.line([(40 + i, 320), (40 + i, 350)], fill=streak_color)
        draw.text((40, 360), f"{streak_percentage:.2f}% of this year", font=font_small, fill=text_color)
        
        today = datetime.now().strftime("%B %d, %Y")
        draw.text((40, 390), f"Today's Date: {today}", font=font_small, fill=text_color)
        
        avatar_img = fetch_github_avatar(username)
        avatar_img = avatar_img.resize((150, 150), Image.Resampling.LANCZOS)
        avatar_img = avatar_img.convert("RGBA")
        avatar_img = make_avatar_circular(avatar_img)
        
        background_img.paste(avatar_img, (730, 40), avatar_img)
        
        draw.text((450, 180), str(datetime.now().year), font=font_year_maxxr, fill=year_color)  # Moved the year down
        draw.rectangle([0, 0, 899, 474], outline="black", width=5)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Avatar image not found")
    
    img_io = BytesIO()
    background_img.save(img_io, "PNG")
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/png", headers={"Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate"})






#for monkeytype streak

def fetch_monkeytype_streak():
    if not APE_KEY:
        raise HTTPException(status_code=500, detail="MonkeyType API Key is missing!")
    
    headers = {"Authorization": f"ApeKey {APE_KEY}"}
    response = requests.get(MONKEYTYPE_URL, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from MonkeyType")
    
    return response.json()

@app.get("/monkeytype/streak")
def get_monkeytype_streak():
    data = fetch_monkeytype_streak()
    if "data" not in data:
        raise HTTPException(status_code=404, detail="Streak data not found")
    
    streak_data = data["data"]
    streak_length = streak_data.get("length", 0)
    max_streak = streak_data.get("maxLength", 0)
    last_timestamp = streak_data.get("lastResultTimestamp", 0)
    last_date = datetime.fromtimestamp(last_timestamp / 1000, tz=timezone.utc).strftime("%B %d, %Y")
    
    return {
        "streak_length": streak_length,
        "max_streak": max_streak,
        "last_active": last_date
    }
@app.get("/monkeytype/streak/image")
def get_monkeytype_streak_image():
    try:
        streak_data = get_monkeytype_streak()
        streak_length = streak_data["streak_length"]
        max_streak = streak_data["max_streak"]
        last_active = streak_data["last_active"]

        width, height = 600, 300
        background_img = Image.open("assets/template.jpg")
        background_img = background_img.resize((width, height))

        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 128))
        background_img.paste(overlay, (0, 0), overlay)

        draw = ImageDraw.Draw(background_img)

        border_thickness = 2
        draw.rectangle([0, 0, width, border_thickness], fill="white")
        draw.rectangle([0, height - border_thickness, width, height], fill="white")

        font_title = load_font(36, bold=True)
        font_max_streak = load_font(50, bold=True)
        font_data = load_font(32)
        font_small = load_font(13)

        draw.text((20, 10), "Happilli's MonkeyType Streak", font=font_title, fill="white")

        text_y_position = 130
        draw.text((20, text_y_position), "Max", font=font_max_streak, fill="white")
        draw.text((20, text_y_position + 60), f"{max_streak} Days", font=font_data, fill="white")

        text_y_position += 150

        streak_text = f"{streak_length}\nDays"
        bbox = draw.textbbox((0, 0), streak_text, font=font_title)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        square_size = max(120, text_width + 30)
        square_x = width - square_size - 20
        square_y = 80
        draw.rectangle([square_x, square_y, square_x + square_size, square_y + square_size], outline="white", width=4)

        draw.text((square_x + (square_size - text_width) // 2, square_y + (square_size - text_height) // 2), streak_text, font=font_title, fill="white")

        draw.text((width - 200, height - 25), f"Last Active: {last_active}", font=font_small, fill="white")

        img_io = BytesIO()
        background_img.save(img_io, "PNG", quality=95)
        img_io.seek(0)
        return StreamingResponse(img_io, media_type="image/png", headers={"Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate"})

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Error generating streak image")
