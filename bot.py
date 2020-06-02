#!/usr/bin/python3
''''
Author: Rehman Ali
Python version used: Python3

NOTE: Please don't mess with code if you don't understand what you are doing.
'''

import conf as config 
import socks
import discord
from discord import errors
import requests
import socket
import re
import logging
from box import Box as box
from colorama import Back, Fore, init, Style

# errorLogger = logging.getLogger(__name__)
# errorLogger.setLevel(logging.ERROR)
# errorLogger.addHandler()
init(autoreset=True)
colorSchemes = {
    'SUCCESS': f"{Back.GREEN}{Fore.BLACK}{Style.NORMAL}",
    'FAILURE': f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}",
    'WARNING': f"{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT}",
    'RESET': f"{Style.RESET_ALL}"
}
colorSchemes = box(colorSchemes)

logging.basicConfig(format=f'{colorSchemes.WARNING}[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)



bot = discord.Client()
baseUrl = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"


def replaceMentions(mentions, msg, channel):
    if channel:
        for ch in mentions:
            # msg = msg.replace(str(f"#{ch.id}"), '')
            msg = re.sub(f"<#{ch.id}>", '', msg)
            msg = re.sub(f"<{ch.id}>", '', msg)
            msg = re.sub(f"<*{ch.id}>", '', msg)
            msg = re.sub(f"<*{ch.id}*>", '', msg)
            msg = re.sub(f"<{ch.id}*>", '', msg)
    elif not channel:
        for member in mentions:
            msg = re.sub(f"<@{member.id}>", '', msg)
            msg = re.sub(f"<@!{member.id}>", '', msg)
            msg = re.sub(f"<{member.id}>", '', msg)
            msg = re.sub(f"<*{member.id}*>", '', msg)
            msg = re.sub(f"<{member.id}*>", '', msg)
            msg = re.sub(f"<*{member.id}>", '', msg)
    return str(msg)

def removeTags(msg):
    msg = msg.replace('#', '%23')
    msg = re.sub(r"@\w*", '', msg)
    return msg




def isPhoto(url):
    imgExts = ["png", "jpg", "jpeg", "webp"]
    if any(ext in url for ext in imgExts):
        return True
    else:
        return False

def isVideo(url):
    vidExts = ["mp4", "MP4", "mkv"]
    if any(ext in url for ext in vidExts):
        return True
    else:
        return False

def isDoc(url):
    docExts = ["zip", "pdf", "gif"]
    if any(ext in url for ext in docExts):
        return True
    else:
        return False

def matchChannel(channel, list):
    found=False
    for ch in list:
        res = ch.find(channel)
        if str(res) != "-1":
            found=True
    return found


def sendMsg(url):
    attempts = 0
    while True:
        if attempts < 5:
            try:
                print(f"[+] Sending Message to Telegram ...")
                resp = requests.post(url)
                if resp.status_code == 200:
                    print(f"{colorSchemes.SUCCESS}[+] Message sent!\n")
                    break
                elif resp.status_code != 200:
                    raise OSError
            except OSError:
                attempts += 1
                print(f"{colorSchemes.FAILURE}[-] Sending failed!\n[+] Trying again ... (Attempt {attempts})")
                continue
            except KeyboardInterrupt:
                print("\n[+] Please wait untill all messages in queue are sent!\n")
        else:
            print(f"{colorSchemes.FAILURE}[-] Message was not sent in 5 attempts. \n[-] Please check your network.")
            break





if config.PROXY:
    if config.AUTHENTICATION:
        if config.USERNAME != None and config.PASSWORD != None:
            socks.set_default_proxy(socks.SOCKS5, config.SOCKS5_SERVER, config.SOCKS5_PORT, username=config.USERNAME, password=config.PASSWORD)
            print(f"[+] Proxy enabled with authentication set!\n[+] Proxy Server: {config.SOCKS5_SERVER}:{config.SOCKS5_PORT}")
        else:
            print(f"{colorSchemes.FAILURE}[-] Proxy authentication enabled but username/password not set.")
            quit()
    elif not config.AUTHENTICATION:
        socks.set_default_proxy(socks.SOCKS5, config.SOCKS5_SERVER, config.SOCKS5_PORT)
        print(f"[+] Proxy enabled without authentication!\n[+] Proxy Server: {config.SOCKS5_SERVER}:{config.SOCKS5_PORT}")
    socket.socket = socks.socksocket
    print(f"[+] Please wait for at least 30 seconds before first message.")





@bot.event
async def on_message(message):
    serverName = message.guild.name
    serversList = config.serversList.keys()
    channelName = message.channel.name
    #print(f"Server: {serverName}, Channel: {channelName}")
    if serverName in serversList:
        channelsList = config.serversList[serverName]
        if matchChannel(channelName, channelsList):
            print(f"\n-------------------------------------------\n[+] Channel: {channelName}")
            if message.content:
                if message.mentions:
                    # print(f"\n----------------\nUser Mentioned\n----------------")
                    message.content = replaceMentions(message.mentions, message.content, channel=False)
                if message.channel_mentions:
                    # print(f"\n----------------\nChannel Mentioned\n----------------")
                    message.content = replaceMentions(message.channel_mentions, message.content, channel=True)
                toSend = f"{message.guild}/{message.channel}/{message.author.name}: {message.content}"
                toSend = removeTags(toSend)
                print(f"[+] Message: {toSend}")
                url = f"{baseUrl}/sendMessage?text={toSend}&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                sendMsg(url)

                if message.attachments:
                    attachmentUrl = message.attachments[0].url
                    if isPhoto(attachmentUrl):
                        url = f"{baseUrl}/sendPhoto?photo={attachmentUrl}&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                        sendMsg(url)
                    elif isVideo(attachmentUrl):
                        url = f"{baseUrl}/sendVideo?video={attachmentUrl}&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                        sendMsg(url)
                    elif isDoc(attachmentUrl):
                        url = f"{baseUrl}/sendDocument?document={attachmentUrl}&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                        sendMsg(url)
                
            if message.embeds:
                embed = message.embeds[0].to_dict()
                print(embed)
                if str(embed['type']) == "rich":
                    if 'title' in embed.keys() and 'description' in embed.keys():
                        toSend = f"{message.guild}/{message.channel}/{message.author.name}: {embed['title']}\n{embed['description']}"
                        toSend = removeTags(toSend)
                    elif 'title' in embed.keys():
                        toSend = f"{message.guild}/{message.channel}/{message.author.name}: {embed['title']}"
                        toSend = removeTags(toSend)
                    elif 'description' in embed.keys():
                        toSend = f"{message.guild}/{message.channel}/{message.author.name}: {embed['description']}"
                        toSend = removeTags(toSend)
                    url = f"{baseUrl}/sendMessage?text={toSend}&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                    sendMsg(url)
                    # print(embed)
                elif str(embed['type']) == "link":
                    toSend = f"{embed['title']}\n{embed['description']}\n{embed['url']}"
                    toSend = removeTags(toSend)
                    url = f"{baseUrl}/sendMessage?text={toSend}&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                    sendMsg(url)


#Run the bot using the user token
try:
    bot.run(config.USER_DISCORD_TOKEN, bot=False)
except RuntimeError:
    print("\n\nPlease Wait ...\nShutting down the bot ... \n")
    quit()
except errors.HTTPException:
    print(f"{colorSchemes.FAILURE}Invalid discord token or network down!")
    quit()
except errors.LoginFailure:
    print(f"{colorSchemes.FAILURE}Login failed to discord. May be bad token or network down!")
    quit()
