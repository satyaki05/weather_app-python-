import requests
import tkinter as tk
from tkinter import messagebox

# OpenWeatherMap API Key (Replace with your key)
API_KEY = "92827bb76321dfffcb0a5182311abd56"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return

    # Fetch current weather
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_label.config(text=f"Weather: {weather}")
        temp_label.config(text=f"Temperature: {temp}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

        # Fetch 5-day forecast
        forecast_response = requests.get(FORECAST_URL, params=params)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            forecast_text = "5-Day Forecast:\n"
            for i in range(0, len(forecast_data["list"]), 8):  # Get one entry per day
                date = forecast_data["list"][i]["dt_txt"].split()[0]
                temp = forecast_data["list"][i]["main"]["temp"]
                description = forecast_data["list"][i]["weather"][0]["description"].capitalize()
                forecast_text += f"{date}: {temp}°C, {description}\n"

            forecast_label.config(text=forecast_text)
        else:
            forecast_label.config(text="Forecast data not available.")
    else:
        messagebox.showerror("Error", f"City not found! Please try again. (Status code: {response.status_code})")

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("500x600")
root.configure(bg="lightblue")

# City input
tk.Label(root, text="Enter City:", font=("Arial", 18), bg="lightblue").pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 18), width=30)
city_entry.pack(pady=10)

# Search button
search_button = tk.Button(root, text="Get Weather", font=("Arial", 18), command=get_weather, bg="green", fg="white")
search_button.pack(pady=20)

# Weather info labels
weather_label = tk.Label(root, text="Weather:", font=("Arial", 16), bg="lightblue")
weather_label.pack(pady=5)
temp_label = tk.Label(root, text="Temperature:", font=("Arial", 16), bg="lightblue")
temp_label.pack(pady=5)
humidity_label = tk.Label(root, text="Humidity:", font=("Arial", 16), bg="lightblue")
humidity_label.pack(pady=5)
wind_label = tk.Label(root, text="Wind Speed:", font=("Arial", 16), bg="lightblue")
wind_label.pack(pady=5)

# Forecast label
forecast_label = tk.Label(root, text="", font=("Arial", 16), bg="lightblue", justify="left")
forecast_label.pack(pady=20)

root.mainloop()
