import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests

# ====================== DATA ======================
CROP_DATA = {
    "Madhya Pradesh": {
        "Kharif (Monsoon)": ["Rice", "Maize", "Soybean", "Cotton", "Pigeon Pea"],
        "Rabi (Winter)": ["Wheat", "Gram (Chickpea)", "Mustard", "Lentil", "Potato"],
        "Zaid (Summer)": ["Vegetables (Tomato, Okra)", "Melon", "Cucumber", "Groundnut"]
    }
}

CROP_GUIDANCE = {
    "Rice": "• Sowing: June–July\n• Harvest: Oct–Nov\n• Soil: Clayey/Loamy, pH 5.5–6.5\n• Water: 1200–1500 mm\n• Tip: Use SRI method to save 30% water",
    "Wheat": "• Sowing: Nov–Dec\n• Harvest: March–April\n• Soil: Loamy, pH 6–7.5\n• Water: 400–500 mm\n• Tip: Zero-tillage saves fuel & moisture",
    "Soybean": "• Sowing: June–July\n• Harvest: Sept–Oct\n• Soil: Well-drained loamy\n• Water: 400–600 mm\n• Tip: Inoculate seeds with Rhizobium for better yield",
    "Maize": "• Sowing: June–July\n• Harvest: Sept–Oct\n• Soil: Any well-drained\n• Water: 500–800 mm\n• Tip: Intercrop with legumes for nitrogen",
    "Cotton": "• Sowing: May–June\n• Harvest: Oct–Feb\n• Soil: Black cotton soil\n• Water: 700–1000 mm\n• Tip: Use Bt varieties & IPM for pest control",
    "Gram (Chickpea)": "• Sowing: Oct–Nov\n• Harvest: Feb–March\n• Soil: Light loamy\n• Water: 300–400 mm\n• Tip: Good for soil health – fixes nitrogen",
}

TIPS = [
    "1. Test your soil every 2 years – healthy soil = higher yield!",
    "2. Use drip irrigation – saves up to 70% water compared to flood method.",
    "3. Practice crop rotation – prevents pest buildup and improves soil fertility.",
    "4. Apply neem-based pesticides – eco-friendly and effective against many insects.",
    "5. Mulching with crop residue reduces evaporation and weed growth.",
    "6. Sow at the right time – follow local Krishi calendar for your district.",
    "7. Use certified seeds – certified seeds give 15–20% more yield.",
    "8. Install bird scarers or use reflective tapes to protect crops from birds.",
    "9. Keep farm records – track expenses, yield and weather for better planning.",
    "10. Join local FPO for better market prices."
]

def get_weather_condition(code):
    conditions = {0: "Clear sky ", 1: "Mainly clear ", 2: "Partly cloudy ", 3: "Overcast ",
                  45: "Fog ", 51: "Light drizzle ", 61: "Light rain ", 63: "Moderate rain ",
                  65: "Heavy rain ", 80: "Rain showers ", 95: "Thunderstorm "}
    return conditions.get(code, "Cloudy ")

def fetch_weather():
    lat, lon = 23.02, 77.72   # Ashta, MP
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=Asia/Kolkata"
    try:
        data = requests.get(url, timeout=8).json()["current"]
        return (f" Temperature: {data['temperature_2m']}°C\n"
                f" Feels like: {data['apparent_temperature']}°C\n"
                f" Humidity: {data['relative_humidity_2m']}%\n"
                f" Wind: {data['wind_speed_10m']} km/h\n"
                f" Condition: {get_weather_condition(data['weather_code'])}\n\n"
                f" Ashta, Madhya Pradesh (Live)")
    except:
        return " Temperature: 28°C\n Feels like: 30°C\n Humidity: 55%\n Wind: 12 km/h\n Condition: Partly Cloudy\n\n Ashta, Madhya Pradesh (Demo Mode)"

# ====================== GUI FUNCTIONS ======================
def clear_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

def show_home():
    clear_main()
    ttk.Label(main_frame, text="Welcome to Farmer Help Portal!", 
              font=("Helvetica", 18, "bold"), foreground="#006400").pack(pady=20)
    ttk.Label(main_frame, text="Your one-stop solution for crop guidance, weather & tips\nHelping farmers of Madhya Pradesh ", 
              font=("Helvetica", 12), wraplength=600, justify="center").pack(pady=10)

def show_crop_suggestions():
    clear_main()
    ttk.Label(main_frame, text=" Crop Suggestions", font=("Helvetica", 16, "bold"), foreground="#006400").pack(pady=15)
    ttk.Label(main_frame, text="Select Season:", font=("Helvetica", 11)).pack(anchor="w", padx=30, pady=5)
    
    season_var = tk.StringVar(value="Kharif (Monsoon)")
    ttk.Combobox(main_frame, textvariable=season_var, values=list(CROP_DATA["Madhya Pradesh"].keys()), 
                 state="readonly", width=30).pack(padx=30, pady=5)
    
    result_label = ttk.Label(main_frame, text="", font=("Helvetica", 11), wraplength=500, justify="left")
    result_label.pack(padx=30, pady=20)

    def suggest():
        crops = CROP_DATA["Madhya Pradesh"][season_var.get()]
        result_label.config(text=f"Recommended Crops:\n\n• " + "\n• ".join(crops))
    ttk.Button(main_frame, text="Get Suggestions", command=suggest).pack(pady=10)

def show_crop_guidance():
    clear_main()
    ttk.Label(main_frame, text=" Crop Guidance", font=("Helvetica", 16, "bold"), foreground="#006400").pack(pady=15)
    ttk.Label(main_frame, text="Select Crop:", font=("Helvetica", 11)).pack(anchor="w", padx=30, pady=5)
    
    crop_var = tk.StringVar()
    ttk.Combobox(main_frame, textvariable=crop_var, values=list(CROP_GUIDANCE.keys()), 
                 state="readonly", width=30).pack(padx=30, pady=5)
    
    guidance_text = scrolledtext.ScrolledText(main_frame, height=12, width=70, wrap=tk.WORD)
    guidance_text.pack(padx=30, pady=15)

    def show():
        if crop_var.get():
            guidance_text.delete(1.0, tk.END)
            guidance_text.insert(tk.END, CROP_GUIDANCE[crop_var.get()])
    ttk.Button(main_frame, text="Show Guidance", command=show).pack(pady=5)

def show_weather():
    clear_main()
    ttk.Label(main_frame, text=" Live Weather", font=("Helvetica", 16, "bold"), foreground="#006400").pack(pady=15)
    weather_label = ttk.Label(main_frame, text="Loading weather...", font=("Helvetica", 11), justify="left")
    weather_label.pack(padx=40, pady=20)
    
    def refresh():
        weather_label.config(text=fetch_weather())
    ttk.Button(main_frame, text=" Refresh", command=refresh).pack(pady=10)
    refresh()

def show_tips():
    clear_main()
    ttk.Label(main_frame, text=" Farming Tips", font=("Helvetica", 16, "bold"), foreground="#006400").pack(pady=15)
    text_area = scrolledtext.ScrolledText(main_frame, height=18, width=70, wrap=tk.WORD)
    text_area.pack(padx=30, pady=10)
    text_area.insert(tk.END, "\n\n".join(TIPS))
    text_area.config(state="disabled")

# ====================== CREATE WINDOW ======================
root = tk.Tk()
root.title("🌾 Farmer Help Portal - Ashta, Madhya Pradesh")
root.geometry("900x650")
root.configure(bg="#f0f0f0")

# Header
tk.Frame(root, bg="#006400", height=80).pack(fill="x")
tk.Label(root, text=" Farmer Help Portal", font=("Helvetica", 22, "bold"), fg="white", bg="#006400").pack(pady=15)

# Sidebar
sidebar = tk.Frame(root, bg="#228B22", width=220)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

style = ttk.Style()
style.theme_use("clam")
style.configure("Accent.TButton", foreground="white", background="#006400", font=("Helvetica", 10, "bold"))

ttk.Button(sidebar, text=" Home", command=show_home, style="Accent.TButton").pack(pady=8, padx=10)
ttk.Button(sidebar, text=" Crop Suggestions", command=show_crop_suggestions, style="Accent.TButton").pack(pady=8, padx=10)
ttk.Button(sidebar, text= "Crop Guidance", command=show_crop_guidance, style="Accent.TButton").pack(pady=8, padx=10)
ttk.Button(sidebar, text=" Weather", command=show_weather, style="Accent.TButton").pack(pady=8, padx=10)
ttk.Button(sidebar, text=" Farming Tips", command=show_tips, style="Accent.TButton").pack(pady=8, padx=10)

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=15, pady=20)
ttk.Button(sidebar, text=" Exit", command=root.quit).pack(pady=10, padx=10)

# Main Frame
main_frame = tk.Frame(root, bg="white", relief="sunken", bd=2)
main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Start with Home
show_home()

root.mainloop()