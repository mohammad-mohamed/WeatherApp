from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "7e2950f3e0b1461c36d2904f1c42b8bd"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈"
    elif 300 <= weather_id <= 321:
        return "🌦"
    elif 500 <= weather_id <= 531:
        return "🌧"
    elif 600 <= weather_id <= 622:
        return "❄"
    elif 701 <= weather_id <= 741:
        return "🌫"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪"
    elif weather_id == 800:
        return "☀"
    elif 801 <= weather_id <= 804:
        return "☁"
    else:
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    url = f"{BASE_URL}?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            temperature_k = data["main"]["temp"]
            temperature_f = (temperature_k * 9/5) - 459.67
            weather_id = data["weather"][0]["id"]
            weather_description = data["weather"][0]["description"]
            weather_emoji = get_weather_emoji(weather_id)

            return jsonify({
                "temperature": f"{temperature_f:.0f}°F",
                "emoji": weather_emoji,
                "description": weather_description
            })
        else:
            return jsonify({"error": "City not found"})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while fetching data"})

if __name__ == '__main__':
    app.run(debug=True)
