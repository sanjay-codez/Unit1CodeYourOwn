# player.py
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina import Audio, Text

from weapon import Weapon, Bullet

class Player:
    def __init__(self, position=(0, 2, 0), speed=5, jump_height=2):
        self.controller = FirstPersonController(position=position)
        self.controller.speed = speed
        self.controller.jump_height = jump_height

        # Adjust weapon position to be visible in first-person view
        self.weapon = Weapon(parent=self.controller.camera_pivot)
        self.weapon.entity.position = Vec3(0.5, -0.5, 1.5)  # Adjust position to make it visible in front of the player
        self.weapon.entity.rotation = Vec3(0, 0, 0)  # Make sure it's oriented correctly

        self.bullets = []
        self.shoot_cooldown = .1  # Cooldown time in seconds
        self.last_shoot_time = 0
        self.health = HealthBar(bar_color=color.lime.tint(-.25), curve=.5, max_value=100, value=100, scale=(.35, .05))

        # Ammo-related attributes
        self.ammo = 60
        self.magazine_capacity = 60
        self.reloading = False
        self.reload_time = 2.5  # Time to reload in seconds

        # Ammo Counter UI
        self.ammo_counter = Text(text=f'MP5K: {self.ammo}/{self.magazine_capacity}', position=(0.70, -0.45), scale=2, origin=(0, 0), color=color.white)

    def update(self):
        if held_keys['shift']:
            self.controller.speed = 10
        else:
            self.controller.speed = 5

        if held_keys['r'] and not self.reloading:
            self.reload()

        if mouse.left and not self.reloading:  # Shooting when not reloading
            self.shoot()

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)

        # Update ammo counter color and text
        self.ammo_counter.text = f'MP5K: {self.ammo}/{self.magazine_capacity}'
        if self.ammo > 20:
            self.ammo_counter.color = color.white
        elif 1 <= self.ammo <= 20:
            self.ammo_counter.color = color.yellow
        else:
            self.ammo_counter.color = color.red

    def shoot(self):
        if time.time() - self.last_shoot_time >= self.shoot_cooldown and self.ammo > 0:
            bullet = self.weapon.shoot()  # Pass in player position
            if bullet:
                self.bullets.append(bullet)
                self.ammo -= 1

            self.last_shoot_time = time.time()

    def reload(self):
        if self.ammo < self.magazine_capacity:
            self.reloading = True
            Audio('reload_sound.mp3', autoplay=True)
            invoke(self.finish_reload, delay=self.reload_time)

    def finish_reload(self):
        self.ammo = self.magazine_capacity
        self.reloading = False