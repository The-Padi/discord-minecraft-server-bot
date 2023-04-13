import discord
import subprocess
import psutil

from datetime import datetime
from discord.ext import tasks

from mcipc.query import Client as mc_query

from user_settings import *

################################################################
#			EDIT BELLOW CODE ONLY AS LAST RESORT			   #
################################################################


###################################
#	  Variables & Parameters	  #
###################################

#EMOJI ID
START_ID = int(START.split(':')[-1].split('>')[0])
STOP_ID = int(STOP.split(':')[-1].split('>')[0])
RESTART_ID = int(RESTART.split(':')[-1].split('>')[0])

#Global
msg_id = 0
auto_restart = 0

#Discord parameters
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


###################################
#	  		Functions	  		  #
###################################

#Function to transform a player list given by a minecraft query to an discord markdown message
def player_list_to_markdown(player_list):
	
	#Start the markdown
	online_players = "```"
	
	counter = 0
	
	#Check if there is no player online
	if len(player_list) != 0:
		
		#Go through the list of players
		for player in player_list:
			counter += 1
			
			#Set one player by line with a number (1 - Username)
			online_players += str(counter) + " - " + str(player) + "\n"
	else:
		
		#Default message if no players are online
		online_players += "No player online..."
		
	#End the markdown
	online_players += "```"
	
	return online_players

#Function to get the CPU usage
def get_cpu_usage():
    
    #Try to get the CPU usage
	try:
		
		#Get the current CPU usage via top command and some pipes
		result = subprocess.run(["top", "-b", "-n", "1"], stdout=subprocess.PIPE, check=True)
		
		#Name of the user on which the server is running
		output = subprocess.run(["grep", server_user], input=result.stdout, stdout=subprocess.PIPE, check=True)
		
		output = subprocess.run(["grep", "java"], input=output.stdout, stdout=subprocess.PIPE, check=True)
		output = subprocess.run(["awk", "{print $9}"], input=output.stdout, stdout=subprocess.PIPE, check=True)
		output_str = output.stdout.decode('utf-8').strip()
		
		#Do a savant calculation to get the total CPU usage and not the CPU usage by tread (more than 100%)
		cpu_percent = psutil.cpu_percent(interval=1)
		cpu_usage = round(float(output_str) * cpu_percent / 100, 2)
		
	#If we get an error, set the value to default
	except:
		cpu_usage = 0
	
	return cpu_usage

#Function to get the Memory usage
def get_mem_usage():
    
    #Try to get the memory usage
	try:
		
		#Get the current Memory usage via top command and some pipes
		result = subprocess.run(["top", "-b", "-n", "1"], stdout=subprocess.PIPE)
		
		#Name of the user on which the server is running
		output = subprocess.run(["grep", server_user], input=result.stdout, stdout=subprocess.PIPE)
		
		output = subprocess.run(["grep", "java"], input=output.stdout, stdout=subprocess.PIPE)
		output = subprocess.run(["awk", "{print $10}"], input=output.stdout, stdout=subprocess.PIPE)
		output_str = output.stdout.decode('utf-8').strip()
		
		#Do a calculation to get the correct total memory usage
		memory_usage = round((float(output_str) / 100) * psutil.virtual_memory().total / (1024 * 1024 * 1024),2)
		
	#If we get an error, set the value to default
	except:
		memory_usage = 0
	
	return memory_usage

#Function to get the server information via query
def get_srv_info_query():
    
    #Try to get the information of the server via query
	try:
		
		#If the server responded, everything is running
		with mc_query('192.168.1.4', 25565) as client_mc:
			full_stats = client_mc.full_stats
			
			#Number of players connected
			number_of_player = full_stats.num_players
			
			#Max number of players of the server
			max_players = full_stats.max_players
			
			#List of players currently online
			player_list = full_stats.players
			
			#Set the status to "Running"
			status = ":green_circle: Running"
		
	#If we get an error, that means that the server is currently restarting
	except:
		
		#Put all our information to default values
		number_of_player = 0
		max_players = 0
		player_list = []
		
		#Set the status to "Restarting"
		status = ":orange_circle: Restarting"
	
	return number_of_player, max_players, player_list, status

#Function to create the embedded message
def create_embed(status, cpu_usage, memory_usage, number_of_player, max_players, online_players):
	
	#Title of the message
	embed=discord.Embed(title="Server Info", description=" ", color=0x38761D)
	
	#Image icon
	embed.set_thumbnail(url=image_link)
	
	#Current status of the server
	embed.add_field(name="Server Status", value=status, inline=False)
	
	#Modpack
	embed.add_field(name=modpack_name, value=modpack_info, inline=True)
	
	#IP
	embed.add_field(name="IP", value=ip, inline=True)
	
	#CPU usage
	embed.add_field(name="CPU Usage", value=str(cpu_usage)+" %", inline=True)
	
	#Memory usage
	embed.add_field(name="Memory Usage", value=str(memory_usage)+" GB", inline=True)
	
	#Player count
	embed.add_field(name="Player Count", value=str(number_of_player)+"/"+str(max_players), inline=True)
	
	#Online players
	embed.add_field(name="Online Players", value=online_players, inline=False)
	
	#Footer
	embed.set_footer(text="Power By Padi • "+datetime.now().strftime('%A %H:%M'))
	
	return embed

#Function to create the embedded message for the logs
def create_embed_logs(username, action):
	
	if action == 'stop':
		
		#Title of the message
		embed=discord.Embed(title="Minecraft Server", description=username + " has sent a [stop] command via the discord bot.", color=0xa80000)
		
		#Edit the Author Field
		embed.set_author(name="⚠️ Alert - Server Stopping ⚠️", icon_url=image_link)
		
	elif action == 'start':
		
		#Title of the message
		embed=discord.Embed(title="Minecraft Server", description=username + " has sent a [start] command via the discord bot.", color=0xa80000)
		
		#Edit the Author Field
		embed.set_author(name="⚠️ Alert - Server Starting ⚠️", icon_url=image_link)
		
	elif action == 'restart':
		
		#Title of the message
		embed=discord.Embed(title="Minecraft Server", description=username + " has sent a [restart] command via the discord bot.", color=0xa80000)
		
		#Edit the Author Field
		embed.set_author(name="⚠️ Alert - Server Restarting ⚠️", icon_url=image_link)
		
	
	#Footer
	embed.set_footer(text="Power By Padi • "+datetime.now().strftime('%A %H:%M'))
	
	return embed

#Discord Bot task that will loop every X seconds, or minutes, or hours
#Main task = edit the embedded message
#Secondary task = Try to restart the server in case it crashes
@tasks.loop(seconds=30)
async def send_message_loop(msg):
    
	#Get the status of the Auto Restart
	global auto_restart
	
	#Check if the screen session of the minecraft server is running
	result = subprocess.run(["screen", "-S", screen_name, "-Q", "select", "."], stdout=subprocess.PIPE)
	server_status = result.stdout.decode('utf-8').strip()
	
	#If the screen session is running
	if server_status == "":
		
		#Reset the Auto Restart status
		auto_restart = 0
		
		#Get the information of the server via query
		number_of_player, max_players, player_list, status = get_srv_info_query()
		
		#Get the CPU usage
		cpu_usage = get_cpu_usage()
		
		#Get the memory usage
		memory_usage = get_mem_usage()
		
	#If the screen session is not running (Server is stopped)
	else:
		
		#Set the status to "Stopped"
		status = ":red_circle: Stopped"
		
		#Put all our information to default values
		number_of_player = 0
		max_players = 0
		player_list = []
		cpu_usage = 0
		memory_usage = 0
		
		#Try to restart the server ones
		if auto_restart == 0:
			
			#Set the status to "Auto Restart"
			status = ":red_circle: Stopped - Auto Restart"
			
			auto_restart = 1
			subprocess.run(restart_script.split())
	
	
	#Format players list to be a markdown for the embedded message
	online_players = player_list_to_markdown(player_list)
	
	#Create the embedded message
	embed = create_embed(status, cpu_usage, memory_usage, number_of_player, max_players, online_players)
	
	#Edit the message
	await msg.edit(embed=embed)

#First action of the Discord Bot
@client.event
async def on_ready():
	
	#Get the msg_id to set it with the first message
	global msg_id
	
	#Small log just to confirm that the bot has successfully started
	print('I am connected as {0.user}'.format(client))
	
	#Set the Bot Status on Discord
	await client.change_presence(activity=discord.Game(name="monitor the server"))
	
	#Check if the screen session of the minecraft server is running
	result = subprocess.run(["screen", "-S", screen_name, "-Q", "select", "."], stdout=subprocess.PIPE)
	server_status = result.stdout.decode('utf-8').strip()
	
	#If the screen session is running
	if server_status == "":
		
		#Get the information of the server via query
		number_of_player, max_players, player_list, status = get_srv_info_query()
		
		#Get the CPU usage
		cpu_usage = get_cpu_usage()
		
		#Get the memory usage
		memory_usage = get_mem_usage()
		
	#If the screen session is not running (Server is stopped)
	else:
		
		#Set the status to "Stopped"
		status = ":red_circle: Stopped"
		
		#Put all our information to default values
		number_of_player = 0
		max_players = 0
		player_list = []
		cpu_usage = 0
		memory_usage = 0
	
	#Format players list to be a markdown for the embedded message
	online_players = player_list_to_markdown(player_list)
	
	#Create the embedded message
	embed = create_embed(status, cpu_usage, memory_usage, number_of_player, max_players, online_players)
	
	#Set the Discord channel
	channel = client.get_channel(channel_minecraft)
	
	#Check if the last message on the channel is from the Bot to avoid a delete + a resend (SPAM)
	last_message = (await channel.history(limit=1).flatten())[-1]
	
	if last_message.author == client.user:
		
		#Use the last message as our new message
		msg_id = last_message.id
		msg = last_message
		
		await msg.edit(embed=embed)
		
		await msg.clear_reactions()
		
		
	else:
		
		#Remove ALL old messages
		await channel.purge()
		
		#Send the message and take it's ID and information for future editing
		msg = await channel.send(embed=embed)
		msg_id = msg.id
	
	#Set the emojis that will be added to the message
	emojis = [START, STOP, RESTART]
	
	#Loop thought the emojis table and add every emoji to the message
	for emoji in emojis:
		await msg.add_reaction(emoji)
	
	#Start the loop task
	send_message_loop.start(msg)

#When an emoji / reaction is added to the message
@client.event
async def on_raw_reaction_add(payload):
    
    #Get the discord information
	guild = client.guilds[0]
	
	#Set the specific role that will be allowed to start actions with the reactions
	role = discord.utils.get(guild.roles, name=discord_role)
	
	#Get the information about the reaction
	channel = await client.fetch_channel(payload.channel_id)
	message = await channel.fetch_message(payload.message_id)
	
	#Get the user
	user = await client.fetch_user(payload.user_id)
	member = guild.get_member(user.id)
	
	#Check if the user is not the bot / if the reaction is on our embedded message / if the user has the good role
	if message.author == client.user and payload.user_id != client.user.id and role in member.roles:
		
		#Remove the reaction
		await message.remove_reaction(payload.emoji, user)
		
		#Execute the the correct action depending on the reaction
		if payload.emoji.id == START_ID:
			
			#Create the embedded message
			embed = create_embed_logs(member.name, 'start')
			
			#Set the Discord channel
			channel = client.get_channel(channel_logs)
			
			#Send the Log
			await channel.send(embed=embed)
			
			#Start the server
			subprocess.run(start_script.split())
			
		elif payload.emoji.id == STOP_ID:
			
			#Create the embedded message
			embed = create_embed_logs(member.name, 'stop')
			
			#Set the Discord channel
			channel = client.get_channel(channel_logs)
			
			#Send the Log
			await channel.send(embed=embed)
			
			#Stop the server
			subprocess.run(stop_script.split())
			
		elif payload.emoji.id == RESTART_ID:
			
			#Create the embedded message
			embed = create_embed_logs(member.name, 'restart')
			
			#Set the Discord channel
			channel = client.get_channel(channel_logs)
			
			#Send the Log
			await channel.send(embed=embed)
			
			#Restart the server
			subprocess.run(restart_script.split())
	
	#If the user has not the good role, simply remove the reaction
	elif message.author == client.user and payload.user_id != client.user.id :
		
		#Remove the reaction
		await message.remove_reaction(payload.emoji, user)

def main():
	#Start the bot (API KEY)
	client.run(API_KEY)

if __name__ == "__main__":
    main()