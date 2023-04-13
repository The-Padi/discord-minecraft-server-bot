#!/bin/bash

/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "say Server Shutdown in 15 sec..."\015'
/bin/sleep 5
/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "say Server Shutdown in 10 sec..."\015'
/bin/sleep 5
/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "say Server Shutdown in 5 sec..."\015'
/bin/sleep 5
/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "save-all"\015'
/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "stop"\015'
