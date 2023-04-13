import locale

################################################################
#					THINGS YOU SHOULD EDIT					   #
################################################################

# EMOJI (<:EMOJI_NAME:EMOJI_ID>)
#To get the ID :
#Send the Emoji in one of your discord channels
#Do a right click on it "Copy the link" and past it in your navigator
#You should have a URL like this : "https://cdn.discordapp.com/emojis/xxxxxxxxxxxxxxxxxxx.webp?size=32&quality=lossless"
# "xxxxxxxxxxxxxxxxxxx" is the ID of your Emoji
START = '<:START:1089682092079730738>'
STOP = '<:STOP:1089682125277630566>'
RESTART = '<:RESTART:1090033853885841609>'

#The ID of the channel in which the server embedded message will be sent
channel_minecraft = 1042580793156976770

#The ID of the channel in which the logs message will be sent
channel_logs = 1042726524543041559

#User on which the screen session is running & your server is located
server_user = 'mcserver'

#Language parameter
locale.setlocale(locale.LC_ALL , 'fr_CH.UTF-8')

#Custom scripts location
#Check my GitHub documentation to know how to execute them as sudo without the password
start_script = f"sudo /home/"+server_user+"/discord-minecraft-server-bot/Commands/service_start.sh"
stop_script = f"sudo /home/"+server_user+"/discord-minecraft-server-bot/Commands/service_stop.sh"
restart_script = f"sudo /home/"+server_user+"/discord-minecraft-server-bot/Commands/service_restart.sh"

#Name of Screen session
screen_name = "mc-server"

#Discord Role name tha should be allowed to start / stop / restart the minecraft server
discord_role = "Admins"

#Information about the modpack of the server
modpack_name = "FTB ModPack"
modpack_info = "StoneBlock 3"

##Connexion information of the server
ip="127.0.0.1:25565"

#The link for the image of the embbed message
image_link = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"

#Discord Bot API KEY
API_KEY = 'xxxXXXXXxxxXXxxXXXXxxx.xxxxXXxxXXx.xxxxxxxxxXXXXXXXXXXXXXXXxxxxxxxXXXXX'

################################################################
#							 END	 						   #
################################################################
