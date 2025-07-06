import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.is_dark_mode = True  # Start with dark mode

        # Widgets
        self.city_label = QLabel("Enter City:")
        self.city_label.setObjectName("city_label")

        self.city_input = QLineEdit()
        self.city_input.setObjectName("city_input")

        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.setObjectName("get_weather_button")

        self.temperature_label = QLabel("℃")
        self.temperature_label.setObjectName("temperature_label")

        self.emoji_label = QLabel("☀️")
        self.emoji_label.setObjectName("emoji_label")

        self.description_label = QLabel("Condition")
        self.description_label.setObjectName("description_label")

        self.toggle_button = QPushButton("🌙 Switch to Light Mode")
        self.toggle_button.setObjectName("toggle_button")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shahid's Weather App")
        self.setFixedSize(400, 520)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.city_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.city_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.get_weather_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.temperature_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.emoji_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.description_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # Connections
        self.get_weather_button.clicked.connect(self.get_weather)
        self.toggle_button.clicked.connect(self.toggle_theme)

        # Initial theme
        self.apply_theme()

    def get_weather(self):
        api_key = "54fc33c907b2480599c201701250607"  # Replace with your WeatherAPI key
        city = self.city_input.text().strip()

        if not city:
            self.display_error("Please enter a city name.")
            return

        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if "error" in data:
                self.display_error(data["error"]["message"])
            else:
                self.display_weather(data)
        except Exception:
            self.display_error("Network Error")

    def display_weather(self, data):
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        emoji = self.get_emoji(condition.lower())

        self.temperature_label.setText(f"{temp:.1f}℃")
        self.emoji_label.setText(emoji)
        self.description_label.setText(condition)

    def display_error(self, message):
        self.temperature_label.setText("Error")
        self.emoji_label.setText("❌")
        self.description_label.setText(message)

    def get_emoji(self, description):
        if "cloud" in description:
            return "☁️"
        elif "rain" in description or "drizzle" in description:
            return "🌧️"
        elif "sun" in description or "clear" in description:
            return "☀️"
        elif "thunder" in description or "storm" in description:
            return "🌩️"
        elif "snow" in description:
            return "❄️"
        elif "fog" in description or "mist" in description:
            return "🌫️"
        else:
            return "🌈"

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: #e0e0e0;
                    font-family: Calibri;
                }
                QLabel#city_label {
                    font-size: 35px;
                    font-style: italic;
                }
                QLineEdit#city_input {
                    font-size: 25px;
                    padding: 8px;
                    background-color: #333;
                    color: #fff;
                    border-radius: 5px;
                }
                QPushButton {
                    font-size: 20px;
                    background-color: #2196F3;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QLabel#temperature_label {
                    font-size: 60px;
                    color: #FFEB3B;
                }
                QLabel#emoji_label {
                    font-size: 80px;
                }
                QLabel#description_label {
                    font-size: 30px;
                    color: #BB86FC;
                }
            """)
            self.toggle_button.setText("☀️ Switch to Light Mode")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                    font-family: Calibri;
                }
                QLabel#city_label {
                    font-size: 35px;
                    font-style: italic;
                }
                QLineEdit#city_input {
                    font-size: 25px;
                    padding: 8px;
                    background-color: #ffffff;
                    color: #000;
                    border-radius: 5px;
                }
                QPushButton {
                    font-size: 20px;
                    background-color: #03A9F4;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #0288D1;
                }
                QLabel#temperature_label {
                    font-size: 60px;
                    color: #FF5722;
                }
                QLabel#emoji_label {
                    font-size: 80px;
                }
                QLabel#description_label {
                    font-size: 30px;
                    color: #3F51B5;
                }
            """)
            self.toggle_button.setText("🌙 Switch to Dark Mode")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
