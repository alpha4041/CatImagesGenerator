from pyrogram import Client, filters
import requests
import os
from os import environ
import json

api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ["TOKEN"]
thecatapi = environ["THECATAPI"]
headers = {'x-api-key': thecatapi}
bot = Client("catgeneratorbot", api_id, api_hash, bot_token=bot_token)


@bot.on_message(filters.command("start"))
def welcome_message(bot, message):
    bot.send_message(
        message.chat.id, "Welcome to Cat Images Generator Bot.\nWith /cat you get random pictures of cats, with /neko pictures of anime girls with cat ears and with /shiba pictures of Shibas.\nThis bot is made by @alph4\nJoin @alph4chat to report any problem or suggest a feature.\nThe source code of the bot is open source! Check it: https://github.com/alpha4041/CatImagesGenerator")


@bot.on_message(filters.command("cat", prefixes=["/", ".", "!"]))
def cat_generator(bot, message):
    query = " ".join(message.command[1:])
    r = requests.get(
        "https://api.thecatapi.com/v1/breeds/search?q=" + query, headers=headers).content
    rdecoded = r.decode()
    rlist = json.loads(rdecoded)
    breed = rlist[0]['id']
    description = rlist[0]['description']
    wikipediaurl = rlist[0]['wikipedia_url']
    if r.status_code != 200:
        print("Error in Cat API")
        bot.send_message(1833693304, "Error occured in Cat API!")
        bot.reply_text(
            "An error occured in the API, try again later or change your request.")
    else:
        breedimageresponse = requests.get(
            "https://api.thecatapi.com/v1/images/search?breed_id=" + breed, headers=headers).content
        breedimageresponsedecoded = breedimageresponse.decode()
        breedimageresponselist = json.loads(breedimageresponsedecoded)
        imageurl = breedimageresponselist[0]["url"]
        photo = requests.get(imageurl).content
        filename = "cat.jpg"
        open(filename, "wb").write(photo)
        message.reply_photo(filename, quote=True,
                            caption=(description + "\n" + "Wikipedia:" + wikipediaurl))
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
