import pygame
import sys

class CheckKeyInput:
	def __init__(self):
		pygame.init()
		
		self.screen = pygame.display.set_mode((300,300))

	def run(self):
		while True:
			self._check_evnts()

	def _check_evnts(self):
		for event in pygame.event.get():
			print(f"{event}\n") 

	def _update_screen(self):
		pygame.display.flip()


if __name__ == '__main__':
	watcher = CheckKeyInput()
	watcher.run()
