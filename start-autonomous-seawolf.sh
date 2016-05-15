# Create the screen
screen -d -m -S seawolf
sleep 1 #TODO: less hackish solution than sleeping

# hub
screen -dr seawolf -p 0 -X title hub
sleep 0.5
screen -dr seawolf -p hub -X stuff "cd db
"
screen -dr seawolf -p hub -X stuff "seawolf-hub -c ../conf/hub.conf
"

# serialapp
screen -dr seawolf -X screen -t serialapp
sleep 1.5
screen -dr seawolf -p serialapp -X stuff "cd serial
"
screen -dr seawolf -p serialapp -X stuff "./bin/serialapp
"

# suite.sh
screen -dr seawolf -X screen -t suite
sleep 1.5
screen -dr seawolf -p suite -X stuff "cd applications
"
screen -dr seawolf -p suite -X stuff "./bin/conductor
"

#watch variable
screen -dr seawolf -X screen -t watchvars
sleep 0.2
screen -dr seawolf -p watchvars -X stuff "cd applications
"
screen -dr seawolf -p watchvars -X stuff "./bin/watchvariables Port Star Stern Bow StrafeT StrafeB Depth DepthPID.Heading
"
screen -dr seawolf -p watchvars -X stuff "
"


screen -dr seawolf -X screen -t bash
sleep 1.5
screen -dr seawolf -p bash -X stuff "cd applications
"
screen -dr seawolf -p bash -X stuff "
"

screen -x
#screen -dr seawolf -X windowlist
