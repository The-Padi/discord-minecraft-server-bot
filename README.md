# Linux Python Discord Bot for Minecraft Server

I created this bot to have a simple and easy way to get informations from a minecraft server and interact with it.

![The_Bot](https://user-images.githubusercontent.com/17253999/230373214-b249628d-2348-4ecd-95d5-58392373b308.png)

## Key Features

- Get dynamic informations about the server
  - Server Status
  - CPU Usage
  - Memory Usage
  - Player Count
  - Online Players Usernames

- Interact with the service that runs the server
  - Restart
  - Shutdown
  - Start

- Auto-restart the server if it crashes

- Logs messages in a separate Discord Channel

## Futur Key Features

- Player Play time
- Send command via Discord
- Player Count as status
- If there is a features that you would like to see, tell me about it !

## Requirements:

- Linux based Host
- [Python 3.8+](https://www.python.org/)
- [A Discord Bot](https://discordpy.readthedocs.io/en/stable/discord.html)
- [Discord.py](https://pypi.org/project/discord.py/)
- [A Discord server !](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server-)

## Installing

This install is based on a FTB server with all the server files in the home directory of the user.

### Install Screen

```console
foo@bar:~$ sudo apt-get update
foo@bar:~$ sudo apt-get install screen
```
### Download the files

Login as the user that runs the minecraft server and execute those commands :
```console
foo@bar:~$ cd ~/
foo@bar:~$ wget https://github.com/Padi1111/discord-minecraft-server-bot/archive/refs/heads/main.zip
foo@bar:~$ unzip main.zip
foo@bar:~$ rm main.zip
foo@bar:~$ mv discord-minecraft-server-bot-main discord-minecraft-server-bot
```

### Move the start script and edit it

Move the start script to the root of the minecraft server folder. In my case, this is the root home of the user.
```console
foo@bar:~$ mv ~/discord-minecraft-server-bot/start.sh ~/.
```

You can then edit it to make it work with your minecraft server
```console
foo@bar:~$ nano ~/start.sh
```

### Edit the Bot

You can now edit the bot to your desire and configure it for your discord server.
To do so, edit the file called ```user_settings.py``` in the ```discord-minecraft-server-bot``` folder.
```console
foo@bar:~$ nano ~/discord-minecraft-server-bot/user_settings.py
```

### Edit /etc/sudoers

To be able to run all the files in the Commands directory as sudo without giving any password we will be addind the scipts to our /etc/sudoers file.
To do so, open it, as sudo, with your any editor :
```console
foo@bar:~$ sudo nano /etc/sudoers
```
Go to this section :
```bash
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
```
And bellow it add the following command, making sure to change the [USERNAME] by the username of the user running the bot :
```bash
[USERNAME]  ALL=(ALL) NOPASSWD: /home/[USERNAME]/discord-minecraft-server-bot/Commands/service_stop.sh
[USERNAME]  ALL=(ALL) NOPASSWD: /home/[USERNAME]/discord-minecraft-server-bot/Commands/service_start.sh
[USERNAME]  ALL=(ALL) NOPASSWD: /home/[USERNAME]/discord-minecraft-server-bot/Commands/service_restart.sh
```
You can now save and close this file.

### Create the Linux Service for the Minecraft Server

We will now be creating the service for the Minecraft Server.

```console
foo@bar:~$ sudo nano /etc/systemd/system/minecraft-server.service
```

Copy paste this, making sure to change the [USERNAME] by the username of the user running the bot :
```bash
[Unit]

Description=Minecraft Server
After=network.target

[Service]

Type=simple
RemainAfterExit=true

WorkingDirectory=/home/[USERNAME]
User=[USERNAME]

Restart=on-failure

ExecStart=/usr/bin/screen -dmS mc-server bash start.sh

ExecStop=bash discord-minecraft-server-bot/stop.sh

[Install]

WantedBy=multi-user.target
```
Save and close this file.

Enable the serivce and start it :
```console
foo@bar:~$ sudo nano systemctl enable minecraft-server.service
foo@bar:~$ sudo nano systemctl start minecraft-server.service
```

If everything whent well, your minecraaft server should now start. To check, login as the user that runs the server and execute this command :
```console
foo@bar:~$ screen -ls
```
You should see something like this :
```console
There is a screen on:
        2590603.mc-server       (15. 04. 23 16:00:18)   (Detached)
1 Socket in /run/screen/S-mcserver.
```

### Create the Linux Service for the Bot

We will now be creating the service for the discord bot.
```console
foo@bar:~$ sudo nano /etc/systemd/system/discord-minecraft-bot.service
```
Copy paste this, making sure to change the [USERNAME] by the username of the user running the bot :
```bash
[Unit]

Description=Discord Minecraft Bot
After=network.target

[Service]

Type=simple
RemainAfterExit=true

WorkingDirectory=/home/[USERNAME]/discord-minecraft-server-bot/
User=[USERNAME]

Restart=always
RestartSec=10

ExecStart=/usr/bin/python discord_bot.py


[Install]

WantedBy=multi-user.target
```
Save and close this file.

Enable the serivce and start it :
```console
foo@bar:~$ sudo nano systemctl enable discord-minecraft-bot.service
foo@bar:~$ sudo nano systemctl start discord-minecraft-bot.service
```

If everything whent well, the bot should be online in your discord server and you should see the embedded message with all the informations about the minecraft server.

## Screenshots

![The_Bot_Restarting](https://user-images.githubusercontent.com/17253999/231829800-59614e03-a354-4219-9181-ff7e4ea4f858.png)
![The_Bot_With_players](https://user-images.githubusercontent.com/17253999/231830655-c86a87dd-4ab1-4502-bf17-c197b648beaf.png)
![The_Bot_logs](https://user-images.githubusercontent.com/17253999/231829049-65bb3aea-20f8-42c2-abb9-13524260bf83.png)
