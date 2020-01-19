from inputs import devices, get_gamepad
import serial, time
from daw import TinyDAW, PEDAL, CLEAR_SIGNAL

KEY_RECORD = 'BTN_SOUTH'
KEY_EXIT = 'BTN_NORTH'
KEY_CLEAR = 'BTN_WEST'

print("\n\n\nWelcome to TinyDAW")

global running 
running = True

daw = TinyDAW()

def exit():
	print("Exiting..")
	daw.exit()

def keyPressed(events, key):
	for event in events:
		if(event.ev_type == 'Key'):
			if(event.code == key and event.state == 1):
				return True

def checkInput():
	events = get_gamepad()
	if(keyPressed(events, KEY_RECORD)):
		# daw.record()
		daw.receiveInput(PEDAL)
	if(keyPressed(events, KEY_CLEAR)):
		# daw.record()
		daw.receiveInput(CLEAR_SIGNAL)
	if(keyPressed(events, KEY_EXIT)):
		global running
		running = False

while running == True:
	checkInput()

exit()

