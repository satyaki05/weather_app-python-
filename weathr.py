import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

# OpenWeatherMap API Key (Replace with your key)
API_KEY = "92827bb76321dfffcb0a5182311abd56"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(200, 200, 600, 800)  # Increased window size

        # Layout
        self.layout = QVBoxLayout()

        # City Input (Bigger Size)
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter City Name")
        self.city_input.setStyleSheet("font-size: 18px; padding: 10px;")  # Bigger text field
        self.layout.addWidget(self.city_input)

        # Fetch Button
        self.fetch_button = QPushButton("Get Weather", self)
        self.fetch_button.setStyleSheet("font-size: 16px; padding: 10px;")  # Bigger button
        self.fetch_button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.fetch_button)

        # Weather Display
        self.weather_label = QLabel("Weather info will appear here", self)
        self.weather_label.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.weather_label)

        self.temp_label = QLabel("Temperature: ", self)
        self.temp_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.temp_label)

        self.humidity_label = QLabel("Humidity: ", self)
        self.humidity_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.humidity_label)

        self.wind_label = QLabel("Wind Speed: ", self)
        self.wind_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.wind_label)

        # Weather Icon
        self.weather_icon = QLabel(self)
        self.layout.addWidget(self.weather_icon)

        # Forecast Display
        self.forecast_label = QLabel("5-Day Forecast:", self)
        self.forecast_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.forecast_label)

        # Larger Map View
        self.map_view = QWebEngineView()
        self.map_view.setMinimumHeight(300)  # Increased map size
        self.layout.addWidget(self.map_view)

        self.setLayout(self.layout)

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            self.weather_label.setText("Please enter a city name!")
            return

        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            icon = data['weather'][0]['icon']
            lat, lon = data['coord']['lat'], data['coord']['lon']

            self.weather_label.setText(f"{city}: {desc}")
            self.temp_label.setText(f"Temperature: {temp}°C")
            self.humidity_label.setText(f"Humidity: {humidity}%")
            self.wind_label.setText(f"Wind Speed: {wind_speed} m/s")
            self.show_icon(icon)
            self.show_map(lat, lon)
            self.get_forecast(city)
        else:
            self.weather_label.setText("City not found!")

    def show_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(icon_url).content)
        self.weather_icon.setPixmap(pixmap)

    def show_map(self, lat, lon):
        map_url = f"https://www.openstreetmap.org/#map=10/{lat}/{lon}"
        self.map_view.setUrl(QUrl(map_url))  # FIXED: Convert to QUrl

    def get_forecast(self, city):
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(FORECAST_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            forecast_text = "5-Day Forecast:\n"
            for i in range(0, len(data["list"]), 8):  # Get one entry per day
                date = data["list"][i]["dt_txt"].split()[0]
                temp = data["list"][i]["main"]["temp"]
                description = data["list"][i]["weather"][0]["description"].capitalize()
                forecast_text += f"{date}: {temp}°C, {description}\n"
            self.forecast_label.setText(forecast_text)
        else:
            self.forecast_label.setText("Forecast data not available.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
