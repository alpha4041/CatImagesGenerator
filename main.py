from pyrogram import Client, filters
import requests
import os
from os import environ

api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ["TOKEN"]

bot = Client("catgeneratorbot", api_id, api_hash, bot_token=bot_token)


@bot.on_message(filters.command("start"))
def welcome_message(bot, message):
    bot.send_message(
        message.chat.id, "Welcome to Cat Images Generator Bot.\nWith /cat you get random pictures of cats, with /neko pictures of anime girls with cat ears and with /shiba pictures of Shibas.\nThis bot is made by @alph4\nJoin @alph4chat to report any problem or suggest a feature.\nThe source code of the bot is open source! Check it: https://github.com/alpha4041/CatImagesGenerator")


@bot.on_message(filters.command("cat", prefixes=["/", ".", "!"]))
def cat_generator(bot, message):
    filename = "cat.jpg"
    url = "https://cataas.com/cat"
    photo = requests.get(url).content
    open(filename, "wb").write(photo)
    message.reply_photo(filename, quote=True)
    os.remove(filename)


@bot.on_message(filters.command("neko", prefixes=["/", ".", "!"]))
def neko_generator(bot, message):
    r = requests.get("https://neko-love.xyz/api/v1/neko")
    photo = requests.get(r.json()["url"]).content
    filename = "neko.jpg"
    open(filename, "wb").write(photo)
    message.reply_photo(filename, quote=True)
    os.remove(filename)


@bot.on_message(filters.command("shiba", prefixes=["/", ".", "!"]))
def shiba_generator(bot, message):
    r = requests.get("https://dog.ceo/api/breed/shiba/images/random")
    photo = requests.get(r.json()["message"]).content
    filename = "shiba.jpg"
    open(filename, "wb").write(photo)
    message.reply_photo(filename, quote=True)
    os.remove(filename)


bot.run()
