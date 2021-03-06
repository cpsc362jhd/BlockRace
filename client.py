#! /usr/bin/env python

import sys, os, socket, threading

from gameClasses import *
from clientNetwork import *

try:
   import cPickle as pickle
except:
   import pickle

try:
   import pygame
   from pygame.locals import *
except:
   print "Pygame not found"

if len(sys.argv) < 2:
   HOST = ''
else:
   HOST = sys.argv[1]

def main():
   # Init pygame
   os.environ["SDL_VIDEO_CENTERED"] = "1"
   pygame.init()

   # Set the display mode
   pygame.display.set_caption("Platformer Demo")
   screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
   pygame.mouse.set_visible(False)
   pygame.font.init()
   pygame.key.set_repeat(500, 30)

   clock = pygame.time.Clock()
   font = pygame.font.Font(None,25)

   # Create all the platforms by parsing the level.
   parse_level()

   # Set up network threads
   commH = commHandler(HOST)
   commH.setDaemon(True)
   commH.start()
   clientH = clientHandler(HOST)
   clientH.setDaemon(True)   
   clientH.start()

   try:
      while True:
         clock.tick()
         
         # Get inputs
         for e in pygame.event.get():
            if e.type == QUIT:
               # Send exit signal over TCP
               os._exit(1)
            if e.type == KEYDOWN:
               put_frame(pygame.key.get_pressed())
               if e.key == K_ESCAPE:
                  # Send exit signal over TCP
                  os._exit(1)
            if e.type == KEYUP:
               put_frame(pygame.key.get_pressed())

         if len(players.sprites()) >= 4:
            for gate in gates.sprites():
               gate.kill()

         #Draw the scene
         screen.fill((0, 0, 0))
         sprites.draw(screen)
         pygame.display.flip()
      # End main loop
   except KeyboardInterrupt:
      os._exit(1)

if __name__ == '__main__':
   main()
