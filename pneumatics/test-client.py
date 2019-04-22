from api import commands, fire, time

for command in commands:
  if command != "Kill":
    fire(command)
    time.sleep(2)
fire('Kill')