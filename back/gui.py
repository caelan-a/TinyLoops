import pygame
import math
import time

WHITE =     (255, 255, 255)
GREY =     (200, 200, 200)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
TEXTCOLOR = (  0,   0,  0)
(width, height) = (400, 400)

def getPos():
    pos = pygame.mouse.get_pos()
    return (pos)

def drawCircle():
    pos=getPos()
    pygame.draw.circle(screen, BLUE, pos, 20) # Here <<<


class LED:
  def __init__(self, x,y,isOn):
    self.x = x
    self.y = y
    self.isOn = isOn
    self.colour = GREY
    self.radius = 20

  def draw(self):
    if self.isOn:
      self.colour = GREEN
    else:
      self.colour = GREY

    pygame.draw.circle(screen, self.colour, (self.x,self.y), self.radius) # Here <<<




class LEDRing:

  def __init__(self, x,y, radius, ledCount):
    self.leds = []
    self.x = x
    self.y = y
    self.ledCount = ledCount
    self.radius = radius
    self.sequenceStep = 0



    angleInterval = 360.0/ledCount;

    print("Making ring of {} LEDs".format(ledCount))
    for i in range(0,ledCount):
      angleToRotate = math.radians(i * angleInterval);
      print(angleToRotate)
      x = self.x + int(radius*math.cos(angleToRotate))
      y = self.y + int(radius*math.sin(angleToRotate))
      self.leds.append(LED(x,y,False))

  def draw(self):
    for led in self.leds:
      led.draw()

  def setLED(self,index, isOn):
    self.leds[index].isOn = isOn;

  def resetLEDs():
    for led in self.leds:
      led.isOn = False

  def updatePattern(self, type):
    if(type == 1):  
      for i in range(0, self.ledCount):
        if i == self.sequenceStep:
          self.leds[i].isOn = True
        else:
          self.leds[i].isOn = False

      if(self.sequenceStep >= self.ledCount-1):
        self.sequenceStep = 0
      else:
        self.sequenceStep += 1
      print(self.sequenceStep)


ring = LEDRing(200, 200, 100, 8);
running = True;
totalTime = 0
lastFrameTime = time.process_time()
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TinyLoops")
screen.fill(WHITE)
pygame.display.update()

while running:
  timeStep = time.process_time() - lastFrameTime
  lastFrameTime = time.process_time()
  totalTime += timeStep

  ev = pygame.event.get()

  for event in ev:
      if event.type == pygame.MOUSEBUTTONUP:
          pygame.display.update()
      if event.type == pygame.QUIT:
          running = False

  if(totalTime % 2 == 0):
    ring.updatePattern(1)
    ring.draw()
  pygame.display.update()


