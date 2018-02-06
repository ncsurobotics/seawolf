import time

def test(navObj, values, tolerance):
	"""
		navObj is the sw3.routines obj to test		
		values is a list of values to go to
		tolerance the tolerance to go to when checking
	"""
	for val in values:
		a = navObj(val, -1, tolerance = tolerance)
		print ("starting")
		startTime = time.time()
		a.start()
		a.wait()
		endTime = time.time()
		print("Obj %10s, value: %5.2f, time %5.3f" % (navObj.__name__, val, endTime - startTime))
		print("waiting before next test")
		time.sleep(2)
		
	print("Done with tests")

