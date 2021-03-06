import bdbf
import os
import ksoftapi
import praw
import datetime

version = (2,2,5)
changelog = {
    "2.2.5":"Added the makeEmbed command",
    "2.2.4":"Upgraded to bdbf 1.1.1",
    "2.2.3":"Small fix in versioning",
    "2.2.2":"Small backend fixes",
    "2.2.1":"Started versioning and making a changelog.\nBetter stats command."
}

heroku = os.environ.get("isHeroku", False)
if not heroku:
    logging = False
    try:
        with open("C:\\Users\\alber\\OneDrive\\Plocha\\discordBotSecrets.txt", "r") as f:
            kclient = eval(f.readline())
            token = eval(f.readline())
            reddit = eval(f.readline())
            githubToken = eval(f.readline())
    except:
        with open("/home/bertik23/Plocha/discordBotSecrets.txt", "r") as f:
            kclient = eval(f.readline())
            token = eval(f.readline())
            reddit = eval(f.readline())
            githubToken = eval(f.readline())

else:
    kclient = ksoftapi.Client(os.environ.get("ksoft_token", None))

    reddit = praw.Reddit(client_id = os.environ.get("reddit_client_id", None),
                        client_secret = os.environ.get("reddit_client_secret", None),
                        user_agent = os.environ.get("reddit_user_agent", None))

    token = os.environ.get('TOKEN', None)
    logging = True

botId = 540563812890443794
#84032 permissions int
#https://discordapp.com/oauth2/authorize?client_id=540563812890443794&scope=bot&permissions=8


client = bdbf.Client(
    commandPrefix = "~",
    embedFooter= {
        "text": "Powered by Bertik23",
        "icon_url": "https://cdn.discordapp.com/avatars/452478521755828224/4cfdbde44582fe6ad05383171ac1b051.png"
        },
    embedColor = (37, 217, 55),
    botName = "TheBot",
    logging = logging,
    createTaskCommands = False
    )

klubik, obecne, choco_afroAnouncements, korona_info = None,None, None, None
botStartTime = datetime.datetime.utcnow()
botReadyTimes = []
