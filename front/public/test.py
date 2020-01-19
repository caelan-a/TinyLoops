import fileinput, sys, json

running = True

def sendResponse(t, message):
    response = {
        'type' : t,
        'message' : message
    }

    print(json.dumps(response))
    sys.stdout.flush()


while running:
    for line in fileinput.input():
        sendResponse('response', line)
