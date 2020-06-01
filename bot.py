#!/usr/bin/python3
''''
Author: Rehman Ali
Python version used: Python3

NOTE: Please don't mess with code if you don't understand what you are doing.
'''
import socks
import discord
from discord import errors
import requests
import socket
import conf as config 

bot = discord.Client()
baseUrl = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"


def replaceMentions(mentions, msg, channel):
    if channel:
        for ch in mentions:
            msg = msg.replace(str(f"#{ch.id}"), str(ch.name))
    elif not channel:
        for member in mentions:
            msg = msg.replace(str(member.id), str(member.name))
    return str(msg)

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
    while True:
        try:
            print(f"[+] Sending Message to Telegram ...")
            resp = requests.post(url)
            if resp.status_code == 200:
                print("[+] Message sent!\n")
                break
            elif resp.status_code != 200:
                raise OSError
        except OSError:
            print("[-] Sending failed!\n[+] Trying again ...")
            continue
        except KeyboardInterrupt:
            print("\n[+] Please wait untill all messages in queue are sent!\n")



if config.PROXY:
    if config.AUTHENTICATION:
        if config.USERNAME != None and config.PASSWORD != None:
            socks.set_default_proxy(socks.SOCKS5, config.SOCKS5_SERVER, config.SOCKS5_PORT, username=config.USERNAME, password=config.PASSWORD)
            print(f"[+] Proxy enabled with authentication set!\n[+] Proxy Server: {config.SOCKS5_SERVER}:{config.SOCKS5_PORT}")
        else:
            print(f"[-] Proxy authentication enabled but username/password not set.")
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
                    message.content = replaceMentions(message.mentions, message.content, channel=False)
                if message.channel_mentions:
                    message.content = replaceMentions(message.channel_mentions, message.content, channel=True)
                toSend = f"{message.guild}/{message.channel}/{message.author.name}: {message.content}"
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
                    elif 'title' in embed.keys():
                        toSend = f"{message.guild}/{message.channel}/{message.author.name}: {embed['title']}"
                    elif 'description' in embed.keys():
                        toSend = f"{message.guild}/{message.channel}/{message.author.name}: {embed['description']}"
                    url = f"{baseUrl}/sendMessage?text='{toSend}'&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                    sendMsg(url)
                    # print(embed)
                elif str(embed['type']) == "link":
                    toSend = f"{embed['title']}\n{embed['description']}\n{embed['url']}"
                    url = f"{baseUrl}/sendMessage?text='{toSend}'&chat_id={config.TELEGRAM_RECEIVER_CHAT_ID}"
                    sendMsg(url)


#Run the bot using the user token
try:
    bot.run(config.USER_DISCORD_TOKEN, bot=False)
except RuntimeError:
    print("\n\nPlease Wait ...\nShutting down the bot ... \n")
    quit()
except errors.HTTPException:
    print("Invalid discord token or network down!")
    quit()
except errors.LoginFailure:
    print("Login failed to discord. May be bad token or network down!")
    quit()
