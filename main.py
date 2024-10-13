# main.py
from ursina import *
from player import Player
from toilets import StandardToilet, FancyToilet

app = Ursina()
# window.fullscreen = True

# Create a flat platform for the player to stand on
platform = Entity(model='plane', scale=(50, 1, 50), texture='white_cube', texture_scale=(50, 50), collider='box')

# Add some visual variety with colors or texture
platform.color = color.gray

# Create a player
player = Player()

# Create a list of toilet objects
toilets = []

toilets.append(StandardToilet(position=(10, 10, 10)))  # Adjusted y to ensure proper placement
toilets.append(FancyToilet(position=(-2, 0.5, -2)))
sf = toilets[0].entity.add_script(SmoothFollow(target=player.controller, offset=(0,2,0), speed=.5))
# Set up lighting and sky
Sky()
light = DirectionalLight()
light.look_at(Vec3(1, -1, -1))

# Set up the game loop
def update():
    player.update()
    # Additional game logic goes here
    if mouse.left and time.time() - player.last_shoot_time >= player.shoot_cooldown: # Fix key detection for shooting
        player.shoot()
    # Example: Check for interactions with toilets
    for toilet in toilets:
        if (player.controller.position - toilet.entity.position).length() < 2:
            print(f"Near the {toilet.__class__.__name__}! Press 'F' to flush.")
            if held_keys['f']:
                toilet.flush()

app.run()