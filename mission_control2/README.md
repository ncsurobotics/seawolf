The run.py file in this directory is what is used to make seawolf run missions. 

To modify the missions seawolf will run, edit the missions list/array in run.py

To run run.py svr and hub must first be running, typically these are initialized by running:
  sh start-autonomous-seawolf.sh (in seawolf/ dir)
  sh start-cams.sh   (in seawolf/cam_scripts)

it is also important to verify that the camera labels are correct in svr (front is front, down is down)


