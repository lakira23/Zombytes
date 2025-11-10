import pygame 
#pygame is a library which helps create a 2d environment/canvas which the user can work with. It especially is very useful with games. "Import" takes this library and connects it to this code, therefore the methods attached to the library can be used.
from pygame.locals import *
# this will import all the attributes and methods regarding pygame.locals, this will specially help in the game loop where the event loop comes about

pygame.init()
# This initializes the library pygame so that it can be used, this is like the starting motor of a car. 
window = pygame.display.set_mode((800, 800))
#This will create a surface, more like a canvas of size 800 by 800 which will help contain sprites
clock = pygame.time.Clock()
#This creates an instance of a clock using the pygame library, this gives the game a sense of time. This is how animations and level timers are implemented into the program. 
running= True

while running:#The main loop which will generate each frame.
	clock.tick(60)
	#Since the game loop is a for loop, the number of frames will depend on the device, therefore some will experience the game in unusual manners. Therefore, we limit the game loop to loop once per 1/600 second. 
	window.fill((0,0,0))
	#This resets the game canvas so that the next frame can be drawn.

	'''most of the objects go here'''
	
	for event in pygame.event.get():
	        if event.type == QUIT:
		        running = False
'''most of the input checks go here'''
'''most of the object updates and rendering goes here'''
pygame.display.update()
# this updates the canvas of the new screen.
		