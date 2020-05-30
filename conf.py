
# The Discord user token. It is a bit hard to obtain. You can follow the online tutorial here to
# obtain your user token for discord. Tutorial: https://www.youtube.com/watch?v=tI1lzqzLQCs&feature=emb_logo
USER_DISCORD_TOKEN = 'NzE0MDcxMjcxNzcxNzM0MDQ2.XspUzw.9umL2DgXFRL7x54mFxnqvo9E7dw'

# Go to your telegram account.
# In the left upper corner in the search box search fot BotFather
# Click on the bot father and then continue below.
# Send /newbot to BotFather and it will ask you to name your bot.
# After naming the bot it will ask you to set the user name for bot. This would be unique.
# Now after the username is set BotFather will give you your bot token paste it here below.
# Altenatively, Follow this (https://core.telegram.org/bots#6-botfather) to create your bot on telegram. It's super easy.

TELEGRAM_BOT_TOKEN = '1105725049:AAGtuXqby-hog2INCN_v_nULv_bCej9lpNg'



# Chat id is the id for the group or channel you want to receive messages at.
# To get this open your browser and paste the following url in the addressbar replacing group or channel name and telegram bot token.
# https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN_HERE>/sendMessage?text=%22Hello%22&chat_id=<YOUR_GROUP_NAME_HERE>
# In the response you will receive a json object containing all the info about the channel.
# Find the channel chat id under the chat. Copy and paste here.
# Alternatively you can use get_id.py script from telegram-msg-forwarder folder. But for that to work you will have to setup the forwarder first.

TELEGRAM_RECEIVER_CHAT_ID = -1001499013531      #"telegram_channel_chat_id_here"





# Configure the channels and server here to from where you want to receive the messages.

serversList = {
    "Server-Name": ["Channel1", "Channel2", "Channel3", "Channel4"],
    "Python": ["discord․py", "help-sodium", "help-zinc", "help-carbon", "help-magincium"],
    "r/Jailbreak": ["general", "checkra1n", "development"],
    "EngineerMan": ["oof-topic"]
}



#SOCKS5 proxy settings
# Set PROXY to False to disable the proxy settings
PROXY = True
SOCKS5_SERVER = '79.164.43.214'
SOCKS5_PORT = 9050