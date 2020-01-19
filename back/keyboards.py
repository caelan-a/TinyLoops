from inputs import devices, get_gamepad


def keyPressed(events, key):
	for event in events:
		if(event.ev_type == 'Key'):
			if(event.code == key and event.state == 1):
				return True

def checkInput():
	events = get_gamepad()
	if(keyPressed(events, 'BTN_SOUTH')):
		print("Hi")

while True:
	checkInput()
