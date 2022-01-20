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
    r = requests.get(
        "https://api.thecatapi.com/v1/breeds/search?q=" + message.command[1:])
    breed = r.json()["id"]
    breedimageurl = requests.get(
        "https://api.thecatapi.com/images/search?breed_id=" + breed)
    if r.status_code != 200:
        print("Error in Cat API")
        bot.send_message(1833693304, "Error occured in Cat API!")
        bot.reply_text(
            "An error occured in the API, try again later or change your request.")
    else:
        photo = requests.get(breedimageurl.json()["url"]).content
        filename = "cat.jpg"
        open(filename, "wb").write(photo)
        message.reply_photo(filename, quote=True,
                            caption=breedimageurl.json()["description"])
        os.remove(filename)


@bot.on_message(filters.command("neko", prefixes=["/", ".", "!"]))
def neko_generator(bot, message):
    r = requests.get("https://neko-love.xyz/api/v1/neko")
    if r.status_code != 200:
        print("Error in Neko API")
        bot.send_message(1833693304, "Error occured in Neko API!")
        bot.reply_text("An error occured in the API, try again later.")
    else:
        photo = requests.get(r.json()["url"]).content
        filename = "neko.jpg"
        open(filename, "wb").write(photo)
        message.reply_photo(filename, quote=True)
        os.remove(filename)


@bot.on_message(filters.command("shiba", prefixes=["/", ".", "!"]))
def shiba_generator(bot, message):
    r = requests.get("https://dog.ceo/api/breed/shiba/images/random")
    if r.status_code != 200:
        print("Error in Shiba API")
        bot.send_message(1833693304, "Error occured in Shiba API!")
        bot.reply_text("An error occured in the API, try again later.")
    else:
        photo = requests.get(r.json()["message"]).content
        filename = "shiba.jpg"
        open(filename, "wb").write(photo)
        message.reply_photo(filename, quote=True)
        os.remove(filename)


bot.run()
