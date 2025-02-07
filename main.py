from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO



load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI()


##cors
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

#test url

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

def load_font(size: int, bold=False):
    try:
        font_path = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()


## Generate the image


def fetch_github_avatar(username: str):
    avatar_url = f"https://avatars.githubusercontent.com/{username}"
    response = requests.get(avatar_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching GitHub avatar")

    avatar_img = Image.open(BytesIO(response.content))
    avatar_img = avatar_img.resize((50, 50))  # Resize avatar to 50x50 px

    # Create a circular mask for the avatar
    mask = Image.new("L", avatar_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_img.size[0], avatar_img.size[1]), fill=255)

    # Apply the mask to the avatar to make it circular
    avatar_img.putalpha(mask)
    return avatar_img



@app.get("/streak/{username}/image")
def get_streak_image(username: str):
    try:
        streak_data = get_github_streak(username)
        current_streak = streak_data["streak_days_from_2024_to_today"]
        total_contributions = streak_data["total_contributions"]

        background_img = Image.open("assets/template.jpg")
        background_img = background_img.convert("RGBA").resize((600, 350))

        overlay = Image.new("RGBA", background_img.size, (0, 0, 0, 128))
        background_img = Image.alpha_composite(background_img, overlay).convert("RGB")

        draw = ImageDraw.Draw(background_img)

        font_big = load_font(40, bold=True)
        font_small = load_font(24)
        font_streak = load_font(50, bold=True)
        font_year = load_font(60, bold=True)  # Font for the current year

        draw.text((40, 40), f"{username}'s GitHub Streak", font=font_big, fill="#FFFFFF")

        streak_box_x, streak_box_y, streak_box_size = 40, 90, 120
        draw.rectangle([streak_box_x, streak_box_y, streak_box_x + streak_box_size, streak_box_y + streak_box_size], outline="#FFFFFF", width=2)
        draw.text((streak_box_x + 20, streak_box_y + 30), f"{current_streak}", font=font_streak, fill="#FFFFFF")

        draw.text((streak_box_x + 20, streak_box_y + 90), "days", font=font_small, fill="#FFFFFF")

        draw.text((40, streak_box_y + streak_box_size + 20), f"Total Contributions: {total_contributions}", font=font_small, fill="#FFFFFF")

        streak_percentage = (current_streak / 365) * 100
        bar_width, bar_height = 500, 30
        draw.rectangle([(40, streak_box_y + streak_box_size + 60), (40 + bar_width, streak_box_y + streak_box_size + 60 + bar_height)], outline="#FFFFFF", width=2)
        for i in range(int(bar_width * streak_percentage / 100)):
            draw.line([(40 + i, streak_box_y + streak_box_size + 60), (40 + i, streak_box_y + streak_box_size + 60 + bar_height)], fill=(255, 255, 255))

        draw.text((40, streak_box_y + streak_box_size + 100), f"{streak_percentage:.2f}% of this year", font=font_small, fill="#FFFFFF")

        today = datetime.now().strftime("%B %d, %Y")
        draw.text((40, streak_box_y + streak_box_size + 140), f"Today's Date: {today}", font=font_small, fill="#FFFFFF")

        # Fetch and add the avatar to the top-right corner
        avatar_img = fetch_github_avatar(username)
        avatar_x = background_img.width - avatar_img.width - 20  # Position from right
        avatar_y = 20  # Position from top
        background_img.paste(avatar_img, (avatar_x, avatar_y), avatar_img)  # Pasting with alpha channel

        # Add current year in a large font on the right side, opposite the streak box
        current_year = datetime.now().year
        year_x = background_img.width - 180  # Position from right
        year_y = streak_box_y + (streak_box_size // 2) - 30  # Vertical alignment with streak box
        draw.text((year_x, year_y), str(current_year), font=font_year, fill="#FFFFFF")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Background image not found")

    img_io = BytesIO()
    background_img.save(img_io, "PNG")
    img_io.seek(0)

    # Adding cache-control headers
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate"}

    return StreamingResponse(img_io, media_type="image/png", headers=headers)
