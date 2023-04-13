#!/bin/bash

/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "say Server will [Restart] in 20 sec..."\015'
/bin/sleep 5
systemctl restart minecraft_server.service