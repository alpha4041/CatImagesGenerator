from pyrogram import Client, filters
import requests
import os
from os import environ

api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ["TOKEN"]

bot = Client("catgeneratorbot", api_id, api_hash, bot_token)


@bot.on_message(filters.command("start"))
def welcome_message(bot, message):
    bot.send_message(
        message.chat.id, "Welcome to Cat Images Generator Bot.\nWith /cat you get random pictures of cats.\nThe bot is made by @alph4")


@bot.on_message(filters.command("cat"))
def cat_generator(bot, message):
    filename = "cat.jpg"
    url = "https://cataas.com/cat"
    photo = requests.get(url).content
    open(filename, "wb").write(photo)
    message.reply_photo(filename, quote=True)
    os.remove(filename)


bot.run()
