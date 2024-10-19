# toilets.py
from ursina import *
from abc import ABC, abstractmethod
from math import atan2, degrees
import time








###############################################################################
###############################################################################

# Abstract Base Class for Toilets
class Toilet(ABC):
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def flush(self):
        pass

# Different Toilet Types
class StandardToilet(Toilet):
    def __init__(self, position, player_entity, all_toilets):
        super().__init__(position)
        self.entity = Entity(
            model='assets/man.fbx',
            scale=(.005, .005, .005),
            position=position,
            color=color.smoke,
            name="StandardToilet",
            double_sided=True,
            collider='box'
        )
        self.player_entity = player_entity
        self.entity.add_script(CustomSmoothFollow(target=player_entity, offset=(0, 2, 0), speed=.5, all_toilets=all_toilets))
        self.last_attack_time = 0



    def flush(self, player):
        distance_to_player = (self.player_entity.position - self.entity.position).length()
        current_time = time.time()
        if distance_to_player < 3 and current_time - self.last_attack_time >= 1:
            player.decrement_health(random.randint(3, 5))
            Audio('hit_sound.mp3', autoplay=True)  # Add hit sound playback here
            self.last_attack_time = current_time


class FancyToilet(Toilet):
    def __init__(self, position, player_entity, all_toilets):
        super().__init__(position)
        self.entity = Entity(
            model='assets/man.fbx',
            scale=(.005, .005, .005),
            position=position,
            color=color.gold,
            name="FancyToilet",
            double_sided=True,
            collider='box'
        )
        self.player_entity = player_entity
        self.entity.add_script(CustomSmoothFollow(target=player_entity, offset=(0, 2, 0), speed=.5, all_toilets=all_toilets))
        self.last_attack_time = 0


    def flush(self, player):
        print("Fancy toilet flush with music!")

        distance_to_player = (self.player_entity.position - self.entity.position).length()
        current_time = time.time()
        if distance_to_player < 3 and current_time - self.last_attack_time >= 1:

            player.decrement_health(random.randint(3, 5))
            Audio('hit_sound.mp3', autoplay=True)  # Add hit sound playback here
            self.last_attack_time = current_time


###############################################################################
###############################################################################



# Custom SmoothFollow Script
class CustomSmoothFollow(SmoothFollow):
    def __init__(self, target, offset=(0, 0, 0), speed=1, all_toilets=[]):
        super().__init__(target=target, offset=offset, speed=speed)
        self.min_distance = 5  # Minimum distance to maintain from the player
        self.all_toilets = all_toilets
        self.min_toilet_distance = 2.5  # Minimum distance to maintain from other toilets

    def update(self):
        distance_to_player = (self.target.position - self.entity.position).length()
        if distance_to_player > self.min_distance:
            super().update()  # Call the original update to follow the player

        # Smoothly rotate the toilet to face the player on the Y-axis only
        target_direction = (self.target.position - self.entity.position).normalized()
        # Calculate the desired yaw (rotation around the Y-axis)
        desired_rotation_y = atan2(target_direction.x, target_direction.z)
        current_rotation_y = self.entity.rotation_y
        self.entity.rotation_y = lerp(current_rotation_y, degrees(desired_rotation_y), time.dt * 2)

        # Ensure the toilet doesn't rotate around the X or Z axis (feet on the ground)
        self.entity.rotation_x = 0
        self.entity.rotation_z = 0

        # make sure the toilets don't overlap each other
        for other in self.all_toilets:
            if other.entity == self.entity:
                continue
            distance_to_other = (other.entity.position - self.entity.position).length()
            if distance_to_other < self.min_toilet_distance:
                # move away from the other toilet
                direction_away = (self.entity.position - other.entity.position).normalized()
                self.entity.position += direction_away * time.dt * self.speed

