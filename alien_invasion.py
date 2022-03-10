import sys
import pygame
from time import sleep
from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
	"""overall class to manage game assets and behavior"""

	def __init__(self):
		"""Initialize the game and create game resources"""
		pygame.init()
		self.settings = Settings()
		
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alein Invasion")

		# create an instance to store game statistics
		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			# Watch for keyboard and mouse events"""
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_aliens()
			self._update_screen()

	def _check_events(self):
		"""Respond to keypresses and mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_evnets(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_evnets(self, event):
		"""Respond to keypresses"""
		# ship movement
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		
		# firing bullets
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		
		# exit
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""Respond to key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		elif event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		# Update bullet positions.
		self.bullets.update()

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

			self._check_bullet_alien_collision()

	def _check_bullet_alien_collision(self):
		"""Respond to bullet-alien collisions"""
		# check for any bullets that have hit aliens
		# if so, get rid of the bullet and the alien
		cllosions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		# remove any bullets and aliens that have collided
		if not self.aliens:
			# destroy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.alien_speed += 0.1

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached to the bottom of the screen"""
		screen_rect = self.screen.get_rect()

		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# treat this the same as if the ship got it
				self._ship_hit()

	def _fire_bullet(self):
		"""Create a new bullet and add it to bullets group"""
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)

	def _create_fleet(self):
		"""Create the fleet of aliens"""
		# create an alien nad find the number of aliens in a row
		# spacing between each alien is equal to one alien width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		# determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# create the first row od aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)		

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in a row"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_aliens(self):
		"""Check if the fleet is at an edge,
		then update the positions of all aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update()

		# look for alien-ship collisions
		if pygame.sprite.spritecollide(self.ship, self.aliens, 1):
			self._ship_hit()
			print("SHIP HIT!!!")

		# Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien"""
		# decrement ships_left
		self.stats.ships_left -= 0.1

		# get rid of any reamining aliens or bullets
		self.aliens.empty()
		self.bullets.empty()

		# create a new fleet and center the ship
		self._create_fleet()
		self.ship.center_ship()

		#pasue
		sleep(0.5)

	def _update_screen(self):
		"""Update images on the screen and flip to the new screen"""
		# Redraw the screen during each pass through the loop
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
	
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		self.aliens.draw(self.screen)

		"""Make the most recently drawn screen visible"""
		pygame.display.flip()


if __name__ == "__main__":
	# Make a game instance and runt the game
	ai = AlienInvasion()
	ai.run_game()
