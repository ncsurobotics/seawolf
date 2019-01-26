import cv2

keyCount = 0
keyVal = ''
keyCountNeeded = 10

def getKeyPress():
  global keyCount, keyVal, keyCountNeeded
  for i in range(keyCountNeeded * 2):
    key = cv2.waitKey(1) & 0xFF
    if key == keyVal:
      keyCount += 1
    elif keyCount >= keyCountNeeded:
      keyCount = 0
      return key
    else:
      keyCount = 1
      keyVal = key
  return ''