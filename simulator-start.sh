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

#svrd
screen -dr seawolf -X screen -t svrd
sleep 1.5
screen -dr seawolf -p svrd -X stuff "svrd
"


#suite.sh
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

# monitor
screen -dr seawolf -X screen -t HUD
sleep 0.2
screen -dr seawolf -p HUD -X stuff "cd applications
"
screen -dr seawolf -p HUD -X stuff "./bin/depthmonitor2
"
screen -dr seawolf -p HUD -X stuff "
"

# svrwatch
screen -dr seawolf -X screen -t svrwatch
sleep 0.5
screen -dr seawolf -p svrwatch -X stuff "svrwatch -a
"


# bash
screen -dr seawolf -X screen -t bash
sleep 1.5
screen -dr seawolf -p bash -X stuff "cd applications
"
screen -dr seawolf -p bash -X stuff "
"

# mission 
screen -dr seawolf -X screen -t MISSION
screen -dr seawolf -p bash -X stuff "cd mission_control
"
screen -dr seawolf -p bash -X stuff "
"

#simulator
screen -dr seawolf -X screen -t simulator
sleep 1.5
screen -dr seawolf -p simulator -X stuff "cd simulator
"
screen -dr seawolf -p simulator -X stuff "python sim.py Conf/new.conf
"

#gui
screen -dr seawolf -X screen -t gui
sleep 1.5
screen -dr seawolf -p gui -X stuff "cd applications/gui/
"
screen -dr seawolf -p gui -X stuff "python gui.py
"

screen -x



