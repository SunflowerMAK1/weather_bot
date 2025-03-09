import telebot
from telebot import types
import requests
import json

TOKEN = "7422080039:AAH72a6KdcWvQaLsyJ1OgfpJu9y0ghxov6M"
API_key = "733b1bc745fd99a72d7f6b2d70b0150f"

bot = telebot.TeleBot(TOKEN)

weather_descriptions = {
    "Clear": "Ясно", "Clouds": "Облачно", "Fog": "Туман", "Mist": "Мгла", "Smoke": "Дымка", "Dust": "Пыль", "Sand": "Песчаная погода",
    "Ash": "Пепельная погода", "Tornado": "Торнадо", "Squall": "Шквал", "Haze": "Легкий туман", "Rain": "Дождь", "Thunderstorm": "Гроза",
    "Drizzle": "Морось", "Snow": "Снег"
}

def weather_picture(weather):
    if weather["weather"][0]["main"] == 'Clear' and weather['clouds']['all'] == 0:
        pic = "weather_pictures/clear_sky.jpg"
    elif weather['clouds']['all'] > 0 and weather['clouds']['all'] <= 25 and weather["weather"][0]["main"] == 'Clouds':
        pic = "weather_pictures/clouds_25%.jpg"
    elif weather['clouds']['all'] > 25 and weather['clouds']['all'] <= 50 and weather["weather"][0]["main"] == 'Clouds':
        pic = "weather_pictures/clouds_50%.jpg"
    elif weather['clouds']['all'] > 50 and weather['clouds']['all'] <= 75 and weather["weather"][0]["main"] == 'Clouds':
        pic = "weather_pictures/clouds_75%.jpg"
    elif weather['clouds']['all'] > 75 and weather['clouds']['all'] <= 100 and weather["weather"][0]["main"] == 'Clouds':
        pic = "weather_pictures/clouds_100%.jpg"
    elif weather["weather"][0]["main"] == 'Fog' or weather["weather"][0]["main"] == 'Mist' or weather["weather"][0]["main"] == 'Smoke':
        pic = "weather_pictures/fog.jpg"
    elif weather["weather"][0]["main"] == 'Dust' or weather["weather"][0]["main"] == 'Sand' or weather["weather"][0]["main"] == 'Ash':
        pic = "weather_pictures/sand_dust.jpg"
    elif weather["weather"][0]["main"] == 'Tornado' or weather["weather"][0]["main"] == 'Squall':
        pic = "weather_pictures/tornado.jpg"
    elif weather["weather"][0]["main"] == 'Haze':
        pic = "weather_pictures/haze.jpg"
    elif weather["weather"][0]["main"] == 'Rain' and (weather["weather"][0]["description"] == 'light rain' or weather["weather"][0]["description"] == 'moderate rain'):
        pic = "weather_pictures/small_rain.jpg"
    elif weather["weather"][0]["main"] == 'Drizzle':
        pic = "weather_pictures/drizzle.jpg"
    elif weather["weather"][0]["main"] == 'Rain' and (weather["weather"][0]["description"] == 'heavy intensity shower rain' or weather["weather"][0]["description"] == 'shower rain' or weather["weather"][0]["description"] == 'ragged shower rain' or weather["weather"][0]["description"] == "extreme rain"):
        pic = "weather_pictures/rainfall.jpg"
    elif weather["weather"][0]["main"] == 'Rain':
        pic = "weather_pictures/medium_rain.jpg"
    elif weather["weather"][0]["main"] == "Thunderstorm" and (weather["weather"][0]["description"] == 'light thunderstorm' or weather["weather"][0]["description"] == 'thunderstorm with rain' or weather["weather"][0]["description"] == 'thunderstorm with light rain' or weather["weather"][0]["description"] == 'thunderstorm with light drizzle'):
        pic = "weather_pictures/light_thunderstorm.jpg"
    elif weather["weather"][0]["main"] == "Thunderstorm":
        pic = "weather_pictures/tunderstorm.jpg"
    elif weather["weather"][0]["main"] == "Snow" and (weather["weather"][0]["description"] == "rain and snow" or weather["weather"][0]["description"] == "light shower snow" or weather["weather"][0]["description"] == "shower snow" or weather["weather"][0]["description"] == "heavy shower snow"):
        pic = "weather_pictures/snow_rain.jpg"
    elif weather["weather"][0]["main"] == "Snow":
        pic = "weather_pictures/snow.jpg"
    else:
        pic = "weather_pictures/xz_weather.jpg"
    return pic



@bot.message_handler(commands=["start", "go"])
def start(incoming_message):
    bot.send_message(incoming_message.chat.id, "Hello!Этот бот подскажет тебе погоду. Введи название города:")

@bot.message_handler(content_types=["text"])
def main(incoming_message):
    city = incoming_message.text.title().strip()
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric")
    if resp.status_code == 200:
        data = json.loads(resp.text)
        pic = weather_picture(data)
        print(data)
        weather_info = (
            f"{weather_descriptions[data["weather"][0]["main"]]}\n"
            f"Температура: {int(data['main']['temp'])} °C\n"
            f"Ощущается как: {int(data['main']['feels_like'])} °C\n"
            f"Скорость ветра: {data['wind']['speed']} м/с\n"                        
            f"Направление ветра: {data['wind']['deg']}°\n"
            f"Влажность: {data['main']['humidity']}%\n"                        
            f"Давление: {data['main']['pressure']} гПа\n"
            f"Видимость: {data['visibility']} метров\n"                        
            f"Облачность: {data['clouds']['all']}%")
        with open(pic, "rb") as picture_w:
            bot.send_photo(incoming_message.chat.id, picture_w, caption=weather_info)
    else:
        bot.send_message(incoming_message.chat.id, "У нас нет такого города! Попробуйте другой.")


bot.infinity_polling()