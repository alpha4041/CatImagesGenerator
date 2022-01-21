from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
import requests
import os
from os import environ
import json

api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ["TOKEN"]
thecatapi = environ["THECATAPI"]
LOG_GROUP = environ["LOG_GROUP"]
headers = {'x-api-key': thecatapi}
bot = Client("catgeneratorbot", api_id, api_hash, bot_token=bot_token)


@bot.on_message(filters.command("start"))
def welcome_message(bot, message):
    bot.send_message(
        message.chat.id,
        "Welcome to Cat Images Generator Bot, use /help for a list of the commands.\nThis bot is made by @alph4\nJoin @alph4chat to report any problem or suggest a feature.\nThe bot is open source!",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Source Code",
                    url="https://github.com/alpha4041/CatImagesGenerator"
                )
                ],
            [
                InlineKeyboardButton(
                    "Support Group",
                    url="https://t.me/alph4chat"
                )
                ]
        ])
        )
    bot.send_message(
        LOG_GROUP,
        "Bot started by" + {message.from_user.mention}
    )


@bot.on_message(filters.command("help", prefixes=["/", ".", "!"]))
def help_message(bot, message):
    message.reply_text(
        "Bot usage:\n/cat {breed} to get a random cat image of the given breed with a description\n/neko to get a picture of an anime girl with cat ears\n/shiba to get a picture of a shiba.")


@bot.on_message(filters.command("cat", prefixes=["/", ".", "!"]))
def cat_generator(bot, message):
    query = " ".join(message.command[1:])
    r = requests.get(
        "https://api.thecatapi.com/v1/breeds/search?q=" + query, headers=headers).content
    rforstatus = requests.get(
            "https://api.thecatapi.com/v1/breeds/search?q=" + query, headers=headers)
    rdecoded = r.decode()
    rlist = json.loads(rdecoded)
    breed = rlist[0]['id']
    description = rlist[0]['description']
    wikipediaurl = rlist[0]['wikipedia_url']
    if rforstatus.status_code != 200:
        print("Error in Cat API")
        bot.send_message(
            LOG_GROUP, "Error occured in Cat API, check Heroku logs!")
        message.reply_text(
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
                            caption=(description + "\n" + "Wikipedia: " + wikipediaurl))
        os.remove(filename)


@bot.on_message(filters.command("neko", prefixes=["/", ".", "!"]))
def neko_generator(bot, message):
    r = requests.get("https://neko-love.xyz/api/v1/neko")
    if r.status_code != 200:
        print("Error in Neko API")
        bot.send_message(LOG_GROUP, "Error occured in Neko API!")
        message.reply_text("An error occured in the API, try again later.")
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
        bot.send_message(LOG_GROUP, "Error occured in Shiba API!")
        message.reply_text("An error occured in the API, try again later.")
    else:
        photo = requests.get(r.json()["message"]).content
        filename = "shiba.jpg"
        open(filename, "wb").write(photo)
        message.reply_photo(filename, quote=True)
        os.remove(filename)


bot.run()
