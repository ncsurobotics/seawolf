# Create the screen
screen -d -m -S seawolf
sleep 1 #TODO: less hackish solution than sleeping

# Hub
screen -dr seawolf -p 0 -X title hub
sleep 0.5
screen -dr seawolf -p hub -X stuff "cd libseawolf"
screen -dr seawolf -p hub -X stuff "./hub"

# Serialapp
screen -dr seawolf -X screen -t serialapp
sleep 0.5
screen -dr seawolf -p serialapp -X stuff "cd serial"
screen -dr seawolf -p serialapp -X stuff "LD_LIBRARY_PATH=../libseawolf/ ./serialapp"

# Mixer
screen -dr seawolf -X screen -t mixer
sleep 0.5
screen -dr seawolf -p mixer -X stuff "cd applications"
screen -dr seawolf -p mixer -X stuff "LD_LIBRARY_PATH=../libseawolf/ ./bin/mixer"

# PIDs

# Tracker
screen -dr seawolf -X screen -t tracker
sleep 0.5
screen -dr seawolf -p tracker -X stuff "cd applications"
screen -dr seawolf -p tracker -X stuff "LD_LIBRARY_PATH=../libseawolf/ ./bin/tracker"

# Tracker Proxy
screen -dr seawolf -X screen -t trackerproxy
sleep 0.5
screen -dr seawolf -p trackerproxy -X stuff "cd applications"
screen -dr seawolf -p trackerproxy -X stuff "LD_LIBRARY_PATH=../libseawolf/ ./bin/trackerproxy"


#screen -dr seawolf -X windowlist
