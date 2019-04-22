# Create the screen
screen -d -m -S seawolf
screen -dr seawolf -p 0 -X title hub
screen -dr seawolf -X screen -t procs
screen -dr seawolf -X screen -t serialapp
screen -dr seawolf -X screen -t suite
screen -dr seawolf -X screen -t watchvars
screen -dr seawolf -X screen -t HUD
screen -dr seawolf -X screen -t imu_cal
screen -dr seawolf -X screen -t bash
screen -dr seawolf -X screen -t MISSION
screen -dr seawolf -X screen -t pneumatics
screen -dr seawolf -X screen -t cams

# start seawolf processes
screen -dr seawolf -p procs -X stuff "./procs.sh
"