import os
import telebot
import requests
import logging
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')
POLLING_TIMEOUT = None
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! what do you want to search for?")


@bot.message_handler(commands=["weather"])
def send_weather(message):
    location = 'Enter location: '
    sent_message = bot.send_message(message.chat.id, location, parse_mode='Markdown')
    bot.register_next_step_handler(sent_message, fetch_weather)
    return location

def location_handler(message):
    location = message.text 
    geolocator = Nominatim(user_agent="my_app")
    
    try:
        location_data = geolocator.geocode(location)
        latitude = round(location_data.latitude, 2)
        longitude = round(location_data.longitude, 2)
        return latitude, longitude
    except AttributeError:
        print('Location not found')
        

def get_weather(latitude, longitude):
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(latitude, longitude, WEATHER_TOKEN)
    response = requests.get(url)
    return response.json()



def fetch_weather(message):
    latitude, longitude = location_handler(message)
    weather = get_weather(latitude, longitude)
    data = weather['list']
    data_2 = data[0]
    info = data_2['weather']
    data_3 = info[0]
    description = data_3['description']
    weather_message = f'*Weather:* {description}\n'
    bot.send_message(message.chat.id, 'Here\'s weather!')
    bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')


@bot.message_handler(func=lambda msg:True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()