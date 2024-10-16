# weapon.py (modified)
import player
from ursina import *
import math
from ursina.shaders import unlit_shader
from ursina import Audio, lerp, Sequence


class Weapon:
    def __init__(self, parent):
        # Position and orientation of the weapon in front of the player
        self.entity = Entity(parent=parent, model='assets/MP5K', color=color.black, scale=(0.02, 0.01, 0.05),
                             position=Vec3(0.5, -0.5, 1.5), shader=unlit_shader)

    def shoot(self):
        # Check if ammo is available before shooting
        bullet_position = self.entity.world_position + self.entity.forward * 1  # Offset from the weapon to avoid collision

        # Use the camera's forward direction for accurate aiming
        bullet_direction = camera.forward.normalized()  # Make the bullet direction match the camera's forward direction

        Audio('shoot_sound.mp3', autoplay=True)

        # Create and shoot the bullet
        bullet = Bullet(position=bullet_position, direction=bullet_direction)
        return bullet


class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(model='cube', scale=0.1, color=color.red, position=position, collider='box')
        self.direction = direction.normalized()  # Direction vector in which the bullet should move
        self.speed = 200  # Adjust speed as necessary
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
