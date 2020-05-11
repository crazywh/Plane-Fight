import pygame
from random import *

class Bullet_Supply(pygame.sprite.Sprite):
	def __init__(self, size):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('image/prop_type_0.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = size[0], size[1]
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
		self.speed = 5
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100

class Bomb_Supply(pygame.sprite.Sprite):
	def __init__(self, size):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('image/prop_type_1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = size[0], size[1]
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
		self.speed = 5
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100