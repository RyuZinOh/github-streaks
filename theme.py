# theme.py

class Theme:
    def __init__(self, name, background_color, text_color, progress_bar_color, circle_fill_color, circle_text_color):
        self.name = name
        self.background_color = background_color
        self.text_color = text_color
        self.progress_bar_color = progress_bar_color
        self.circle_fill_color = circle_fill_color
        self.circle_text_color = circle_text_color

# Define some themes
themes = {
    "midnight": Theme(
        name="midnight",
        background_color="#1e1e1e",
        text_color="#ffffff",
        progress_bar_color="#00FF00",
        circle_fill_color="#ffffff",
        circle_text_color="#000000"
    ),
    "sunset": Theme(
        name="sunset",
        background_color="#FFA07A",
        text_color="#000000",
        progress_bar_color="#FF4500",
        circle_fill_color="#FFD700",
        circle_text_color="#000000"
    ),
    "ocean": Theme(
        name="ocean",
        background_color="#1E90FF",
        text_color="#ffffff",
        progress_bar_color="#00FFFF",
        circle_fill_color="#00BFFF",
        circle_text_color="#000000"
    ),
    "forest": Theme(
        name="forest",
        background_color="#228B22",
        text_color="#ffffff",
        progress_bar_color="#32CD32",
        circle_fill_color="#006400",
        circle_text_color="#ffffff"
    ),
    "neon": Theme(
        name="neon",
        background_color="#000000",
        text_color="#39ff14",
        progress_bar_color="#ff00ff",
        circle_fill_color="#00ffff",
        circle_text_color="#ff00ff"
    ),
    "cyberpunk": Theme(
        name="cyberpunk",
        background_color="#ff00ff",
        text_color="#00ffff",
        progress_bar_color="#ff4500",
        circle_fill_color="#000000",
        circle_text_color="#ff00ff"
    ),
    "galaxy": Theme(
        name="galaxy",
        background_color="#191970",
        text_color="#ADD8E6",
        progress_bar_color="#9370DB",
        circle_fill_color="#8A2BE2",
        circle_text_color="#ffffff"
    ),
    "matrix": Theme(
        name="matrix",
        background_color="#000000",
        text_color="#00FF00",
        progress_bar_color="#008000",
        circle_fill_color="#00FF00",
        circle_text_color="#000000"
    ),
    "rose_gold": Theme(
        name="rose_gold",
        background_color="#b76e79",
        text_color="#ffffff",
        progress_bar_color="#ffcccb",
        circle_fill_color="#ff69b4",
        circle_text_color="#ffffff"
    ),
    "dark_knight": Theme(
        name="dark_knight",
        background_color="#121212",
        text_color="#ffcc00",
        progress_bar_color="#8b0000",
        circle_fill_color="#ff4500",
        circle_text_color="#000000"
    ),
    "aurora": Theme(
        name="aurora",
        background_color="#4B0082",
        text_color="#00FF00",
        progress_bar_color="#FFD700",
        circle_fill_color="#FF69B4",
        circle_text_color="#000000"
    ),
    "lava": Theme(
        name="lava",
        background_color="#8B0000",
        text_color="#FFD700",
        progress_bar_color="#FF4500",
        circle_fill_color="#DC143C",
        circle_text_color="#000000"
    )
}

def get_theme(theme_name: str):
    """Get a theme by name. Returns the default 'midnight' theme if not found."""
    return themes.get(theme_name, themes["midnight"])