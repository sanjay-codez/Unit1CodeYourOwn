# main.py
from ursina import *
from player import Player
from toilets import StandardToilet, FancyToilet
import keyboard

app = Ursina()

# Global variables
player = None
toilets = []
flush_pressed = False

# Start Menu Elements
def start_game():
    global player, toilets
    start_button.disable()
    other_button.disable()
    title_text.disable()

    # Create a flat platform for the player to stand on
    platform = Entity(model='assets/arena',  texture=None, texture_scale=(50, 50),  position=(0, 7.5, 0))

    platform = Entity(model='plane', scale=(10000, 1, 10000), texture='white_cube', texture_scale=(50, 50), collider='box')
    # Add some visual variety with colors or texture
    platform.color = color.gray

    # Create a player
    player = Player()

    # Create a list of toilet objects
    toilets = []

    # Pass the toilets list itself to each toilet's constructor
    toilets.append(StandardToilet(position=(10, 0.5, 10), player_entity=player.controller, all_toilets=toilets))
    toilets.append(FancyToilet(position=(-2, 0.5, -2), player_entity=player.controller, all_toilets=toilets))
    #sf = toilets[0].entity.add_script(SmoothFollow(target=player.controller, offset=(0, 2, 0), speed=.5))

    # Set up lighting and sky
    Sky()
    light = DirectionalLight()
    light.look_at(Vec3(1, -1, -1))

# Set up the game loop
def update():
    global flush_pressed
    if player:
        player.update()
        # Additional game logic goes here
        if mouse.left and time.time() - player.last_shoot_time >= player.shoot_cooldown:  # Fix key detection for shooting
            player.shoot()
        # Example: Check for interactions with toilets
        for toilet in toilets:
            if (player.controller.position - toilet.entity.position).length() < 3:
                print(f"Near the {toilet.__class__.__name__}! Press 'F' to flush.")
                if keyboard.is_pressed('f') and not flush_pressed:  # Check if 'f' was pressed, not held
                    toilet.flush()
                    player.decrement_health(1)
                    flush_pressed = True
                if not keyboard.is_pressed('f'):
                    flush_pressed = False

app.update = update

# Start Menu UI Elements
title_text = Text(text='My 3D Game', scale=2, origin=(0, 0), y=0.3, color=color.white)

# Start Button
start_button = Button(text='Start Game', color=color.azure, scale=(0.25, 0.1), y=-0.1)
start_button.on_click = start_game  # Attach the function to the button click

# Other Button
other_button = Button(text='Other', color=color.orange, scale=(0.25, 0.1), y=-0.3)

# Run the app
app.run()