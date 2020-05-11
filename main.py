#main.py
import pygame, sys, traceback, os

from pygame.locals import *
from random import *

import myplane
import enemy
import bullet
import supply

# 设置窗口打开位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 30"

pygame.init()
pygame.mixer.init()

size = width, height = 480, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("飞机大战")
icon = pygame.image.load('image/icon72x72.png').convert_alpha()
pygame.display.set_icon(icon)
background = pygame.image.load('image/background.png').convert()
# 颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# 字体
score_font = pygame.font.Font('font/Marker Felt.ttf', 36)

#载入游戏音乐
pygame.mixer.music.load('sound/game_music.mp3')
pygame.mixer.music.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('sound/big_spaceship_flying.wav')
enemy3_fly_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy2_down_sound.set_volume(0.1)
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.1)
me_down_sound = pygame.mixer.Sound('sound/game_over.wav')
me_down_sound.set_volume(0.1)
upgrade_sound = pygame.mixer.Sound('sound/achievement.wav')
upgrade_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)
# supply_sound = pygame.mixer.Sound('sound/')
get_bullet_sound = pygame.mixer.Sound('sound/get_double_laser.wav')
get_bullet_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.1)

def add_small_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.SmallEnemy(size)
		group1.add(e1)
		group2.add(e1)

def add_mid_enemies(group1, group2, num):
	for i in range(num):
		e2 = enemy.MidEnemy(size)
		group1.add(e2)
		group2.add(e2)

def add_big_enemies(group1, group2, num):
	for i in range(num):
		e3 = enemy.BigEnemy(size)
		group1.add(e3)
		group2.add(e3)

# 增加速度
def inc_speed(target, inc):
	for each in target:
		each.speed += inc

def main():
	pygame.mixer.music.play(-1)
	clock = pygame.time.Clock()
	running = True
	
	# 用于飞机图片切换
	switch_fly = True
	# 图片切换延迟
	delay = 100
	# 中弹图片索引
	e1_destory_index = 0
	e2_destory_index = 0
	e3_destory_index = 0
	me_destory_index = 0
	# 统计得分
	score = 0
	# 暂停相关
	paused = False
	pause_nor_image = pygame.image.load('image/game_pause_nor.png').convert_alpha()
	pause_pressed_image = pygame.image.load('image/game_pause_pressed.png').convert_alpha()
	resume_nor_image = pygame.image.load('image/game_resume_nor.png').convert_alpha()
	resume_pressed_image = pygame.image.load('image/game_resume_pressed.png').convert_alpha()
	paused_rect = pause_nor_image.get_rect()
	paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
	paused_image = pause_nor_image
	# 游戏结束画面
	game_over_font = pygame.font.Font('font/Marker Felt.ttf', 48)
	again_image1 = pygame.image.load('image/restart_nor.png').convert_alpha()
	again_image2 = pygame.image.load('image/restart_sel.png').convert_alpha()
	again_image = again_image1
	again_rect = again_image.get_rect()
	gameover_image1 = pygame.image.load('image/quit_nor.png').convert_alpha()
	gameover_image2 = pygame.image.load('image/quit_sel.png').convert_alpha()
	gameover_image = gameover_image1
	gameover_rect = gameover_image.get_rect()
	# 设置游戏难度
	level = 1
	# 全屏炸弹
	bomb_image = pygame.image.load('image/bomb.png').convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font('font/Marker Felt.ttf', 48)
	bomb_num = 3
	# 每30秒触发一个补给包
	bullet_supply = supply.Bullet_Supply(size)
	bomb_supply = supply.Bomb_Supply(size)
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
	# 超级子弹定时器
	DOUBLE_BULLET_TIME = USEREVENT + 1
	# 无敌状态定时器
	INVINCIBLE_TIME = USEREVENT + 2
	# 设置子弹标志
	is_double_bullet = False 
	# 生命数量
	life_image = pygame.image.load('image/plane.png').convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3
	# 限制打开文件次数
	recorded = False
	# 生成我方飞机
	me = myplane.MyPlane(size)
	# 生成普通子弹
	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4
	for i in range(BULLET1_NUM):
		bullet1.append(bullet.Bullet1(me.rect.midtop))
	# 生成超级子弹
	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 16
	for i in range(BULLET2_NUM):
		bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
		bullet2.append(bullet.Bullet2((me.rect.centerx + 33, me.rect.centery)))
	#敌方飞机
	enemies = pygame.sprite.Group()
	# 生成敌方小型飞机
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies, enemies, 15)
	# 生成敌方中型飞机
	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies, enemies, 4)
	# 生成敌方大型飞机
	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies, enemies, 2)

	while running :
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused
					if paused_image == pause_pressed_image:
						paused_image = resume_pressed_image
					else:
						paused_image = pause_pressed_image
					if paused:
						pygame.time.set_timer(SUPPLY_TIME, 0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					else:
						pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()

			elif event.type == MOUSEMOTION:
				if paused_rect.collidepoint(event.pos):
					if paused:
						paused_image = resume_pressed_image
					else:
						paused_image = pause_pressed_image
				else:
					if paused:
						paused_image = resume_nor_image
					else:
						paused_image = pause_nor_image
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if bomb_num:
						bomb_num -= 1
						bomb_sound.play()
						for each in enemies:
							if each.rect.bottom > 0:
								each.active = False		
			elif event.type == SUPPLY_TIME:
				# supply_sound.play()
				if choice([True, False]):
					bullet_supply.reset()
				else:
					bomb_supply.reset()					
			elif event.type == DOUBLE_BULLET_TIME:
				is_double_bullet = False
				pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
			elif event.type == INVINCIBLE_TIME:
				me.invincible = False
				pygame.time.set_timer(INVINCIBLE_TIME, 0)

		# 根据得分增加难度
		if level == 1 and score > 50000:
			level = 2
			upgrade_sound.play()
			# 增加3架小，2架中，1架大
			add_small_enemies(small_enemies, enemies, 3)
			add_mid_enemies(mid_enemies, enemies, 2)
			add_big_enemies(big_enemies, enemies, 1)
			# 提升飞机速度
			inc_speed(small_enemies, 1)
		elif level == 2 and score > 300000:
			level = 3
			upgrade_sound.play()
			# 增加5架小，3架中，2架大
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			# 提升飞机速度
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)
		elif level == 3 and score > 600000:
			level = 4
			upgrade_sound.play()
			# 增加5架小，3架中，2架大
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			# 提升飞机速度
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)
		elif level == 4 and score > 1000000:
			level = 5
			upgrade_sound.play()
			# 增加5架小，3架中，2架大
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			# 提升飞机速度
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)		

		screen.blit(background, (0, 0))
		# 检测用户键盘操作
		keys = pygame.key.get_pressed()
		if keys[K_ESCAPE]:
			pygame.quit()
			sys.exit()
		if life_num:
			if not paused:
				if keys[K_w] or keys[K_UP]:
					me.moveUp()
				if keys[K_s] or keys[K_DOWN]:
					me.moveDown()
				if keys[K_a] or keys[K_LEFT]:
					me.moveLeft()
				if keys[K_d] or keys[K_RIGHT]:
					me.moveRight()

				# 绘制补给并检测
				if bomb_supply.active:
					bomb_supply.move()
					screen.blit(bomb_supply.image, bomb_supply.rect)
					if pygame.sprite.collide_mask(bomb_supply, me):
						get_bomb_sound.play()
						if bomb_num < 3:
							bomb_num += 1
						bomb_supply.active = False

				if bullet_supply.active:
					bullet_supply.move()
					screen.blit(bullet_supply.image, bullet_supply.rect)
					if pygame.sprite.collide_mask(bullet_supply, me):
						get_bullet_sound.play()
						is_double_bullet = True
						pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
						bullet_supply.active = False

				# 发射子弹
				if not(delay % 10):
					bullet_sound.play()		
					if is_double_bullet:
						bullets = bullet2
						bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
						bullets[bullet2_index + 1].reset((me.rect.centerx + 33, me.rect.centery))
						bullet2_index = (bullet2_index + 2) % BULLET2_NUM
					else:
						bullets = bullet1
						bullets[bullet1_index].reset(me.rect.midtop)
						bullet1_index = (bullet1_index + 1) % BULLET1_NUM
				# 检测子弹是否击中
				for b in bullets:
					if b.active:
						b.move()
						screen.blit(b.image, b.rect)
						enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
						if enemy_hit:
							b.active = False
							for e in enemy_hit:
								if e in mid_enemies or e in big_enemies:
									e.energy -= 1
									e.hit = True
									if e.energy == 0: 
										e.active = False
								else:
									e.active = False
				# 绘制大型敌机
				for each in big_enemies:
					if each.active:
						each.move()
						if each.hit:
							#绘制被击中特效
							screen.blit(each.image_hit, each.rect)
							each.hit = False
						else:
							if switch_fly:
								screen.blit(each.image1, each.rect)
							else:
								screen.blit(each.image2, each.rect)
						# 绘制血槽
						pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)
						#当生命大于20%时显示绿色
						energy_remain = each.energy / enemy.BigEnemy.energy
						if energy_remain > 0.2:
							energy_color = GREEN
						else:
							energy_color = RED
						pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)
						#即将出现时播放音效
						if each.rect.bottom == -50:
							enemy3_fly_sound.play(-1)
					else:
						#毁灭
						if not (delay % 3):
							if e3_destory_index == 0:
								enemy3_down_sound.play()
							screen.blit(each.destory_images[e3_destory_index], each.rect)
							e3_destory_index = (e3_destory_index + 1) % 6
							if e3_destory_index == 0:
								score += 10000
								enemy3_fly_sound.stop()
								each.reset()
				# 绘制中型敌机
				for each in mid_enemies:
					if each.active:
						each.move()
						if each.hit:
							screen.blit(each.image_hit, each.rect)
							each.hit = False
						else:
							screen.blit(each.image, each.rect)
						# 绘制血槽
						pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)
						#当生命大于20%时显示绿色
						energy_remain = each.energy / enemy.MidEnemy.energy
						if energy_remain > 0.2:
							energy_color = GREEN
						else:
							energy_color = RED
						pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)
					else:
						#毁灭
						if not (delay % 3):
							if e2_destory_index == 0:
								enemy2_down_sound.play()
							screen.blit(each.destory_images[e2_destory_index], each.rect)
							e2_destory_index = (e2_destory_index + 1) % 4
							if e2_destory_index == 0:
								score += 6000
								each.reset()
				# 绘制小型敌机
				for each in small_enemies:
					if each.active:
						each.move()
						screen.blit(each.image, each.rect)
					else:
						#毁灭
						if not (delay % 3):
							if e1_destory_index == 0:
								enemy1_down_sound.play()
							screen.blit(each.destory_images[e1_destory_index], each.rect)
							e1_destory_index = (e1_destory_index + 1) % 4
							if e1_destory_index == 0:
								score += 1000
								each.reset()
				
				# 检测我方飞机是否被撞(精确)
				enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
				if enemies_down and not me.invincible:
					me.active = False
					for e in enemies_down:
						e.active = False

				# 绘制我方飞机
				if not (delay % 5):
					switch_fly = not switch_fly
				
				if me.active:
					if switch_fly:
						screen.blit(me.image1, me.rect)
					else:
						screen.blit(me.image2, me.rect)
				else:
					#我方飞机毁灭
					if not (delay % 3):
						if me_destory_index == 0:
							me_down_sound.play()
						screen.blit(me.destory_images[me_destory_index], me.rect)
						me_destory_index = (me_destory_index + 1) % 4
						if me_destory_index == 0:
							life_num -= 1
							me.reset()
							pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
			
				# 绘制炸弹
				bomb_text = bomb_font.render("x " + str(bomb_num), True, WHITE)
				text_rect = bomb_text.get_rect()
				screen.blit(bomb_image,(10, height - 10 - bomb_rect.height))
				screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

				# 绘制生命数量
				if life_num:
					for i in range(life_num):
						screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))

					#绘制暂停按钮
			screen.blit(paused_image, paused_rect)
			score_text = score_font.render("Score: " + str(score), True, WHITE)
			screen.blit(score_text, (10, 5))
		else:
			# bgm停止
			pygame.mixer.music.stop()
			pygame.mixer.stop()
			# 计时器停止
			pygame.time.set_timer(SUPPLY_TIME, 0)
			# 读取历史记录
			if not recorded:
				recorded = True
				with open('record.txt', 'r') as f:
					record_score = int(f.read())
				# 对比分数
				if score > record_score:
					with open('record.txt', 'w') as f:
						f.write(str(score))
			# 绘制结束画面
			record_score_text = game_over_font.render("Best: " + str(record_score), True, BLACK)
			screen.blit(record_score_text, (50, 50))
			gameover_text = game_over_font.render("Your Score: " + str(score), True, BLACK)
			gameover_text_rect = gameover_text.get_rect()
			gameover_text_rect.left, gameover_text_rect.top = (width - gameover_text_rect.width) // 2, height // 2 - gameover_text_rect.height - 10
			screen.blit(gameover_text, gameover_text_rect)

			again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text_rect.bottom + 10
			screen.blit(again_image, again_rect)

			gameover_rect.left, gameover_rect.top = (width - gameover_rect.width) // 2, again_rect.bottom + 10
			screen.blit(gameover_image, gameover_rect)

			#检测用户操作
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] <again_rect.bottom:
					main()
				elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
					pygame.quit()
					sys.exit()
			else:
				pos = pygame.mouse.get_pos()
				if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] <again_rect.bottom:
					again_image = again_image2
				else:
					again_image = again_image1
				if gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
					gameover_image = gameover_image2
				else:
					gameover_image = gameover_image1


		delay -= 1
		if not delay:
			delay = 100
		
		pygame.display.update()
		clock.tick(60)

if __name__ == "__main__":
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()