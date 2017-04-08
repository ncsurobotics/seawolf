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

# monitor
screen -dr seawolf -X screen -t HUD
sleep 0.2
screen -dr seawolf -p HUD -X stuff "cd applications
"
screen -dr seawolf -p HUD -X stuff "./bin/depthmonitor2
"
screen -dr seawolf -p HUD -X stuff "
"

# Arduino
screen -dr seawolf -X screen -t imu_cal
sleep 0.2
screen -dr seawolf -p imu_cal -X "cd ~/software/external/razor-9dof-ahrs/Arduino/Razor_AHRS/
"
screen -dr seawolf -p imu_cal -X stuff "pwd
"
#screen -dr seawolf -p imu_cal -X stuff "arduino
#"

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

# cameras
screen -dr seawolf -X screen -t cams
sleep 0.2
screen -dr seawolf -p bash -X stuff "sh cam_scripts/start-cams.sh
"
screen -dr seawolf -p bash -X stuff "
"
screen -dr seawolf -p bash -X stuff "cd 
"


screen -x
#screen -dr seawolf -X windowlist

