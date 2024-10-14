# weapon.py
import player
from ursina import *
import math

class Weapon:
    def __init__(self, parent):
        self.entity = Entity(parent=parent, model='quad', color=color.blue, scale=(0.1, 0.05))

    # def shoot(self, the_position, the_rotation_z):
    #     bullet = Bullet(the_position, the_rotation_z)
    #     return bullet

    def shoot(self):
        bullet_position = camera.world_position + camera.forward * 1  # Offset from the camera to avoid immediate collision
        bullet_direction = camera.forward  # The direction where the camera is looking
        bullet = Bullet(position=bullet_position, direction=bullet_direction)
        return bullet
class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(model='cube', scale=0.1, color=color.red, position=position, collider='box')
        self.direction = direction.normalized()  # Direction vector in which the bullet should move
        self.speed = 5  # Adjust speed as necessary
        self.world_parent = scene
        self.alive = True
        invoke(self.destroy_bullet, delay=3)  # Automatically destroy bullet after 3 seconds

    def update(self):
        if self.alive:
            self.position += self.direction * self.speed * time.dt
            hit_info = self.intersects(ignore=[self])
            if hit_info.hit:
                # Check if the hit entity has a 'name' attribute
                if hasattr(hit_info.entity, 'name'):
                    entity_name = hit_info.entity.name
                else:
                    entity_name = hit_info.entity.__class__.__name__
                print(f"Bullet hit the {entity_name}!")
                self.destroy_bullet()

    def destroy_bullet(self):
        if self.alive:
            self.alive = False
            destroy(self)