import seawolf

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Python Test App")

seawolf.notify.filter(seawolf.FILTER_ACTION, "EVENT")
seawolf.notify.filter(seawolf.FILTER_ACTION, "THRUSTER_REQUEST")
#seawolf.notify.filter(seawolf.FILTER_ACTION, "UPDATED")
seawolf.notify.filter(seawolf.FILTER_ACTION, "PING")
seawolf.notify.filter(seawolf.FILTER_ACTION, "PIDPAUSED")
seawolf.notify.filter(seawolf.FILTER_ACTION, "GO")
seawolf.notify.filter(seawolf.FILTER_ACTION, "COMPLETED")
while 1:
	print seawolf.notify.get()
