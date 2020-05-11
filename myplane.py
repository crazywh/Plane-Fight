import pygame

class MyPlane(pygame.sprite.Sprite):
	def __init__(self, size):
		pygame.sprite.Sprite.__init__(self)

		self.image1 = pygame.image.load('image/hero1.png').convert_alpha()
		self.image2 = pygame.image.load('image/hero2.png').convert_alpha()
		self.destory_images = []
		self.destory_images.extend([pygame.image.load('image/hero_blowup_n1.png').convert_alpha(), pygame.image.load('image/hero_blowup_n2.png').convert_alpha(), pygame.image.load('image/hero_blowup_n3.png').convert_alpha(), pygame.image.load('image/hero_blowup_n4.png').convert_alpha()])
		self.rect = self.image1.get_rect()
		self.width, self.height = size[0], size[1]
		self.rect.left = (self.width - self.rect.width) // 2
		self.rect.top = self.height - 60 - self.rect.height
		# 飞机速度
		self.speed = 10
		self.active = True
		self.invincible = False
		#将非透明部分作为碰撞检测
		self.mask = pygame.mask.from_surface(self.image1)

	def moveUp(self):
		if self.rect.top > 0:
			self.rect.top -= self.speed
		else:
			self.rect.top = 0

	def moveDown(self):
		if self.rect.bottom < self.height - 60:
			self.rect.bottom += self.speed
		else:
			self.rect.bottom = self.height - 60

	def moveLeft(self):
		if self.rect.left > 0:
			self.rect.left -= self.speed
		else:
			self.rect.left = 0

	def moveRight(self):
		if self.rect.right < self.width:
			self.rect.right += self.speed
		else:
			self.rect.right = self.width

	def reset(self):
		self.active = True
		self.rect.left = (self.width - self.rect.width) // 2
		self.rect.top = self.height - 60 - self.rect.height
		self.invincible = True