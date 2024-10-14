# player.py
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

from weapon import Weapon, Bullet

class Player:
    def __init__(self, position=(0, 2, 0), speed=5, jump_height=2):
        self.controller = FirstPersonController(position=position)
        self.controller.speed = speed
        self.controller.jump_height = jump_height
        self.weapon = Weapon(parent=camera)
        self.bullets = []
        self.shoot_cooldown = .25  # Cooldown time in seconds
        self.last_shoot_time = 0
        self.health = HealthBar(bar_color=color.lime.tint(-.25), curve=.5, max_value=100, value=100, scale=(.5,.1))

    def update(self):
        if held_keys['shift']:
            self.controller.speed = 10
        else:
            self.controller.speed = 5

        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)


        # print("bullets" + str(self.bullets))
    def shoot(self):
        bullet = self.weapon.shoot() # pass in player position
        if bullet:
            self.bullets.append(bullet)

        self.last_shoot_time = time.time()


    def decrement_health(self, number):
        # if number - then raise SkibidiCustomError
        if self.health.value >= number:
            self.health.value -= number
        else:
            self.health.value = 0
