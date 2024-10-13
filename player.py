# player.py
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
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